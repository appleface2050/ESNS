# coding=utf-8
# Date: 11-12-8
# Time: 下午10:28
import json
import datetime
import threading
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Q
import time
from django.views.generic import TemplateView
import thread
from needserver.models import Person, Project, Group, FileGroup, ProjectRechargeRecord, ProjectPersonChangeRecord, \
    NeedMessage
# from needserver.mongodb_doc import RequestCounter, DangerUser
from util import PROJECT_POWER_TIMELINE, PERSON_TIMELINE, PROJECT_IS_ACTIVE, PROJECT_INFO, MY_PROJECT_QUERY_LIST
from util.jsonresult import getResult
from django.conf import settings
from django.utils import timezone
from util.project_power_cache import get_cache_project_power_timeline
from django.contrib.auth import  logout as auth_logout
from util.jsonresult import MyEncoder
from company.models import CompanyPerson
from Need_Server.settings import SYS_MESSAGE
__author__ = u'王健'


def client_admin_login_required(func=None):
    """
    系统管理员校验
    by:王健 at:2015-05-12
    优化管理员登陆校验
    by:王健 at:2015-05-12
    :param func:
    :return:
    """
    def test(request, *args, **kwargs):
        if isinstance(request, TemplateView):
            request2 = args[0]
        else:
            request2 = request
        if not request2.user.is_anonymous():
            if request2.user.is_active and request2.user.is_staff:
                return func(request, *args, **kwargs)
            else:
                return getResult(False, u'系统管理员才能进行此操作。', None, 5)
        else:
            return getResult(False, u'请先登录', None, 1)

    return test

def client_login_required_widthout_tel(func=None):
    """
    登录校验, 不判断 手机号
    by:王健 at:2015-1-15
    :param func:
    :return:
    """
    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_active:
                return func(request, *args, **kwargs)
            else:
                return getResult(False, u'用户已被禁用。', None, 5)
        else:
            return getResult(False, u'请先登录', None, 1)

    return test


def client_login_required(func=None):
    """
    登录校验
    by:王健 at:2015-1-3
    添加手机号判断
    by:王健 at:2015-1-15
    修改逻辑
    by:尚宗凯 at:2015-3-26
    :param func:
    :return:
    """
    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_active:
                if request.user.tel == None:
                    project_id = int(kwargs.get('project_id','0'))
                    if project_id == settings.SHOW_PROJECT_ID:
                        return func(request, *args, **kwargs)
                    return getResult(False, u'请登记手机号。', None, status_code=9)
                return func(request, *args, **kwargs)
            else:
                return getResult(False, u'用户已被禁用。', None, 5)
        else:
            return getResult(False, u'请先登录', None, 1)

    return test


def client_login_project_required(func=None):
    """
    选择组织校验
    by:王健 at:2015-1-3
    使用缓存 提高效率
    by:王健 at:2015-3-9
    添加示例项目，判断
    by:王健 at:2015-3-25
    :param func:
    :return:
    """
    @client_login_required
    def test(request, *args, **kwargs):
        project_id = int(kwargs.get('project_id'))
        if project_id:
            if project_id == settings.SHOW_PROJECT_ID:
                return func(request, *args, **kwargs)

            timeline = int(time.time())
            if not request.session.has_key('my_project'):
                project_list = []

                project_dict = {}
                my_project = {'project_list': project_list, 'project_dict': project_dict}
            else:
                my_project = request.session['my_project']
                project_list = my_project['project_list']
                project_dict = my_project['project_dict']
            if project_id in project_list and project_dict[str(project_id)] > timeline:
                return func(request, *args, **kwargs)
            elif project_id in project_list and project_dict[str(project_id)] == 0:
                return getResult(False, u'您不是 %s 的成员。' % Project.objects.get(pk=project_id).total_name, None, 6)
            else:
                try:
                    person = Person.objects.get(user=request.user, project_id=project_id)
                    project_list.append(project_id)
                    if person.is_active:
                        project_dict[str(project_id)] = timeline + settings.CACHES_TIMEOUT
                    else:
                        project_dict[str(project_id)] = 0
                    request.session['my_project'] = my_project
                    return func(request, *args, **kwargs)
                except Person.DoesNotExist:
                    return getResult(False, u'您不是 %s 的成员。' % Project.objects.get(pk=project_id).total_name, None, 6)
        else:
            return getResult(False, u'请选择正确的项目', {'name': request.user.name}, 2)

    return test


