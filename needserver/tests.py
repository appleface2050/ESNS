# coding=utf-8
# Date:2015/1/4
# Email:wangjian2254@gmail.com
import calendar
import datetime
import json
from django.db import connection
from django.db.models import Q, Sum
from django.conf import settings
from django.utils import timezone
from company.models import CompanyPerson, BigCompany, Company, SysNews, SysColumn, SaveNews, CompanyBanner, \
    CompanyColumn, CompanyNews, FollowCompany, SysBanner
from needserver import FILE_GROUP_FLAGS, FILE_GROUP_FLAGS_FILES, FILE_GROUP_FLAGS_BGIMAGES, FILE_GROUP_FLAGS_IMAGES
from needserver.jifenutil import login_jifen, create_data_jifen, query_fen_by_uid, remove_fen, login_jifen2, \
    create_data_jifen2, query_fen_by_uid2

from needserver.models import Project, SGlog, SGTQlog, ProjectApply, FileRecord, Person, FileGroupJSON, EngineCheck, \
    GYSAddress, WuZiRecord, Group, RecordDate, SysMessage, ProjectMessage, ProjectRechargeRecord, \
    ProjectPersonChangeRecord, NeedMessage, FileGroup, LastReadTimeProjectSysMessage
from needserver.views_project import get_flag_unread_num, is_have_new_data
from needserver.views_user import person_2_dict, group_2_dict, person_show_project_2_dict
from nsbcs.models import File
from util.apicloud import has_replay, query_replay_by_timeline, query_replay_num_by_timeline, has_replay_zan, \
    has_replay_or_zan, test_query_replay_by_timeline, get_last_replay_by_timeline
from util.basetest import BaseTestCase
from nsbcs.models import BaseFile

from django.contrib.auth import get_user_model
from util.cache_handle import query_project_filegroup_data_
from util.jsonresult import getTestResult, MyEncoder
# from needserver.sql.create_view_sql import CREATE_VIEW_NSUSER_USERINFO_PERSON_BASEFILE_SQL
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from needserver.models import NSUser
from util.project_power_cache import all_flag_user_have_power_by_flag
from Need_Server.settings import DELETE_PROJECT_PUBLICITY_PERIOD
from util import PROJECT_INFO

__author__ = u'王健'

from django.test import TestCase

username = '18622231518'
truename = u'测试用户1'


