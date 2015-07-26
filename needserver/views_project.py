# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import copy
import datetime
import logging
import json
import urllib2
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction, OperationalError
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from needserver import FILE_GROUP_FLAGS

from needserver.forms import ProjectForm
from needserver.models import Group, Person, ProjectApply, Project, ProjectRechargeRecord, \
    ProjectPersonChangeRecord, NeedMessage, UserLastReadTimeline, EngineCheck, LastReadTimeProjectSysMessage, SysMessage
from nsbcs.models import File, QN_PROJECT_ICON_BUCKET
from submail.app_configs import MESSAGE_CONFIGS
from submail.message_xsend import MESSAGEXsend
from util import PROJECT_INFO, MY_PROJECT_QUERY_LIST, USERINFO_INFO, PROJECT_USER_REALPOWERS, \
    RED_DOT_UNREAD_NUMBER, RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE, \
    RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE, RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER, \
    RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE, PROJECT_GROUP_USER
from util.cache_handle import get_file_group_id_by_flag_from_cache, query_project_filegroup_data_, \
    get_last_new_data_timeline, get_last_filerecord_timeline_by_project, get_project_user_group_use_cache, \
    get_my_project_query_list
from util.jsonresult import getResult, MyEncoder, getErrorFormResult
from util.loginrequired import client_login_required, login_project_manager_required, client_login_project_required, \
    client_login_required_widthout_tel,api_request_counter, login_project_super_manager_required, \
    login_project_status_zero_required, login_project_status_zero_or_one_required
from django.conf import settings
from needserver.models import SGlog, ProjectMessage, FileRecord, RecordDate, GYSAddress, FileGroup, FileGroupJSON, \
    WuZiRecord, NSUser, NSPersonTel
from nsbcs.models import BaseFile, File
from util.project_power_cache import whether_user_have_power_by_flag, all_flag_user_have_power_by_flag
from webhtml.models import Order
from Need_Server.settings import SHOW_PROJECT_ID, SYS_MESSAGE, API_WARNING_DANGER_COUNTER_PER_DAY,DELETE_PROJECT_PUBLICITY_PERIOD

__author__ = u'王健'


@client_login_project_required
@transaction.atomic()
def leave_project(request, project_id=None):
    """
    脱离组织
    自己点击的，主动脱离
    by:王健 at:2015-1-3
    测试用户退出测试项目
    by:尚宗凯 at:2015-3-26
    通过SHOW_PROJECT_ID判断是否是测试项目
    by:尚宗凯 at:2015-4-7
    发送need消息
    by:尚宗凯 at:2015-4-14
    #退出项目成功时才发送消息
    by:尚宗凯 at:2015-5-12
    增加缓存内容
    by：尚宗凯 at：2015-05-21
    """
    if int(project_id) == SHOW_PROJECT_ID:
        return getResult(False, u"无法退出示例项目", None)
    # if request.user.tel == None:
    # return getResult(False, u"无法退出测试项目", None)
    else:
        success, msg = del_person_by_project(request.user.pk, project_id)
        project_name = ""
        if Project.objects.filter(pk=project_id).exists():
            project_name = Project.objects.get(pk=project_id).total_name
        if success:
            NeedMessage.create_sys_message(request.user.pk, "title", SYS_MESSAGE['leave_project'] % project_name)
        cache.delete(PROJECT_GROUP_USER % project_id)
        return getResult(success, msg, None)


@login_project_manager_required
@transaction.atomic()
def remove_person(request, project_id=None):
    """
    移出项目
    被管理员点击的被动脱离
    by:王健 at:2015-1-3
    增加操作人的id
    by:王健 at:2015-2-6
    #增加系统消息
    by：尚宗凯 at：2015-04-10
    #修改need消息内容
    by：尚宗凯 at：2015-04-14
    #只有退出项目成功才发送need消息
    by：尚宗凯 at：2015-04-30
    增加缓存内容
    by：尚宗凯 at：2015-05-21
    """
    user_id = request.REQUEST.get('user_id')
    success, msg = del_person_by_project(user_id, project_id, request.user.pk)
    project_name = ""
    if Project.objects.filter(pk=project_id).exists():
        project_name = Project.objects.get(pk=project_id).total_name
    if success:
        NeedMessage.create_sys_message(user_id, "title", SYS_MESSAGE['remove_person'] % project_name)
    cache.delete(PROJECT_GROUP_USER % project_id)
    return getResult(success, msg, None)


def del_person_by_project(user_id, project_id=None, author_id=None):
    """
    根据用户id,和 项目id 删除用户
    by:王健 at:2015-1-3
    移出用户时，更新一下 群组的时间戳
    by:王健 at:2015-1-16
    删除成员时，减去成员数, 系统管理员判断
    by:王健 at:2015-1-30
    管理员只能被超级管理员移除，或管理员自己移除
    by:王健 at:2015-2-6
    解决移除用户时 没有限制项目的bug
    by:王健 at:2015-2-9
    修改文字提示
    by：尚宗凯 at：2015-05-06
    取消对chengyaun_num的维护
    by:王健 at:2015-05-07
    增加缓存内容
    by：尚宗凯 at：2015-05-21
    :param user_id:
    :param project_id:
    :return:
    """
    # todo 用户从项目中脱离，还要把在项目中的其他分组中删除
    user_id = int(user_id)
    person = Person.objects.get(user_id=user_id, project_id=project_id)
    project = Project.objects.get(pk=project_id)
    if project.manager_id == user_id:
        return False, u'不能退出本人创建的项目。'
    if author_id and author_id != project.manager_id:
        if Group.objects.filter(project_id=project_id, type='sys_manage').filter(
                        Q(say_members=person.user_id) | Q(look_members=person.user_id)).exists():
            return False, u'项目的管理员，只能由超级管理员来删除。'

    person.is_active = False
    person.save()
    # project.chengyuan_num -= 1
    # project.save()
    for group in Group.objects.filter(project_id=project_id).filter(
                    Q(say_members=person.user_id) | Q(look_members=person.user_id)):
        group.say_members.remove(person.user)
        group.look_members.remove(person.user)
        group.save()
    cache.delete(PROJECT_GROUP_USER % project_id)
    return True, u'脱离项目成功'


@client_login_required
@transaction.atomic()
def apply_project(request, project_id=None):
    """
    向项目发出申请
    by:王健 at:2015-1-3
    验证信息，字段参数名改为text
    by:王健 at:2015-1-8
    #增加系统消息
    by：尚宗凯 at：2015-04-10
    增加发送多人系统消息
    by：尚宗凯 at：2015-04-13
    创建申请信息，未处理的始终保持一个
    by：王健 at：2015-04-13
    修改申请加入项目
    by：尚宗凯 at：2015-04-14
    解决ios输入表情字符引起的问题
    by：尚宗凯 at：2015-04-14
    修改推送信息, 推送消息 使用项目的全称
    by:王健 at:2015-05-12
    优化need系统消息提示语句
    by：尚宗凯 at：2015-05-15
    """
    content = request.REQUEST.get('text')
    if project_id and content:
        if not Person.objects.filter(user=request.user, project_id=project_id, is_active=True).exists():
            orgapply, create = ProjectApply.objects.get_or_create(project_id=project_id, user=request.user, status=None)
            orgapply.content = content
            try:
                orgapply.save()
            except OperationalError:
                return getResult(False, u'申请信息错误，请重新填写', None)

            # send_chat('join_apply', project_id, msg=u'用户：%s 申请加入项目' % request.user.name)
            # pids = set()
            # for p in orgapply.org.managers.all():
            # pids.add(p.pk)
            notify = {'type': 'join_apply'}
            # update_notify(pid=list(pids), msg=u'用户：%s 申请加入项目' % request.user.name, notify=notify)
            receiver_user_ids = []
            grp = Group.objects.filter(project_id=project_id).filter(type='sys_manage')[0]
            say_members = [u[0] for u in grp.say_members.values_list('id')]
            look_members = [u[0] for u in grp.look_members.values_list('id')]
            receiver_user_ids = receiver_user_ids + say_members + look_members
            receiver_user_ids = list(set(receiver_user_ids))

            NeedMessage.create_multiple_sys_message(receiver_user_ids, "title",
                                                    SYS_MESSAGE['apply_project_manager'] % (orgapply.user.name, orgapply.project.total_name))
            NeedMessage.create_sys_message(orgapply.user_id, "title", SYS_MESSAGE['apply_project'] % (orgapply.project.total_name))
            return getResult(True, None, {'apply_id': orgapply.pk, 'id': project_id})
        else:
            return getResult(False, u'您已经是该项目成员了，无需申请', None)
    else:
        return getResult(False, u'请填写申请信息', None)


def applyproject_to_dict(orgapp):
    """
    项目申请，从model转化为dict
    by:王健 at:2015-1-8
    create_date 改为 create_time
    by:王健 at:2015-1-12
    project_id 改为 project
    by:王健 at:2015-1-13
    修改申请信息的 icon_url 字段
    by:王健 at:2015-2-7
    返回数据增加user_id
    by:尚宗凯 at：2015-05-11
    :param orgapp:
    :return:
    """
    p = {'id': orgapp.pk, 'user_name': orgapp.user.name, 'icon_url': '',
         'text': orgapp.content, 'create_time': orgapp.create_time.strftime('%Y-%m-%d %H:%M:%S'),
         'project': orgapp.project_id,
         'status': orgapp.status, 'checker_id': None, 'timeline': orgapp.timeline,
         "user_id": orgapp.user_id
    }
    if orgapp.user.icon_url:
        p['icon_url'] = orgapp.user.icon_url.get_url()
    if orgapp.checker:
        p['checker_id'] = orgapp.checker.user_id
    return p