def login_project_is_active_required(func=None):
    """
    组织可用性校验（是否还有余额）
    by:王健 at:2015-1-3
    使用缓存，优化效率
    by:王健 at:2015-3-9
    修改 判断项目是否可用
    by:王健 at:2015-3-15
    添加示例项目，判断
    by:王健 at:2015-3-25
    优化项目是否可用
    by:王健 at:2015-05-08
    :param func:
    :return:
    """
    @client_login_project_required
    def test(request, *args, **kwargs):
        """
        优化缓存结果的非空判断
        by:王健 at:2015-05-21
        修改控制校验
        by:王健 at:2015-05-21
        增加删除MY_PROJECT_QUERY_LIST缓存
        by：尚宗凯 at：2015-07-01
        欠费时为管理员和超级管理员发消息
        """
        project_id = int(kwargs.get('project_id'))
        if project_id == settings.SHOW_PROJECT_ID:
            return func(request, *args, **kwargs)
        today = timezone.now().strftime('%Y-%m-%d')
        project_active = cache.get(PROJECT_IS_ACTIVE % (project_id, today))
        if project_active is None:
            record_list = ProjectPersonChangeRecord.objects.filter(project_id=project_id).order_by('-create_date')[:1]
            if len(record_list) > 0:
                pre = record_list[0]
            else:
                pre = None
            project_active = 1 # 不可用
            if pre:
                project_active = pre.commit_days_real() + 2
                if project_active < 1:
                    if Project.objects.filter(pk=project_id).exists():
                        p = Project.objects.get(pk=project_id)
                        p.status = 1
                        p.save()
                        receiver_user_ids = [i.pk for i in p.group_set.filter(Q(type="root")|Q(type="sys_manage"))]
                        NeedMessage.create_multiple_sys_message(receiver_user_ids, "title", SYS_MESSAGE['project_arrears'] % (p.total_name))
                        cache.set(PROJECT_INFO % project_id, MyEncoder.default(p), settings.CACHES_TIMEOUT)
                        cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            cache.set(PROJECT_IS_ACTIVE % (project_id, today), project_active, settings.CACHES_TIMEOUT)
        if project_active and project_active > 1:
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u'%s 的可使用额度不足，请续费后继续使用。' % Project.objects.get(pk=kwargs.get('project_id')).total_name, None, 7)
    return test


def login_project_status_zero_or_one_required(func=None):
    """
    要求项目status为 0 1
    by：尚宗凯 at：2015-06-02
    """
    @client_login_project_required
    def test(request, *args, **kwargs):
        project_id = int(kwargs.get('project_id'))
        if project_id == settings.SHOW_PROJECT_ID:
            return func(request, *args, **kwargs)
        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            if Project.objects.filter(pk=project_id).exists():
                project = Project.objects.get(pk=project_id)
                project = MyEncoder.default(project)
                cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
        if int(project["status"]) in (0, 1):
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u"项目状态非正常或欠费，不能操作")
    return test


def login_project_status_zero_required(func=None):
    """
    要求项目status为 0
    by：尚宗凯 at：2015-05-31
    """
    @client_login_project_required
    def test(request, *args, **kwargs):
        project_id = int(kwargs.get('project_id'))
        if project_id == settings.SHOW_PROJECT_ID:
            return func(request, *args, **kwargs)
        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            if Project.objects.filter(pk=project_id).exists():
                project = Project.objects.get(pk=project_id)
                project = MyEncoder.default(project)
                cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
        if int(project["status"]) == 0:
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u"项目状态非正常，不能操作")
    return test


def login_project_manager_required(func=None):
    """
    管理员权限校验
    by:王健 at:2015-1-3
    解决bug，修复成员查询bug
    by:王健 at:2015-1-7
    只要是管理员 就可以操作
    by:王健 at:2015-3-20
    :param func:
    :return:
    """
    @login_project_is_active_required
    def test(request, *args, **kwargs):
        group = Group.objects.get(project_id=kwargs.get('project_id'), type='sys_manage')
        if group.look_members.filter(id=request.user.id).exists() or group.say_members.filter(id=request.user.id).exists():
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u'本操作只有管理员可以执行。' , None)
    return test


def login_project_super_manager_required(func=None):
    """
    管理员权限校验
    by:王健 at:2015-1-3
    改为超级管理员
    by：尚宗凯 at：2015-05-29
    :param func:
    :return:
    """
    @login_project_is_active_required
    def test(request, *args, **kwargs):
        group = Group.objects.get(project_id=kwargs.get('project_id'), type='root')
        if group.say_members.filter(id=request.user.id).exists() or group.say_members.filter(id=request.user.id).exists():
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u'本操作只有超级管理员可以执行。' , None)
    return test