class RegUserTest(BaseTestCase):
    """
    注册用户、登录、创建项目 接口单元测试
    by:王健 at:2015-1-5
    使用自定义单元测试类，兼容积分返回值
    by:王健 at:2015-2-5
    """

    def tearDown(self):
        """
        测试完成，删除数据的操作
        屏蔽mongodb
        by:王健 at:2015-3-8
        :return:
        """
        # remove_fen()

    def reg_user(self, u, name):
        """
        按照用户名和密码 注册新用户
        by:王健 at:2015-1-7
        username 改为tel字段
        by:王健 at:2015-1-8
        增加了smsdebug 参数，方便测试
        by:王健 at:2015-1-15
        修改个人信息返回值
        by:王健 at:2015-1-20
        :return:
        """
        # 注册新用户
        newuserdata = {"password": '123456', 'tel': u,
                       'name': name, 'smsdebug': 'sdf'}
        response = self.client.post('/ns/reg_user', newuserdata)

        self.assertEqual(200, response.status_code, u'注册新用户报错')
        user = get_user_model().objects.get(tel=u)
        self.assertJSONEqual(response.content, getTestResult(True, u'注册成功',
                                                             user.get_user_map(True)), u'注册新用户，返回结果有变化，需要确认，或修改单元测试')

    def setUp(self):
        """
        所有单元测试前的 基础设置，注册用户、创建项目
        by:王健 at:2015-1-5
        username 改为tel字段
        by:王健 at:2015-1-8
        增加了smsdebug 参数，方便测试
        by:王健 at:2015-1-15
        修改个人信息返回值
        by:王健 at:2015-1-20
        将创建的项目，作为成员变量存入单元测试类
        by:王健 at:2015-1-21
        :return:
        """
        # 注册新用户
        newuserdata = {"password": '123456', 'tel': username,
                       'name': truename, 'smsdebug': 'sdf'}
        response = self.client.post('/ns/reg_user', newuserdata)

        self.assertEqual(200, response.status_code, u'注册新用户报错')
        user = get_user_model().objects.get(tel=username)
        self.assertJSONEqual(response.content, getTestResult(True, u'注册成功',
                                                             user.get_user_map(True)), u'注册新用户，返回结果有变化，需要确认，或修改单元测试')

        # 创建项目
        newuserdata = {"name": u'测试项目1', 'total_name': u'单元测试创建的项目', 'jzmj': 300, 'jglx': u'钢结构',
                       'jzcs': 3, 'htzj': 340000, 'kg_date': '2015-12-01', 'days': 50, 'address': 1,
                       'jsdw': u'水水水水是建设六局', 'jsdw_fzr': u'小刘',
                       'kcdw': u'勘察第一分院', 'kcdw_fzr': u'喜洋洋',
                       'sjdw': u'设计第二院', 'sjdw_fzr': u'灰太狼',
                       'sgdw': u'施工第三局', 'sgdw_fzr': u'美羊羊',
                       'jldw': u'监理第二单位', 'jldw_fzr': u'村长',
        }
        response = self.client.post('/ns/reg_project', newuserdata)

        self.assertEqual(200, response.status_code, u'注册新用户报错')
        self.project = Project.objects.filter(manager=user)[0]
        self.assertJSONEqual(response.content,
                             getTestResult(True, u'成功创建：%s' % self.project.total_name, MyEncoder.default(self.project)),
                             u'创建项目，返回结果有变化，需要确认，或修改单元测试')

    def login(self, username, password):
        """
        登录 接口测试
        by:王健 at:2015-1-5
        username 改为tel字段
        by:王健 at:2015-1-8
        返回值 修改
        by:王健 at:2015-1-16
        修改个人信息返回值
        by:王健 at:2015-1-20
        记录当前登录的用户对象
        by:王健 at:2015-3-25
        """
        # 登录
        login_response = self.client.post('/ns/login', {'tel': username, 'password': password})
        self.assertEqual(200, login_response.status_code, u'用户登录报错')
        user = get_user_model().objects.get(tel=username)

        self.login_user = user

        self.assertJSONEqual(login_response.content,
                             getTestResult(True, u'登录成功', user.get_user_map(True)),
                             u'用户登录，返回结果有变化，需要确认，或修改单元测试')

    def submit_user_tel(self, username, password):
        """
        验证手机号 接口测试
        by:王健 at:2015-1-15
        验证手机号，接口返回结果修改
        by:王健 at:2015-1-16
        """

        login_response = self.client.post('/ns/submit_user_tel',
                                          {'tel': username, 'code': password, 'name': u'试试', 'smsdebug': 'sd'})
        self.assertEqual(200, login_response.status_code, u'验证手机号')
        self.assertJSONEqual(login_response.content,
                             getTestResult(True, u'验证手机号成功', None),
                             u'验证手机号，返回结果有变化，需要确认，或修改单元测试')

    def logout(self):
        """
        登出接口测试
        by:王健 at:2015-1-5
        :return:
        """
        # 登录
        login_response = self.client.post('/ns/logout')
        self.assertEqual(200, login_response.status_code, u'用户登录报错')

    def current_user(self):
        """
        获取当前用户的信息接口 测试
        by:王健 at:2015-1-5
        username 改为tel字段
        by:王健 at:2015-1-8
        修改个人信息返回值
        by:王健 at:2015-1-20
        :return:
        """
        # 登录组织
        login_response = self.client.post('/ns/current_user', {})
        self.assertEqual(200, login_response.status_code, u'获取当前用户的信息接口 错误')
        user = get_user_model().objects.get(tel=username)
        self.assertJSONEqual(login_response.content, getTestResult(True, '', user.get_user_map(True)),
                             u'获取当前用户的信息接口，返回结果有变化，需要确认，或修改单元测试')

    def update_userinfo(self, username, **kwargs):
        """
        用户修改自己的基础信息
        by:王健 at:2015-1-18
        修改个人信息返回值
        by:王健 at:2015-1-20
        :return:
        """
        login_response = self.client.post('/ns/update_userinfo', kwargs)
        self.assertEqual(200, login_response.status_code, u'用户修改自己的基础信息 错误')
        user = get_user_model().objects.get(tel=username)
        u = MyEncoder.default(user.userinfo)
        u.update(user.get_user_map(True))
        self.assertJSONEqual(login_response.content, getTestResult(True, u'修改个人信息成功', u),
                             u'用户修改自己的基础信息，返回结果有变化，需要确认，或修改单元测试')


    def close_project(self, project_id):
        """
        测试关闭项目
        by：尚宗凯 at：2015-05-31
        :return:
        """
        response = self.client.post('/ns/%s/close_project' % project_id, {"smsdebug":1})
        self.assertEqual(200, response.status_code, u'测试关闭项目错误')
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = 2
            p.save()
            p = MyEncoder.default(p)
        self.assertJSONEqual(response.content,
                             getTestResult(True, u'成功关闭项目'),
                             u'关闭项目失败，需要确认，或修改单元测试')


    def delete_project(self, project_id):
        """
        测试删除项目
        by：尚宗凯 at：2015-05-31
        修改单元测试
        by：尚宗凯 at：2015-06-01
        :return:
        """
        from Need_Server.settings import DELETE_PROJECT_PUBLICITY_PERIOD
        response = self.client.post('/ns/%s/delete_project' % project_id, {"smsdebug":1})
        self.assertEqual(200, response.status_code, u'测试关闭项目错误')
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = 3
            p.save()
            p = MyEncoder.default(p)
        self.assertJSONEqual(response.content,
                             getTestResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD),
                             u'关闭项目失败，需要确认，或修改单元测试')


    def get_unread_num_by_flag(self, user_id, project_id, flags):
        """
        测试获取未读数量
        by：尚宗凯 at：2015-05-06
        """
        login_response = self.client.post('/ns/%s/get_unread_num_by_flag'%project_id, {"flags":flags, "user_id":user_id})
        flag_list = flags.split(",")
        result = []
        for flag in flag_list:
            if FileGroup.is_flag_is_a_father_flag(flag):                                            #flag是一个父级节点
                fgs = FileGroup.get_child_flag(flag)
                total = 0
                for fg in fgs:
                    num = get_flag_unread_num(fg.flag, user_id, project_id)
                    # result.append(copy.deepcopy({"project_id":project_id, "flag":flag, "num":num}))
                    total += num
                    result.append({"project_id":project_id, "flag":fg.flag, "num":num})
                result.append({"project_id":project_id, "flag":flag, "num":total})
            else:                                                                                   #flag是一个子节点
                num = get_flag_unread_num(flag, user_id, project_id)
                result.append({"project_id":project_id, "flag":flag, "num":num})
        for i in result:
            i["project_id"] = str(i["project_id"])
        self.assertEqual(200, login_response.status_code, u'测试获取未读数量错误')
        self.assertJSONEqual(login_response.content,
                             getTestResult(True, u'获取未读数量成功', result),
                             u'获取未读数量失败，需要确认，或修改单元测试')

    def update_project(self, project_id, **kwargs):
        """
        修改项目信息
        by:王健 at:2015-2-3
        :return:
        """
        login_response = self.client.post('/ns/%s/update_project?id=%s' % (project_id, project_id), kwargs)
        self.assertEqual(200, login_response.status_code, u'修改项目信息 错误')
        project = Project.objects.get(pk=project_id)
        u = MyEncoder.default(project)
        self.assertJSONEqual(login_response.content, getTestResult(True, u'修改信息成功', u),
                             u'修改项目信息，返回结果有变化，需要确认，或修改单元测试')

    def get_upload_files_url(self, project_id, **kwargs):
        """
        上传附件测试
        by:尚宗凯 at:2015-3-4
        :return:
        """
        login_response = self.client.post('/nf/%s/get_upload_files_url' % (project_id), kwargs)
        self.assertEqual(200, login_response.status_code, u'上传附件错误')
        project = Project.objects.get(pk=project_id)
        fileobj = File.objects.all().order_by('-create_time')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, u'', {'fileid': fileobj.pk,
                                                                               'posturl': fileobj.get_post_url(),
                                                                               'puturl': fileobj.get_put_url()}),
                             u'修改项目信息，返回结果有变化，需要确认，或修改单元测试')

    def get_userinfo(self, project_id, userid):
        """
        获取某个用户的个人信息
        by:王健 at:2015-1-18
        修改个人信息返回值
        by:王健 at:2015-1-20
        修改userinfo接口的id值
        by:王健 at:2015-2-25
        变更为使用视图测试
        by:尚宗凯 at:2015-3-7
        查询表替代视图
        by:尚宗凯 at:2015-3-8
        :return:
        """
        login_response = self.client.post('/ns/%s/get_userinfo' % project_id, {'user_id': userid})
        self.assertEqual(200, login_response.status_code, u'获取某个用户的个人信息 错误')
        if Person.objects.filter(user_id=userid, project_id=project_id).exists():
            user = get_user_model().objects.get(pk=userid)
            p = user.get_user_map()
            if hasattr(user, 'userinfo') and user.userinfo:
                p.update(MyEncoder.default(user.userinfo))
            p['id'] = user.pk
            # p = VNSUseruUserInfoPersonBaseFile.objects.get(user_id=userid,project_id=project_id)
            # p = p.toJSON()
            # p['id'] = p['user_id']
            self.assertJSONEqual(login_response.content, getTestResult(True, '', p),
                                 u'获取某个用户的个人信息，返回结果有变化，需要确认，或修改单元测试')
        else:
            self.assertJSONEqual(login_response.content, getTestResult(False, u'不是项目组内成员'),
                                 u'获取某个用户的个人信息，返回结果有变化，需要确认，或修改单元测试')

    def my_project(self):
        """
        获取当前用户关注的项目接口 测试
        by:王健 at:2015-1-5
        优化查询条件, 修改返回值
        by:王健 at:2015-1-30
        元祖改为字符串
        by:王健 at:2015-1-31
        优化我的项目 单元测试
        by:王健 at:2015-4-3
        修改我的项目的单元测试
        by:王健 at:2015-04-16
        :return:
        """
        # 我关注的项目列表
        login_response = self.client.post('/ns/my_project', {})
        self.assertEqual(200, login_response.status_code, u'获取当前用户关注的接口 错误')
        user = get_user_model().objects.get(tel=self.login_user.tel)
        pl = Project.objects.filter(pk__in=[u[0] for u in user.person_set.values_list('project_id')]).order_by('-id')
        l = []
        for p in pl:
            pd = p.toJSON()
            pd['is_guanzhu'] = False
            l.append(pd)
        # for p in Project.objects.filter(pk__in=ProjectApply.objects.filter(user=user, status=None).values(('project_id'))):
        #     pd = p.toJSON()
        #     pd['is_guanzhu'] = True
        #     l.append(pd)
        self.assertJSONEqual(login_response.content, getTestResult(True, None, l),
                             '获取我关注的项目，返回结果有变化，需要确认，或修改单元测试')

    def my_project2(self):
        """
        获取当前用户关注的项目接口 测试，第二版
        by:王健 at:2015-05-20
		修改my_project2
		by：尚宗凯 at：2015-06-04
        :return:
        """
        # 我关注的项目列表
        login_response = self.client.post('/ns/my_project2', {})
        self.assertEqual(200, login_response.status_code, u'获取当前用户关注的接口 错误')
        user = get_user_model().objects.get(tel=self.login_user.tel)
        project_ids = [u[0] for u in user.person_set.values_list('project_id')]
        project_ids2 = [u for u in user.person_set.values(('project_id'))]
        pl = Project.objects.filter(pk__in=project_ids).order_by('-id')
        l = []
        for p in pl:
            pd = p.toJSON()
            pd['is_guanzhu'] = False
            if "status" in pd.keys() and pd['status'] == 4 and pd['delete_project_time'] and (datetime.datetime.now() - datetime.datetime.strptime(pd['delete_project_time'],'%Y-%m-%d %H:%M:%S') >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD)):
                    project = Project.objects.get(pk=p['id'])
                    project.status = 3
                    project.save()
                    cache.delete(PROJECT_INFO % project.pk)
                    pd['status'] = 3
                    pd['delete'] = True
                    pd['is_active'] = False
            l.append(pd)
        show_project = Project.objects.get(pk=settings.SHOW_PROJECT_ID).toJSON()
        show_project["is_show_project"] = True
        l.append(show_project)
        have_new_data = is_have_new_data(project_ids, self.login_user.pk)
        # for p in Project.objects.filter(pk__in=ProjectApply.objects.filter(user=user, status=None).values(('project_id'))):
        # pd = p.toJSON()
        #     pd['is_guanzhu'] = True
        #     l.append(pd)
        self.assertJSONEqual(login_response.content, getTestResult(True, None, {"resultlist": l, "have_new_data": have_new_data}),
                             '获取我关注的项目 第二版，返回结果有变化，需要确认，或修改单元测试')

    def query_project(self, start=0, address='0'):
        """
        查询默认的项目列表的接口 测试
        by:王健 at:2015-1-5
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/query_project', {'start': start, 'address': address})
        self.assertEqual(200, login_response.status_code, u'查询默认的项目列表的接口')
        l = Project.objects.all()
        if int(address):
            l = l.filter(address=address)
        l = l.order_by('-timeline')[start:start + 20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询默认的项目列表的接口，返回结果有变化，需要确认，或修改单元测试')

    def query_project_by_key(self, start=0, address='0', key=''):
        """
        根据关键字查询项目列表接口 测试
        by:王健 at:2015-1-5
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/query_project', {'start': start, 'address': address, 'key': key})
        self.assertEqual(200, login_response.status_code, u'根据关键字查询项目列表接口')
        l = Project.objects.order_by('-timeline')
        if int(address):
            l = l.filter(address=address)
        if key:
            l = l.filter(total_name__icontains=key)
        l = l[start:start + 20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'根据关键字查询项目列表接口，返回结果有变化，需要确认，或修改单元测试')

    def update_log_by_date(self, project_id, text, sg_tq_id, day, fengli, qiwen):
        """
        提交日志 测试
        by:王健 at:2015-1-6
        参数名字修改
        by:王健 at:2015-1-6
        datetime 改为 create_time
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        增加项目id，条件
        by:王健 at:2015-1-21
        日志 测试，因为返回值变化，所以修改
        by:王健 at:2015-1-29
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/update_log_by_date' % project_id,
                                          {'text': text, 'sg_tq_id': sg_tq_id, 'weather': day, 'wind': fengli,
                                           'qiwen': qiwen, })
        self.assertEqual(200, login_response.status_code, u'提交日志')
        sglog = SGlog.objects.all().order_by('-create_time')[0]
        sgtqlog = MyEncoder.default(sglog.sg_tq_log)
        sgtqlog.update(MyEncoder.default(sglog))
        self.assertJSONEqual(login_response.content, getTestResult(True, u'保存日志成功', sgtqlog),
                             u'提交日志，返回结果有变化，需要确认，或修改单元测试')

    def del_log_by_id(self, project_id, logid):
        """
        删除日志，根据id
        by:王健 at:2015-2-10
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/del_log_by_id' % project_id,
                                          {'id': logid})
        self.assertEqual(200, login_response.status_code, u'删除日志')
        sglognum = SGlog.objects.filter(pk=logid, is_active=True).count()
        self.assertEqual(0, sglognum, u'删除日志失败，还有数据')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'删除日志成功', str(logid)),
                             u'删除日志，返回结果有变化，需要确认，或修改单元测试')

    def query_log_date_list(self, project_id, start):
        """
        查询日志天气列表 测试
        by:王健 at:2015-1-6
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        参数改为timeline
        by:王健 at:2015-1-20
        增加项目id条件
        by:王健 at:2015-1-21
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_log_date_list' % project_id, {'timeline': start})
        self.assertEqual(200, login_response.status_code, u'查询日志天气列表')
        l = SGTQlog.objects.filter(project_id=project_id).order_by('-date')[start:start + 20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询日志天气列表，返回结果有变化，需要确认，或修改单元测试')

    def query_log_date_list_old(self, project_id, start):
        """
        查询日志测试
        by:尚宗凯 at:2015-3-4
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_log_date_list_old' % project_id, {'timeline': start})
        self.assertEqual(200, login_response.status_code, u'查询日志天气列表')
        l = SGTQlog.objects.filter(project_id=project_id).order_by('-date')[start:start + 20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询日志天气列表，返回结果有变化，需要确认，或修改单元测试')

    def query_log_list_by_date(self, project_id, sg_tq_id):
        """
        获取某一天的日志的接口 测试
        by:王健 at:2015-1-6
        datetime 改为 create_time
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        增加项目id条件
        by:王健 at:2015-1-21
        修改参数
        by:尚宗凯 at:2015-3-25
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_log_list_by_date' % project_id, {'sg_tq_id': sg_tq_id})
        self.assertEqual(200, login_response.status_code, u'获取某一天的日志的接口')
        l = SGlog.objects.filter(project_id=project_id, sg_tq_log_id=sg_tq_id).order_by('timeline')
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'获取某一天的日志的接口，返回结果有变化，需要确认，或修改单元测试')

    def query_log_list_by_date_2(self, project_id, sg_tq_id, timeline):
        """
        获取某一天的日志的接口2 测试
        by:王健 at:2015-1-6
        datetime 改为 create_time
        by:王健 at:2015-1-12
        修改Model名字，去除下划线， 优化带有日期查询的排序问题，防止隔过数据
        by:王健 at:2015-1-13
        增加项目id条件
        by:王健 at:2015-1-21
        修改参数
        by:尚宗凯 at:2015-3-25
        :return:
        """
        # 查询项目列表

        login_response = self.client.post('/ns/%s/query_log_list_by_date' % project_id,
                                          {'sg_tq_id': sg_tq_id, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'获取某一天的日志的接口2')
        l = SGlog.objects.filter(project_id=project_id, sg_tq_log_id=sg_tq_id, timeline__gt=timeline).order_by(
            'timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'获取某一天的日志的接口2，返回结果有变化，需要确认，或修改单元测试')

    def apply_project(self, project_id, text, authorname):
        """
        使用当前登录用户的身份发送请求加入项目中id为*的项目
        by:王健 at:2015-1-7
        create_date 改为 create_time
        by:王健 at:2015-1-12
        增加项目id条件
        by:王健 at:2015-1-21
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/apply_project' % project_id, {'text': text})
        self.assertEqual(200, login_response.status_code, u'发出项目请求')
        papply = ProjectApply.objects.filter(project_id=project_id, user__tel=authorname).order_by('-create_time')[0]
        self.assertJSONEqual(login_response.content,
                             getTestResult(True, None, {'apply_id': papply.pk, 'id': str(project_id)}),
                             u'发出项目请求，返回结果有变化，需要确认，或修改单元测试')

    def get_all_applyproject(self, project_id):
        """
        使用当前登录用户的身份 获取所有本项目的加入申请
        by:王健 at:2015-1-7
        优化了model到dict的算法
        by:王健 at:2015-1-8
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/get_all_applyproject' % project_id, {})
        self.assertEqual(200, login_response.status_code, u'获取所有的未处理申请')
        result = []
        from views_project import applyproject_to_dict

        for orgapp in ProjectApply.objects.filter(project_id=project_id, status=None):
            result.append(applyproject_to_dict(orgapp))
        self.assertJSONEqual(login_response.content, getTestResult(True, None, result),
                             u'获取所有的未处理申请，返回结果有变化，需要确认，或修改单元测试')

    def change_applyproject_add(self, project_id, apply_id, group_id):
        """
        处理 申请（添加）
        by:王健 at:2015-1-7
        create_date 改为 create_time
        by:王健 at:2015-1-12
        添加分组id
        by:王健 at:2015-2-10
        优化审批申请接口测试
        by:王健 at:2015-3-25
        :return:
        """
        orgapp = ProjectApply.objects.get(pk=apply_id)

        is_member = Person.objects.filter(project_id=project_id, user_id=orgapp.user_id, is_active=True).exists()

        # 查询项目列表
        login_response = self.client.post('/ns/%s/change_applyproject' % project_id,
                                          {'apply_id': apply_id, 'do': 'true', 'group_id': group_id})
        self.assertEqual(200, login_response.status_code, u'处理 申请（添加）')
        if is_member:
            self.assertJSONEqual(login_response.content, getTestResult(False, u'%s 已经是项目成员了' % orgapp.user.name, None),
                                 u'处理 申请（添加），返回结果有变化，需要确认，或修改单元测试')
        else:
            self.assertJSONEqual(login_response.content, getTestResult(True, None, None),
                                 u'处理 申请（添加），返回结果有变化，需要确认，或修改单元测试')

    def change_applyproject_remove(self, project_id, apply_id):
        """
        处理 申请（拒绝）
        by:王健 at:2015-1-7
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/change_applyproject' % project_id,
                                          {'apply_id': apply_id, 'do': 'false'})
        self.assertEqual(200, login_response.status_code, u'处理 申请（移除）')
        self.assertJSONEqual(login_response.content, getTestResult(True, None, None),
                             u'处理 申请（移除），返回结果有变化，需要确认，或修改单元测试')

    def change_user_group(self, project_id, group_id, do, user_id):
        """
        修改用户所属的分组
        by:王健 at:2015-2-6
        修改了 改变分组 的逻辑，修改相应的单元测试
        by:王健 at:2015-2-13
        修改单元测试的验证条件，临时原因 改为从say_members 里校验
        by:王健 at:2015-3-2
        逻辑变化，再测look_members
        by:王健 at:2015-3-16
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/change_user_group' % project_id,
                                          {'user_id': user_id, 'do': do, 'group_id': group_id})
        self.assertEqual(200, login_response.status_code, u'修改用户所属的分组')
        group = Group.objects.get(pk=group_id)
        if do == 'join':
            self.assertTrue(group.look_members.filter(pk=user_id).exists(), u'加入分组成员 失败')
        else:
            self.assertFalse(group.look_members.filter(pk=user_id).exists(), u'移出分组成员 失败')
        if Person.objects.filter(project_id=project_id, user_id=user_id, is_active=True).exists():
            self.assertJSONEqual(login_response.content, getTestResult(True, u'操作成功', None),
                                 u'修改用户所属的分组，返回结果有变化，需要确认，或修改单元测试')
        else:
            user = get_user_model().objects.get(id=user_id)
            self.assertJSONEqual(login_response.content, getTestResult(True, u'%s 已经被移出项目' % user.name, None),
                                 u'修改用户所属的分组，返回结果有变化，需要确认，或修改单元测试')

    def query_person(self, project_id, timeline, user=None):
        """
        查询项目内所有的用户
        by:王健 at:2015-1-16
        兼容示例项目的单元测试
        by:王健 at:2015-3-25
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_person' % project_id, {'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询项目内所有的用户')
        if not timeline:
            l = Person.objects.filter(project_id=project_id).order_by('-timeline')
        else:
            l = Person.objects.filter(project_id=project_id, timeline__gt=int(timeline)).order_by('timeline')
        ul = []
        for person in l:
            ul.append(person_2_dict(person))
        if not timeline and int(project_id) == settings.SHOW_PROJECT_ID:
            ul.append(person_show_project_2_dict(self.login_user))
        self.assertJSONEqual(login_response.content, getTestResult(True, None, ul),
                             u'查询项目内所有的用户，返回结果有变化，需要确认，或修改单元测试')

    def query_group(self, project_id, timeline):
        """
        查询项目内所有的群组
        by:王健 at:2015-1-16
        获取项目内有用群组，排除root
        by:王健 at:2015-2-2
        不排除 root 组，方便客户端 组织“未分组” 。
        by:王健 at:2015-2-3
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_group' % project_id, {'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询项目内所有的群组')
        if not timeline:
            l = Group.objects.filter(project_id=project_id).order_by('-timeline')
        else:
            l = Group.objects.filter(project_id=project_id, timeline__gt=int(timeline)).order_by('timeline')
        ul = []
        for person in l:
            ul.append(group_2_dict(person))
        self.assertJSONEqual(login_response.content, getTestResult(True, None, ul),
                             u'查询项目内所有的群组，返回结果有变化，需要确认，或修改单元测试')

    def check_file_upload_status(self, project_id, fileid):
        """
        根据fileid 检查文件是否已在bcs上
        by:尚宗凯 at:2015-3-4
        :return:
        """
        login_response = self.client.post('/nf/%s/check_file_upload_status' % project_id, {'fileid': fileid})
        self.assertEqual(200, login_response.status_code, u'获取文件下载url 错误')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'', False),
                             u'获取文件下载url，返回结果有变化，需要确认，或修改单元测试')

    def query_app_list(self, project_id):
        """
        获取项目的应用列表
        by:王健 at:2015-1-12
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_app_list' % project_id, {})
        self.assertEqual(200, login_response.status_code, u'获取项目的应用列表')
        result = json.loads(login_response.content)
        if len(result['result']) > 0:
            f = True
        else:
            f = False
        self.assertEqual(True, f, u'获取项目的应用列表，返回结果有变化，需要确认，或修改单元测试')

    def query_app_list2(self, project_id, timeline):
        """
        获取项目的应用列表,附带时间戳参数
        by:王健 at:2015-1-13
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_app_list' % project_id, {'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'获取项目的应用列表')
        result = json.loads(login_response.content)
        if result.has_key('result') and len(result['result']) > 0:
            f = True
        else:
            f = False
        self.assertEqual(False, f, u'获取项目的应用列表，返回结果有变化，需要确认，或修改单元测试')

    def query_app_list3(self, project_id):
        """
        获取项目的应用列表,附带时间戳参数
        by:王健 at:2015-1-13
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/query_app_list' % project_id, {'timeline': 234})
        self.assertEqual(200, login_response.status_code, u'获取项目的应用列表')
        result = json.loads(login_response.content)
        if result.has_key('result') and len(result['result']) > 0:
            f = True
        else:
            f = False
        self.assertEqual(True, f, u'获取项目的应用列表，返回结果有变化，需要确认，或修改单元测试')

    def create_file_by_group(self, project_id, fileid, title, text):
        """
        向项目项里 添加 文件
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        增加默认filetype参数
        by:尚宗凯 at:2015-3-30
        使用正确的flag
        by:王健 at:2015-06-02
        :return:
        """
        login_response = self.client.post('/ns/%s/create_file_by_group' % project_id,
                                          {'fileid': fileid, 'flag': 'jin_du_ji_hua', 'title': title, 'text': text, "filetype": "jpg"})
        self.assertEqual(200, login_response.status_code, u'向项目项里 添加 文件')
        filerecord = FileRecord.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(filerecord)),
                             u'向项目项里 添加 文件，返回结果有变化，需要确认，或修改单元测试')
        return filerecord

    def delete_file_by_filerecord_id(self, project_id, filerecord_id, flag):
        """
        测试删除上传的文件信息
        by:尚宗凯 at:2015-3-27
        """
        login_response = self.client.post('/ns/%s/delete_file_by_filerecord_id' % project_id, {'filerecord_id': filerecord_id, 'flag': flag})
        self.assertEqual(200, login_response.status_code, u'删除上传的文件信息')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'成功删除上传的文件信息', str(filerecord_id)),
                             u'删除上传的文件信息，返回结果有变化，需要确认，或修改单元测试')        

    def delete_enginecheck_by_enginecheck_id(self, project_id, enginecheck_id, flag):
        """
        测试删除工程检查
        by:尚宗凯 at:2015-3-30
        """
        login_response = self.client.post('/ns/%s/delete_enginecheck_by_enginecheck_id' % project_id, {'enginecheck_id': enginecheck_id, 'flag': flag})
        self.assertEqual(200, login_response.status_code, u'删除上传的文件信息')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'成功删除工程检查', str(enginecheck_id)),
                             u'删除工程检查，返回结果有变化，需要确认，或修改单元测试')

    def create_file_by_gong_cheng_xing_xiang_jin_du(self, project_id, **kwargs):
        '''
        工程形象进度上传后点击保存测试
        by:尚宗凯 at:2015-3-4
        :param project_id:
        :param kwargs:
        :return:
        '''
        login_response = self.client.post('/ns/%s/create_file_by_group' % (project_id), kwargs)
        self.assertEqual(200, login_response.status_code, u'工程形象进度点击保存')
        filerecord = FileRecord.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(filerecord)),
                             u'添加工程形象进度图片，返回结果有变化，需要确认，或修改单元测试')
        return filerecord

    def create_file_by_bao_guang_jing_gao(self, project_id, **kwargs):
        '''
        违章曝光上传后点击保存测试
        by:尚宗凯 at:2015-3-5
        :param project_id:
        :param kwargs:
        :return:
        '''
        login_response = self.client.post('/ns/%s/create_file_by_group' % (project_id), kwargs)
        self.assertEqual(200, login_response.status_code, u'违章曝光点击保存')
        filerecord = FileRecord.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(filerecord)),
                             u'添加违章曝光图片，返回结果有变化，需要确认，或修改单元测试')
        return filerecord

    def append_file_by_group(self, project_id, fileid, filerecord_id):
        """
        向项目项里 追加 文件
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        :return:
        """
        login_response = self.client.post('/ns/%s/create_file_by_group' % project_id,
                                          {'fileid': fileid, 'flag': 'gong_cheng_jin_du', 'id': filerecord_id})
        self.assertEqual(200, login_response.status_code, u'向项目项里 添加 文件')
        filerecord = FileRecord.objects.get(pk=filerecord_id)
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(filerecord)),
                             u'向项目项里 添加 文件，返回结果有变化，需要确认，或修改单元测试')
        return filerecord

    def query_file_by_group_1(self, project_id):
        """
        查询项目里的文件
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        :return:
        """
        login_response = self.client.post('/ns/%s/query_file_by_group' % project_id, {'flag': 'gong_cheng_jin_du'})
        self.assertEqual(200, login_response.status_code, u'查询项目里的文件')
        l = FileRecord.objects.filter(project_id=project_id, file_group__flag='gong_cheng_jin_du').order_by(
            '-create_time')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询项目里的文件，返回结果有变化，需要确认，或修改单元测试')

    def query_file_by_group_2(self, project_id):
        """
        查询项目里的文件
        by:王健 at:2015-1-12
        修改Model名字，去除下划线
        by:王健 at:2015-1-13
        修改create_time 为timeline
        by:王健 at:2015-2-13
        :return:
        """
        dt = datetime.datetime.now() - datetime.timedelta(days=-1)
        login_response = self.client.post('/ns/%s/query_file_by_group' % project_id, {'flag': 'gong_cheng_jin_du',
                                                                                      'timeline': calendar.timegm(
                                                                                          dt.utctimetuple())})
        self.assertEqual(200, login_response.status_code, u'查询项目里的文件2')
        l = FileRecord.objects.filter(project_id=project_id, file_group__flag='gong_cheng_jin_du',
                                      create_time__gt=dt).order_by('-create_time')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询项目里的文件2，返回结果有变化，需要确认，或修改单元测试')

    def create_enginecheck_by_group(self, project_id, fileid, flag, desc):
        """
        创建工程检查
        by:王健 at:2015-1-13
        :return:
        """
        login_response = self.client.post('/ns/%s/create_enginecheck_by_group' % project_id,
                                          {'flag': flag, 'fileid': fileid, 'desc': desc})
        self.assertEqual(200, login_response.status_code, u'创建工程检查')
        l = EngineCheck.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, u'创建工程检查成功', MyEncoder.default(l)),
                             u'创建工程检查，返回结果有变化，需要确认，或修改单元测试')
        return l

    def update_enginecheck_by_group(self, project_id, id, fileid, chuli, fucha, status, flag):
        """
        修改工程检查
        by:王健 at:2015-1-13
        修改工程检查 参数
        by:王健 at:2015-3-5
        :return:
        """
        login_response = self.client.post('/ns/%s/update_enginecheck_by_group' % project_id,
                                          {'id': id, 'fileid': fileid, 'chuli': chuli, 'fucha': fucha,
                                           'status': status, 'flag': flag})
        self.assertEqual(200, login_response.status_code, u'修改工程检查')
        l = EngineCheck.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'修改工程检查，返回结果有变化，需要确认，或修改单元测试')

    def query_enginecheck_by_group(self, project_id, flag, timeline):
        """
        查询工程检查
        by:王健 at:2015-1-13
        :return:
        """
        login_response = self.client.post('/ns/%s/query_enginecheck_by_group' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询工程检查')
        if not timeline:
            l = EngineCheck.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = EngineCheck.objects.filter(project_id=project_id, file_group__flag=flag,
                                           timeline__gt=int(timeline)).order_by('timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询工程检查，返回结果有变化，需要确认，或修改单元测试')

    def query_enginecheck_by_group_old(self, project_id, flag, timeline):
        """
        查询工程检查
        by:王健 at:2015-1-13
        :return:
        """
        login_response = self.client.post('/ns/%s/query_enginecheck_by_group_old' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询工程检查')
        if not timeline:
            l = EngineCheck.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = EngineCheck.objects.filter(project_id=project_id, file_group__flag=flag,
                                           timeline__lt=int(timeline)).order_by('-timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询工程检查2，返回结果有变化，需要确认，或修改单元测试')

    def create_gysaddress_by_group(self, project_id, id, flag, name, ghs, ghs_fzr, ghs_fzr_tel, is_hetong, pay_type,
                                   shr, shr_tel, bz):
        """
        创建供应商名录
        by:王健 at:2015-1-14
        修改返回值了
        by:王健 at:2015-1-29
        :return:
        """
        login_response = self.client.post('/ns/%s/create_gysaddress_by_group' % project_id,
                                          {'id': id, 'flag': flag, 'name': name, 'ghs': ghs, 'ghs_fzr': ghs_fzr,
                                           'ghs_fzr_tel': ghs_fzr_tel,
                                           'is_hetong': is_hetong, 'pay_type': pay_type, 'shr': shr, 'shr_tel': shr_tel,
                                           'bz': bz})
        self.assertEqual(200, login_response.status_code, u'创建供应商名录')
        l = GYSAddress.objects.order_by('-id')[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, u'创建供应商名录成功', MyEncoder.default(l)),
                             u'创建供应商名录，返回结果有变化，需要确认，或修改单元测试')
        return l

    def query_gysaddress_by_group(self, project_id, flag, timeline):
        """
        查询供应商名录
        by:王健 at:2015-1-14
        :return:
        """
        login_response = self.client.post('/ns/%s/query_gysaddress_by_group' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询供应商名录')
        if not timeline:
            l = GYSAddress.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = GYSAddress.objects.filter(project_id=project_id, file_group__flag=flag,
                                          timeline__gt=int(timeline)).order_by('timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询供应商名录，返回结果有变化，需要确认，或修改单元测试')

    def query_gysaddress_by_group_old(self, project_id, flag, timeline):
        """
        查询供应商名录
        by:王健 at:2015-1-14
        :return:
        """
        login_response = self.client.post('/ns/%s/query_gysaddress_by_group_old' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询供应商名录')
        if not timeline:
            l = GYSAddress.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = GYSAddress.objects.filter(project_id=project_id, file_group__flag=flag,
                                          timeline__lt=int(timeline)).order_by('-timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询供应商名录2，返回结果有变化，需要确认，或修改单元测试')

    def create_wuzirecord_by_group(self, project_id, id, flag, name, gg, num, company, lingliaoren, count, status):
        """
        创建物资记录
        by:王健 at:2015-1-14
        修改返回值了
        by:王健 at:2015-1-29
        :return:
        """
        login_response = self.client.post('/ns/%s/create_wuzirecord_by_group' % project_id,
                                          {'id': id, 'flag': flag, 'name': name, 'gg': gg, 'num': num,
                                           'company': company,
                                           'lingliaoren': lingliaoren, 'count': count, 'status': status})
        self.assertEqual(200, login_response.status_code, u'创建物资记录')
        l = WuZiRecord.objects.order_by('-id')[0]
        result = MyEncoder.default(l.record_date)
        result.update(MyEncoder.default(l))
        self.assertJSONEqual(login_response.content, getTestResult(True, u'创建物资记录成功', result),
                             u'创建物资记录，返回结果有变化，需要确认，或修改单元测试')
        return l

    def del_wuzirecord_by_id(self, project_id, logid):
        """
        删除物资记录，根据id
        by:王健 at:2015-2-10
        :return:
        """
        # 查询项目列表
        login_response = self.client.post('/ns/%s/del_wuzirecord_by_id' % project_id,
                                          {'id': logid})
        self.assertEqual(200, login_response.status_code, u'删除物资记录')
        sglognum = WuZiRecord.objects.filter(pk=logid, is_active=True).count()
        self.assertEqual(0, sglognum, u'删除物资记录失败，还有数据')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'删除物资记录成功', str(logid)),
                             u'删除物资记录，返回结果有变化，需要确认，或修改单元测试')

    def del_gysaddress_by_id(self, project_id, gysid):
        """
        删除供应商地址记录，根据id
        by:尚宗凯 at:2015-3-26
        :return:
        """
        login_response = self.client.post('/ns/%s/del_gysaddress_by_id' % project_id, {'id': gysid})
        self.assertEqual(200, login_response.status_code, u'删除供应商记录')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'删除供应商记录成功', str(gysid)),
                             u'删除供应商记录，返回结果有变化，需要确认，或修改单元测试')


    def query_wuzirecord_by_group(self, project_id, flag, timeline, record_date_id):
        """
        查询物资记录
        by:王健 at:2015-1-14
        添加记录日期id
        by:王健 at:2015-1-31
        :return:
        """
        login_response = self.client.post('/ns/%s/query_wuzirecord_by_group' % project_id,
                                          {'flag': flag, 'timeline': timeline, 'record_date_id': record_date_id})
        self.assertEqual(200, login_response.status_code, u'查询物资记录')
        if not timeline:
            l = WuZiRecord.objects.filter(project_id=project_id, record_date_id=record_date_id,
                                          file_group__flag=flag).order_by('-timeline')
        else:
            l = WuZiRecord.objects.filter(project_id=project_id, record_date_id=record_date_id, file_group__flag=flag,
                                          timeline__gt=int(timeline)).order_by('timeline')
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询物资记录，返回结果有变化，需要确认，或修改单元测试')

    def query_record_date_by_group(self, project_id, flag, timeline):
        """
        查询记录日期
        by:王健 at:2015-1-29
        :return:
        """
        login_response = self.client.post('/ns/%s/query_record_date_by_group' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询记录日期')
        if not timeline:
            l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag,
                                          timeline__gt=int(timeline)).order_by('timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询记录日期，返回结果有变化，需要确认，或修改单元测试')

    def query_record_date_by_group_old(self, project_id, flag, timeline):
        """
        查询记录日期旧数据
        by:王健 at:2015-1-29
        :return:
        """
        login_response = self.client.post('/ns/%s/query_record_date_by_group_old' % project_id,
                                          {'flag': flag, 'timeline': timeline})
        self.assertEqual(200, login_response.status_code, u'查询记录日期旧数据')
        if not timeline:
            l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
        else:
            l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag,
                                          timeline__lt=int(timeline)).order_by('-timeline')[:20]
        self.assertJSONEqual(login_response.content, getTestResult(True, None, MyEncoder.default(l)),
                             u'查询记录日期旧数据，返回结果有变化，需要确认，或修改单元测试')

    def get_project(self, project_id):
        """
        根据项目ID查询项目
        by:范俊伟 at:2015-01-22
        :param project_id:
        :return:
        """
        resonse = self.client.post('/ns/get_project', {"project_id": project_id})
        self.assertEqual(200, resonse.status_code, u'根据项目ID查询项目')
        list_all = []
        for i in Project.objects.all():
            list_all.append(i)
        try:
            project = Project.objects.get(id=project_id)
            test_getResult = getTestResult(True, None, MyEncoder.default(project))
        except Project.DoesNotExist:
            test_getResult = getTestResult(False, u'项目不存在')
        except ValueError:
            test_getResult = getTestResult(False, u'参数格式错误')
        self.assertJSONEqual(resonse.content, test_getResult,
                             u'根据项目ID查询项目，返回结果有变化，需要确认，或修改单元测试')

    def get_show_project(self):
        """
        获取示例项目信息
        by:王健 at:2015-03-25
        :return:
        """
        resonse = self.client.post('/ns/get_show_project', {})
        self.assertEqual(200, resonse.status_code, u'获取示例项目信息')
        try:
            project = Project.objects.get(id=settings.SHOW_PROJECT_ID)
            test_getResult = getTestResult(True, None, MyEncoder.default(project))
        except Project.DoesNotExist:
            test_getResult = getTestResult(False, u'项目不存在')
        except ValueError:
            test_getResult = getTestResult(False, u'参数格式错误')
        self.assertJSONEqual(resonse.content, test_getResult,
                             u'获取示例项目信息，返回结果有变化，需要确认，或修改单元测试')

    def leave_project(self, project_id, tel):
        """
        用户离开项目
        by:王健 at:2015-01-30
        :param project_id:
        :return:
        """
        resonse = self.client.post('/ns/%s/leave_project' % project_id, {"project_id": project_id})
        self.assertEqual(200, resonse.status_code, u'用户离开项目')
        person = Person.objects.get(user__tel=tel, project_id=project_id)
        self.assertEqual(False, person.is_active, u'用户离开项目失败')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'脱离项目成功', None),
                             u'用户离开项目，返回结果有变化，需要确认，或修改单元测试')

    def remove_person(self, project_id, user_id):
        """
        用户被移除项目
        by:王健 at:2015-01-30
        :param project_id:
        :return:
        """
        resonse = self.client.post('/ns/%s/remove_person' % project_id,
                                   {"project_id": project_id, "user_id": get_user_model().objects.get(tel=user_id).pk})
        self.assertEqual(200, resonse.status_code, u'用户被移除项目')
        person = Person.objects.get(user__tel=user_id, project_id=project_id)
        self.assertEqual(False, person.is_active, u'用户被移除项目失败')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'脱离项目成功', None),
                             u'用户被移除项目，返回结果有变化，需要确认，或修改单元测试')

    def guanzhu_project(self, project_id, user, do):
        """
        根据项目ID关注项目
        by:王健 at:2015-01-30
        元祖改为字符串
        by:王健 at:2015-1-31
        :param project_id:
        :return:
        """
        resonse = self.client.post('/ns/guanzhu_project', {"project_id": project_id, 'do': do})
        self.assertEqual(200, resonse.status_code, u'根据项目ID关注项目')
        project = Project.objects.get(pk=project_id)
        if do == 'join':
            msg = u'关注%s成功'
        else:
            msg = u'取消关注%s成功'
        self.assertJSONEqual(resonse.content, getTestResult(True, msg % project.name,
                                                            {'project': MyEncoder.default(project),
                                                             'guanzhuprojectlist': [p[0] for p in
                                                                                    user.guanzhu.values_list('id')]}),
                             u'根据项目ID关注项目，返回结果有变化，需要确认，或修改单元测试')

    def get_url_by_file(self, project_id, fileid):
        """
        获取文件下载url 测试
        by:尚宗凯 at:2015-3-4
        :return:
        """
        login_response = self.client.post('/nf/%s/get_url_by_file' % project_id, {'fileid': fileid})
        self.assertEqual(200, login_response.status_code, u'获取文件下载url 错误')
        fileobj = File.objects.get(pk=fileid)
        self.assertJSONEqual(login_response.content, getTestResult(True, u'',
                                                                   {'id': fileobj.id, 'geturl': fileobj.get_url(),
                                                                    'name': fileobj.name, 'filetype': fileobj.filetype,
                                                                    'size': fileobj.size}),
                             u'获取文件下载url，返回结果有变化，需要确认，或修改单元测试')

    def add_person_by_tel(self, project_id, telparm, group_id):
        """
        根据上传的手机号，加入项目
        by:王健 at:2015-01-25
        增加userlist 返回属性
        by:王健 at:2015-02-13
        根据新接口测试
        by:王健 at:2015-03-10
        修改加人的 逻辑
        by:王健 at:2015-03-15
        优化 加人的单元测试
        by:王健 at:2015-03-20
        :param project_id:
        :param tel:
        :return:
        """
        tels = telparm.split(',')
        addlist = []
        sendlist = []
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
                get_user_model().objects.get(tel=tel)
                addlist.append(tel)
                sendlist.append(tel)
            except get_user_model().DoesNotExist:
                error_tel.append(tel)
                # addlist.append(t)

        resonse = self.client.post('/ns/%s/add_person_by_tel' % project_id,
                                   {"tel": telparm, 'smsdebug': 'sf', 'group_id': group_id})
        self.assertEqual(200, resonse.status_code, u'根据上传的手机号，加入项目')

        self.assertJSONEqual(resonse.content,
                             getTestResult(True, u'操作成功', {'addlist': addlist, 'sendlist': sendlist, 'userlist': [],
                                                           'error_tel': error_tel}),
                             u'根据上传的手机号，加入项目，返回结果有变化，需要确认，或修改单元测试')

    def add_person_by_tel3(self, project_id, telparm, group_id):
        """
        手机号添加用户
        by:尚宗凯 at:2015-03-25
        """
        tels = telparm.split(',')
        addlist = []
        sendlist = []
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

                # try:
                # get_user_model().objects.get(tel=tel)
                # addlist.append(tel)
                #     sendlist.append(tel)
                # except get_user_model().DoesNotExist:
                #     error_tel.append(tel)
                #     # addlist.append(t)

        resonse = self.client.post('/ns/%s/add_person_by_tel' % project_id,
                                   {"tel": telparm, 'smsdebug': 'sf', 'group_id': group_id})
        self.assertEqual(200, resonse.status_code, u'根据上传的手机号，加入项目')
        self.assertJSONEqual(resonse.content,
                             getTestResult(True, u'操作成功', {'addlist': addlist, 'sendlist': sendlist, 'userlist': [],
                                                           'error_tel': error_tel}),
                             u'根据上传的手机号，加入项目，返回结果有变化，需要确认，或修改单元测试')

    def add_person_by_tel3_add(self, project_id):
        """
        手机号添加用户
        by:尚宗凯 at:2015-03-25
        """
        group = Group.objects.get(project_id=project_id, type="sys_xmjl")
        resonse = self.client.post('/ns/%s/add_person_by_tel' % project_id,
                                   {"tel": ','.join([str(11111111111), str(22222222222), str(33333333333)]),
                                    'smsdebug': 'sf', 'group_id': group.pk})
        self.assertEqual(200, resonse.status_code, u'根据上传的手机号，加入项目')
        login_user = self.login_user
        self.reg_user(11111111111, "8888")
        # self.login(11111111111, '123456')
        user = get_user_model().objects.get(tel=11111111111)
        # group.look_members.filter(id=user.pk).exists()
        self.assertEqual(True, group.look_members.filter(id=user.pk).exists(), u"手机号加人未进组")

        self.login(login_user.tel, '123456')


    def guest_app_url(self):
        """
        根据浏览器的系统，跳转不同的网址
        by:王健 at:2015-01-25
        统计模块 接口测试
        by:王健 at:2015-04-3
        :return:
        """

        resonse = self.client.post('/tj/guest_app_url', {})
        self.assertEqual(302, resonse.status_code, u'根据浏览器的系统，跳转不同的网址')

    def send_social_success(self):
        """
        获取分享成功的积分
        by:王健 at:2015-2-5
        :param project_id:
        :return:
        """
        resonse = self.client.post('/ns/send_social_success', {})
        self.assertEqual(200, resonse.status_code, u'获取分享成功的积分')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'', None),
                             u'获取分享成功的积分，返回结果有变化，需要确认，或修改单元测试')


    def query_my_jifen(self, uid):
        """
        获取我的积分值
        by:王健 at:2015-2-6
        :return:
        """
        resonse = self.client.post('/ns/query_my_jifen', {})
        self.assertEqual(200, resonse.status_code, u'获取我的积分值')
        request = TestRequest(uid)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'', query_fen_by_uid(request)),
                             u'获取我的积分值，返回结果有变化，需要确认，或修改单元测试')

    def ding_filerecord_by_id(self, project_id, id):
        """
        顶一条记录
        by:王健 at:2015-2-25
        赞一条记录
        by:王健 at:2015-05-28
        :return:
        """
        filerecord0 = FileRecord.objects.get(pk=id)
        resonse = self.client.post('/ns/%s/ding_filerecord_by_id' % project_id, {'id': id, 'flag': filerecord0.file_group.flag})
        self.assertEqual(200, resonse.status_code, u'顶一条记录')
        result = has_replay_zan(project_id, filerecord0.file_group.flag, id, self.login_user.pk)
        tmp_data = json.loads(resonse.content)
        self.assertJSONEqual(resonse.content,
                             getTestResult(True, u'成功对 %s 点了个赞。' % filerecord0.title, result[0]),
                             u'顶一条记录，返回结果有变化，需要确认，或修改单元测试')

    def delete_ding_filerecord_by_id(self, project_id, id):
        """
        删除赞
        by:王健 at:2015-05-28
        :return:
        """
        filerecord0 = FileRecord.objects.get(pk=id)
        resonse = self.client.post('/ns/%s/delete_ding_filerecord_by_id' % project_id, {'id': id, 'flag': filerecord0.file_group.flag})
        self.assertEqual(200, resonse.status_code, u'顶一条记录')
        result = has_replay_zan(project_id, filerecord0.file_group.flag, id, self.login_user.pk)
        self.assertJSONEqual(resonse.content,
                             getTestResult(True, u'成功 %s 取消了赞。' % filerecord0.title, result),
                             u'顶一条记录，返回结果有变化，需要确认，或修改单元测试')

    def replay_filerecord_by_id(self, project_id, id, content, to_user):
        """
        评论一条记录
        by:王健 at:2015-2-25
        增加to_user
        by:尚宗凯 at：2015-04-30
        发出评论
        by:王健 at:2015-05-28
        :return:
        """
        filerecord0 = FileRecord.objects.get(pk=id)
        resonse = self.client.post('/ns/%s/replay_filerecord_by_id' % project_id, {'id': id, 'flag': filerecord0.file_group.flag, 'content': content,'to_user':to_user})
        self.assertEqual(200, resonse.status_code, u'评论一条记录')
        result = has_replay(project_id, filerecord0.file_group.flag, id, self.login_user.pk)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'发布评论成功。', result[-1]),
                             u'评论一条记录，返回结果有变化，需要确认，或修改单元测试')

    def query_replay_filerecord_by_id(self, project_id, id):
        """
        查询一条记录的评论
        by:王健 at:2015-2-25
        屏蔽mongodb
        by:王健 at:2015-3-8
        查询所有的评论
        by:王健 at:2015-05-28
        :return:
        """
        resonse = self.client.post('/ns/%s/query_replay_filerecord_by_id' % project_id, {'id': id, 'flag': FileRecord.objects.get(pk=id).file_group.flag})
        self.assertEqual(200, resonse.status_code, u'查询一条记录的评论')
        # from mango import database as db

        # l = db.filereplay.find({'f_id': int(id)})
        resultlist = has_replay_or_zan(project_id, FileRecord.objects.get(pk=id).file_group.flag, id)
        # for r in l:
        # resultlist.append(r)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取评论成功。', {'pinglun': resultlist, 'filerecord': FileRecord.objects.get(pk=id).toJSON()}),
                             u'查询一条记录的评论，返回结果有变化，需要确认，或修改单元测试')

    def query_replay_filerecord_by_timeline(self, project_id):
        """
        查询一条记录的评论
        by:王健 at:2015-2-25
        屏蔽mongodb
        by:王健 at:2015-3-8
        根据时间轴查询所有的评论
        by:王健 at:2015-05-28
        优化评论时间戳设计
        by:王健 at:2015-06-02
        修改结果，数据
        by:王健 at:2015-06-02
        :return:
        """
        person = self.login_user.person_set.filter(project_id=project_id)[0]
        all_flag = query_project_filegroup_data_(project_id)
        all_have_power_flag = all_flag_user_have_power_by_flag(self.login_user.pk, project_id, None)
        result = test_query_replay_by_timeline(person.replay_timeline, self.login_user.pk, project_id, all_have_power_flag)
        resonse = self.client.post('/ns/%s/query_replay_filerecord_by_timeline' % project_id, {})
        self.assertEqual(200, resonse.status_code, u'查询一条记录的评论')
        if isinstance(result, list):
            l = {'images': [], 'jc': [], 'files': [], 'bgimages': []}
            dl = {'images': [], 'jc': [], 'files': [], 'bgimages': []}
            for p in result:
                if p['flag'] in FILE_GROUP_FLAGS_FILES:
                    l['files'].append(p['filerecord'])
                elif p['flag'] in FILE_GROUP_FLAGS_BGIMAGES:
                    l['bgimages'].append(p['filerecord'])
                elif p['flag'] in FILE_GROUP_FLAGS_IMAGES:
                    l['images'].append(p['filerecord'])
                elif p['flag'] in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
                    l['jc'].append(p['filerecord'])
                else:
                    pass
            if l['images']:
                dl['images'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['images'], project_id=project_id)])
            if l['bgimages']:
                dl['bgimages'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['bgimages'], project_id=project_id)])
            if l['files']:
                dl['files'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['files'], project_id=project_id)])
            if l['jc']:
                dl['jc'].extend([f.toJSON() for f in EngineCheck.objects.filter(pk__in=l['jc'], project_id=project_id)])
            for r in dl.values():
                for f in r:
                    f['flag'] = all_flag['flags'][f['file_group']]
            dl['pinglun'] = result

        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取评论成功。', dl),
                             u'查询一条记录的评论，返回结果有变化，需要确认，或修改单元测试')

    def count_replay_filerecord_by_timeline(self, project_id):
        """
        查询一条记录的评论
        by:王健 at:2015-2-25
        屏蔽mongodb
        by:王健 at:2015-3-8
        根据时间轴查询评论数量
        by:王健 at:2015-05-28
        优化评论数据
        by:王健 at:2015-05-28
        优化评论时间戳设计
        by:王健 at:2015-06-02
        修改返回数据
        by:王健 at:2015-06-02
        调整单元测试的变量bug
        by:王健 at:2015-06-27
        :return:
        """
        resonse = self.client.post('/ns/%s/count_replay_filerecord_by_timeline' % project_id, {})
        self.assertEqual(200, resonse.status_code, u'查询一条记录的评论')
        person = self.login_user.person_set.filter(project_id=project_id)[0]
        all_flag = query_project_filegroup_data_(project_id)
        all_have_power_flag = all_flag_user_have_power_by_flag(self.login_user.pk, project_id, None, all_flag)
        result = query_replay_num_by_timeline(person.replay_timeline, self.login_user.pk, project_id, all_have_power_flag)
        p = get_last_replay_by_timeline(self.login_user.pk, project_id, all_have_power_flag)
        result['pinglun'] = p
        if p:
            if result['pinglun']['flag'] in FILE_GROUP_FLAGS:
                result['filerecord'] = FileRecord.objects.get(pk=result['pinglun']['filerecord']).toJSON()
            elif result['pinglun']['flag'] in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
                result['filerecord'] = EngineCheck.objects.get(pk=result['pinglun']['filerecord']).toJSON()
            result['filerecord']['flag'] = all_flag['flags'][result['filerecord']['file_group']]
            if result['pinglun']['flag'] in FILE_GROUP_FLAGS_BGIMAGES:
                result['filerecord']['typeflag'] = 'bgimages'
            elif result['pinglun']['flag'] in FILE_GROUP_FLAGS_FILES:
                result['filerecord']['typeflag'] = 'files'
            elif result['pinglun']['flag'] in FILE_GROUP_FLAGS_IMAGES:
                result['filerecord']['typeflag'] = 'images'
            else:
                result['filerecord']['typeflag'] = 'jc'
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取评论数量成功。', result),
                             u'查询一条记录的评论，返回结果有变化，需要确认，或修改单元测试')

    def create_sysmessage(self, project_id, group_id, user_id, title, text):
        """
        创建一条系统消息
        by:王健 at:2015-2-26
        系统消息 校验修改
        by:王健 at:2015-3-17
        :return:
        """
        resonse = self.client.post('/ns/create_sysmessage',
                                   dict(project_id=project_id, group_id=group_id, user_id=user_id, title=title,
                                        text=text))
        self.assertEqual(200, resonse.status_code, u'创建一条系统消息')
        msg = SysMessage.objects.filter(project_id=project_id).order_by('-id')[0]
        self.assertJSONEqual(resonse.content, getTestResult(True, u'创建系统消息成功', MyEncoder.default(msg)),
                             u'创建一条系统消息，返回结果有变化，需要确认，或修改单元测试')

    def query_sysmessage(self, project_id, group_id, user_id, timeline):
        """
        查询系统消息
        by:王健 at:2015-2-26
        group 改为 to_group
        by:王健 at:2015-2-27
        :return:
        """
        resonse = self.client.post('/ns/%s/query_sysmessage' % project_id, {'group_id': group_id, 'timeline': timeline})
        self.assertEqual(200, resonse.status_code, u'查询系统消息')
        if user_id:
            l = SysMessage.objects.filter(project_id=project_id).filter(Q(user_id=user_id) | Q(user=None))
        else:
            l = SysMessage.objects.filter(project_id=project_id)
        if timeline:
            l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
        else:
            l = l.order_by('-timeline')

        if group_id:
            l = l.filter(to_group_id=group_id)
        else:
            l = l.filter(to_group_id=None)

        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取系统消息', MyEncoder.default(l[:20])),
                             u'查询系统消息，返回结果有变化，需要确认，或修改单元测试')

    def create_needmessage(self, title='', text='', create_user_id='',to_user_id='', status='', type=''):
        """
        测试创建用户消息
        by:尚宗凯 at:2015-3-31
        修改创建消息
        by:尚宗凯 at:2015-4-1
        """
        resonse = self.client.post('/ns/create_needmessage',{"title":title, "text":text, "create_user_id":create_user_id, "to_user_id":to_user_id, "status":status, "type":type})
        self.assertEqual(200, resonse.status_code, u'创建一条NEED消息')
        msg = NeedMessage.objects.filter(title=title).order_by('-timeline')[0]
        self.assertJSONEqual(resonse.content, getTestResult(True, u'创建NEED消息成功', MyEncoder.default(msg)),
                             u'创建一条用户消息，返回结果有变化，需要确认，或修改单元测试')

    def query_need_message(self, title='', create_user_id='', to_user_id='', timeline='', status='', type=''):
        """
        测试查询用户消息
        by:尚宗凯 at:2015-3-31
        修改查询消息
        by:尚宗凯 at:2015-4-1
        优化Need消息 单元测试
        by:王健 at:2015-4-3
        """
        resonse = self.client.post('/ns/query_need_message',{"title":title, "timeline":timeline, "create_user_id":create_user_id, "to_user_id":to_user_id,"status":status, "type":type})
        self.assertEqual(200, resonse.status_code, u'查询NEED消息')
        l = NeedMessage.objects.all()