@login_project_manager_required
def get_all_applyproject(request, project_id=None):
    """
    获取所有的申请
    by:王健 at:2015-1-3
    获取所有的未处理申请
    by:王健 at:2015-1-7
    优化查询的查询逻辑
    by:王健 at:2015-1-8
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    result = []
    if not timeline:
        for orgapp in ProjectApply.objects.filter(project_id=project_id, status=None):
            result.append(applyproject_to_dict(orgapp))
    else:
        for orgapp in ProjectApply.objects.filter(project_id=project_id, timeline__gt=int(timeline)):
            result.append(applyproject_to_dict(orgapp))
    return getResult(True, None, result)


@login_project_manager_required
def get_applyproject_user_infomation(request, project_id=None):
    """
    获取申请的用户的用户信息
    by:尚宗凯 at：2015-05-11
    """
    user_id = request.REQUEST.get('user_id')
    if not user_id:
        return getResult(False, u"参数错误")
    if not ProjectApply.objects.filter(project_id=project_id, user_id=user_id).exists():
        return getResult(False, u"用户无申请加入该项目")
    else:
        user = NSUser.objects.get(pk=user_id)
        p = user.get_user_map()
        if hasattr(user, 'userinfo') and user.userinfo:
            p.update(MyEncoder.default(user.userinfo))
        p['id'] = user.pk
        return getResult(True, u'获取用户信息成功', p)


@login_project_manager_required
@transaction.atomic()
def change_applyproject(request, project_id=None):
    """
    处理 申请，根据do 参数
    by:王健 at:2015-1-3
    已经在项目分组内的用户的申请，忽略操作,
    给加入的 用户创建 Person数据
    by:王健 at:2015-1-7
    处理过的申请，直接返回已经处理过了
    by:王健 at:2015-1-8
    优化处理过的 申请 的处理逻辑
    by:王健 at:2015-1-11
    添加群组成员，刷新群组的时间戳
    by:王健 at:2015-1-16
    退出了可以再加入
    by:王健 at:2015-2-5
    对退出又增加进来的人做关注和成员数处理
    by:王健 at:2015-2-6
    增加group_id 参数，设置成员审批时的加入分组
    by:王健 at:2015-2-10
    已经是项目成员的员工，不能再被处理
    by:王健 at:2015-2-12
    不恩能够加入社会大众通道
    by:王健 at:2015-2-15
    批准进入管理员的也加入到项目经理部，加入项目 获得推送信息, 拒绝时获得推送信息
    by:王健 at:2015-04-19
    去除对chengyuan_num的维护
    by:王健 at:2015-05-07
    优化need消息提示
    by：尚宗凯 at：2015-05-15
    优化need消息提示
    by：尚宗凯 at：2015-05-15
    增加缓存内容
    by：尚宗凯 at：2015-05-21
    """
    apply_id = request.REQUEST.get('apply_id')
    do = request.REQUEST.get('do')
    if apply_id:
        orgApp = ProjectApply.objects.get(pk=apply_id, project_id=project_id)
        if orgApp.status != None:
            return getResult(False, u'申请已经被%s 处理过了。' % orgApp.checker, None)
        if do == 'true':
            group_id = request.REQUEST.get('group_id')
            if not group_id:
                return getResult(False, u'请提供，成员的分组信息', None)
            temp_group = Group.objects.get(project_id=orgApp.project_id, pk=group_id)
            if temp_group.type == 'sys_shdztd':
                return getResult(False, u'项目成员无需加入 社会大众通道 。')
            group = Group.objects.get(project=orgApp.project, type='root')
            is_member = True
            if not group.say_members.filter(id=orgApp.user_id).exists() and not group.look_members.filter(
                    id=orgApp.user_id).exists():
                is_member = False
            if is_member:
                return getResult(False, u'%s 已经是项目成员了' % orgApp.user.name, None)
            orgApp.status = True
            person, created = Person.objects.get_or_create(user=orgApp.user, project=orgApp.project)
            if not person.is_active:
                person.is_active = True
                person.save()

            group.look_members.add(orgApp.user)
            group.save()
            if not temp_group.say_members.filter(id=orgApp.user_id).exists() and not temp_group.look_members.filter(
                    id=orgApp.user_id).exists():
                temp_group.look_members.add(orgApp.user)
                temp_group.save()
                if temp_group.type == 'sys_manage':
                    xm_group = Group.objects.get(project_id=project_id, type='sys_xmjl')
                    xm_group.say_members.add(person.user)
                    xm_group.save()
                NeedMessage.create_sys_message(person.user_id, "title",
                                               settings.SYS_MESSAGE['change_applyproject'] % person.project.total_name)
                receiver_user_ids = []
                grp = Group.objects.filter(project_id=project_id).filter(type='sys_manage')[0]
                say_members = [u[0] for u in grp.say_members.values_list('id')]
                look_members = [u[0] for u in grp.look_members.values_list('id')]
                receiver_user_ids = receiver_user_ids + say_members + look_members
                receiver_user_ids = list(set(receiver_user_ids))
                NeedMessage.create_multiple_sys_message(receiver_user_ids,
                                                        "title",
                                                        SYS_MESSAGE['appley_project_approval_group_person'] % (orgApp.project.total_name,request.user.name,orgApp.user.name))   #orgApp.project.manager.name
        else:
            orgApp.status = False
            NeedMessage.create_sys_message(orgApp.user_id, "title",
                                           settings.SYS_MESSAGE['reject_applyproject'] % orgApp.project.total_name)
            receiver_user_ids = []
            grp = Group.objects.filter(project_id=project_id).filter(type='sys_manage')[0]
            say_members = [u[0] for u in grp.say_members.values_list('id')]
            look_members = [u[0] for u in grp.look_members.values_list('id')]
            receiver_user_ids = receiver_user_ids + say_members + look_members
            receiver_user_ids = list(set(receiver_user_ids))
            NeedMessage.create_multiple_sys_message(receiver_user_ids,
                                                    "title",
                                                    SYS_MESSAGE['appley_project_reject_group_person'] % (orgApp.project.total_name,request.user.name,orgApp.user.name))  #orgApp.project.manager.name
        orgApp.checker = Person.objects.get(user=request.user, project_id=project_id)
        orgApp.save()
        cache.delete(PROJECT_GROUP_USER % project_id)
        return getResult(True, None, None)
    else:
        return getResult(False, u'删除申请失败', None)


def create_project_by_company(request):
    """
    公司创建项目
    by：尚宗凯 at：2015-06-27
    优化创建项目
    by：尚宗凯 at：2015-06-30
    优化company_id参数的读取
    by: 范俊伟 at:2015-07-01
    """
    person = Person()
    person.user = request.user

    orgform = ProjectForm(request.POST)
    if not orgform.is_valid():
        return getErrorFormResult(orgform)
    orgform.instance.manager = request.user
    project = orgform.save()
    project.manager = request.user
    project.pay_type = 0
    project.company_id = request.REQUEST.get("company_id") or None
    project.save()
    rootgroup = Group()
    rootgroup.user = request.user
    rootgroup.name = project.total_name
    rootgroup.type = 'root'
    rootgroup.project = project
    rootgroup.save()
    person.project = project
    person.save()

    rootgroup.say_members.add(person.user)

    group = Group()
    group.name = u'管理员'
    group.type = 'sys_manage'
    group.project = project
    group.sorted = 0
    group.save()
    group.say_members.add(person.user)
    group.save()

    group = Group()
    group.name = u'行政主管'
    group.type = 'sys_xzzg'
    group.project = project
    group.sorted = 1
    group.save()

    group = Group()
    group.name = u'建设单位'
    group.type = 'sys_jsdw'
    group.project = project
    group.sorted = 2
    group.save()

    group = Group()
    group.name = u'设计单位'
    group.type = 'sys_sjdw'
    group.project = project
    group.sorted = 3
    group.save()

    group = Group()
    group.name = u'勘察单位'
    group.type = 'sys_kcdw'
    group.project = project
    group.sorted = 4
    group.save()

    group = Group()
    group.name = u'监理单位'
    group.type = 'sys_jldw'
    group.project = project
    group.sorted = 5
    group.save()

    group = Group()
    group.name = u'施工单位'
    group.type = 'sys_sgdw'
    group.project = project
    group.sorted = 6
    group.save()

    group = Group()
    group.name = u'项目经理部'
    group.type = 'sys_xmjl'
    group.project = project
    group.sorted = 7
    group.is_needhx = True
    group.save()
    group.say_members.add(person.user)

    group = Group()
    group.name = u'劳务分包单位'
    group.type = 'sys_lwfbdw'
    group.project = project
    group.sorted = 8
    group.save()

    group = Group()
    group.name = u'专业分包单位'
    group.type = 'sys_zyfbdw'
    group.project = project
    group.sorted = 9
    group.save()

    # group = Group()
    # group.name = u'社会大众通道'
    # group.type = 'sys_shdztd'
    # group.project = project
    # group.sorted = 1000
    # group.save()

    return project



def create_project(request):
    """
    创建项目（项目、根部门、未分组部门、员工信息）
    by:王健 at:2015-1-3
    Person 不再提供默认分组
    by:王健 at:2015-1-8
    增加新的分组
    by:王健 at:2015-1-31
    排序字段修改
    by:王健 at:2015-2-3
    增加社会大众通道，保持社会化大众的分组在最后一个
    by:王健 at:2015-2-15
    管理员默认进入项目组
    by:王健 at:2015-2-16
    优化初始创建群聊
    by:王健 at:2015-3-20
    取消社会大众 分组
    by:王健 at:2015-4-9
    """
    person = Person()
    person.user = request.user

    orgform = ProjectForm(request.POST)
    if not orgform.is_valid():
        return getErrorFormResult(orgform)
    orgform.instance.manager = request.user
    project = orgform.save()
    project.manager = request.user
    project.save()
    rootgroup = Group()
    rootgroup.user = request.user
    rootgroup.name = project.total_name
    rootgroup.type = 'root'
    rootgroup.project = project
    rootgroup.save()
    person.project = project
    person.save()

    rootgroup.say_members.add(person.user)

    group = Group()
    group.name = u'管理员'
    group.type = 'sys_manage'
    group.project = project
    group.sorted = 0
    group.save()
    group.say_members.add(person.user)
    group.save()

    group = Group()
    group.name = u'行政主管'
    group.type = 'sys_xzzg'
    group.project = project
    group.sorted = 1
    group.save()

    group = Group()
    group.name = u'建设单位'
    group.type = 'sys_jsdw'
    group.project = project
    group.sorted = 2
    group.save()

    group = Group()
    group.name = u'设计单位'
    group.type = 'sys_sjdw'
    group.project = project
    group.sorted = 3
    group.save()

    group = Group()
    group.name = u'勘察单位'
    group.type = 'sys_kcdw'
    group.project = project
    group.sorted = 4
    group.save()

    group = Group()
    group.name = u'监理单位'
    group.type = 'sys_jldw'
    group.project = project
    group.sorted = 5
    group.save()

    group = Group()
    group.name = u'施工单位'
    group.type = 'sys_sgdw'
    group.project = project
    group.sorted = 6
    group.save()

    group = Group()
    group.name = u'项目经理部'
    group.type = 'sys_xmjl'
    group.project = project
    group.sorted = 7
    group.is_needhx = True
    group.save()
    group.say_members.add(person.user)

    group = Group()
    group.name = u'劳务分包单位'
    group.type = 'sys_lwfbdw'
    group.project = project
    group.sorted = 8
    group.save()

    group = Group()
    group.name = u'专业分包单位'
    group.type = 'sys_zyfbdw'
    group.project = project
    group.sorted = 9
    group.save()

    # group = Group()
    # group.name = u'社会大众通道'
    # group.type = 'sys_shdztd'
    # group.project = project
    # group.sorted = 1000
    # group.save()

    return project


@client_login_required
def query_project_name(request):
    """
    查询类似项目名
    by:王健 at:2015-3-3
    """
    key = request.REQUEST.get('key', '')
    if not key:
        return getResult(True, u'没有相似项目名', None)
    l = [x[0] for x in
         Project.objects.filter(total_name__icontains=key).order_by('-create_time').values_list('total_name')[:20]]
    return getResult(True, u'获取相似项目名', l)


def reg_project_by_company(request):
    """
    公司创建项目
    by：尚宗凯 at：2015-06-27
    """
    try:
        if Project.objects.filter(total_name=request.REQUEST.get('total_name')).exists():
            return getResult(False, u'创建项目失败，项目名已经存在，您可以在个人设置界面提交反馈')
        with transaction.atomic():
            project = create_project_by_company(request)
        if isinstance(project, HttpResponse):
            return project
        NeedMessage.create_sys_message(request.user.pk, "title", SYS_MESSAGE['reg_project'] % project.total_name)
        return getResult(True, u'成功创建：%s' % project.total_name, MyEncoder.default(project))
    except Exception, e:
        if settings.ENVIRONMENT == 'baidu':
            log = logging.getLogger('django')
            log.error(str(e))
        return getResult(False, u'创建项目失败')



@client_login_required
@api_request_counter('reg_project', warning_count=API_WARNING_DANGER_COUNTER_PER_DAY["class1"][0], danger_count=API_WARNING_DANGER_COUNTER_PER_DAY["class1"][1])
def reg_project(request):
    """
    已登录用户创建项目
    by:王健 at:2015-1-3
    如果是数据项录入错误，就直接返回有好的错误信息
    by:王健 at:2015-1-18
    项目名 全称 校验。如果已经有了，提示客户不能创建
    by:王健 at:2015-3-3
    添加needmessage消息
    by：尚宗凯 at：2015-04-09
    去除 发系统消息的错误代码
    by：王健 at：2015-04-14
    增加统计装饰器
    by：尚宗凯 at：2015-05-18
    创建项目失败，输出日志
    by:王健 at:2015-05-20
    优化接口被调用的频率装饰器
    by:王健 at:2015-05-20
    """
    try:
        if Project.objects.filter(total_name=request.REQUEST.get('total_name')).exists():
            return getResult(False, u'创建项目失败，项目名已经存在，您可以在个人设置界面提交反馈')
        with transaction.atomic():
            project = create_project(request)
        if isinstance(project, HttpResponse):
            return project
        NeedMessage.create_sys_message(request.user.pk, "title", SYS_MESSAGE['reg_project'] % project.total_name)
        return getResult(True, u'成功创建：%s' % project.total_name, MyEncoder.default(project))
    except Exception, e:
        if settings.ENVIRONMENT == 'baidu':
            log = logging.getLogger('django')
            log.error(str(e))
        return getResult(False, u'创建项目失败')


@login_project_manager_required
def update_project(request, project_id):
    """
    修改项目信息
    by:王健 at:2015-2-3
    解决项目修改 bug， 可以不传 id
    by:王健 at:2015-2-15
    """
    try:
        with transaction.atomic():

            project = Project.objects.get(pk=project_id)
            for k in request.POST.keys():
                setattr(project, k, request.POST.get(k))
            project.save()

        return getResult(True, u'修改信息成功', MyEncoder.default(project))
    except Exception, e:
        return getResult(False, u'修改信息失败')


@client_login_required
def my_project(request):
    """
    根据登陆用户获取关注项目列表
    by:王健 at:2015-1-3
    优化了查询方法。MyEncoder.default 不能接受list类型的变量
    by:王健 at:2015-1-5
    添加时间线参数，带时间线参数的，判断一下这个成员是否被移出
    被移出的project，只输出 id 和 delete属性
    by:王健 at:2015-1-8
    我关注的我参与的项目
    by:王健 at:2015-1-30
    改变 代码格式
    by:王健 at:2015-2-15
    修复bug，values 参数不能用 元祖
    by:王健 at:2015-2-16
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改 我的项目 列表
    by:王健 at:2015-4-3
    更改 我的项目 列表
    by:尚宗凯 at:2015-4-10
    降低缓存数据时间
    by:王健 at:2015-4-13
    修改project_id 获取方式
    by: 王健 at:2015-04-14
    只获取我加入的项目，未来再改为 审核中的项目
    by:王健 at:2015-04-16
    为兼容ios，增加is_active字段
    by:王健 at:2015-05-12
    """
    timeline = int(request.REQUEST.get('timeline', '0'))

    if not timeline:
        l = cache.get(MY_PROJECT_QUERY_LIST % request.user.pk)
        if l is not None:
            return getResult(True, None, l)
        l = Project.objects.filter(
            pk__in=request.user.person_set.filter(is_active=True).values(('project_id'))).order_by('-id')
        resultlist = []
        myprojectids = []
        for p in l:
            myprojectids.append(p.pk)
            pd = p.toJSON()
            pd['is_guanzhu'] = False
            resultlist.append(pd)
        # project_ids = [u[0] for u in ProjectApply.objects.filter(user=request.user, status=None).values_list('project_id')]
        # for p in Project.objects.filter(pk__in=project_ids):
        # pd = p.toJSON()
        # pd['is_guanzhu'] = True
        #     resultlist.append(pd)
        cache.set(MY_PROJECT_QUERY_LIST % request.user.pk, resultlist, 60)
        return getResult(True, None, resultlist)
    else:
        l = []
        myprojectids = []
        pklist = []
        for person in request.user.person_set.filter(timeline__gt=int(timeline)):
            if person.is_active:
                pd = person.project.toJSON()
                pd['is_guanzhu'] = False
                l.append(pd)
                pklist.append(person.project_id)
            else:
                l.append({'id': person.project_id, 'delete': True, 'is_active': False})
                pklist.append(person.project_id)
            myprojectids.append(person.project_id)
        # project_ids = [u[0] for u in ProjectApply.objects.filter(user=request.user, status=None, timeline__gt=int(timeline)).exclude(pk__in=pklist).values_list('project_id')]
        # for p in Project.objects.filter(pk__in=project_ids):
        # pd = p.toJSON()
        # pd['is_guanzhu'] = True
        #     l.append(pd)
        #     pklist.append(p.pk)
        # project_ids = [u[0] for u in ProjectApply.objects.filter(user=request.user, status=False, timeline__gt=int(timeline)).exclude(pk__in=pklist).values_list('project_id')]
        # for p in Project.objects.filter(pk__in=project_ids):
        #     l.append({'id': p.pk, 'delete': True})
        return getResult(True, None, l)


        # else:
        #     l = []
        #     myprojectids = []
        #     pklist = []
        #     for person in request.user.person_set.filter(timeline__gt=int(timeline)):
        #         if person.is_active:
        #             pd = person.project.toJSON()
        #             pd['is_guanzhu'] = False
        #             l.append(pd)
        #             pklist.append(person.project_id)
        #         else:
        #             l.append({'id': person.project_id, 'delete': True})
        #             pklist.append(person.project_id)
        #         myprojectids.append(person.project_id)
        #     for p in Project.objects.filter(pk__in=ProjectApply.objects.filter(user=request.user, status=None, timeline__gt=int(timeline)).exclude(pk__in=pklist).values(('project_id'))):
        #         pd = p.toJSON()
        #         pd['is_guanzhu'] = True
        #         l.append(pd)
        #         pklist.append(p.pk)
        #     for p in Project.objects.filter(pk__in=ProjectApply.objects.filter(user=request.user, status=False, timeline__gt=int(timeline)).exclude(pk__in=pklist).values(('project_id'))):
        #         l.append({'id': p.pk, 'delete': True})
        #     return getResult(True, None, l)


@client_login_required
def my_project2(request):
    """
    增加返回project是否有未读数据
    by:尚宗凯 at：2015-05-07
    修复cache导致的bug
    by：尚宗凯 at：2015-05-08
    为兼容ios，增加is_active字段
    by:王健 at:2015-05-12
    修改示例用户示例项目红点bug
    by：尚宗凯 at：2015-05-14
    修复小红点bug
    by：尚宗凯 at：2015-05-21
    优化查询用户的项目时，时间戳的查询条件
    by:王健 at:2015-05-21
    增加验证项目状态
    by：尚宗凯 at：2015-06-01
    修复删人以后出现的bug
    by：尚宗凯 at：2015-06-01
    修复公示期存在的一个bug
    by：尚宗凯 at：2015-06-02
    status 4 变为 3 时增加删除内容
    by：尚宗凯 at：2015-06-03
    status 为5 时变更为4
    by：尚宗凯 at：2015-06-05
    增加返回示例项目数据在timeline为空的时候
    by：尚宗凯 at：2015-06-17
    返回结果中不包含已删除的项目
    by：尚宗凯 at：2015-06-24
    增加这个用户是否属于某个项目
    by：尚宗凯 at：2015-07-01
    修复bug
    by：尚宗凯 at：2015-07-01
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    project_ids = [x[0] for x in request.user.person_set.filter(is_active=True).values_list('project_id')]
    have_new_data = is_have_new_data(project_ids, request.user.pk)
    if settings.SHOW_PROJECT_ID in project_ids or settings.SHOW_USER_ID == request.user.pk:
        have_new_data[0]['have_new_data'] = False
    if not timeline:
        # l = cache.get(MY_PROJECT_QUERY_LIST % request.user.pk)
        # if l is not None:
        #     return getResult(True, None, {"resultlist": l, "have_new_data": have_new_data})
        # l = Project.objects.filter(pk__in=project_ids).order_by('-id')
        # resultlist = []
        # myprojectids = []
        # for p in l:
        #     myprojectids.append(p.pk)
        #     pd = p.toJSON()
        #     pd['is_guanzhu'] = False
        #     resultlist.append(pd)
        # cache.set(MY_PROJECT_QUERY_LIST % request.user.pk, resultlist, 60)
        l = get_my_project_query_list(request.user.pk, project_ids)
        for i in l:
            if i['status'] == 5:
                i['status'] = 4
        show_project = Project.objects.get(pk=settings.SHOW_PROJECT_ID).toJSON()
        show_project["is_show_project"] = True
        l.append(show_project)
        for i in l:                                   # 返回结果中去掉已经停项目
            if i["status"] == 3:
                l.remove(i)
        for i in l:
            i["does_user_in_project"] = True
        return getResult(True, None, {"resultlist": l, "have_new_data": have_new_data})
    else:
        l = []
        myprojectids = []
        pklist = []
        for person in request.user.person_set.filter(project__timeline__gt=int(timeline)):
            if person.is_active:
                pd = person.project.toJSON()
                pd['is_guanzhu'] = False
                l.append(pd)
                pklist.append(person.project_id)
            else:
                l.append({'id': person.project_id, 'delete': True, 'is_active': False})
                pklist.append(person.project_id)
            myprojectids.append(person.project_id)
            for p in l:
                if "status" in p.keys() and p['status'] in (4,5) and p['delete_project_time'] and (datetime.datetime.now() - datetime.datetime.strptime(p['delete_project_time'],'%Y-%m-%d %H:%M:%S') >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD)):
                    project = Project.objects.get(pk=p['id'])
                    project.status = 3
                    project.save()
                    cache.delete(PROJECT_INFO % project.pk)
                    p['status'] = 3
                    p['delete'] = True
                    p['is_active'] = False
                if "status" in p.keys() and p['status'] == 5:
                    p['status'] = 4
                if "status" in p.keys() and p['status'] == 3:
                    l.remove(p)
                    l.append({'id': person.project_id, 'delete': True, 'is_active': False})
            for p in l:
                p["does_user_in_project"] = True
        return getResult(True, None, {"resultlist": l, "have_new_data": have_new_data})


