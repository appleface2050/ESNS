# coding=utf-8
# Date:2015/1/4
# Email:wangjian2254@gmail.com
import calendar
import datetime
import json
import time
from django.db import connection
from django.db.models import Q, Sum
from django.conf import settings
from django.utils import timezone
from company.models import CompanyPerson, BigCompany, Company, SysNews, SysColumn, SaveNews, CompanyBanner, \
    CompanyColumn, CompanyNews, FollowCompany, SysBanner, Permission
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
    has_replay_or_zan, test_query_replay_by_timeline, get_last_replay_by_timeline, del_favorite_news_by_id
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
from util.apicloud import create_company_page_view,query_count_company_page_view,zan_news_by_id,del_zan_news_by_id,favorite_news_by_id

__author__ = u'王健'

from django.test import TestCase

username = '18622231518'
truename = u'测试用户1'


class CompanyTest(BaseTestCase):
    """
    公司测试
    by:尚宗凯 at:2015-6-19
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



    def logout(self):
        """
        登出接口测试
        by:王健 at:2015-1-5
        :return:
        """
        # 登录
        login_response = self.client.post('/ns/logout')
        self.assertEqual(200, login_response.status_code, u'用户登录报错')

    def create_company(self, user_id, bigcompany_id, name, logo):
        """
        创建公司
        by:尚宗凯 at：2015-06-11
		完善测试
		by:尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/create_company', {"bigcompany_id":bigcompany_id, "name":name, "logo":logo})
        bigcompany_id = bigcompany_id
        name = name
        logo = logo
        expired_date = ""
        if expired_date:
            expired_date = datetime.datetime.strptime(expired_date, "%Y-%m-%d")
        else:
            expired_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
        c = Company()
        c.bigcompany_id = bigcompany_id
        c.name = str(name)
        c.expired_date = expired_date
        if logo:
            c.logo = logo
        c.save()
        CompanyColumn.init_company_column(c)
        self.assertEqual(200, resonse.status_code, u'')
        # self.assertJSONEqual(resonse.content, getTestResult(True, u'创建公司成功', data),
        #                      u'失败')

    def get_default_sys_news(self):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/get_default_sys_news', {})
        sn = SysNews.objects.all()
        result = []
        for i in sn:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'默认展示的行业资讯成功', result),
                             u'错误')


    def get_all_big_company(self):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/get_all_big_company', {})
        bc = BigCompany.objects.all()
        result = []
        for i in bc:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取默认展示的集团成功', result),
                             u'错误')

    def company_banner(self, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        完善单元测试
        by：尚宗凯 at：2015-07-02
        """
        if company_id:
            resonse = self.client.post('/cp/%s/company_banner'% company_id)
            # banner = CompanyBanner.objects.get(company_id=company_id)
            l = []
            for banner in CompanyBanner.objects.filter(company_id=company_id).order_by('index_num')[0:20]:
                l.append(banner.toJSON())
            self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公司banner成功', l),
                         u'错误')


    def add_user_to_company(self, user_id_list ,company_id):
        """
        测试
        by：尚宗凯 at：2015-07-02
        """
        response = self.client.post('/cp/add_user_to_company', {"id":user_id_list,"company_id":company_id})
        user_ids = [int(x) for x in user_id_list]
        ids = [x[0] for x in CompanyPerson.objects.filter(user_id__in=user_ids, company_id=company_id).values_list('user_id')]
        for user in get_user_model().objects.filter(pk__in=set(user_ids)-set(ids)):
            cp,created = CompanyPerson.objects.get_or_create(user=user, company_id=company_id)
        self.assertEqual(200, response.status_code, u'错误')
        self.assertJSONEqual(response.content, getTestResult(True, u'添加成员成功'),
                         u'错误')

    def set_company_admin(self, user_id, company_id, do="manager"):
        """
        设置公司管理员
        by：尚宗凯 at：2015-06-11
        完善单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/set_company_admin'%str(company_id), {"user_id":user_id,"do":do})
        # if user_id and company_id:
        #     if CompanyPerson.objects.filter(company_id=company_id, user_id=user_id).exists():
        #         cp = CompanyPerson.objects.get(company_id=company_id, user_id=user_id)
        #         cp.creator_type = 1
        #         cp.save()
        #     self.assertJSONEqual(resonse.content, getTestResult(True, u'设置公司管理员成功'),
        #                  u'错误')
        # user_id = request.REQUEST.get("user_id","")
        if user_id and company_id:
            if CompanyPerson.objects.filter(company_id=company_id, user_id=user_id).exists():
                cp = CompanyPerson.objects.get(company_id=company_id, user_id=user_id)
                if do == "manager":
                    cp.creator_type = 1
                cp.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'设置成功'),
                                 u'错误')

    def get_company_detail_by_id(self, company_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/get_company_detail_by_id' % str(company_id))
        if Company.objects.filter(pk=company_id).exists():
            c = Company.objects.get(pk=company_id)

        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", c.toJSON()),
                             u'错误')

    def get_permission(self, company_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/get_permission' % str(company_id))
        p = Permission.objects.filter(company_id=company_id)
        result = []
        for i in p:
            result.append( str(CompanyColumn.objects.get(pk=i.column_id).flag)+"*"+str(i.group_flag)+"*"+str(i.perm))
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", result),
                             u'错误')

    def update_permission(self, company_id, power):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/update_permission' % str(company_id), {"power":power})
        for i in power:
            tmp = i.split("*")
            flag = tmp[0]
            group_flag = tmp[1]
            perm = tmp[2]
            # try:
            Permission.update_perm(company_id=company_id, flag=flag, group_flag=group_flag, perm=perm)
            # except Exception as e:
            #     print e
            #     return getResult(False, u"false")
        p = Permission.objects.filter(company_id=company_id)
        result = []
        for i in p:
            result.append( str(CompanyColumn.objects.get(pk=i.column_id).flag)+"*"+str(i.group_flag)+"*"+str(i.perm))
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", result),
                             u'错误')

    def get_child_comapny_column_list(self, company_id, flag):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/get_child_comapny_column_list' % str(company_id), {"flag":flag})
        columns = [x.toJSON() for x in CompanyColumn.objects.filter(company_id=company_id, father__flag=flag, is_active=True).order_by('index_num')]
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", columns),
                             u'错误')

    def get_company_column_by_flag(self, company_id, flag="GONGSIJIANJIE"):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/%s/get_company_column_by_flag' % str(company_id), {"flag":flag})
        if CompanyColumn.objects.filter(company_id=company_id, flag=flag):
            cc = CompanyColumn.objects.get(company_id=company_id, flag=flag)
        self.assertJSONEqual(resonse.content, getTestResult(True, u"获取公司企业动态信息成功", {"company_column_id":cc.pk}),
                             u'错误')

    def delete_project(self, project_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/delete_project',{"project_id":project_id})
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = 5
            p.delete_project_time = datetime.datetime.now()
            p.save()
            receiver_user_ids = [i.pk for i in p.group_set.filter(is_active=True)]
            p = MyEncoder.default(p)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD),
                             u'错误')

    def cancel_delete_project(self, project_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/cancel_delete_project',{"project_id":project_id})
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = 0
            p.delete_project_time = None
            p.save()
            p = MyEncoder.default(p)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功恢复项目'),
                             u'错误')


    def show_zhgl_list(self, company_id, column_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/zhgl/%s/%s'% (str(company_id), str(column_id)))
        page_start = 0
        newsquery = CompanyNews.objects.filter(company_id=company_id, company_column_id=column_id, is_active=True).order_by('-publish_time')
        l = []
        for n in newsquery[page_start:page_start+20]:
            l.append(n.toJSON2())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'',l),
                             u'错误')

    def close_project(self, project_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/close_project', {"project_id":project_id})
        if Project.objects.filter(id=project_id).exists():
            p = Project.objects.get(id=project_id)
            p.status = 2
            p.save()
            receiver_user_ids = [i.pk for i in p.group_set.filter(is_active=True)]
            # NeedMessage.create_multiple_sys_message(receiver_user_ids, "title", SYS_MESSAGE['project_close'] % (p.total_name))
            p = MyEncoder.default(p)
        self.assertJSONEqual(resonse.content, getTestResult(True, u"成功关闭项目"),
                             u'错误')

    def query_company_project(self, company_id, key="123"):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/%s/query_company_project' % str(company_id))
        projects = Project.objects.filter(company_id=company_id).filter(Q(name__icontains=key) | Q(total_name__icontains=key))
        result = []
        for i in projects[0:20]:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", result),
                             u'错误')

    def get_company_column_by_company(self, company_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/%s/get_company_column_by_company' % str(company_id))
        father_cc = CompanyColumn.objects.get(company_id=company_id, flag='ZONGHEGUANLI')
        cc = CompanyColumn.objects.filter(father_id=father_cc.pk)
        result = []
        for i in cc:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", result),
                             u'错误')

    def get_news_by_flag(self, company_id, is_active="true"):
        """
        单元测试
        by：尚宗凯 at：2015-07-03
        """
        resonse = self.client.post('/cp/%s/get_news_by_flag' % str(company_id), {"is_active":is_active})
        flag = "GONGSIJIANJIE"
        if company_id:
            news = CompanyNews.objects.filter(company_id=company_id)
            news = news.filter(Q(company_column__flag=flag)|Q(company_column__father__flag=flag))
            if is_active.lower() == "true":
                news = news.filter(is_active=True)
            elif is_active.lower() == 'false':
                news = news.filter(is_active=False)
            result = []
            news = news.order_by("-id")
            for i in news[0:20]:
                result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u"获取公司企业动态信息成功", result),
                             u'错误')

    def get_qiyezixun_news(self, company_id, is_active="true"):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/get_qiyezixun_news' % str(company_id), {"is_active":is_active})
        if company_id:
            news = CompanyNews.objects.filter(company_id=company_id)
            news = news.filter(company_column__flag='QIYEZIXUN')

            if is_active.lower() == "true":
                news = news.filter(is_active=True)
            elif is_active.lower() == 'false':
                news = news.filter(is_active=False)
            result = []
            news = news.order_by("-id")
            for i in news[0:20]:
                result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u"获取公司企业动态信息成功", result),
                             u'错误')


    def query_permission(self, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/query_permission' % str(company_id))
        if CompanyPerson.objects.filter(company_id=company_id, user_id=user_id).exists():
            zhgl = True
        else:
            zhgl = False
        if Person.objects.filter(user_id=user_id, is_active=True).exists():
            gcxmgl = True
        else:
            gcxmgl = False
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", {"zhgl":zhgl, "gcxmgl":gcxmgl}),
                             u'错误')


    def delete_company_user(self, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/delete_company_user' % str(company_id), {"user_id":user_id})

        if CompanyPerson.objects.filter(user_id=user_id, company_id=company_id):
            try:
                cp = CompanyPerson.objects.filter(user_id=user_id, company_id=company_id)[0]
                cp.delete()
            except:
                pass
        self.assertJSONEqual(resonse.content, getTestResult(False, u"用户不存在"),
                             u'错误')

    def update_company_column(self, company_id, name, columntype, index_num, is_active, father_id, flag, company_column_id):
        """
        修改公司栏目
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/update_company_column', {"company_id":company_id, "name":name, "columntype":columntype, "index_num":index_num, "is_active":is_active, "father_id":father_id, "flag":flag, "company_column_id":company_column_id})
        if company_column_id:
            if CompanyColumn.objects.filter(pk=company_column_id).exists():
                cc = CompanyColumn.objects.get(pk=company_column_id)
                if company_id:
                    cc.company_id = company_id
                if name:
                    cc.name = name
                if columntype:
                    cc.columntype = columntype
                if index_num:
                    cc.index_num = index_num
                if is_active == "False":
                    cc.is_active = False
                if is_active == "True":
                    cc.is_active = True
                if father_id:
                    cc.father_id = father_id
                if flag:
                    cc.flag = father_id
                cc.timeline = timezone.now()
                cc.save()
                self.assertJSONEqual(resonse.content, getTestResult(True, u'修改公司栏目成功'),
                         u'错误')


    def get_company_column(self, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11	
		完善测试
		by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/get_company_column'% str(company_id))
        if company_id:
            cl = CompanyColumn.objects.filter(company_id=company_id)
            result = []
            for i in cl:
                result.append(i.toJSON())
            for i in result:
                if i['father']:
                    i["name"] = CompanyColumn.objects.get(pk=i["father"]).name + "-" +  i["name"]
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公司栏目成功', result),
                             u'错误')

    def get_company_news(self, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        is_active = "true"
        page_start = 0
        resonse = self.client.post('/cp/get_company_news',{"company_id":company_id, "is_active":is_active})
        if company_id:
            news = CompanyNews.objects.filter(company_id=company_id)
            if is_active.lower() == "true":
                news = news.filter(is_active=True)
            elif is_active.lower() == 'false':
                news = news.filter(is_active=False)
            result = []
            news = news.order_by("-id")
            for i in news[page_start:page_start+20]:
                result.append(i.toJSON())
            # return getResult(True, u'获取公司企业动态信息成功', result)
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公司企业动态信息成功', result),
                             u'错误')

    def get_project_by_company(self, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/get_project_by_company',{"company_id":company_id})

        if company_id:
            projects = Project.objects.filter(company_id=company_id)
            result = []
            for i in projects:
                result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取公司的项目成功', result),
                             u'错误')


    def set_follow_company(self, user_id, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/set_follow_company', {"company_id":company_id})
        if company_id != "":
            fc = FollowCompany()
            fc.user_id = user_id
            fc.company_id = int(company_id)
            fc.create_time = timezone.now()
            fc.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'设置关注企业成功'),
                             u'错误')


    def create_bigcompany(self, name, logo):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/create_bigcompany', {"logo":logo, "name":name})
        if logo != "" and name != "":
            bc = BigCompany()
            bc.logo = logo
            bc.name = name
            bc.save()
        # self.assertJSONEqual(resonse.content, getTestResult(True, u'客服创建企业成功', bc.toJSON()),
        #                      u'错误')

    def release_sys_news(self, sys_news_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/release_sys_news', {"sys_news_id":sys_news_id})
        if sys_news_id and SysNews.objects.filter(pk=sys_news_id).exists():
            sys_news = SysNews.objects.get(pk=sys_news_id)
            sys_news.is_active = True
            sys_news.publish_time = timezone.now()
            sys_news.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'客服发布新闻成功'),
                             u'错误')

    def cancel_release_sys_news(self, sys_news_id):
        """
        客服取消发布新闻
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/cancel_release_sys_news', {"sys_news_id":sys_news_id})
        if sys_news_id and SysNews.objects.filter(pk=sys_news_id).exists():
            sys_news = SysNews.objects.get(pk=sys_news_id)
            sys_news.is_active = False
            sys_news.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'客服取消发布新闻成功'),
                             u'错误')


    def create_company_news(self, com_column_id, company_id, pre_title, title, pre_content, content, author_id):
        """
        创建公司新闻
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/create_company_news', {"com_column_id":com_column_id, "company_id":company_id, "pre_title":pre_title, "title":title, "pre_content":pre_content,"content":content, "author_id":author_id})
        sn = CompanyNews()
        sn.com_column_id = com_column_id
        sn.company_id = company_id
        sn.pre_title = pre_title
        sn.title = title
        sn.pre_content = pre_content
        sn.content = content
        sn.author_id = author_id
        sn.is_active = False
        sn.create_time = timezone.now()
        try:
            sn.save()
            self.assertJSONEqual(resonse.content, getTestResult(True, u'创建公司新闻成功'),u'错误')
        except:
            pass

    def set_company_banner(self, image, url, index_num, is_active, company_banner_id):
        """
        设置公司首页banner
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/set_company_banner', {"image":image, "url":url, "index_num":index_num, "is_active":is_active, "company_banner_id":company_banner_id})
        if company_banner_id:
            if CompanyBanner.objects.filter(pk=company_banner_id).exists():
                cb = CompanyBanner.objects.get(pk=company_banner_id)
                if image:
                    cb.image = image
                if url:
                    cb.url = url
                if index_num:
                    cb.index_num = index_num
                if is_active == "False":
                    cb.is_active = False
                if is_active == "True":
                    cb.is_active = True
                cb.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'设置公司首页banner成功'),
                             u'错误')

    def query_company_by_name(self):
        """
        测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/query_company_by_name')
        l = Company.objects.all()
        l = l.order_by('-create_time')[0:20]
        l = MyEncoder.default(l)
        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", l),
                             u'错误')

    def query_company_by_bigcompnay(self):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/query_company_by_bigcompnay')
        c = Company.objects.all()
        c = MyEncoder.default(c)
        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u"success", c),
                             u'错误')

    def query_company_pv(self, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/query_company_pv' % str(company_id))
        if company_id:
            result = query_count_company_page_view(company_id)
            create_company_page_view(company_id, user_id)
            # if result is None or (isinstance(result, dict) and result.has_key("code")):
            #     return getResult(True, u"success", {"pv": 0})
            # else:
            #     return getResult(True, u"success", {"pv": result['count']})
            self.assertEqual(200, resonse.status_code, u'错误')

    def ding_news_by_id(self, news_id, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/ding_news_by_id' % str(company_id), {"id":news_id})
        if news_id:
            if company_id:
                news = CompanyNews.objects.get(pk=news_id)
            else:
                news = SysNews.objects.get(pk=news_id)
            if news:
                if company_id:
                    result = zan_news_by_id(user_id, company_id, news_id, news.company_column_id, int(time.time()), False)
                else:
                    result = zan_news_by_id(user_id, company_id, news_id, news.sys_column_id, int(time.time()), True)
                news.add_zan_num()
                # return getResult(True, u'成功对 %s 点了个赞。' % news.title, result)
        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功对 %s 点了个赞。' % news.title, result),
                             u'错误')

    def ding_favorite_by_id(self, news_id, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/favorite_news_by_id' % str(company_id), {"id":news_id})
        if news_id:
            if company_id:
                news = CompanyNews.objects.get(pk=news_id).toJSON()
            else:
                news = SysNews.objects.get(pk=news_id).toJSON()
            if news:
                if company_id:
                    result = favorite_news_by_id(user_id, company_id, news_id, news['company_column'], int(time.time()), False, news['title'], news['news_url'], news['icon_url'])
                else:
                    result = favorite_news_by_id(user_id, company_id, news_id, news['sys_column'], int(time.time()), True, news['title'], news['news_url'], news['icon_url'])

        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功收藏了新闻 %s 。' % news['title'], result),
                             u'错误')

    def set_company_status(self, company_id, status):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/set_company_status'% str(company_id), {"status":status})
        # if Company.objects.filter(pk=company_id).exists():
        #     c = Company.objects.get(pk=company_id)
        #     c.status = int(status)
        #     c.save()
        # self.assertEqual(200, resonse.status_code, u'错误')
        if company_id and status:
            if Company.objects.filter(pk=company_id).exists():
                c = Company.objects.get(pk=company_id)
                c.status = int(status)
                c.save()
                # return getResult(True, u'成功')

        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功'),
                             u'错误')



    def get_sys_column_by_column_id(self, sys_column_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/get_sys_column_by_column_id', {"sys_column_id":sys_column_id})
        if SysColumn.objects.filter(pk=sys_column_id).exists():
            query = SysColumn.objects.get(pk=sys_column_id)
        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'', query.toJSON()),
                             u'错误')

    def delete_favorite_news_by_id(self, news_id, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/delete_favorite_news_by_id' % str(company_id), {"id":news_id})

        if news_id:
            if company_id:
                news = CompanyNews.objects.get(pk=news_id)
            else:
                news = SysNews.objects.get(pk=news_id)
            if news:
                if company_id:
                    result = del_favorite_news_by_id(user_id, news_id, False)
                else:
                    result = del_favorite_news_by_id(user_id, news_id, True)
        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功取消收藏 %s 。' % news.title, result),
                             u'错误')




    def delete_ding_news_by_id(self, news_id, company_id, user_id):
        """
        单元测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/delete_ding_news_by_id' % str(company_id), {"id":news_id})
        if news_id:
            if company_id:
                news = CompanyNews.objects.get(pk=news_id)
            else:
                news = SysNews.objects.get(pk=news_id)
            if news:
                if company_id:
                    result = del_zan_news_by_id(user_id, news_id, False)
                else:
                    result = del_zan_news_by_id(user_id, news_id, True)
                news.add_zan_num(-1)

        self.assertEqual(200, resonse.status_code, u'错误')
        self.assertJSONEqual(resonse.content, getTestResult(True, u'成功对 %s 取消了赞。' % news.title, result),
                             u'错误')

    def update_sys_column(self, sys_column_id, name):
        """
        测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/update_sys_column', {"sys_column_id":sys_column_id, "name":name})
        if sys_column_id:
            if SysColumn.objects.filter(pk=sys_column_id).exists():
                sc = SysColumn.objects.get(pk=sys_column_id)
                if name:
                    sc.name = name
                sc.save()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'修改系统栏目成功'),
                             u'错误')


    def create_zhgl_company_news(self, company_id, type_flag, flag, user_id):
        """
        测试
        by：尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/%s/create_zhgl_company_news'%str(company_id), {"type_flag":type_flag, "flag":flag})
        company_column_id = CompanyColumn.objects.get(company_id=company_id, flag=flag).pk
        sn = CompanyNews()
        sn.company_id = company_id
        sn.company_column_id = company_column_id
        sn.author_id = user_id
        sn.pre_title = ""
        # if type_flag not in ("files", "images"):
        #     sn.pre_content = ""
        # else:
        #     fileids = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
        #     for fid in fileids:
        #         sn.append_file(fid)
        sn.title = sn.pre_title
        sn.content = sn.pre_content
        sn.is_active = True
        if type_flag:
            sn.type_flag = type_flag
        try:
            sn.save()
            self.assertJSONEqual(resonse.content["message"], getTestResult(True, u'创建公司新闻成功'),
                             u'错误')
        except Exception:
            pass

    def create_sys_column(self, name, index_num, father_id, flag):
        """
        客服创建系统栏目
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/create_sys_column', {"name":name, "index_num":index_num, "father_id":father_id, "flag":flag})
        sc = SysColumn()
        sc.name = name
        sc.index_num = index_num
        sc.is_active = True
        sc.father_id = father_id
        sc.flag = flag
        sc.timeline = 0
        try:
            sc.save()
            self.assertJSONEqual(resonse.content, getTestResult(True, u'客服创建系统栏目成功'),
                             u'错误')
        except:
            pass

    def set_sys_banner(self, image, url, index_num, is_active, sys_banner_id):
        """
        设置系统首页banner
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/set_sys_banner', {"image":image, "url":url, "index_num":index_num, "is_active":is_active, "sys_banner_id":sys_banner_id})
        if sys_banner_id:
            if SysBanner.objects.filter(pk=sys_banner_id).exists():
                sb = SysBanner.objects.get(pk=sys_banner_id)
                if image:
                    sb.image = image
                if url:
                    sb.url = url
                if index_num:
                    sb.index_num = index_num
                if is_active == "False":
                    sb.is_active = False
                if is_active == "True":
                    sb.is_active = True
                sb.save()
                self.assertJSONEqual(resonse.content, getTestResult(True, u'设置系统首页banner成功'),
                             u'错误')

    def create_sys_news(self, sys_column_id, company_id, pre_title, title, pre_content, content, author_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/create_sys_news', {"sys_column_id":sys_column_id, "company_id":company_id, "pre_title":pre_title, "title":title, "pre_content":pre_content, "content":content,"author_id":author_id})
        sn = SysNews()
        sn.sys_column_id = sys_column_id
        sn.company_id = company_id
        sn.pre_title = pre_title
        sn.title = title
        sn.pre_content = pre_content
        sn.content = content
        sn.author_id = author_id
        sn.is_active = False
        sn.create_time = timezone.now()
        try:
            sn.save()
            self.assertJSONEqual(resonse.content, getTestResult(True, u'客服上传系统新闻成功'),
                         u'错误')
        except Exception as e:
            pass


    def cancel_follow_company(self, user_id, company_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/cancel_follow_company', {"company_id":company_id})
        if company_id != "":
            if FollowCompany.objects.filter(company_id=company_id, user_id=user_id).exists():
                fc = FollowCompany.objects.filter(company_id=company_id, user_id=user_id)
                for i in fc:
                    i.delete()
        self.assertJSONEqual(resonse.content, getTestResult(True, u'取消关注企业成功'),
                             u'错误')


    def get_my_save_news(self, user_id):
        """
        测试
        by：尚宗凯 at：2015-06-11
        """
        resonse = self.client.post('/cp/get_my_save_news')
        news = SaveNews.objects.filter(user_id=user_id)
        result = []
        for i in news:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取我的收藏成功', result),
                             u'错误')


    # def save_news(self, user_id, news_id, news_type):
    #     """
    #     测试
    #     by：尚宗凯 at：2015-06-11
    #     """
    #     resonse = self.client.post('/cp/save_news', {"news_id":news_id, "news_type":news_type})
    #     # if news_id:
    #     #     s = SaveNews()
    #     #     s.user_id = user_id
    #     #     s.news_id = news_id
    #     #     s.create_time = timezone.now()
    #     #     s.news_type = news_type
    #     #     s.save()
    #
    #     if news_id:
    #         s = SaveNews()
    #         s.user_id = user_id
    #         s.news_id = news_id
    #         s.create_time = timezone.now()
    #         s.news_type = news_type
    #         s.save()
    #     self.assertJSONEqual(resonse.content, getTestResult(True, u'收藏新闻成功'),
    #                          u'错误')


    def get_default_big_company(self):
        """
        测试
        by：尚宗凯 at：2015-06-11
        修改逻辑
        by：尚宗凯 at：2015-06-19
        """
        resonse = self.client.post('/cp/get_default_big_company', {})
        self.assertEqual(200, resonse.status_code, u'')
        bc = BigCompany.objects.filter(is_display=True)
        # bc = BigCompany.objects.all()
        result = []
        for i in bc:
            result.append(i.toJSON())
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取默认展示的集团成功', result),
                             u'错误')

    def my_company(self, user_id):
        """
        测试my_company
        by：尚宗凯 at：2015-06-11
        修改单元测试
        by:尚宗凯 at：2015-07-02
        """
        resonse = self.client.post('/cp/my_company', {})
        self.assertEqual(200, resonse.status_code, u'')
        # cp = CompanyPerson.objects.filter(user_id=user_id)
        # if cp:
        #     result = []
        #     for i in cp:
        #         result.append(i.company.toJSON())
        user = get_user_model().objects.get(id=user_id)
        companyquery = [x.toJSON() for x in Company.objects.filter(status__in=[0, 1]).filter(Q(companyperson__user=user, companyperson__is_active=True) | Q(project__person__user=user, project__person__is_active=True))]
        self.assertJSONEqual(resonse.content, getTestResult(True, u'获取我的企业成功', companyquery),
                             u'获取分享成功的积分，返回结果有变化，需要确认，或修改单元测试')

    def test_company(self):
        self.login(username, '123456')

        #测试公司接口
        #by:尚宗凯 at：2015-6-11
        test_bc = BigCompany()
        test_bc.name = "测试name"
        test_bc.logo = "1"
        test_bc.save()

        user = get_user_model().objects.get(tel=1003)
        self.login(user.tel, u'123456')
        self.create_company(user.pk, test_bc.pk, 2, 2 )
        self.my_company(user.pk)
        self.get_default_big_company()
        self.get_default_sys_news()
        self.get_all_big_company()

        sys_column = SysColumn()
        sys_column.name = "1"
        sys_column.index_num = 0
        sys_column.is_active = True
        sys_column.flag = "1"
        sys_column.timeline = 0
        sys_column.save()
        sys_news = SysNews()
        sys_news.sys_column_id = sys_column.pk
        sys_news.company_id = Company.objects.all()[0].pk
        sys_news.pre_title = "pre_title"
        sys_news.title = "title"
        sys_news.pre_content = "pre_comtent"
        sys_news.content = "content"
        sys_news.author_id = user.pk
        sys_news.is_active = True
        sys_news.create_time = timezone.now()
        sys_news.publish_time = timezone.now()
        sys_news.save()
        # self.save_news(user.pk, sys_news.pk, 0)
        # self.get_my_save_news(user.pk)

        company_banner = CompanyBanner()
        company_banner.company_id = Company.objects.all()[0].pk
        company_banner.image = 1
        company_banner.url = " "
        company_banner.index_num = 0
        company_banner.is_active = True
        company_banner.timeline = 0
        company_banner.save()

        sys_banner = SysBanner()
        sys_banner.image = 0
        sys_banner.url = " "
        sys_banner.index_num = 1
        sys_banner.is_active = True
        sys_banner.timeline = 0
        sys_banner.save()
        self.set_company_banner(1, "https://www.baidu.com/img/bdlogo.png", 1 ,"True", company_banner.pk)
        self.set_sys_banner(1,"https://www.baidu.com/img/bdlogo.png",1,"True",sys_banner.pk)


        company_column = CompanyColumn()
        company_column.company_id = Company.objects.all()[0].pk
        company_column.name = "company_column"
        company_column.columntype = 0
        company_column.index_num = 1
        company_column.is_active = True
        company_column.flag = "company_column"
        company_column.save()

        # self.create_company_news(company_column.pk, Company.objects.all()[0].pk, "pre_title", "title", "pre_content", "content", user.pk)
        #增加新的一批单元测试
        #by：尚宗凯 at：2015-07-02
        self.add_user_to_company([user.pk], Company.objects.all()[0].pk)
        self.set_company_admin(user.pk, Company.objects.all()[0].pk)
        self.get_company_detail_by_id(Company.objects.all()[0].pk)
        # a = CompanyPerson.objects.get(user_id=user.pk, company_id=Company.objects.all()[0].pk)
        # a.creator_type = True
        # a.save()
        self.create_zhgl_company_news(Company.objects.all()[0].pk,"news","TONGZHIGONGGAO",user.pk)
        self.update_sys_column(sys_column.pk,"测试名字")
        self.query_company_by_name()
        self.query_company_by_bigcompnay()
        self.query_company_pv(Company.objects.all()[0].pk, user.pk)
        self.ding_news_by_id(sys_news.pk, Company.objects.all()[0].pk, user.pk)
        self.delete_ding_news_by_id(sys_news.pk, Company.objects.all()[0].pk, user.pk)
        self.ding_favorite_by_id(sys_news.pk, Company.objects.all()[0].pk, user.pk)
        # self.delete_favorite_news_by_id(sys_news.pk, Company.objects.all()[0].pk, user.pk)
        self.get_sys_column_by_column_id(sys_column.pk)
        self.set_company_admin(user.pk, Company.objects.all()[0].pk)
        self.set_company_status(Company.objects.all()[0].pk, "0")
        self.delete_company_user(Company.objects.all()[0].pk,11)
        self.get_permission(Company.objects.all()[0].pk)
        self.query_permission(Company.objects.all()[0].pk,user.pk)
        # self.get_child_comapny_column_list(Company.objects.all()[0].pk,"GONGSIJIANJIE")
        self.get_qiyezixun_news(Company.objects.all()[0].pk)
        self.get_news_by_flag(Company.objects.all()[0].pk)
        self.get_company_column_by_flag(Company.objects.all()[0].pk)
        self.get_company_column_by_company(Company.objects.all()[0].pk)
        project = Project.objects.all()[0]
        self.close_project(project.pk)
        self.delete_project(project.pk)
        self.show_zhgl_list(Company.objects.all()[0].pk,company_column.pk)

        # self.update_company_column(Company.objects.all()[0].pk, "new column", 1, 1, "True", None, "flag", company_column.pk)
        self.set_company_admin(user.pk, Company.objects.all()[0].pk)
        self.company_banner(Company.objects.all()[0].pk)
        self.get_company_column(Company.objects.all()[0].pk)
        self.get_company_news(Company.objects.all()[0].pk)
        self.get_project_by_company(Company.objects.all()[0].pk)
        self.set_follow_company(user.pk, Company.objects.all()[0].pk)
        self.cancel_follow_company(user.pk, Company.objects.all()[0].pk)
        self.create_bigcompany(name="a",logo=2)
        self.create_sys_news(sys_column.pk,Company.objects.all()[0].pk,"pre_title","title","pre_content","content",user.pk)
        self.release_sys_news(SysNews.objects.all()[0].pk)
        self.cancel_release_sys_news(SysNews.objects.all()[0].pk)
        self.create_sys_column("test_column",1,None,"test_column")