def login_company_admin_required(func=None):
    """
    公司管理员校验
    by：尚宗凯 at：2015-06-29
    优化查询，creator_type＝1为公司管理员
    by: 范俊伟 at:2015-07-01
    """
    def test(request, *args, **kwargs):
        if CompanyPerson.objects.filter(user_id=request.user.pk, creator_type=1, is_active=True).exists():
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u'本操作只有公司管理员可以执行。' , None)
    return test


def login_company_customer_service_required(func=None):
    """
    公司客服校验
    by：尚宗凯 at：2015-06-29
    """
    def test(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            return getResult(False, u'本操作只有客服可以执行。' , None)
    return test


def app_power_permissions(flag=None, flag_name=None, add=False, update=False, delete=False, app_add=False,
                                app_update=False, app_del=False):
    def user_permissions(func=None):
        """
        组织可用性校验（是否还有余额）
        by:王健 at:2015-1-3
        优化权限 校验
        by:王健 at:2015-3-5
        优化 json 转 list
        by:王健 at:2015-3-6
        优化使用缓存技术，替代数据库查询, 修改判断错误
        by:王健 at:2015-3-9
        对不同的 权限 使用 不同的 项目校验，只是查询的话，只校验登录项目，其他则校验 项目余额
        by:王健 at:2015-3-10
        增加用户时间线缓存
        by:王健 at:2015-3-14
        添加示例项目，判断
        by:王健 at:2015-3-25
        优化权限校验算法
        by:王健 at:2015-05-13
        :param func:
        :return:
        """
        @login_project_is_active_required
        def active_fun(request, *args, **kwargs):
            return test(request, *args, **kwargs)

        @client_login_project_required
        def login_fun(request, *args, **kwargs):
            return test(request, *args, **kwargs)

        def test(request, *args, **kwargs):
            """
            优化缓存结果的非空判断
            by:王健 at:2015-05-21
            修改控制校验
            by:王健 at:2015-05-21
            """
            user = request.user
            project_id = int(kwargs.get('project_id'))

            if not (add or update or delete or app_add or app_update or app_del):
                if project_id == settings.SHOW_PROJECT_ID:
                    return func(request, *args, **kwargs)

            # cache_key_project = PROJECT_POWER_TIMELINE % project_id
            project_powers, project_powers_flag = get_cache_project_power_timeline(project_id)

            if not flag:
                flags = request.REQUEST.get(flag_name, '')
                filegroup_id = project_powers['flag'].get(flags, 0)
            else:
                filegroup_id = project_powers['flag'].get(flag)

            has_prower = filegroup_id * 100
            if add:
                has_prower += 1
            if update:
                has_prower += 2
            if delete:
                has_prower += 3
            if app_add:
                has_prower += 4
            if app_update:
                has_prower += 5
            if app_del:
                has_prower += 6
            # 获取个人 权限
            if not request.session.has_key('project_id_%s' % project_id):
                person_powers = None
            else:
                person_powers = request.session['project_id_%s' % project_id]
                person_timeline = cache.get(PERSON_TIMELINE % (project_id, request.user.pk))
                if person_timeline is None:
                    person_timeline = Person.objects.get(user=request.user, project_id=project_id).timeline
                    cache.set(PERSON_TIMELINE % (project_id, request.user.pk), person_timeline, settings.CACHES_TIMEOUT)
            # powers = None
            if not person_powers or (person_powers.has_key('person_timeline') and person_timeline > person_powers['person_timeline']):
                person_powers = {'timeline': int(time.time()), 'person_timeline': int(time.time()), 'group': [], 'person': []}

                person = Person.objects.get(user=user, project_id=project_id)
                person_powers['person'] = person.real_powers()
                request.session['project_id_%s' % project_id] = person_powers

            #判断权限
            if person_powers['person'] and has_prower in person_powers['person']:
                return func(request, *args, **kwargs)
            # for gid in person_powers['group']:
            #     if project_powers['powers'] and project_powers['powers'].has_key(str(gid)) and has_prower in project_powers['powers'][str(gid)]:
            #         return func(request, *args, **kwargs)
            return getResult(False, u'您的权限不足,不能进行本项操作。' , None, status_code=8)
        if add or update or delete or app_add or app_update or app_del:
            return active_fun
        else:
            return login_fun

    return user_permissions

#
# def get_filegroup_by_father_pk(pk_or_mod):
#     """
#     根据father id 查询filegroup
#     by:王健 at:2015-3-5
#     :param pk_or_mod:主键或实例
#     :return:
#     """
#     try:
#         if isinstance(pk_or_mod, FileGroup):
#             if not pk_or_mod.father_id:
#                 return pk_or_mod
#             else:
#                 return get_filegroup_by_father_pk(pk_or_mod.father)
#         else:
#             f = FileGroup.objects.get(flag=pk_or_mod)
#             if f.father_id:
#                 return get_filegroup_by_father_pk(f.father)
#             else:
#                 return f
#     except Exception, e:
#         raise e



def api_request_counter(key=None, key_name=None, check_fun=None, warning_count=settings.API_WARNING_DANGER_COUNTER_PER_DAY["class1"][0], danger_count=settings.API_WARNING_DANGER_COUNTER_PER_DAY["class1"][1]):
    """

    接口请求计数
    by: 范俊伟 at:2015-04-16
    修改默认的参数
    by：尚宗凯 at：2015-05-22
    @api_require_counter('gong_cheng_ri_zhi',check_fun=lambda request,*arg,**kwargs:request.REQUEST.get('text'))
    :param key: 标示
    :param key_name: 从request获取的参数,可为字串或数组
    :return:
    """

    def send_warning_message(text):
        """
        发送警告信息
        by: 范俊伟 at:2015-04-16
        :param text:
        :return:
        """
        try:
            send_mail('接口调用报警', text, settings.EMAIL_HOST_USER, [settings.SEND_WARNING_EMAIL_TO])
        except Exception, e:
            print e

    def api_request_counter_func(func=None):
        """
        接口请求计数
        by: 范俊伟 at:2015-04-16
        优化警告值和锁定值的用法
        by:王健 at:2015-05-20
        :param func:
        :return:
        """

        def test(request, *args, **kwargs):
            user = request.user
            if not request.user.is_active:
                # 未登录状态不记录
                return func(request, *args, **kwargs)
            hasCheckFunc = hasattr(check_fun, '__call__')
            if hasCheckFunc and not check_fun(request, *args, **kwargs):
                return func(request, *args, **kwargs)
            # counter_doc = RequestCounter()
            # counter_doc.uid = user.pk
            # key_list = []
            # if key:
            #     key_list.append(key)
            # if key_name:
            #     if type(key_name) == list or type(key_name) == tuple:
            #         # 多个key_name情况
            #         for i in key_name:
            #             v = request.REQUEST.get(i, '')
            #             key_list.append(v)
            #     else:
            #         v = request.REQUEST.get(str(key_name), '')
            #         key_list.append(v)

            # out_key = '_'.join(key_list)
            # counter_doc.key = out_key
            # counter_doc.save()

            # begin_time = datetime.datetime.now() - datetime.timedelta(days=1)
            # count = RequestCounter.objects.filter(uid=user.pk, key=out_key, create_time__gt=begin_time).count()

            # if count > warning_count or count > danger_count:
            #     danger_user = DangerUser()
            #     danger_user.uid = user.pk
            #     danger_user.count = count
            #     if count > warning_count:
            #         thread.start_new_thread(send_warning_message, (
            #             "警告\n用户:%s\n调用:%s\n次数: %d\n超出API_WARNING_COUNTER_PER_DAY" % (user.tel, out_key, count),))
            #         danger_user.flag = 0
            #     elif count > danger_count:
            #         thread.start_new_thread(send_warning_message, (
            #             "危险\n用户:%s\n调用:%s\n次数: %d\n超出API_DANGER_COUNTER_PER_DAY" % (user.tel, out_key, count),))
            #         # 禁用账号
            #         danger_user.flag = 1
            #         user.is_active = False
            #         user.save()
            #
            #         auth_logout(request)
            #     danger_user.save()

            return func(request, *args, **kwargs)

        return test

    return api_request_counter_func


def ns_manage_login_required(func=None):
    """
    后台管理登陆校验
    by: 范俊伟 at:2015-06-12
    :param func:
    :return:
    """

    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_active:
                can_login = False
                if request.user.is_staff:
                    can_login = True
                elif hasattr(request.user, 'backuserinfo'):
                    backuserinfo = request.user.backuserinfo
                    if backuserinfo.user_type >= 0:
                        can_login = True
                if can_login:
                    return func(request, *args, **kwargs)
                else:
                    return getResult(False, u'权限不足。', 8)
            else:
                return getResult(False, u'用户已被禁用。', None, 5)
        else:
            return getResult(False, u'请先登录', None, 1)

    return test

def ns_manage_admin_login_required(func=None):
    """
    后台管理超级管理员登陆校验
    by: 范俊伟 at:2015-06-12
    :param func:
    :return:
    """

    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_active:
                if request.user.is_staff:
                    return func(request, *args, **kwargs)
                else:
                    return getResult(False, u'权限不足。', 8)
            else:
                return getResult(False, u'用户已被禁用。', None, 5)
        else:
            return getResult(False, u'请先登录', None, 1)

    return test