# @client_login_required
def query_project(request):
    """
    默认查询项目列表
    by:王健 at:2015-1-3
    优化了查询方法。可附带地址
    by:王健 at:2015-1-5
    根据关键词查询项目列表
    by:王健 at:2015-1-10
    默认按照 创建时间排序
    by:王健 at:2015-1-15
    使用缓存，加快速度
    by:王健 at:2015-3-9
    查询项目列表，无需登录
    by:王健 at:2015-3-25
    添加com字段，查询公司关键字
    by:王健 at:2015-4-13
    """
    start = int(request.REQUEST.get('start', '0'))
    address = int(request.REQUEST.get('address', '0'))
    key = request.REQUEST.get('key', '')
    com = request.REQUEST.get('com', '')
    # cache_name = PROJECT_QUERY_LIST % ('%s_%s_%s' % (start, address, key),)
    # l = cache.get(cache_name)
    # if l:
    # return getResult(True, None, l)
    l = Project.objects.all()
    if address:
        l = l.filter(address=address)
    if key:
        l = l.filter(total_name__icontains=key)
    if com:
        l = l.filter(
            Q(jsdw__icontains=com) | Q(kcdw__icontains=com) | Q(jsdw__icontains=com) | Q(sgdw__icontains=com) | Q(
                jldw__icontains=com))
    l = l.order_by('-create_time')[start:start + 20]
    l = MyEncoder.default(l)
    # cache.set(cache_name, l, 3600)
    return getResult(True, None, l)