#        if not create_user_id:
#            create_user_id = request.user
#        if not to_user_id:
#            to_user_id = request.user
#        if status != '':
#            status = int(status)
#        type = request.REQUEST.get('type','')
#        if type != '':
#            type = int(type)
#        l = NeedMessage.objects.all()
        if status:
            l = l.filter(status=int(status))
        if type:
            l = l.filter(type=int(type))
        if title:
            l = l.filter(title=title)
        if create_user_id and to_user_id:
            l = l.filter(Q(create_user=create_user_id)|Q(to_user=to_user_id))
        elif create_user_id:
            l = l.filter(create_user=create_user_id)
        elif to_user_id:
            l = l.filter(to_user=to_user_id)
        if timeline:
            l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
        else:
            l = l.order_by('-timeline')
        res = []
        if l:
            for i in l[:20]:
                tmp = i.toJSON()
                if i.create_user and i.create_user.icon_url:
                    tmp['create_user_icon_url'] = i.create_user.icon_url.get_url()
                    tmp['create_user_name'] = i.create_user.name
                else:
                    tmp['create_user_icon_url'] = ""

                if i.to_user and i.to_user.icon_url:
                    tmp['to_user_icon_url'] = i.to_user.icon_url.get_url()
                    tmp['to_user_name'] = i.to_user.name
                else:
                    tmp['to_user_icon_url'] = ""
                res.append(tmp)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取NEED消息', res),
                             u'查询用户消息，返回结果有变化，需要确认，或修改单元测试')

    def query_sysmessage_old(self, project_id, group_id, user_id, timeline):
        """
        查询系统消息旧数据
        by:王健 at:2015-2-26
        group 改为 to_group
        by:王健 at:2015-2-27
        :return:
        """
        resonse = self.client.post('/ns/%s/query_sysmessage_old' % project_id,
                                   {'group_id': group_id, 'timeline': timeline})
        self.assertEqual(200, resonse.status_code, u'查询系统消息旧数据')
        if user_id:
            l = SysMessage.objects.filter(project_id=project_id).filter(Q(user_id=user_id) | Q(user=None))
        else:
            l = SysMessage.objects.filter(project_id=project_id)
        if timeline:
            l = l.filter(timeline__lt=int(timeline)).order_by('-timeline')
        else:
            l = l.order_by('-timeline')

        if group_id:
            l = l.filter(to_group_id=group_id)
        else:
            l = l.filter(to_group_id=None)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取系统消息', MyEncoder.default(l[:20])),
                             u'查询系统消息旧数据，返回结果有变化，需要确认，或修改单元测试')

    def create_project_message(self, project_id, group_id, title, text):
        """
        创建分组公告
        by:王健 at:2015-2-26
        :return:
        """
        resonse = self.client.post('/ns/%s/create_project_message' % project_id,
                                   {'group_id': group_id, 'title': title, 'text': text})
        self.assertEqual(200, resonse.status_code, u'创建分组公告')
        msg = ProjectMessage.objects.filter(project_id=project_id).order_by('-timeline')[0]

        self.assertJSONEqual(resonse.content, getTestResult(True, u'发布公告成功', MyEncoder.default(msg)),
                             u'创建分组公告，返回结果有变化，需要确认，或修改单元测试')

    def query_project_message(self, project_id, group_id, timeline):
        """
        查询公告消息
        by:王健 at:2015-2-26
        group 改为 to_group
        by:王健 at:2015-2-27
        :return:
        """
        resonse = self.client.post('/ns/%s/query_project_message' % project_id,
                                   {'group_id': group_id, 'timeline': timeline})
        self.assertEqual(200, resonse.status_code, u'查询公告消息')
        l = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id)
        if timeline:
            l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
        else:
            l = l.order_by('-timeline')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公告', MyEncoder.default(l[:20])),
                             u'查询公告消息，返回结果有变化，需要确认，或修改单元测试')

    def query_project_message_old(self, project_id, group_id, timeline):
        """
        查询公告消息旧数据
        by:王健 at:2015-2-26
        group 改为 to_group
        by:王健 at:2015-2-27
        :return:
        """
        resonse = self.client.post('/ns/%s/query_project_message_old' % project_id,
                                   {'group_id': group_id, 'timeline': timeline})
        self.assertEqual(200, resonse.status_code, u'查询公告消息旧数据')
        l = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id)
        if timeline:
            l = l.filter(timeline__lt=int(timeline)).order_by('-timeline')
        else:
            l = l.order_by('-timeline')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公告', MyEncoder.default(l[:20])),
                             u'查询公告消息旧数据，返回结果有变化，需要确认，或修改单元测试')

    def get_project_balance(self, project_id):
        """
        获取项目的余额信息
        by:王健 at:2015-3-2
        查询剩余额度的算法优化
        by:王健 at:2015-3-15
        修改余额计算方式
        by:王健 at:2015-3-16
        增加新的字段
        by：尚宗凯 at：2015-06-19
        :return:
        """
        resonse = self.client.post('/ns/%s/get_project_balance' % project_id)
        self.assertEqual(200, resonse.status_code, u'获取项目的余额信息')
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
        result['used_days'] = 25
        result['project_company'] = u'项目所属'
        result['status'] = 1
        result['yw_tel'] = '23423423423'
        result['kf_tel'] = '23423423423'
        result['project_id'] = project_id
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取项目余额信息', result),
                             u'获取项目的余额信息，返回结果有变化，需要确认，或修改单元测试')
        return result

    def set_project_baoting(self, project_id, days=20):
        """
        设置项目报停
        by:王健 at:2015-3-15
        :return:
        """
        ppcr0 = ProjectPersonChangeRecord.objects.filter(project_id=project_id).order_by('-create_date')[:1]
        if len(ppcr0) == 1:
            ppcr0 = ppcr0[0]
        resonse = self.client.post('/ns/%s/set_project_baoting' % project_id, {'days': days})
        self.assertEqual(200, resonse.status_code, u'设置项目报停')

        ppcr = ProjectPersonChangeRecord.objects.filter(project_id=project_id).order_by('-create_date')[:1]
        if len(ppcr) == 1:
            ppcr = ppcr[0]
        self.assertNotEqual(ppcr0.end_date, ppcr.end_date)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'处理报停成功', ppcr.end_date.strftime('%Y-%m-%d')),
                             u'处理报停，返回结果有变化，需要确认，或修改单元测试')

    def query_project_name(self, key):
        """
        查询相似项目名称
        by:王健 at:2015-3-4
        :return:
        """
        resonse = self.client.post('/ns/query_project_name', {'key': key})
        self.assertEqual(200, resonse.status_code, u'查询相似项目名称')
        l = [x[0] for x in
             Project.objects.filter(total_name__icontains=key).order_by('-create_time').values_list('total_name')[:20]]
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取相似项目名', l),
                             u'查询相似项目名称，返回结果有变化，需要确认，或修改单元测试')

    def change_power_by_group(self, project_id, group_id, powers):
        """
        修改分组权限
        by:王健 at:2015-3-27
        修改分组权限 新逻辑
        by:王健 at:2015-05-07
        :param project_id:
        :param group_id:
        :param powers:
        :return:
        """
        # group = Group.objects.get(pk=group_id)

        resonse = self.client.post('/ns/%s/change_power_by_group' % project_id,
                                   {'group_id': group_id, 'powers': ','.join([str(p) for p in powers])})
        self.assertEqual(200, resonse.status_code, u'修改分组权限')
        group = Group.objects.get(pk=group_id)
        group.init_powers()
        r = False
        if len(powers) == len(group.powers) and len(set(powers) - set(group.powers)) == 0:
            r = True
        self.assertEqual(True, r, u'分组权限修改的不正确')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'修改权限成功'),
                                 u'删除权限，返回结果有变化，需要确认，或修改单元测试')

    def change_power_by_person(self, project_id, user_id, powers):
        """
        修改个人权限
        by:王健 at:2015-3-27
        修改个人权限，新逻辑
        by:王健 at:2015-05-07
        个人权限修改校验
        by:王健 at:2015-05-12
        :param project_id:
        :param user_id:
        :param powers:
        :return:
        """
        # group = Person.objects.get(user_id=user_id, project_id=project_id)

        resonse = self.client.post('/ns/%s/change_power_by_person' % project_id,
                                   {'user_id': user_id, 'powers': ','.join([str(p) for p in powers])})
        self.assertEqual(200, resonse.status_code, u'修改个人权限')
        person = Person.objects.get(user_id=user_id, project_id=project_id)
        powers_set0 = person.real_powers()
        powers_set = set()
        for p in powers_set0:
            if p % 100 == 0:
                powers_set.add(p)
        r = False
        if len(powers) == len(powers_set) and len(set(powers) - set(powers_set)) == 0:
            r = True
        self.assertEqual(True, r, u'个人权限修改的不正确')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'修改权限成功'),
                                 u'修改权限，返回结果有变化，需要确认，或修改单元测试')

    def test_join_org(self):
        """
        按照登录、获取用户信息、登出的顺序测试
        by:王健 at:2015-1-5
        增加 日志查询、创建的测试
        增加 项目申请的测试，获取所有未处理申请的测试
        以管理员的身份处理 项目申请
        by:王健 at:2015-1-7
        添加项目列表项接口（创建、查询）测试
        by:王健 at:2015-1-12
        修改Model名字，去除下划线, 工程检查接口 测试
        by:王健 at:2015-1-13
        供应商接口、物资管理接口
        by:王健 at:2015-1-14
        更新个人信息的接口、获取项目内用户的个人信息
        by:王健 at:2015-1-18
        update_userinfo 接口增加一个 数字类型的校验
        by:王健 at:2015-1-19
        增加项目id条件
        by:王健 at:2015-1-21
        增加根据项目ID查询项目
        by:范俊伟 at:2015-01-22
        增加根据tel添加项目成员的接口测试，根据手机端操作系统，跳转界面的接口测试
        by:范俊伟 at:2015-01-25
        增加根据id 关注、取消关注项目的接口
        by:范俊伟 at:2015-01-30
        元祖改为字符串, 物资查询添加记录日期id
        by:王健 at:2015-1-31
        分享获取积分接口测试
        by:王健 at:2015-2-5
        查询我的积分
        by:王健 at:2015-2-6
        增加日志删除、物资删除接口测试，加入人增加gorup_id
        by:王健 at:2015-2-10
        顶、评论的接口测试
        by:王健 at:2015-2-25
        优化URL参数 timeline 0 和空 一致
        by:王健 at:2015-2-26
        增加了新的个人信息测试，相似项目名接口测试
        by:王健 at:2015-3-4
        修改工程检查 参数
        by:王健 at:2015-3-5
        屏蔽mongodb
        by:王健 at:2015-3-8
        添加获取示例项目的接口测试，测试示例项目的 查询功能
        by:王健 at:2015-3-25
        修改query_log_list_by_date_2，query_log_list_by_date测试
        by:尚宗凯 at:2015-3-25
        添加人后，tel注册，自动进入项目和分组
        by:王健 at:2015-3-25
        增加删除工程检查测试
        by:尚宗凯 at:2015-3-30
        添加评论单元测试
        by:王健 at:2015-05-28
        去除无需单元测试的接口
        by:王健 at:2015-05-29
        优化评论时间戳设计
        by:王健 at:2015-06-02
        :return:
        """
        # 加入组织

        self.login(username, '123456')
        self.current_user()

        self.query_project_name(key=u'天津')
        self.query_project_name(key=u'依子轩')
        self.update_userinfo(username, name=u'周杰伦')
        self.update_userinfo(username, nickname=u'双节棍')
        self.update_userinfo(username, sex=u'false')
        self.update_userinfo(username, address=u'1')
        self.update_userinfo(username)
        self.update_userinfo(username, zhiyezigezheng=u'41272819870313083X')
        self.update_userinfo(username, zhicheng=u'造价师')
        self.update_userinfo(username, qq=u'534199530')
        self.update_userinfo(username, department=u'土木')
        self.update_userinfo(username, title=u'大工')
        self.submit_user_tel(username, '23423')
        self.my_project()



        self.query_project(0, '0')
        self.query_project(20, '0')
        self.query_project(40, '0')
        self.query_project_by_key(0, '0', u'测试')
        self.query_project_by_key(20, '0', u'测试')
        self.query_project_by_key(40, '0', u'23')
        self.get_project(1)
        self.get_project(2)
        self.get_project('xxx')
        self.update_log_by_date(self.project.pk, u'今天干了好多的工作，浇筑了一个大楼', '', u'天气晴朗', u'威风', u'很热')
        self.update_log_by_date(self.project.pk, u'sdf今天干了好多的工作，浇筑了一个大楼', '', u'天气晴朗', u'威风', u'很热')
        self.update_log_by_date(self.project.pk, u'sdf今天干了好多的工作，浇筑了一个大楼', '', u'天气晴朗', u'威风', u'很热')
        sglog = SGlog.objects.all().order_by('-create_time')[0]
        self.del_log_by_id(self.project.pk, sglog.pk)
        self.query_log_date_list(self.project.pk, 0)
        self.query_log_list_by_date(self.project.pk, sglog.sg_tq_log_id)
        self.query_log_list_by_date_2(self.project.pk, sglog.sg_tq_log_id, 1)

        self.update_project(self.project.pk, name=u'说说', total_name=u'存储')

        # 测试 充值
        # by:王健 at:2015-3-15
        #修改充值 构造
        #by:王健 at:2015-3-17
        # self.get_project_balance(self.project.pk)
        p = ProjectRechargeRecord()
        p.project = self.project
        p.price0 = 6000
        p.save(user_id=self.project.manager_id)
        # self.get_project_balance(self.project.pk)
        p = ProjectRechargeRecord()
        p.project = self.project
        p.price0 = 6000
        p.save(user_id=self.project.manager_id)
        # project_blance = self.get_project_balance(self.project.pk)

        # self.assertEqual((project_blance['total'] - project_blance['price']), 12599, u'计算余额不对')

        #测试手机号添加用户后注册
        #by:尚宗凯 at:2015-3-15

        self.add_person_by_tel3_add(self.project.pk)


        #创建系统消息
        #增加user_id参数
        #by：尚宗凯 at：2015-05-12
        test_user = self.login_user
        user_id = test_user.pk
        self.create_sysmessage(self.project.pk, group_id='', user_id=user_id, title=u'测试系统消息', text=u'测试消息测试消息')
        self.query_sysmessage(self.project.pk, '', user_id, 0)
        self.query_sysmessage_old(self.project.pk, '', user_id, 1)
        project_message_group = Group.objects.get(project_id=self.project.pk, type="sys_xmjl")
        project_message_group.say_members.add(get_user_model().objects.get(tel=username))
        self.create_project_message(self.project.pk, group_id=project_message_group.pk, title=u'测试标题', text=u'测试公告公告')
        self.query_project_message(self.project.pk, group_id=project_message_group.pk, timeline=0)
        self.query_project_message_old(self.project.pk, group_id=project_message_group.pk, timeline=1)
        
        #用户消息测试
        #by:尚宗凯 at:2015-3-31
        #修改函数名和参数
        #by:尚宗凯 at:2015-4-1
        # test_user = get_user_model().objects.all().order_by("-create_time")[0]
        test_user = self.login_user
        # self.login(test_user.tel, '123456')
        # self.create_needmessage(title=u"测试用户消息title", text=u"测试用户消息text", create_user_id=test_user.pk, to_user_id=test_user.pk, type=1)
        # self.query_need_message()
        # self.query_need_message(title=u"测试用户消息title", timeline=0, create_user_id=test_user.pk, to_user_id=test_user.pk, type=1)
        # self.create_needmessage(title=u"测试NEED消息title2", text=u"测试用户消息text", to_user_id=test_user.pk, type=2)
        # self.create_needmessage(title=u"title3",create_user_id="")
        # self.logout()

        self.query_app_list(self.project.pk)
        self.query_app_list3(self.project.pk)

        self.query_app_list2(self.project.pk, FileGroupJSON.objects.get(project_id=self.project.pk).timeline)
        fileobj = File()
        fileobj.name = 'ss'
        fileobj.fileurl = '/2/948cd68e-3e40-4665-8440-7f51a1cf39af.PNG'
        fileobj.filetype = 'PNG'
        fileobj.size = '22222'
        fileobj.user = get_user_model().objects.get(tel=username)
        fileobj.project_id = self.project.pk
        fileobj.save()
        url = fileobj.get_url()
        # 追加文件
        # by:王健 at:2015-1-31
        filerecord = self.create_file_by_group(self.project.pk, fileobj.id, u'公共进度1', u'看一看公共的进度')
        filerecord = self.append_file_by_group(self.project.pk, fileobj.id, filerecord.pk)
        self.query_file_by_group_1(self.project.pk)
        self.query_file_by_group_2(self.project.pk)

        #测试删除上传的文件信息
        fileobj1 = File()
        fileobj1.name = '11'
        fileobj1.fileurl = '11.PNG'
        fileobj1.filetype = 'PNG'
        fileobj1.size = '1111'
        fileobj1.user = get_user_model().objects.get(tel=username)
        fileobj1.project_id = self.project.pk
        fileobj1.save()

        fileobj2 = File()
        fileobj2.name = '22'
        fileobj2.fileurl = '22.PNG'
        fileobj2.filetype = 'PNG'
        fileobj2.size = '2222'
        fileobj2.user = get_user_model().objects.get(tel=username)
        fileobj2.project_id = self.project.pk
        fileobj2.save()

        filerecord_for_delete = self.create_file_by_group(self.project.pk, ",".join([str(fileobj1.id),str(fileobj2.id)]), u'待删记录', u'待删记录')
        self.delete_file_by_filerecord_id(self.project.pk, filerecord_for_delete.pk, filerecord_for_delete.file_group.flag)

        # self.ding_filerecord_by_id(self.project.pk, filerecord.id)
        self.delete_ding_filerecord_by_id(self.project.pk, filerecord.id)
        # self.replay_filerecord_by_id(self.project.pk, filerecord.id, u'这是测试评论',get_user_model().objects.get(tel=username))
        # self.count_replay_filerecord_by_timeline(self.project.pk)
        # self.replay_filerecord_by_id(self.project.pk, filerecord.id, u'这是测试评论',get_user_model().objects.get(tel=username))
        # self.replay_filerecord_by_id(self.project.pk, filerecord.id, u'这是测试评论',get_user_model().objects.get(tel=username))
        # self.replay_filerecord_by_id(self.project.pk, filerecord.id, u'这是测试评论',get_user_model().objects.get(tel=username))
        # self.query_replay_filerecord_by_id(self.project.pk, filerecord.id)
        # self.count_replay_filerecord_by_timeline(self.project.pk)
        # self.query_replay_filerecord_by_timeline(self.project.pk)


        engine = self.create_enginecheck_by_group(self.project.pk, fileobj.id, 'bao_guang_jing_gao', u'快速修复')
        self.update_enginecheck_by_group(self.project.pk, engine.id, fileobj.id, u'XX出了问题', u'快速修复', 'Y',
                                         'bao_guang_jing_gao')

        self.query_enginecheck_by_group(self.project.pk, 'bao_guang_jing_gao', 0)
        self.query_enginecheck_by_group(self.project.pk, 'bao_guang_jing_gao', 1)
        self.query_enginecheck_by_group_old(self.project.pk, 'bao_guang_jing_gao', 0)
        self.query_enginecheck_by_group_old(self.project.pk, 'bao_guang_jing_gao', 1)

        engine_for_delete = self.create_enginecheck_by_group(self.project.pk, fileobj.id, 'bao_guang_jing_gao', u'修复')
        self.delete_enginecheck_by_enginecheck_id(self.project.pk, engine_for_delete.pk, 'bao_guang_jing_gao')

        # 供应商名录
        # 修改参数，传递一个false 型
        # by:王健 at:2015-1-22
        # 添加del_gysaddress_by_id单元测试
        # by:尚宗凯 at:2015-3-26
        gys = self.create_gysaddress_by_group(self.project.pk, '', 'gong_ying_shang_ming_lu', u'铸铁', u'xxxx材料公司', u'张三',
                                              u'18622231518', 'false', u'协议支付', u'李四', u'18622231517', u'')
        self.create_gysaddress_by_group(self.project.pk, gys.pk, 'gong_ying_shang_ming_lu', u'铸铁1', u'xxxx材料公司', u'张三',
                                        u'18624231518', True, u'协议支付', u'李四2', u'18622231517', u'')
        gys_del = self.create_gysaddress_by_group(self.project.pk, gys.pk, 'gong_ying_shang_ming_lu', u'铀矿', u'铀矿公司',
                                                  u'张铀',
                                                  u'18624231518', True, u'协议支付', u'李铀', u'18622231517', u'')
        self.del_gysaddress_by_id(self.project.pk, gys_del.pk)
        self.query_gysaddress_by_group(self.project.pk, 'gong_ying_shang_ming_lu', 0)
        self.query_gysaddress_by_group(self.project.pk, 'gong_ying_shang_ming_lu', 1)
        self.query_gysaddress_by_group_old(self.project.pk, 'gong_ying_shang_ming_lu', 0)
        self.query_gysaddress_by_group_old(self.project.pk, 'gong_ying_shang_ming_lu', 1)

        # 物资购买记录
        gys = self.create_wuzirecord_by_group(self.project.pk, '', 'wu_zi_cai_gou_ji_lu', u'铸铁', u'30*30', 21,
                                              u'甲乙丙丁公司', u'王春贵', 45,
                                              u'buy')
        wzrecord = self.create_wuzirecord_by_group(self.project.pk, gys.pk, 'wu_zi_cai_gou_ji_lu', u'铸铁', u'30*30', 32,
                                                   u'甲乙丙丁公司', u'王春贵', 56,
                                                   u'buy')

        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_cai_gou_ji_lu', 0, wzrecord.record_date_id)
        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_cai_gou_ji_lu', 1, wzrecord.record_date_id)
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_cai_gou_ji_lu', '')
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_cai_gou_ji_lu', 1)

        # 物资入库记录
        gys = self.create_wuzirecord_by_group(self.project.pk, '', 'wu_zi_ru_ku_ji_lu', u'铸铁', u'30*30', 21, u'甲乙丙丁公司',
                                              u'王春贵', 45,
                                              u'come')
        wzrecord = self.create_wuzirecord_by_group(self.project.pk, gys.pk, 'wu_zi_ru_ku_ji_lu', u'铸铁', u'30*30', 32,
                                                   u'甲乙丙丁公司', u'王春贵', 56,
                                                   u'come')

        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_ru_ku_ji_lu', 0, wzrecord.record_date_id)
        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_ru_ku_ji_lu', 1, wzrecord.record_date_id)
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_ru_ku_ji_lu', '')
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_ru_ku_ji_lu', 1)

        # 物资出库记录
        gys = self.create_wuzirecord_by_group(self.project.pk, '', 'wu_zi_chu_ku_ji_lu', u'铸铁', u'30*30', 21, u'甲乙丙丁公司',
                                              u'王春贵', 45,
                                              u'out')
        wzrecord = self.create_wuzirecord_by_group(self.project.pk, gys.pk, 'wu_zi_chu_ku_ji_lu', u'铸铁', u'30*30', 32,
                                                   u'甲乙丙丁公司', u'王春贵', 56,
                                                   u'out')
        wzrecord2 = self.create_wuzirecord_by_group(self.project.pk, gys.pk, 'wu_zi_chu_ku_ji_lu', u'铸铁', u'30*30', 32,
                                                    u'甲乙丙丁公司', u'王春贵', 56,
                                                    u'out')
        self.del_wuzirecord_by_id(self.project.pk, wzrecord2.pk)

        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_chu_ku_ji_lu', 0, wzrecord.record_date_id)
        self.query_wuzirecord_by_group(self.project.pk, 'wu_zi_chu_ku_ji_lu', 1, wzrecord.record_date_id)
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_chu_ku_ji_lu', '')
        # self.query_wuzirecord_by_group_old(self.project.pk,  'wu_zi_chu_ku_ji_lu', 1)

        self.query_record_date_by_group(self.project.pk, 'wu_zi_chu_ku_ji_lu', 0)
        self.query_record_date_by_group(self.project.pk, 'wu_zi_chu_ku_ji_lu', 1)
        self.query_record_date_by_group_old(self.project.pk, 'wu_zi_chu_ku_ji_lu', 0)
        self.query_record_date_by_group_old(self.project.pk, 'wu_zi_chu_ku_ji_lu', 1)

        self.logout()

        new_username = 123456789011
        new_name = u'王大大'
        self.reg_user(new_username, new_name)
        self.login(new_username, '123456')
        # self.my_project2()
        self.apply_project(self.project.pk, u'让我加入吧 我是热心市民', new_username)
        # 根据id取消关注和关注项目
        # by:王健 at:2015-1-30
        self.guanzhu_project(self.project.pk, get_user_model().objects.get(tel=new_username), do='join')
        self.logout()
        self.login(new_username, '123456')
        self.guanzhu_project(self.project.pk, get_user_model().objects.get(tel=new_username), do='out')
        self.logout()
        self.assertEqual(1, ProjectApply.objects.filter(project_id=self.project.pk, status=None).count(), u'项目申请数量不对')

        new_username2 = 18622231514
        new_name2 = u'王大大2'
        self.reg_user(new_username2, new_name2)
        self.login(new_username2, '123456')
        # self.my_project2()
        self.apply_project(self.project.pk, u'让我加入吧 我是热心市民', new_username2)
        #测试我的项目
        #by:王健 at:2015-4-3
        self.my_project()
        self.logout()
        self.assertEqual(2, ProjectApply.objects.filter(project_id=self.project.pk, status=None).count(), u'项目申请数量不对')

        new_username3 = 18622231511
        new_name3 = u'王大大3'
        self.reg_user(new_username3, new_name3)
        self.logout()

        new_username4 = 18622231512
        new_name4 = u'王大大3'
        self.reg_user(new_username4, new_name4)
        self.logout()

        new_username5 = 18622231513
        new_name5 = u'王大大3'
        self.reg_user(new_username5, new_name5)
        self.logout()

        # 添加group_id
        self.login(username, '123456')  # 用第一个项目的管理员登陆 获取所有的加入申请，未处理额
        #使用项目部组，同时做环信群组的测试
        #by:王健 at:2015-2-27
        group = Group.objects.get(project_id=self.project.pk, type="sys_xmjl")
        # pre_project_blance = self.get_project_balance(self.project.pk)
        self.add_person_by_tel(self.project.pk, ','.join(
            [str(new_username2), str(new_username3), str(new_username4), str(new_username5), '3333333']), group.pk)
        self.get_all_applyproject(self.project.pk)
        # after_project_blance = self.get_project_balance(self.project.pk)
        # ppcr = ProjectPersonChangeRecord()
        # ppcr.project = self.project
        # ppcr.create_date = timezone.now() + datetime.timedelta(days=4)
        # ppcr.save()

        # 测试报停
        #by:2015-3-15
        self.set_project_baoting(self.project.pk, 14)
        ppcr, created = ProjectPersonChangeRecord.objects.get_or_create(project_id=self.project.pk,
                                                                        create_date=timezone.now() + datetime.timedelta(
                                                                            days=4))
        ppcr.stop_days += 10
        ppcr.save()
        # after_project_blance2 = self.get_project_balance(self.project.pk)
        p = ProjectRechargeRecord()
        p.date = timezone.now() + datetime.timedelta(days=100)
        p.project = self.project
        p.price0 = 6000
        #修改充值构造
        #by:王健 at:2015-3-17
        p.save(user_id=self.project.manager_id)
        ppcr = ProjectPersonChangeRecord.objects.filter(project_id=self.project.pk).order_by('-create_date')[:1]
        if len(ppcr) == 1:
            ppcr = ppcr[0]
        days = ppcr.commit_days(timezone.now() + datetime.timedelta(days=100))
        # after_project_blance2 = self.get_project_balance(self.project.pk)

        # 设置用户加入或移出某个分组
        # by:王健 at:2015-2-6
        group = self.project.group_set.filter(type='sys_jsdw')[0]
        self.change_user_group(self.project.pk, group.pk, 'join', get_user_model().objects.get(tel=new_username3).pk)
        self.change_user_group(self.project.pk, group.pk, 'join', get_user_model().objects.get(tel=new_username2).pk)
        self.change_user_group(self.project.pk, group.pk, 'join', get_user_model().objects.get(tel=new_username4).pk)
        # self.change_user_group(self.project.pk, group.pk, 'out', get_user_model().objects.get(tel=new_username2).pk)
        #设计测试 离开、移除项目
        #by:王健 at:2015-1-30
        #暂时不测试 审核加人
        #by:王健 at:2015-3-15
        # addusers = []

        # for i, app in enumerate(ProjectApply.objects.filter(project_id=self.project.pk, status=None)):
        #     if i < 3:
        #         #添加goroup_id
        #         self.change_applyproject_add(app.project_id, app.id, group.pk)
        #         addusers.append(app.user.tel)
        #     else:
        #         self.change_applyproject_remove(app.project_id, app.id)
        self.query_person(self.project.pk, 0)
        self.query_person(self.project.pk, 1)
        self.query_group(self.project.pk, 0)
        self.query_group(self.project.pk, 1)
        user = get_user_model().objects.get(tel=new_username)
        self.get_userinfo(self.project.pk, user.pk)
        user = get_user_model().objects.get(tel=new_username2)
        self.get_userinfo(self.project.pk, user.pk)

        #测试修改分组和个人权限是否正确
        #by:王健 at:2015-3-27
        # 修改权限单元测试的位置
        # by:王健 at:2015-05-13
        group = Group.objects.filter(project_id=self.project.pk).order_by('id')[2]
        self.change_power_by_group(self.project.pk, group.pk, [100, 200, 400, 500, 1700])
        person = Person.objects.filter(project_id=self.project.pk, is_active=True).order_by('-id')[0]
        self.change_power_by_person(self.project.pk, person.user_id, [100, 200, 300, 1700])

        #修改测试数据
        #by:王健 at:2015-3-15
        self.remove_person(self.project.pk, new_username3)
        self.logout()
        self.login(new_username2, u'123456')
        self.leave_project(self.project.pk, new_username2)
        self.send_social_success()
        self.logout()

        self.guest_app_url()

        #测试心情短语
        #by:尚宗凯 at:2015-3-15
        user = get_user_model().objects.get(tel=1003)
        self.login(user.tel, u'123456')
        self.update_userinfo(user.tel, phrase="我真的无用？")
        phrase = user.userinfo.phrase
        p = Project.objects.filter(name='依子轩办公大楼')[0]
        self.get_userinfo(p.pk, user.pk)
        self.logout()

        #测试获取未读数量
        user = get_user_model().objects.get(tel=1003)
        self.login(user.tel, u'123456')
        # self.get_unread_num_by_project_id(user_id=user.pk, project_id=self.project.pk)
        self.logout()

        user = get_user_model().objects.get(tel=username)
        self.login(user.tel, u'123456')
        p = Project.objects.get(name="测试项目1")
        self.close_project(p.pk)
        p.status = 0
        p.save()
        self.delete_project(p.pk)
        # self.my_project2()
        p.status = 0
        p.save()
        self.logout()