@client_login_required
def get_project(request):
    """
    根据项目ID查询项目
    by:范俊伟 at:2015-01-22
    添加缓存
    by:王健 at:2015-3-9
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    project_id = request.REQUEST.get('project_id', '')
    try:
        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            project = Project.objects.get(id=project_id)
            project = MyEncoder.default(project)
            cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
        return getResult(True, None, MyEncoder.default(project))
    except Project.DoesNotExist:
        return getResult(False, u'项目不存在')
    except ValueError:
        return getResult(False, u'参数格式错误')


# @client_login_required
# def close_project(request):
#     """
#     关闭项目
#     by:尚宗凯 at:2015-05-05
#     优化缓存结果的非空判断
#     by:王健 at:2015-05-21
#     修改控制校验
#     by:王健 at:2015-05-21
#     """
#     project_id = request.REQUEST.get('project_id', '')
#     try:
#         project = cache.get(PROJECT_INFO % project_id)
#         if project is None:
#             project = Project.objects.get(id=project_id)
#             project = MyEncoder.default(project)
#             cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
#         if not project['is_active']:
#             return getResult(False, u'项目已关闭')
#         else:
#             if project['manager'] == request.user.pk:
#                 p = Project.objects.get(id=project['id'])
#                 p.is_active = False
#                 p.save()
#                 return getResult(True, u'关闭项目成功')
#             else:
#                 return getResult(False, u'非管理员不能关闭项目')
#     except Project.DoesNotExist:
#         return getResult(False, u'项目不存在')
#     except ValueError:
#         return getResult(False, u'参数格式错误')


@client_login_required
def active_project(request):
    """
    开放项目
    by:尚宗凯 at:2015-05-05
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    project_id = request.REQUEST.get('project_id', '')
    try:
        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            project = Project.objects.get(id=project_id)
            project = MyEncoder.default(project)
            cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
        if project['is_active']:
            return getResult(False, u'项目已开放')
        else:
            if project['manager'] == request.user.pk:
                p = Project.objects.get(id=project['id'])
                p.is_active = True
                p.save()
                return getResult(True, u'开放项目成功')
            else:
                return getResult(False, u'非管理员不能开放项目')
    except Project.DoesNotExist:
        return getResult(False, u'项目不存在')
    except ValueError:
        return getResult(False, u'参数格式错误')


# @client_login_required
def get_show_project(request):
    """
    获取展示项目的信息
    by:王健 at:2015-3-25
    获取展示项目，无需登录
    by:王健 at:2015-3-25
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    project_id = settings.SHOW_PROJECT_ID
    try:
        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            project = Project.objects.get(id=project_id)
            project = MyEncoder.default(project)
            cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
        return getResult(True, None, MyEncoder.default(project))
    except Project.DoesNotExist:
        return getResult(False, u'项目不存在')
    except ValueError:
        return getResult(False, u'参数格式错误')


@login_project_manager_required
def add_person_by_tel(request, project_id):
    """
    根据手机号，将成员加入项目
    by：王健 at:2015-1-25
    优化管理员增加人员的方法，增加group_id 参数
    by：王健 at:2015-2-10
    排除已经加入项目的成员
    by：王健 at:2015-2-12
    发送短信，追加随机数，防止重复短信发不出去
    by：王健 at:2015-3-4
    优化settings 使用
    by:王健 at:2015-3-9

    by:王健 at:2015-3-10
    #增加系统消息
    by：尚宗凯 at：2015-04-10
    #不发消息了
    by：尚宗凯 at：2015-04-14
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    :param request:
    :param project_id:
    :return:
    """
    tels = [x for x in request.REQUEST.get('tel', '').strip(',').split(',') if x]
    group_id = request.REQUEST.get('group_id', None)
    if not group_id:
        return getResult(False, u'请提供分组信息', None)
    smsdebug = request.REQUEST.get('smsdebug', '')
    temp_group = Group.objects.get(project_id=project_id, pk=group_id)
    group = Group.objects.get(project_id=project_id, type='root')
    addlist = []
    sendlist = []
    userlist = []
    for tel in tels:
        try:
            user = get_user_model().objects.get(tel=tel)
            person, create = Person.objects.get_or_create(project_id=project_id, user=user)
            if not create and person.is_active:
                userlist.append(tel)
                continue
            person.is_active = True
            person.save()
            group.look_members.add(person.user)
            temp_group.look_members.add(person.user)
            addlist.append(tel)
            # NeedMessage.create_sys_message(user.pk, "title", SYS_MESSAGE['add_person_by_tel'])
        except get_user_model().DoesNotExist:
            # todo:发送短信，邀请该手机号
            if not smsdebug:
                submail = MESSAGEXsend(MESSAGE_CONFIGS)
                submail.add_to(tel)
                submail.set_project('U7C1M')
                submail.add_var('from', request.user.name)
                submail.add_var('project', group.project.name)
                import random

                submail.add_var('url', '%s?t=%s' % (settings.MESSAGE_URL, random.randint(0, 100) ))
                submail.xsend()
            sendlist.append(tel)
        except Exception, e:
            pass
    group.save()
    temp_group.save()

    return getResult(True, u'操作成功', {'addlist': addlist, 'sendlist': sendlist, 'userlist': userlist})


@login_project_manager_required
@transaction.atomic()
def add_person_by_tel2(request, project_id):
    """
    根据手机号，将成员加入项目,自动创建用户账号
    by:王健 at:2015-3-10
    优化逻辑，消除 get_or_create bug
    by:王健 at:2015-3-10
    加入项目 即 发短信
    by:王健 at:2015-3-14
    修改 数字 无法 通过join 合并, 去除 +86，没有名字的使用 手机号
    by:王健 at:2015-3-16
    优化根据手机号添加成员逻辑
    by:王健 at:2015-3-19
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    :param request:
    :param project_id:
    :return:
    @var(from),邀请您加入项目：@var(project)，您可以从@var(url) 下载我们的手机端App应用，使用登录账号：@var(tel) 和密码：@var(password)，登录手机App应用了解项目的相关信息或与其他成员交流。【依子轩科技】
    """
    tels = [x for x in request.REQUEST.get('tel', '').strip(',').split(',') if x]
    group_id = request.REQUEST.get('group_id', None)
    if not group_id:
        return getResult(False, u'请提供分组信息', None)
    smsdebug = request.REQUEST.get('smsdebug', '')
    temp_group = Group.objects.get(project_id=project_id, pk=group_id)
    group = Group.objects.get(project_id=project_id, type='root')
    addlist = []
    sendlist = []
    userlist = []
    error_tel = []
    import random

    for telstr in tels:
        tellist = []
        for c in telstr.replace('+86', ''):
            try:
                int(c)
                tellist.append(c)
            except:
                pass
        if len(tellist) == 11:
            tel = ''.join(tellist)
        else:
            error_tel.append(telstr)
            continue

        try:
            user = get_user_model().objects.get(tel=tel)
            create_user = False
            # tel = telstr
        except:

            create_user = True
            user = get_user_model()()
            user.name = tel
            user.tel = tel
            user.set_password(tel[-6:])
            user.save()
        person, create = Person.objects.get_or_create(project_id=project_id, user=user)
        if not create and person.is_active:
            userlist.append(telstr)
            continue
        person.is_active = True
        person.save()
        group.look_members.add(person.user)
        temp_group.look_members.add(person.user)
        addlist.append(telstr)
        if not smsdebug:
            submail = MESSAGEXsend(MESSAGE_CONFIGS)
            submail.add_to(tel)
            if create_user:
                submail.set_project('U7C1M')
                submail.add_var('password', tel[-6:])
            else:
                submail.set_project('a0efv1')
            submail.add_var('from', (True and [request.user.name] or [request.user.tel])[0])
            submail.add_var('project', group.project.name)
            submail.add_var('url', '%s' % settings.MESSAGE_URL)
            submail.add_var('tel', tel)

            submail.xsend()
        sendlist.append(telstr)
        if not create_user:
            cache.delete(MY_PROJECT_QUERY_LIST % user.pk)
            cache.delete(USERINFO_INFO % user.pk)
    group.save()
    temp_group.save()
    return getResult(True, u'操作成功',
                     {'addlist': addlist, 'sendlist': sendlist, 'userlist': userlist, 'error_tel': error_tel})

@login_project_status_zero_required
@login_project_manager_required
@transaction.atomic()
def add_person_by_tel3(request, project_id):
    """
    根据手机号将用户加入项目，未注册的手机号，不再自动注册
    by:王健 at:2015-3-24
    添加手机号保存逻辑
    by:尚宗凯 at:2015-3-25
    分组记录 优化
    by:王健 at:2015-03-25
    拉人改为可以拉多个人
    by:尚宗凯 at:2015-04-08
    修改短信文字
    by:王健 at:2015-04-14
    加入管理员分组的成员 默认都加入项目经理部
    by:王健 at:2015-04-19
    拉人加入不发系统消息
    by:王健 at:2015-04-20
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    优化need消息
    by：尚宗凯 at：2015-05-15
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    增加项目状态为 0 装饰器
    by:尚宗凯 at：2015-05-31
    :param request:
    :param project_id:
    :return:
    @var(from),邀请您加入项目：@var(project)，您可以从@var(url) 下载和了解我们。【依子轩软件科技】
    """
    tels = [x for x in request.REQUEST.get('tel', '').strip(',').split(',') if x]
    group_id = request.REQUEST.get('group_id', None)
    if not group_id:
        return getResult(False, u'请提供分组信息', None)
    smsdebug = request.REQUEST.get('smsdebug', '')
    temp_group = Group.objects.get(project_id=project_id, pk=group_id)
    group = Group.objects.get(project_id=project_id, type='root')
    addlist = []
    sendlist = []
    userlist = []
    error_tel = []
    for telstr in tels:
        tellist = []
        for c in telstr.replace('+86', ''):
            try:
                int(c)
                tellist.append(c)
            except:
                pass
        if len(tellist) == 11:
            tel = ''.join(tellist)
        else:
            error_tel.append(telstr)
            continue

        try:
            user = get_user_model().objects.get(tel=tel)
            person, create = Person.objects.get_or_create(project_id=project_id, user=user)
            if not create and person.is_active:
                userlist.append(telstr)
                continue
            person.is_active = True
            person.save()
            group.look_members.add(person.user)
            group.save()
            temp_group.look_members.add(person.user)
            temp_group.save()
            if temp_group.type == 'sys_manage':
                xm_group = Group.objects.get(project_id=project_id, type='sys_xmjl')
                xm_group.say_members.add(person.user)
                xm_group.save()

            addlist.append(telstr)
            cache.delete(MY_PROJECT_QUERY_LIST % user.pk)
            cache.delete(USERINFO_INFO % user.pk)
            NeedMessage.create_sys_message(user.pk, "title",
                                           settings.SYS_MESSAGE['add_person_by_tel'] % person.project.total_name)
            # receiver_user_ids = []
            # grp = Group.objects.filter(project_id=project_id).filter(type='sys_manage')[0]
            # say_members = [u[0] for u in grp.say_members.values_list('id')]
            # look_members = [u[0] for u in grp.look_members.values_list('id')]
            # receiver_user_ids = receiver_user_ids + say_members + look_members
            # receiver_user_ids = list(set(receiver_user_ids))
            receiver_user_ids = []
            grps = Group.objects.filter(project_id=project_id).all()
            for grp in grps:
                say_members = [u[0] for u in grp.say_members.values_list('id')]
                look_members = [u[0] for u in grp.look_members.values_list('id')]
                receiver_user_ids = receiver_user_ids + say_members + look_members
            receiver_user_ids = list(set(receiver_user_ids))
            NeedMessage.create_multiple_sys_message(receiver_user_ids,
                                                    "title",
                                                    SYS_MESSAGE['add_person_by_tel_project_member'] % (Project.objects.get(pk=project_id).total_name, request.user.name, user.name))  #orgApp.project.manager.name


        except Exception as e:
            pt = NSPersonTel()
            pt.tel = tel
            pt.create_time = datetime.datetime.now()
            pt.from_user = request.user
            pt.group = temp_group
            pt.project = Project.objects.get(pk=project_id)
            pt.save()

        if not smsdebug:
            import random

            submail = MESSAGEXsend(MESSAGE_CONFIGS)
            submail.add_to(tel)
            submail.set_project('rT7w11')
            submail.add_var('from', (True and [request.user.name] or [request.user.tel])[0])
            submail.add_var('project', group.project.name)
            submail.add_var('url', '%s?v=%s' % (settings.MESSAGE_URL, random.randint(0, 100)))
            submail.xsend()
        sendlist.append(telstr)

    group.save()
    temp_group.save()
    cache.delete(PROJECT_GROUP_USER % project_id)
    return getResult(True, u'操作成功',
                     {'addlist': addlist, 'sendlist': sendlist, 'userlist': userlist, 'error_tel': error_tel})


@login_project_manager_required
def get_upload_project_icon_url(request, project_id):
    """
    获取上传项目图标的url
    by：王健 at:2015-1-28
    上传到七牛
    by: 范俊伟 at:2015-04-14
    修改 获取url的函数，无需参数
    by: 王健 at:2015-04-14
    :param request:
    :param project_id:
    :return:
    """
    from nsbcs.views_bcsfile import create_fileobj
    from nsbcs.models import QN_PROJECT_ICON_BUCKET

    fileobj = create_fileobj(request, project_id=project_id, bucket=QN_PROJECT_ICON_BUCKET)
    return getResult(True, u'',
                     {'fileid': fileobj.pk, 'posturl': fileobj.get_post_url(), 'puturl': fileobj.get_put_url()})