class TestSession():
    def __init__(self):
        self.m = {}

    def __setitem__(self, key, value):
        self.m[key] = value

    def __getitem__(self, item):
        return self.m[item]

    def __contains__(self, item):
        return self.m.has_key(item)

    def __getattr__(self, item):
        return self.m[item]

    def __delitem__(self, key):
        if self.m.has_key(key):
            del self.m[key]


class TestUser():
    def __init__(self, pk):
        self.pk = pk
        self.id = pk


class TestRequest():
    def __init__(self, pk):
        self.session = TestSession()
        self.user = TestUser(pk)


class JiFenTest(TestCase):
    def jifen(self):
        """
        积分测试，先往 数据库里插入一些数据，最后再清空
        by:尚宗凯 at:2015-3-7
        :return:
        """
        date = datetime.datetime(2015, 1, 1)
        for k in range(0, 2):

            request = TestRequest(k)
            # query_fen_by_uid(request, date + datetime.timedelta(days=0), test=True)
            for i in range(0, 10):
                if i == 10:
                    continue
                # query_fen_by_uid(request, date + datetime.timedelta(days=i), test=True)
                for j in range(0, 10):
                    r, f, m = login_jifen(request, date + datetime.timedelta(days=j))
                    print '---jifen---', r, ":", f, ":", m, ":"
                for j in range(0, 12):
                    r, f, m = create_data_jifen(request, settings.CREATE_DATA, date + datetime.timedelta(days=i))
                    print '---jifen---', r, ":", f, ":", m, ":"
                query_fen_by_uid(request, date + datetime.timedelta(days=i), test=True)
                for j in range(0, 5):
                    r, f, m = create_data_jifen(request, settings.FENXIANG, date + datetime.timedelta(days=i))
                    print '---jifen---', r, ":", f, ":", m, ":"
                query_fen_by_uid(request, date + datetime.timedelta(days=i), test=True)

    def test_query_jifen(self):
        self.jifen()


class RedisSessionTest(TestCase):
    """
    测试Redis Session
    by:尚宗凯 at:2015-3-8
    """

    def start_test(self):
        """
        运行测试
        :return:
        """
        cache.set('a-unique-key', 'this is a string which will be cached')
        print cache.get('a-unique-key')  # Will return None if key is not found in cache
        print cache.get('another-unique-key', 'default value')
        cache.set_many({'a': 1, 'b': 2, 'c': 3})
        print cache.get_many(['a', 'b', 'c'])
        # You can store complex types in the cache:
        cache.set('a-unique-key', {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple'    : (1, 2, 3, 4),
          'dict'      : {'A': 1, 'B' : 2},
        })
        print cache.get('a-unique-key')

        s = SessionStore()
        # stored as seconds since epoch since datetimes are not serializable in JSON.
        # s['login_time'] = json.loads(json.dumps(datetime.datetime.now()))

        s['login_time'] = json.dumps({"a":1, "b":2})
        print type(s['login_time'])
        s.save()
        session_key = s.session_key
        # print session_key
        s = Session.objects.get(pk=session_key)
        print s.expire_date
        # print s['login_time']

        request = TestRequest(999)


        a = request.session.get('has_commented', False)
        request.session['id'] = 1
        print a
        print ""