@login_project_manager_required
def get_qn_upload_project_icon_url(request, project_id):
    """
    七牛云存储接口,获取上传项目图标的url
    by: 范俊伟 at:2015-04-08
    :param request:
    :param project_id:
    :return:
    """
    from nsbcs.views_bcsfile import create_fileobj
    from nsbcs.models import PROJECT_ICON_BUCKET

    fileobj = create_fileobj(request, project_id=project_id, bucket=QN_PROJECT_ICON_BUCKET)
    return getResult(True, u'',
                     {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


@login_project_manager_required
@transaction.atomic()
def update_project_icon_url(request, project_id):
    """
    修改项目图标的url
    by：王健 at:2015-1-28
    解决 删除项目的bug
    by:王健 at:2015-2-5
    解决 删除项目的bug
    by:王健 at:2015-2-9
    :param request:
    :param project_id:
    :return:
    """
    fileid = request.REQUEST.get('fileid')
    if fileid:
        fileobj = get_object_or_404(File, pk=fileid, project_id=project_id)
        fileobj.file_status = True
        fileobj.save()
        old_icon = None
        if fileobj.project.icon_url:
            old_icon = fileobj.project.icon_url
        fileobj.project.icon_url = fileobj
        fileobj.project.save()
        if old_icon:
            old_icon.delete()
        return getResult(True, u'上传成功', None)
    else:
        return getResult(False, u'没有上传文件id', None)


@client_login_project_required
def get_project_balance(request, project_id):
    """
    获取项目的余额信息
    by:王健 at:2015-3-2
    修改余额，算法
    by:王健 at:2015-3-15
    以消耗值 和 余额取反了
    by:王健 at:2015-3-16
    添加新的参数
    by:王健 at:2015-06-18
    增加项目id
    by:王健 at:2015-06-18
    优化关于界面内容
    by:王健 at:2015-06-27
    天数计算错了
    by:王健 at:2015-06-27
    优化返回结果
    by：尚宗凯 at：2015-07-01
    已使用天数，当天也算一天
    by:王健 at:2015-07-01
    :param request:
    :param project_id:
    :return:
    """
    record_list = ProjectRechargeRecord.objects.filter(project_id=project_id).order_by('-date')[:1]
    if len(record_list) > 0:
        pre = record_list[0]
    else:
        pre = ProjectRechargeRecord(date=datetime.datetime(year=2105, month=1, day=1))
    result = {'total': pre.price2}
    ppcr = ProjectPersonChangeRecord.objects.filter(project_id=project_id).order_by('-create_date')[:1]
    if len(ppcr) == 1:
        ppcr = ppcr[0]
    result['price'] = result['total'] - ppcr.commit_value()
    if not result['price']:
        result['price'] = 0
    result['person_nums'] = ppcr.members
    result['days'] = ppcr.commit_days()
    result['used_days'] = (timezone.now() - ppcr.project.create_time).days + 1
    result['project_company'] = u''
    if ppcr.project.company_id:
        result['project_company'] = ppcr.project.company.name
    result['status'] = ppcr.project.pay_type
    # result['yw_tel'] = '23423423423'
    result['kf_tel'] = '400 001 5552'
    result['project_id'] = project_id

    return getResult(True, u'获取项目余额信息', result)


@client_login_project_required
def set_project_baoting(request, project_id):
    """
    项目报停
    by:王健 at:2015-3-15
    :param request:
    :param project_id:
    :return:
    """
    days = int(request.REQUEST.get('days', '0'))

    ppcr, created = ProjectPersonChangeRecord.objects.get_or_create(project_id=project_id, create_date=timezone.now())
    if created:
        ppcr.members = ppcr.project.person_set.filter(is_active=True).count()
    ppcr.stop_days += days
    ppcr.save()
    return getResult(True, u'处理报停成功', ppcr.end_date.strftime('%Y-%m-%d'))


# @client_login_project_required
# @transaction.atomic()
# def delete_project(request, project_id):
#     """
#     删除项目，以及项目所有相关内容
#     by :尚宗凯 at：2015-03-18
#     增加装饰器
#     by :尚宗凯 at：2015-03-19
#     修改方法名称
#     by:尚宗凯 at:2015-3-30
#     :param project_id:
#     :return:
#     """
#     result = {}
#     try:
#         p = Project.objects.get(id=project_id)
#     except Exception as e:
#         print e
#         msg = u"该工程不存在"
#     if p:
#         # webhtml_order存在这个p就不删除了
#         if Order.objects.filter(project_id=project_id).count() != 0:
#             msg = u"这个工程存在于webhtml_order中，不删除"
#         else:
#             sg = SGlog.objects.filter(project_id=project_id)  # 删除施工日志
#             for i in sg:
#                 i.delete()
#             for i in RecordDate.objects.filter(project_id=project_id):  # 删除RecordDate
#                 i.delete()
#             filegroup = FileGroup.objects.filter(project_id=project_id)  # 删除FileGroup
#             for i in filegroup:
#                 i.delete()
#             filegruopjson = FileGroupJSON.objects.filter(project_id=project_id)  # 删除FileGroupJSON
#             for i in filegruopjson:
#                 i.delete()
#             pa = ProjectApply.objects.filter(project_id=project_id)  # 删除项目申请
#             for i in pa:
#                 i.delete()
#             pm = ProjectMessage.objects.filter(project_id=project_id)  # 删除系统消息
#             for i in pm:
#                 i.delete()
#             fr = FileRecord.objects.filter(project_id=project_id)  # 删除FileRecord
#             for i in fr:
#                 # i.delete()
#                 i.set_is_active_false()
#                 i.save()
#             grps = Group.objects.filter(project_id=project_id)  # 删除Group
#             for grp in grps:
#                 grp.delete()
#             person = Person.objects.filter(project_id=project_id)  # 删除Person
#             for i in person:
#                 i.delete()
#             for i in WuZiRecord.objects.filter(project_id=project_id):
#                 i.delete()
#             file = File.objects.filter(project_id=project_id)  # 删除BaseFile,File
#             for i in file:
#                 pk = i.pk
#                 i.delete()
#                 basefile = BaseFile.objects.filter(id=pk)
#                 for j in basefile:
#                     j.delete()
#             user = p.nsuser_set.all()  # 删除NSUser的关注
#             for i in user:
#                 i.guanzhu.remove(p)
#             gys = GYSAddress.objects.filter(project_id=project_id)  # 删除供应商信息
#             for i in gys:
#                 i.delete()
#             prr = ProjectRechargeRecord.objects.filter(project_id=project_id)  # 删除ProjectRechargeRecord
#             for i in prr:
#                 i.delete()
#             ppcr = ProjectPersonChangeRecord.objects.filter(project_id=project_id)
#             for i in ppcr:
#                 i.delete()
#             p.delete()  # 删除项目
#             msg = u"删除成功"
#     return getResult(True, msg, None)


@login_project_manager_required
@transaction.atomic()
def change_power_by_group(request, project_id):
    """
    向分组中添加、删除权限
    by:王健 at:2014-3-27
    :param request:
    :param project_id:
    :return:
    """
    group_id = request.REQUEST.get('group_id')
    power = request.REQUEST.get('power')
    do = request.REQUEST.get('do')
    if group_id and power and do:
        group = Group.objects.get(pk=group_id, project_id=project_id)
        if do == 'add':
            if not group.has_prower(power):
                group.append_prower(power)
                group.save()
            return getResult(True, u'添加权限成功')
        if do == 'remove':
            if group.has_prower(power):
                group.remove_prower(power)
                group.save()
            return getResult(True, u'删除权限成功')
    return getResult(False, u'修改权限失败，缺少参数')


@login_project_manager_required
@transaction.atomic()
def change_power_by_group2(request, project_id):
    """
    向分组中添加、删除权限
    by:王健 at:2014-5-6
    更新分组内的所有用户时间戳
    by:王健 at:2015-05-07
    优化分组权限修改
    by:王健 at:2015-05-12
    修改分组权限bug，更person中的timeline
    by:王健 at:2015-05-13
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    增加缓存删除
    by：尚宗凯 at：2105-05-21
    :param request:
    :param project_id:
    :return:
    """
    group_id = request.REQUEST.get('group_id')
    powers = [x for x in request.REQUEST.get('powers', '').strip(',').split(',') if x]
    if group_id and powers:
        group = Group.objects.get(pk=group_id, project_id=project_id)
        if group.type in ['sys_manage', 'sys_xmjl']:
            return getResult(False, u'修改权限失败，管理员分组和项目经理部分组无需修改权限')
        group.init_powers()
        group.powers = []
        for p in powers:
            if p:
                group.append_prower(p)
        group.save()
        user_ids = []
        for p in group.look_members.all():
            user_ids.append(p.id)
        for p in group.say_members.all():
            user_ids.append(p.id)
        for p in Person.objects.filter(user_id__in=user_ids, project_id=project_id):
            p.save(update_fields=['timeline'])

        for user_id in user_ids:
            cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("project_message", user_id, project_id, group_id))
            cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("sysmessage", user_id, project_id, group_id))
        return getResult(True, u'修改权限成功')
    return getResult(False, u'修改权限失败，缺少参数')


@login_project_manager_required
@transaction.atomic()
def change_power_by_person(request, project_id):
    """
    向个人中添加、删除权限
    by:王健 at:2014-3-27
    :param request:
    :param project_id:
    :return:
    """
    user_id = request.REQUEST.get('user_id')
    power = request.REQUEST.get('power')
    do = request.REQUEST.get('do')
    if user_id and power and do:
        person = Person.objects.get(user_id=user_id, project_id=project_id)
        if do == 'add':
            if not person.has_prower(power):
                person.append_prower(power)
                person.save()
            return getResult(True, u'添加权限成功')
        if do == 'remove':
            if person.has_prower(power):
                person.remove_prower(power)
                person.save()
            return getResult(True, u'删除权限成功')
    return getResult(False, u'修改权限失败，缺少参数')


@login_project_manager_required
@transaction.atomic()
def change_power_by_person2(request, project_id):
    """
    修改个人的权限，计算出逆权限
    by:王健 at:2015-05-06
    修改个人权限调试bug
    by:王健 at:2015-05-11
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    增加删除缓存
    by：尚宗凯 at：2015-05-21
    :param request:
    :param project_id:
    :return:
    """
    user_id = request.REQUEST.get('user_id')
    powers1 = [x for x in request.REQUEST.get('powers', '').strip(',').split(',') if x]
    p_set = set()
    for p in powers1:
        if p:
            p_set.add(int(p))
            # powers.append(p)
    # p_set = set([int(p) for p in powers])
    if user_id and powers1:
        person = Person.objects.get(user_id=user_id, project_id=project_id)

        powers_set = set(person.real_powers())

        for p in set(person.powers) - p_set:
            if p % 100 == 0:
                person.remove_prower(p)
        powers_set.update(set(person.powers))
        for p in p_set - powers_set:
            person.append_prower(p)
            person.remove_disprower(p)
        for p in powers_set - p_set:
            if p % 100 == 0:
                person.append_disprower(p)
        person.save()

        for g in Group.objects.filter(project_id=project_id):
            look_members_user_id_list = [i['id'] for i in g.look_members.values("id")]
            say_members_user_id_list = [i['id'] for i in g.say_members.values("id")]
            user_id_list = look_members_user_id_list + say_members_user_id_list
            if int(user_id) in user_id_list:
                cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("project_message", user_id, project_id, g.pk))
                cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("sysmessage", user_id, project_id, g.pk))
        return getResult(True, u'修改权限成功')

    return getResult(False, u'修改权限失败，缺少参数')


@client_login_project_required
@transaction.atomic()
def get_unread_num_by_flag(request, project_id):
    """
    获取某用户某项目各个flag的未读数量
    by:尚宗凯 at;2015-05-06
    优化如果用户无某个flag权限则显示数字为0
    by:尚宗凯 at;2015-05-15
    优化flag split
    by:王健 at:2015-05-18
    解决示例项目的bug
    by：尚宗凯 at：2015-05-18
    优化查询
    by：尚宗凯 at：2015-05-20
    优化获取权限节点
    by:王健 at:2015-05-28
    关闭 已删除项目未读数量设为0
    by：尚宗凯 at：2015-05-31
    修复一个bug
    by：尚宗凯 at：2015-05-31
    """
    flags = [x for x in request.REQUEST.get('flag', '').split(',') if x]
    user_id = request.user.pk
    if not flags:
        return getResult(False, u'参数错误')
    # result = cache.get(UNREAD_NUM_BY_FLAG % (project_id,user_id,flags))
    # if not result:


    result = []
    project = cache.get(PROJECT_INFO % project_id)
    if project is None:
        if Project.objects.filter(pk=project_id).exists():
            project = Project.objects.get(pk=project_id)
            project = MyEncoder.default(project)
            cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
    if int(project['status']) not in (0, 1):
        for flag in flags:
            result.append({"project_id": project_id, "flag": flag, "num": 0})
            return getResult(True, u'获取未读数量成功', result)

    for flag in flags:
        if int(project_id) == settings.SHOW_PROJECT_ID:
            result.append({"project_id": project_id, "flag": flag, "num": 0})
    all = query_project_filegroup_data_(project_id)
    flags_powers_dict = whether_user_have_power_by_flag(user_id, project_id, flags, all)

    # if not whether_user_have_power_by_flag(user_id, project_id, flags):
    for flag in flags_powers_dict.keys():
        if not flags_powers_dict[flag]:
            result.append({"project_id": project_id, "flag": flag, "num": 0})
        else:
            if not all['flag_child'][flag]:
                num = get_flag_unread_num_use_cache(flag, all['flags2'][flag], user_id, project_id)
                result.append({"project_id": project_id, "flag": flag, "num": num})
            else:
                total = 0
                for fg in all['flag_child'][flag]:
                    num = get_flag_unread_num_use_cache(fg, all['flags2'][fg], user_id, project_id)
                    result.append({"project_id": project_id, "flag": fg, "num": num})
                    total += num
                result.append({"project_id": project_id, "flag": flag, "num": total})

            # cache.set(UNREAD_NUM_BY_FLAG % (project_id,user_id,flags), result, settings.CACHES_TIMEOUT)
    return getResult(True, u'获取未读数量成功', result)


def get_flag_unread_num_use_cache(flag, file_group_id, user_id, project_id):
    """
    根据flag获取未读数量
    by: 尚宗凯 at：2015-05-20
    """
    num = cache.get(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id))
    last_read_time = UserLastReadTimeline.get_last_read_timeline(project_id=project_id,
                                                                 file_group_id=file_group_id,
                                                                 user_id=user_id)
    last_new_data_time = get_last_new_data_timeline(project_id, file_group_id, flag)
    if last_new_data_time and last_read_time and last_read_time > last_new_data_time:
        if num is not None:
            return num
    num = get_flag_unread_num(flag, file_group_id, user_id, project_id)
    cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), num, settings.CACHES_TIMEOUT)
    return num


def get_flag_unread_num(flag, file_group_id, user_id, project_id):
    """
    根据flag获取未读数量
    by：尚宗凯 at：2015-05-06
    增加缓存判断
    by：尚宗凯 at：2015-05-20
    """
    last_read_time = UserLastReadTimeline.get_last_read_timeline(project_id=project_id,
                                                                 file_group_id=file_group_id,
                                                                 user_id=user_id)
    last_new_data_time = get_last_new_data_timeline(project_id, file_group_id, flag)
    if last_new_data_time is not None and last_read_time > last_new_data_time:             #如果用户最后阅读某节点时间>节点最新数据时间
        return 0
    if flag == "gong_cheng_ri_zhi":  # 施工日志
        num = SGlog.objects.filter(project_id=project_id, timeline__gt=last_read_time, is_active=True).count()

        return num

    if flag in ["gong_cheng_xing_xiang_jin_du", "gong_zuo_ying_xiang_ji_lu", "gong_cheng_shi_ti", "an_quan_wen_ming",
                "bao_guang_jing_gao", "xiang_mu_wen_hua",  # filerecord
                "jin_du_ji_hua", "jin_du_fen_xi", "wen_jian_tong_zhi", "hui_yi_ji_yao", "jia_fang_jian_li_fa_wen",
                "xuan_chuan_bao_dao", "gong_cheng_liang_yu_suan",
                "ge_lei_jie_suan", "chan_zhi_bao_biao", "gui_fan_biao_zhun", "tu_ji", "qi_ta_zhi_shi",
                "shi_gong_zong_ping_mian_tu", "wo_xing_wo_xiu", "ri_chang_xun_cha"]:
        num = FileRecord.objects.filter(project_id=project_id, is_active=True, timeline__gt=last_read_time,
                                        file_group_id=file_group_id).count()
        return num

    if flag in ["shi_ce_shi_liang", "zhi_liang_jian_cha",
                "an_quan_wen_ming_jian_cha"]:  # enginecheck              #日常巡查虽然属于工程检查但是数据保存在filerecord里面
        num = EngineCheck.objects.filter(project_id=project_id, is_active=True,
                                         file_group_id=file_group_id,
                                         timeline__gt=last_read_time).count()
        return num

    if flag in ['gong_ying_shang_ming_lu']:  # gysaddress
        num = GYSAddress.objects.filter(project_id=project_id, file_group_id=file_group_id,
                                        timeline__gt=last_read_time).count()
        return num

    if flag in ['wu_zi_cai_gou_ji_lu', 'wu_zi_ru_ku_ji_lu', 'wu_zi_chu_ku_ji_lu']:  # wuzirecord
        num = WuZiRecord.objects.filter(project_id=project_id, file_group_id=file_group_id,
                                        is_active=True, timeline__gt=last_read_time).count()
        return num


@client_login_required_widthout_tel
@transaction.atomic()
def flush_project_last_read_timeline(request, project_id):
    """
    刷新工程最后一次阅读时间
    by：尚宗凯 at：2015-05-07
    改一下参数
    by：尚宗凯 at：2015-05-08
    """
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=0, user_id=user_id)
    return getResult(True, u'刷新最后一次阅读时间成功')


def get_needmessage_unread_number(request):
    """
    获取NEED消息未读数
    by:尚宗凯 at：2015-05-28
    """
    session_key = request.session.session_key
    jsonstr = urllib2.urlopen(settings.NEED_KF_BASE_URL+'/kf/get_needmessage_unread_number?sessionid=%s'%session_key).read()
    result = json.loads(jsonstr)
    return getResult(result['success'], result['message'], result)


# @client_login_required_widthout_tel
# @transaction.atomic()
# def get_project_message_unread_number(request, project_id):
#     """
#     获取项目公告未读数量
#     by：尚宗凯 at：2015-05-07
# 	修改不在项目管理部的人项目公告bug
# 	by：尚宗凯 at：2015-05-14
#     """
#     group_id = request.REQUEST.get('group_id')
#     user_id = request.user.pk
#     if not Group.is_user_is_sysmanager(project_id,user_id):
#         return getResult(True, u'成功获取项目公告未读数量', {"num": 0})
#     last_read_time = LastReadTimeProjectSysMessage.get_last_read_timeline(type="project_message", user_id=user_id,
#                                                                           project_id=project_id, group_id=group_id)
#     try:
#         num = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id,
#                                             timeline__gt=last_read_time).count()
#         result = {"num": num}
#         return getResult(True, u'成功获取项目公告未读数量', result)
#     except:
#         return getResult(False, u'获取项目公告未读数量失败')


# @client_login_required_widthout_tel
# @transaction.atomic()
# def get_sysmessage_unread_number(request, project_id):
#     """
#     获取系统消息未读数量
#     by：尚宗凯 at：2015-05-07
#     """
#     group_id = request.REQUEST.get('group_id')
#     user_id = request.user.pk
#     last_read_time = LastReadTimeProjectSysMessage.get_last_read_timeline(type="sysmessage", user_id=user_id,
#                                                                           project_id=project_id, group_id=group_id)
#
#     try:
#         l = SysMessage.objects.filter(project_id=project_id)
#         if last_read_time:
#             l = l.filter(timeline__gt=last_read_time)
#         if group_id:
#             l = l.filter(Q(user_id=user_id) | Q(user=None) | Q(to_group_id=group_id))
#         else:
#             l = l.filter(to_group_id=None).filter(Q(user_id=request.user.pk) | Q(user=None))
#         num = l.count()
#         result = {"num": num}
#         return getResult(True, u'成功获取系统消息未读数量', result)
#     except:
#         return getResult(False, u'获取系统消息未读数量失败')

    


def get_projectmessage_sysmessage_unread_number(request, project_id):
    """
    获取系统消息未读数量
    by：尚宗凯 at：2015-05-08
    如果用户不在项目经理部，则项目公告数量为0
    by:尚宗凯 at：2015-05-19
	解决系统消息小红点bug
	by：尚宗凯 at：2015-05-19
	增加缓存
	by：尚宗凯 at：2015-05-21
	修复系统消息小红点bug(系统消息传的茶树group_id有数据，但是query_sysmessage中的group_id无数据)
	by：尚宗凯 at：2015-05-22
    """
    group_id = request.REQUEST.get('group_id')
    user_id = request.user.pk

    result = {}
    sysmessage_last_read_time = LastReadTimeProjectSysMessage.get_last_read_timeline(type="sysmessage",
                                                                                     user_id=user_id,
                                                                                     project_id=project_id,
                                                                                     group_id=None)
    project_message_last_read_time = LastReadTimeProjectSysMessage.get_last_read_timeline(type="project_message",
                                                                                          user_id=user_id,
                                                                                          project_id=project_id,
                                                                                          group_id=group_id)
    sys_message_last_new_data_timeline = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE % ("sysmessage",project_id,group_id))
    if sys_message_last_new_data_timeline is not None and sysmessage_last_read_time > sys_message_last_new_data_timeline:
        sysmessage_num = 0
    else:
        sysmessage_num = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("sysmessage", user_id, project_id, None))
        if sysmessage_num == None:
            l = SysMessage.objects.filter(project_id=project_id)
            if sysmessage_last_read_time:
                l = l.filter(timeline__gt=sysmessage_last_read_time)
            if group_id:
                l = l.filter(Q(user_id=user_id) | Q(user=None) | Q(to_group_id=group_id))
            else:
                l = l.filter(to_group_id=None).filter(Q(user_id=request.user.pk) | Q(user=None))
            sysmessage_num = l.count()
            cache.set(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("sysmessage", user_id, project_id, None), sysmessage_num, settings.CACHES_TIMEOUT)
    result.update({"sysmessage_num": sysmessage_num})

    project_message_last_new_data_timeline = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE % ("project_message",project_id,group_id))
    if project_message_last_new_data_timeline is not None and project_message_last_read_time > project_message_last_new_data_timeline:
        project_message_num = 0
    else:
        project_message_num = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message_num", user_id, project_id, group_id))
        if project_message_num == None:
            #如果用户不在项目经理部，则项目公告数量为0
            project_user_group = get_project_user_group_use_cache(project_id)
            if user_id in project_user_group[Group.objects.get(project_id=project_id,type="sys_xmjl").pk]:
                project_message_num = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id, timeline__gt=project_message_last_read_time).count()
            else:
                project_message_num = 0
            cache.set(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message", user_id, project_id, group_id), project_message_num, settings.CACHES_TIMEOUT)
    result.update({"project_message_num": project_message_num})
    return getResult(True, u'成功获取系统消息未读数量', result)


    # try:
    #     sysmessage_num = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("sysmessage", user_id, project_id, None))
    #     if sysmessage_num == None:
    #         l = SysMessage.objects.filter(project_id=project_id)
    #         if sysmessage_last_read_time:
    #             l = l.filter(timeline__gt=sysmessage_last_read_time)
    #         if group_id:
    #             l = l.filter(Q(user_id=user_id) | Q(user=None) | Q(to_group_id=group_id))
    #         else:
    #             l = l.filter(to_group_id=None).filter(Q(user_id=request.user.pk) | Q(user=None))
    #         sysmessage_num = l.count()
    #         cache.set(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("sysmessage", user_id, project_id, group_id), sysmessage_num, settings.CACHES_TIMEOUT)
    #     result.update({"sysmessage_num": sysmessage_num})
    #
    #     project_message_num = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message_num", user_id, project_id, None))
    #     if project_message_num == None:
    #         #如果用户不在项目经理部，则项目公告数量为0
    #         if group_id and Group.objects.get(pk=group_id).type != "sys_xmjl":
    #             project_message_num = 0
    #         else:
    #             project_message_num = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id, timeline__gt=project_message_last_read_time).count()
    #         cache.set(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message", user_id, project_id, group_id), project_message_num, settings.CACHES_TIMEOUT)
    #     result.update({"project_message_num": project_message_num})
    #     return getResult(True, u'成功获取系统消息未读数量', result)
    # except:
    #     return getResult(False, u'获取系统消息和项目公告未读数量和失败')


def is_have_new_data(project_ids, user_id):
    """
    获取项目是否有新数据
    by：尚宗凯 at：2015-05-07
    针对示例项目特殊处理
    by：尚宗凯 at：2015-05-11
    根据项目状态返回是否有新数据
    by：尚宗凯 at：2015-05-31
    """
    result = []
    for project_id in project_ids:
        p = cache.get(PROJECT_INFO % project_id)
        if p is None:
            if Project.objects.filter(pk=project_id).exists():
                p = Project.objects.get(pk=project_id)
                p = MyEncoder.default(p)
                cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
        if int(p["status"]) not in (0,1):
            new_data = False
        if project_id == settings.SHOW_PROJECT_ID:
            new_data = False
        else:
            # new_data = get_whether_user_project_have_new_data(project_id, user_id)
            new_data = get_whether_user_project_have_new_data_with_cache(project_id, user_id)
        result.append({'project_id': project_id, "have_new_data": new_data})
    return result


# def get_whether_user_project_have_new_data(project_id, user_id):
#     """
#     根据user_id,project_id查询是否存在新数据
#     by：尚宗凯 at：2015-05-07
# 	修改参数
# 	by：尚宗凯 at：2015-05-08
# 	修改小红点出现的bug
# 	by：尚宗凯 at：2015-05-13
# 	根据flag判断权限是否有数据
# 	by：尚宗凯 at：2015-05-15
#     """
#     file_record_flags = ["gong_cheng_xing_xiang_jin_du","gong_cheng_jian_cha","xing_xiang_zhan_shi",
#                          "xiang_mu_wen_hua","gong_cheng_jin_du","wen_jian_chuan_da","gong_cheng_yu_jue_suan","zhi_shi_ku",
#                          "shi_gong_zong_ping_mian_tu","wo_xing_wo_xiu","bao_guang_jing_gao"]
#     last_read_time = UserLastReadTimeline.get_last_read_timeline(project_id=project_id, file_group_id=0,
#                                                                  user_id=user_id)
#     if Group.whether_user_have_power_by_flag(user_id, project_id, flag="gong_cheng_ri_zhi") and SGlog.objects.filter(project_id=project_id, timeline__gt=last_read_time, is_active=True).exclude(user_id=user_id).exists():  # 施工日志
#         return True
#     # elif SysMessage.has_new_message(project_id=project_id, last_read_time=last_read_time, user_id=user_id):
#     #     return True
#     elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="gong_cheng_jian_cha") and EngineCheck.objects.filter(project_id=project_id, is_active=True,
#                                     timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # enginecheck              #日常巡查虽然属于工程检查但是数据保存在filerecord里面
#         return True
#     elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="wu_zi_guan_li") and GYSAddress.objects.filter(project_id=project_id, timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # gysaddress
#         return True
#     elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="wu_zi_guan_li") and WuZiRecord.objects.filter(project_id=project_id, is_active=True,
#                                    timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # wuzirecord
#         return True
#     elif Group.whether_user_have_power_by_multi_flag(user_id, project_id,flags=file_record_flags) and FileRecord.objects.filter(project_id=project_id, is_active=True,timeline__gt=last_read_time).exclude(user_id=user_id).exists():
#         return True
#     else:
#         return False


def get_whether_user_project_have_new_data_with_cache(project_id, user_id):
    """
    根据user_id,project_id查询是否存在新数据,首先根据缓存判断
    by:尚宗凯 at：2105-05-20
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    优化获取权限节点
    by:王健 at:2015-05-28
    """
    project_last_new_data_timeline = cache.get(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
    flag_last_read_time = UserLastReadTimeline.get_last_read_timeline(project_id=project_id, file_group_id=0, user_id=user_id)
    if project_last_new_data_timeline is not None and project_last_new_data_timeline>flag_last_read_time:
        return True
    elif project_last_new_data_timeline is not None and project_last_new_data_timeline<= flag_last_read_time:
        return False

    all_flag = query_project_filegroup_data_(project_id)
    all_have_power_flag = all_flag_user_have_power_by_flag(user_id, project_id, all_flag['flags2'].keys(), all_flag)
    f = False
    for flag in all_have_power_flag:
        if flag in FILE_GROUP_FLAGS:
            if f:
                timeline = 0
            else:
                timeline = get_last_filerecord_timeline_by_project(project_id)
                f = True
        else:
            timeline = get_last_new_data_timeline(project_id, all_flag['flags2'][flag], flag)
        if flag_last_read_time < timeline:
            return True
    return False

@login_project_status_zero_or_one_required
@login_project_super_manager_required
def close_project(request, project_id):
    """
    关闭项目
    by：尚宗凯 at：2015-05-29
    删除 MY_PROJECT_QUERY_LIST 缓存
    by：尚宗凯 at:2015-06-01
    增加关闭项目要求项目状态为正常或欠费
    by：尚宗凯 at：2015-06-02
    短信验证码使用后从session中删除
    by: 范俊伟 at:2015-07-01
    """
    smsdebug = request.REQUEST.get('smsdebug', '')
    sms_code = request.REQUEST.get('sms_code')
    if not sms_code and smsdebug == "":
        return getResult(False, u'短信验证码不能为空。')
    if sms_code != request.session.get('smscode', None) and smsdebug == "":
        return getResult(False, u'短信验证码错误。')
    try:
        p = Project.objects.get(id=project_id)
        p.status = 2
        p.save()
        p = MyEncoder.default(p)
        cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
        cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
        request.session['smscode'] = None
        return getResult(True, u'成功关闭项目')
    except Project.DoesNotExist:
        return getResult(False, u'关闭项目失败')


@login_project_super_manager_required
def cancel_delete_project(request, project_id):
    """
    恢复删除项目
    by：尚宗凯 at：2015-06-01
    增加状态为 5 的恢复逻辑
    by：尚宗凯 at：2015-06-05
    短信验证码使用后从session中删除
    by: 范俊伟 at:2015-07-01
    """
    smsdebug = request.REQUEST.get('smsdebug', '')
    sms_code = request.REQUEST.get('sms_code')
    if not sms_code and smsdebug == "":
        return getResult(False, u'短信验证码不能为空。')
    if sms_code != request.session.get('smscode', None) and smsdebug == "":
        return getResult(False, u'短信验证码错误。')
    if Project.objects.filter(id=project_id).exists():
        p = Project.objects.get(id=project_id)
        request.session['smscode'] = None
        if p.status == 3:
            return getResult(False, u'项目已经是删除状态，不能恢复')
        elif p.status == 1:
            return getResult(False, u'项目是正常状态，不能恢复')
        elif p.status == 2:
            return getResult(False, u'项目是欠费，不能恢复')
        elif p.status == 4:
            p.status = 0
            p.delete_project_time = None
            p.save()
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'成功恢复项目')
        elif p.status == 5:
            p.status = 2
            p.delete_project_time = None
            p.save()
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'成功恢复项目为关闭')
    else:
        return getResult(False, u'恢复项目失败')

@login_project_super_manager_required
def set_project_status(request, project_id):
    """
    设置项目状态，方便开发
    by: 尚宗凯 at：2015-06-04
    """
    status = request.REQUEST.get('status','')
    if status != "":
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = int(status)
            if p.status == 4:
                p.delete_project_time = datetime.datetime.now()
            else:
                p.delete_project_time = None
            p.save()
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'设置项目成功')
    else:
        return getResult(False, u'设置项目失败')


@login_project_super_manager_required
def delete_project(request, project_id):
    """
    删除项目
    by：尚宗凯 at：2015-05-29
    增加删除公示期
    by: 尚宗凯 at：2015-06-01
    关闭状态项目不能删除
    by：尚宗凯 at：2015-06-04
    短信验证码使用后从session中删除
    by: 范俊伟 at:2015-07-01
    """
    smsdebug = request.REQUEST.get('smsdebug', '')
    sms_code = request.REQUEST.get('sms_code')
    if not sms_code and smsdebug == "":
        return getResult(False, u'短信验证码不能为空。')
    if sms_code != request.session.get('smscode', None) and smsdebug == "":
        return getResult(False, u'短信验证码错误。')
    if Project.objects.filter(id=project_id).exists():
        p = Project.objects.get(id=project_id)
        request.session['smscode'] = None
        if p.status == 3:
            return getResult(False, u'项目已经是删除状态')
        elif p.status == 4:
            return getResult(False, u'项目已经处于删除公示期')
        elif p.status == 2:
            p.status = 5
            p.delete_project_time = datetime.datetime.now()
            p.save()
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD)
        else:
            p.status = 4
            p.delete_project_time = datetime.datetime.now()
            p.save()
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD)
    else:
        return getResult(False, u'删除项目失败')


# @client_admin_login_required
# @transaction.atomic()
# def set_project_expired_date(request):
#     """
#     客服设置项目过期时间
#     by: 尚宗凯 at：2015-06-08
#     """
#     project_id = request.REQUEST.get('project_id', '')
#     user_id = request.user.pk
#     order_id = request.REQUEST.get('order_id', None)
#     contract_code = request.REQUEST.get('contract_code', None)
#     price = request.REQUEST.get('price', 0)
#     expired_date = request.REQUEST.get('expired_date', '')
#     if expired_date and project_id:
#         try:
#             expired_date = datetime.datetime.strptime(expired_date, "%Y-%m-%d").date()
#             p = Project.objects.get(pk=project_id)
#             p.expired_date = expired_date
#             p.save()
#
#             recharge_record = RechargeRecord()
#             recharge_record.order_id = order_id
#             recharge_record.contract_code = contract_code
#             recharge_record.user_id = user_id
#             recharge_record.project_id = project_id
#             recharge_record.price = price
#             recharge_record.expired_date = expired_date
#             recharge_record.recharge_type = 0
#             recharge_record.create_time = timezone.now()
#             recharge_record.save()
#             return getResult(True, u'设置成功')
#         except Exception as e:
#             print e
#             return getResult(False, u'创建失败')
#     else:
#         return getResult(False, u'expired_date和project_id不能为空')










