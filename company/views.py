# coding=utf-8
import datetime
import random
from django.shortcuts import render_to_response
from django.template import RequestContext
from company.models import CompanyPerson, BigCompany, SysNews, CompanyNews, SaveNews, CompanyBanner, CompanyColumn, \
    Company, FollowCompany, SysColumn, SysBanner, Permission
from needserver.models import Project, NSUser, Person, NeedMessage, Group, ProjectRechargeRecord, \
    ProjectPersonChangeRecord
from ns_manage.models import BackUserInfo
from nsbcs.models import ComFile, SysFile
from util import PROJECT_INFO, MY_PROJECT_QUERY_LIST
from util.apicloud import query_count_company_page_view, create_company_page_view, query_favorite_by_author
from util.jsonresult import getResult
from company.base.views import FrameView
# from manage.base.views import FrameView
from django.utils import timezone
from util.loginrequired import ns_manage_login_required, ns_manage_admin_login_required, \
    login_company_customer_service_required, login_company_admin_required
from django.contrib.auth import logout as auth_logout, get_user_model
from django import http
from django.db.models import Q
from util.jsonresult import MyEncoder
from django.conf import settings
import time
from django.core.cache import cache
from Need_Server.settings import DELETE_PROJECT_PUBLICITY_PERIOD, SYS_MESSAGE
from webhtml.base.views import BaseView

__author__ = 'EasyShare004'

def my_company(request):
    """
    获取我的企业
    by：尚宗凯 at：2015-06-10
    优化接口
    by：尚宗凯 at：2015-06-18
    接口只返回状态为0 1 的公司
    by：尚宗凯 at：2015-06-23
    优化接口，公司下项目 也可显示
    by:王健 at:2015-07-01
    """
    companyquery = [x.toJSON() for x in Company.objects.filter(status__in=[0, 1]).filter(Q(companyperson__user=request.user, companyperson__is_active=True) | Q(project__person__user=request.user, project__person__is_active=True))]

    return getResult(True, u'获取我的企业成功', companyquery)


def get_default_big_company(request):
    """
    获取默认展示的集团
    by：尚宗凯 at：2015-06-10
    增加is_display为True
    by：尚宗凯 at：2015-06-16
    """
    bc = BigCompany.objects.filter(is_display=True)
    result = []
    for i in bc:
        result.append(i.toJSON())
    return getResult(True, u'获取默认展示的集团成功', result)


def get_default_sys_news(request):
    """
    默认展示的行业资讯
    by:尚宗凯 at：2015-06-10
    完善逻辑
    by:尚宗凯 at：2015-06-18
    改为倒叙
    by:尚宗凯 at：2015-06-25
    最多显示5条
    by：尚宗凯 at：2015-06-25
    只显示已经发布的新闻
    by:王健 at:2015-06-27
    """
    sn = SysNews.objects.filter(is_active=True).order_by("-publish_time")[:5]
    result = []
    for i in sn:
        if i.publish_time:
            result.append(i.toJSON())
    return getResult(True, u'默认展示的行业资讯成功', result)


def get_all_big_company(request):
    """
    查询所有集团
    by：尚宗凯 at：2015-06-10
    """
    bc = BigCompany.objects.all()
    result = []
    for i in bc:
        result.append(i.toJSON())
    return getResult(True, u'获取默认展示的集团成功', result)


# def get_all_big_company(request):
#     """
#     按栏目查询所有资讯
#     by：尚宗凯 at：2015-06-10
#     """
#     company_id = request.REQUEST.get("company_id","")
#     if not company_id:
#         return getResult(True, u'获取失败')
#     bc = BigCompany.objects.filter(company_id=company_id)
#     result = []
#     for i in bc:
#         result.append(i.toJSON())
#     return getResult(True, u'按栏目查询所有资讯成功', result)


def save_news(request):
    """
    设置收藏
    by：尚宗凯 at：2015-06-10
    完善接口
    by：尚宗凯 at：2015-06-11
    """
    news_id = request.REQUEST.get("news_id","")
    news_type = request.REQUEST.get("news_type","")
    if news_type == "":
        return getResult(False, u'参数不正确')
    if int(news_type) == 0:
        if not SysNews.objects.filter(pk=news_id).exists():
            return getResult(False, u'新闻不存在')
    elif int(news_type) == 1:
        if not CompanyNews.objects.filter(pk=news_id).exists():
            return getResult(False, u'新闻不存在')

    if news_id:
        s = SaveNews()
        s.user_id = request.user.pk
        s.news_id = news_id
        s.create_time = timezone.now()
        s.news_type = news_type
        s.save()
        return getResult(True, u'收藏新闻成功')
    else:
        return getResult(False, u'收藏新闻失败,参数错误')


def cancel_save_news(request):
    """
    取消收藏
    by：尚宗凯 at：2015-06-10
    优化取消收藏
    by：尚宗凯 at：2015-06-11
    """
    news_id = request.REQUEST.get("news_id","")
    news_type = request.REQUEST.get("news_type","")
    if news_type == "":
        return getResult(False, u'参数不正确')
    if int(news_type) == 0:
        if not SysNews.objects.filter(pk=news_id).exists():
            return getResult(False, u'新闻不存在')

    if SaveNews.objects.filter(news_id=news_id, user_id=request.user.pk, news_type=news_type).exists():
        s = SaveNews.objects.get(news_id=news_id, user_id=request.user.pk, news_type=news_type)
        s.delete()
        return getResult(True, u'取消新闻成功')
    else:
        return getResult(False, u'取消新闻失败，参数错误')


def get_my_save_html(request):
    """
    获取我的收藏html
    by：尚宗凯 at：2015-06-17
    更改html位置
    by:王健 at:2015-06-19
    完善这个接口
    by：尚宗凯 at：2015-06-22
    显示我的收藏
    by:王健 at:2015-06-23
    优化显示 我的收藏html
    by:王健 at:2015-06-25
    """
    # result = [{"title":"测试收藏网址"}]
    l = query_favorite_by_author(request.user.pk)

    return render_to_response('cp_manage/phone/my_save_news_html.html', RequestContext(request, {"news": l}))


def get_my_save_news(request):
    """
    获取我的收藏
    by：尚宗凯 at：2015-06-10
    """
    news = SaveNews.objects.filter(user_id=request.user.pk)
    result = []
    for i in news:
        result.append(i.toJSON())
    return getResult(True, u'获取我的收藏成功', result)


def all_sys_banner(request):
    """
    获取所有首页banner
    by：尚宗凯 at：2015-06-16
    增加分页
    by：尚宗凯 at:2015-06-18
    按照顺序排序
    by:王健 at:2015-06-29
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    sb = SysBanner.objects.all().order_by('index_num')
    result = []
    for i in sb[page_start:page_start+20]:
        result.append(i.toJSON())
    return getResult(True, u'获取首页banner', result)


def all_sys_column(request):
    """
    获取所有sys栏目
    by：尚宗凯 at：2015-06-17
    增加分页
    by：尚宗凯 at:2015-06-18
    优化系统栏目名称
    by：尚宗凯 at：2015-06-24
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    query = SysColumn.objects.all().order_by('-id')
    result = []
    for i in query[page_start:page_start+20]:
        result.append(i.toJSON())
    for i in result:
        if i['father']:
            i["name"] = SysColumn.objects.get(pk=i["father"]).name + "-" + i["name"]
    return getResult(True, u'获取首页   column', result)


def sys_banner(request):
    """
    获取首页banner
    by：尚宗凯 at：2015-06-12
    优化系统banner 排序
    by:王健 at:2015-06-22
    """
    sb = SysBanner.objects.filter(is_active=True).order_by('index_num')
    result = []
    for i in sb:
        result.append(i.toJSON())
    return getResult(True, u'获取首页banner', result)


def company_banner(request, company_id=None):
    """
    获取公司banner
    by：尚宗凯 at：2015-06-10
    获取公司banner 优化
    by:王健 at:2015-06-22
    增加分页查询
    by：尚宗凯 at：2015-06-23
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    if company_id:
        try:
            l = []
            for banner in CompanyBanner.objects.filter(company_id=company_id).order_by('index_num')[page_start:page_start+20]:
                l.append(banner.toJSON())
            return getResult(True, u'获取公司banner成功', l)
        except Exception as e:
            return getResult(False, u'获取公司banner失败')
    else:
        return getResult(False, u'获取公司banner失败,参数错误')


def get_company_column(request, company_id=None):
    """
    获取公司栏目
    by：尚宗凯 at：2015-06-10
    优化接口
    by：尚宗凯 at：2015-06-19
    """
    if company_id:
        cl = CompanyColumn.objects.filter(company_id=company_id)
        result = []
        for i in cl:
            result.append(i.toJSON())
        for i in result:
            if i['father']:
                i["name"] = CompanyColumn.objects.get(pk=i["father"]).name + "-" +  i["name"]
        return getResult(True, u'获取公司栏目成功', result)
    else:
        return getResult(False, u'获取公司栏目,参数错误')


def get_qyzx_company_news(request, company_id):
    """
    获得企业资讯新闻
    by：尚宗凯 at：2015-06-27
    添加返回数量限制
    by:王健 at:2015-06-27
    缩减企业咨询的默认数量
    by:王健 at:2015-07-03
    """
    try:
        qyex = CompanyColumn.objects.get(flag="QIYEZIXUN", company_id=company_id)
    except:
        return getResult(False, u'获取公司的企业资讯栏目失败')
    if company_id:
        news = CompanyNews.objects.filter(company_id=company_id, is_active=True, company_column_id=qyex.pk).order_by("-publish_time")[:4]
        result = []
        for i in news:
            result.append(i.toJSON())
        return getResult(True, u'获取公司企业动态信息成功', result)
    else:
        return getResult(False, u'获取公司企业动态信息失败,参数错误')


def get_company_news(request):
    """
    获取公司企业动态信息
    by: 尚宗凯 at：2015-06-10
    增加分页功能
    by：尚宗凯 at：2015-06-22
    增加搜索功能
    by：尚宗凯 at：2015-06-23
    增加栏目查询
    by：尚宗凯 at：2015-06-24
    修复分页bug
    by：尚宗凯 at：2015-06-24
    增加新闻排序
    by：尚宗凯 at：2015-06-24
    增加是否发布查询条件
    by：尚宗凯 at：2015-06-26
    is_active 转换为小写再判断
    by：王健 at：2015-06-26
    is_active 转换bug
    by：尚宗凯 at：2015-06-26
    优化查询逻辑
    by：王健 at：2015-06-26
    逻辑优化，改为如果是父节点则返回所有子节点的新闻
    by：尚宗凯 at：2015-06-29
    """
    key = request.REQUEST.get("key","")
    page_start = int(request.REQUEST.get('page_start', 0))
    company_id = request.REQUEST.get("company_id","")
    company_column_id = request.REQUEST.get("company_column_id","")
    is_active = request.REQUEST.get("is_active","")

    if company_id:
        news = CompanyNews.objects.filter(company_id=company_id)
        if company_column_id:
            father_id = CompanyColumn.objects.get(pk=company_column_id).father_id
            if not father_id:
                child_cc_id_list = [i.pk for i in CompanyColumn.objects.filter(father_id=company_column_id)]
                news = news.filter(company_column__in=child_cc_id_list)
            else:
                news = news.filter(company_column_id=company_column_id)
        if key:
            news = news.filter(company_id=company_id).filter(Q(title__icontains=key) | Q(content__icontains=key)|Q(pre_title__icontains=key) | Q(pre_content__icontains=key))
        if is_active.lower() == "true":
            news = news.filter(is_active=True)
        elif is_active.lower() == 'false':
            news = news.filter(is_active=False)
        result = []
        news = news.order_by("-id")
        for i in news[page_start:page_start+20]:
            result.append(i.toJSON())
        return getResult(True, u'获取公司企业动态信息成功', result)
    else:
        return getResult(False, u'获取公司企业动态信息失败,参数错误')



def get_project_by_company(request):
    """
    获取公司的项目
    by：尚宗凯 at：2015-06-10
    添加项目成员数量
    by:王健 at:2015-06-17
    增加消费金额
    by:王健 at:2015-06-19
    增加用户是否在项目里面
    by：尚宗凯 at：2015-06-30
    公司项目，先简单计算使用金豆数量，未来再根据公司的合同来计算实际使用数量
    by:王健 at:2015-07-01
    """
    company_id = request.REQUEST.get("company_id","")
    if company_id:
        projects = Project.objects.filter(company_id=company_id)
        result = []
        for i in projects:
            d = i.toJSON()
            if Person.objects.filter(user_id=request.user.pk, project_id=i.pk).exists():
                d["does_user_in_project"] = True
            else:
                d["does_user_in_project"] = False
            d['person_num'] = i.person_set.filter(is_active=True).count()
            #todo:这种计算方法没有考虑到 合同未签时的试用时间，待合同开发后再来修改
            d['price_num'] = ((timezone.now() - i.create_time).days + 1)*50
            result.append(d)
        return getResult(True, u'获取公司的项目成功', result)
    else:
        return getResult(False, u'获取公司的项目失败,参数错误')


def create_company(request):
    """
    创建公司(客服用)
    by：尚宗凯 at：2015-06-10
    完善接口
    by：尚宗凯 at：2015-06-11
    修改一个bug
    by：尚宗凯 at：2015-06-12
    更改默认id
    by：尚宗凯 at：2015-06-16
    增加公司字段
    by：尚宗凯 at：2015-06-18
    增加初始化公司column
    by：尚宗凯 at：2015-06-18
    优化公司创建
    by:王健 at:2015-6-19
    创建公司后，返回公司的信息
    by:王健 at:2015-06-22
    修复增加companyPerson
    by：尚宗凯 at：2015-06-22
    优化创建公司时集团选择
    by：尚宗凯 at：2015-06-24
    增加company_id
    by：尚宗凯 at：2015-06-24
    优化集团id
    by：尚宗凯 at：2015-06-24
    优化初始化公司栏目
    by：尚宗凯 at：2015-06-26
    优化创建和修改接口
    by:王健 at:2015-06-27
    修复无法创建公司bug
    by：尚宗凯 at：2015-06-29
    """
    bigcompany_id = request.REQUEST.get("bigcompany_id",None)
    company_id = request.REQUEST.get("company_id","")

    if bigcompany_id and not BigCompany.objects.filter(pk=bigcompany_id).exists():
        # return getResult(False, u'创建公司失败，不存在这个集团')
        bigcompany_id = None
    name = request.REQUEST.get("name","")
    logo = request.REQUEST.get("logo",0)
    address = request.REQUEST.get("address","")
    phone = request.REQUEST.get("phone","")
    expired_date = request.REQUEST.get("expired_date","")
    if expired_date:
        expired_date = datetime.datetime.strptime(expired_date, "%Y-%m-%d")
    else:
        expired_date = datetime.datetime.now().date() + datetime.timedelta(days=7)
    if company_id:
        c, created = Company.objects.get_or_create(pk=int(company_id))

    else:
        c = Company()
    c.bigcompany_id = bigcompany_id
    c.name = str(name)
    if logo:
        c.logo = logo
    if not company_id:
        c.expired_date = expired_date
    if address:
        c.address = address
    if phone:
        c.phone = phone
    c.save()

    if not company_id:
        CompanyColumn.init_company_column(c)
    return getResult(True, u'创建公司成功', c.toJSON())


def set_follow_company(request):
    """
    设置关注企业
    by: 尚宗凯 at：2015-06-10
    优化一下
    by：尚宗凯 at：2015-06-11
    """
    company_id = request.REQUEST.get("company_id","")
    user_id = request.user.pk
    if company_id != "":
        if not Company.objects.filter(pk=company_id).exists():
            return getResult(False, u'设置关注企业失败,企业不存在')
        elif FollowCompany.objects.filter(user_id=user_id, company_id=company_id).exists():
            return getResult(False, u'已关注')
        else:
            fc = FollowCompany()
            fc.user_id = user_id
            fc.company_id = int(company_id)
            fc.create_time = timezone.now()
            fc.save()
            return getResult(True, u'设置关注企业成功')
    else:
        return getResult(False, u'设置关注企业失败,参数错误')


def cancel_follow_company(request):
    """
    取消关注企业
    by: 尚宗凯 at：2015-06-10
    完善一下
    by：尚宗凯 at：2015-06-11
    """
    company_id = request.REQUEST.get("company_id","")
    if company_id != "":
        if FollowCompany.objects.filter(company_id=company_id, user_id=request.user.pk).exists():
            fc = FollowCompany.objects.filter(company_id=company_id, user_id=request.user.pk)
            for i in fc:
                i.delete()
            return getResult(True, u'取消关注企业成功')
        else:
            return getResult(False, u'未关注该企业')
    else:
        return getResult(False, u'取消关注企业失败,参数错误')


def create_bigcompany(request):
    """
    #客服创建企业
    #by：尚宗凯 at：2015-06-11
    集团创建和修改以及获取兼容
    by:王健 at:2015-06-27
    修复逻辑bug
    by：尚宗凯 at：2015-06-29
    """
    logo = request.REQUEST.get("logo","")
    name = request.REQUEST.get("name","")
    pk = request.REQUEST.get("id","")
    if pk:
        bc = BigCompany.objects.get(pk=pk)
    else:
        bc = BigCompany()
    if logo:
        bc.logo = logo
    if name:
        bc.name = name
    if logo != "" or name != "":
        bc.save()
    return getResult(True, u'客服创建企业成功', bc.toJSON())


def create_sys_news(request):
    """
    客服上传系统新闻
    by：尚宗凯 at：2015-06-11
    优化逻辑
    by: 尚宗凯 at：2015-06-16
    优化新闻创建的返回值
    by:王健 at:2015-06-24
    """
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = SysNews.objects.get(pk=pk)
    else:
        sn = SysNews()
    sn.sys_column_id = request.REQUEST.get("sys_column_id",1)
    sn.company_id = None
    sn.pre_title = request.REQUEST.get("title","")
    sn.pre_content = request.REQUEST.get("content","")
    sn.author_id = request.user.pk
    sn.is_active = False
    sn.create_time = timezone.now()
    try:
        sn.save()
        return getResult(True, u'客服上传系统新闻成功', sn.toJSON())
    except Exception as e:
        return getResult(False, u'客服上传系统新闻失败')


def get_sys_news_by_id(request):
    """
    根据id获取新闻信息，方便编辑
    输出栏目信息 ，方便前端显示
    by:王健 at:2015-06-17
    添加sys_column 属性
    by:王健 at:2015-06-30
    :param request:
    :return:
    """
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = SysNews.objects.get(pk=pk)
        column_list = [x.toJSON() for x in SysColumn.objects.all()]
        return getResult(True, u'', {'id': sn.pk, 'sys_column_id': sn.sys_column_id, 'sys_column': sn.sys_column_id, 'title': sn.pre_title, 'content': sn.pre_content, 'column_list': column_list})
    else:
        return getResult(False, u'没有找到新闻')


def get_company_news_by_id(request):
    """
    根据id获取新闻信息，方便编辑
    by：尚宗凯 at：2015-06-23
    """
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = CompanyNews.objects.get(pk=pk)
        column_list = [x.toJSON() for x in CompanyColumn.objects.all()]
        return getResult(True, u'', {'id': sn.pk, 'company_column_id': sn.company_column_id, 'title': sn.pre_title, 'content': sn.pre_content, 'column_list': column_list})
    else:
        return getResult(False, u'没有找到新闻')


def get_company_news_by_id2(request):
    """
    根据id获取新闻信息，column_list内容为这个新闻的父节点下面的所有子节点
    by：尚宗凯 at：2015-06-27
    添加company_column 属性
    by:王健 at:2015-06-30
    增加返回type_flag
    by:尚宗凯 at：2015-07-02
    增加附件的url地址
    by：尚宗凯 at：2015-07-03
    """
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = CompanyNews.objects.get(pk=pk)
        if CompanyColumn.objects.get(pk=sn.company_column_id).flag == "QIYEZIXUN":
            column_list = []
        else:
            father_id = CompanyColumn.objects.get(pk=sn.company_column_id).father_id
            column_list = [x.toJSON() for x in CompanyColumn.objects.filter(father_id=father_id)]
        file_url_list = []
        if sn.files:
            for fileid in sn.files.strip("[]").split(","):
                try:
                    # file_url_list.append(SysFile.objects.get(pk=fileid).get_url())
                    file_url_list.append(ComFile.objects.get(pk=fileid).get_url())
                except Exception:
                    pass
        return getResult(True, u'', {"type_flag":sn.type_flag, 'id': sn.pk, 'company_column_id': sn.company_column_id, 'company_column': sn.company_column_id, 'title': sn.pre_title, 'content': sn.pre_content, 'column_list': column_list, "file_url_list":file_url_list})
    else:
        return getResult(False, u'没有找到新闻')



def get_company_by_id(request):
    """
    根据id获取公司
    by：尚宗凯 at：2015-06-18
    优化返回值
    by：王建 at：2015-06-24
    """
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = Company.objects.get(pk=pk)
        # for cp in CompanyPerson.objects.filter(company_id=pk):
        #     cp.user.name
        column_list = [(x.user.name, x.user_id) for x in CompanyPerson.objects.filter(company_id=pk)]
        result = sn.toJSON()
        result['column_list'] = column_list
        return getResult(True, u'', result)
    else:
        return getResult(False, u'没有找到公司')


def get_user_by_company_id(request, company_id):
    """
    根据公司id查询公司下用户
    by:尚宗凯 at：2015-06-19
    """
    key = request.REQUEST.get("key","")
    cp = CompanyPerson.objects.filter(company_id=company_id)
    result = []
    for i in cp:
        if key:
            if key in (i.user.name) or key in (i.user.tel):
                result.append(i.user)
        else:
            result.append(i.user)
    return getResult(True, u'', result)


def get_sys_column_by_column_id(request):
    """
    系统栏目id获取栏目信息
    by:尚宗凯 at：2015-06-22
    修改一下返回一个数据
    by：尚宗凯 at：2015-06-22
    """
    sys_column_id = request.REQUEST.get("sys_column_id","")
    if not sys_column_id:
        return getResult(False, u'参数错误')
    if SysColumn.objects.filter(pk=sys_column_id).exists():
        query = SysColumn.objects.get(pk=sys_column_id)

    return getResult(True, u'', query.toJSON())


def create_sys_banner(request):
    """
    创建系统banner
    by：尚宗凯 at：2015-06-16
    优化接口
    by：尚宗凯 at：2015-06-23
    """
    b = SysBanner()
    b.image = request.REQUEST.get("image","")
    b.url = request.REQUEST.get("url","")
    # if b.url == "":
    #     b.url = "https://git.oschina.net/logo.gif"
    b.index_num = request.REQUEST.get("index_num","")
    if b.index_num == "":
        b.index_num = SysBanner.objects.all().count()
    b.is_active = False
    b.timeline = 0
    try:
        b.save()
        return getResult(True, u'创建系统banner成功')
    except Exception as e:
        return getResult(False, u'创建系统banner失败')


def create_company_banner(request, company_id=None):
    """
    创建公司banner
    by：尚宗凯 at：2015-06-23
    """
    if not company_id:
        return getResult(False, u'参数错误')
    c = CompanyBanner()
    c.image = request.REQUEST.get("image","")
    c.url = request.REQUEST.get("url","")
    c.company_id = company_id
    c.index_num = request.REQUEST.get("index_num",0)
    c.timeline = 0
    c.is_active = False
    try:
        c.save()
        return getResult(True, u'创建公司banner成功')
    except Exception as e:
        return getResult(False, u'创建公司banner失败')


def release_sys_news(request):
    """
    客服发布新闻
    by：尚宗凯 at：2015-06-11
    """
    sys_news_id = request.REQUEST.get("sys_news_id","")
    if sys_news_id and SysNews.objects.filter(pk=sys_news_id).exists():
        sys_news = SysNews.objects.get(pk=sys_news_id)
        sys_news.is_active = True
        sys_news.publish_time = timezone.now()
        sys_news.save()
        return getResult(True, u'客服发布新闻成功')
    else:
        return getResult(True, u'客服发布新闻失败')


def cancel_release_sys_news(request):
    """
    客服取消发布新闻
    by：尚宗凯 at：2015-06-11
    """
    sys_news_id = request.REQUEST.get("sys_news_id","")
    if sys_news_id and SysNews.objects.filter(pk=sys_news_id).exists():
        sys_news = SysNews.objects.get(pk=sys_news_id)
        sys_news.is_active = False
        sys_news.save()
        return getResult(True, u'客服取消发布新闻成功')
    else:
        return getResult(True, u'客服取消发布新闻失败')


def create_sys_column(request):
    """
    客服创建系统栏目
    by：尚宗凯 at：2015-06-11
    增加flag唯一校验
    by：尚宗凯 at：2015-06-17
    """
    sc = SysColumn()
    sc.name = request.REQUEST.get("name","")
    sc.index_num = request.REQUEST.get("index_num",0)
    sc.is_active = True
    sc.father_id = request.REQUEST.get("father_id","")
    if sc.father_id == "":
        sc.father_id = None
    sc.flag = request.REQUEST.get("flag",None)
    # if SysColumn.objects.filter(flag=sc.flag).exists():
    #     return getResult(False, u'flag已存在')
    sc.timeline = request.REQUEST.get("timeline",0)
    try:
        sc.save()
        return getResult(True, u'客服创建系统栏目成功')
    except:
        return getResult(True, u'客服创建系统栏目失败')


def set_sys_banner(request):
    """
    设置系统首页banner
    by：尚宗凯 at：2015-06-11
    完善接口
    by：尚宗凯 at：2015-06-12
    """
    image = request.REQUEST.get("image","")
    url = request.REQUEST.get("url","")
    index_num = request.REQUEST.get("index_num","")
    is_active = request.REQUEST.get("is_active","")
    sys_banner_id = request.REQUEST.get("sys_banner_id","")
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
            return getResult(True, u'设置系统首页banner成功')
        else:
            return getResult(False, u'设置系统首页banner失败')
    else:
        return getResult(False, u'设置系统首页banner失败')



def set_company_banner(request):
    """
    设置公司首页banner
    by：尚宗凯 at：2015-06-11
    完善接口
    by：尚宗凯 at：2015-06-12
    """
    image = request.REQUEST.get("image","")
    url = request.REQUEST.get("url","")
    index_num = request.REQUEST.get("index_num","")
    is_active = request.REQUEST.get("is_active","")
    company_banner_id = request.REQUEST.get("company_banner_id","")
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
            return getResult(True, u'设置公司首页banner成功')
        else:
            return getResult(False, u'设置公司首页banner失败')
    else:
        return getResult(False, u'设置公司首页banner失败')

@login_company_admin_required
def create_zhgl_company_news(request, company_id):
    """
    创建综合管理新闻
    by：尚宗凯 at：2015-06-27
    增加title设置
    by：尚宗凯 at：2015-06-27
    优化内容保存
    by:王健 at:2015-06-27
    创建后马上设置为已发布状态
    by：尚宗凯 at：2015-07-01
    """
    type_flag = request.REQUEST.get("type_flag","")
    flag = request.REQUEST.get("flag","")
    if not flag:
        return getResult(False, u'flag不能不传')
    try:
        company_column_id = CompanyColumn.objects.get(company_id=company_id, flag=flag).pk
    except Exception:
        return getResult(False, u'公司栏目不存在')
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = CompanyNews.objects.get(pk=pk)
    else:
        sn = CompanyNews()
    sn.company_id = company_id
    sn.company_column_id = company_column_id
    sn.author_id = request.user.pk
    sn.pre_title = request.REQUEST.get("pre_title","")
    if type_flag not in ("files", "images"):

        sn.pre_content = request.REQUEST.get("pre_content","")
        # sn.is_active = False
    else:
        fileids = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
        for fid in fileids:
            sn.append_file(fid)
    sn.title = sn.pre_title
    sn.content = sn.pre_content
    sn.is_active = True
    if type_flag:
        sn.type_flag = type_flag
    try:
        sn.save()
        return getResult(True, u'创建公司新闻成功', sn.toJSON())
    except Exception as e:
        return getResult(False, u'创建公司新闻失败')


def create_company_news(request, company_id=None):
    """
    创建公司新闻
    by：尚宗凯 at：2015-06-11
    优化代码
    by：尚宗凯 at:2015-06-22
    优化新建公司新闻接口
    by：尚宗凯 at：2015-06-23
    优化新闻创建的返回值
    by:王健 at:2015-06-24
    优化接口，兼容综合管理上传数据
    by：尚宗凯 at：2015-06-27
    修复不能修改bug
    by：尚宗凯 at：2015-07-01
    修改后发布状态变为未发布
    by：尚宗凯 at：2015-07-01
    """
    # type_flag = request.REQUEST.get("type_flag","")
    # assert type_flag in ("news", "files", "images", "")
    pk = request.REQUEST.get('id', None)
    if pk:
        sn = CompanyNews.objects.get(pk=pk)
        sn.is_active = False
    else:
        sn = CompanyNews()
    # if type_flag not in ("files", "images"):
        sn.company_id = company_id
    sn.company_column_id = request.REQUEST.get("com_column_id","")
    sn.pre_title = request.REQUEST.get("pre_title","")
    sn.pre_content = request.REQUEST.get("pre_content","")
    sn.author_id = request.user.pk
    sn.is_active = False
    sn.create_time = timezone.now()
    try:
        sn.save()
        return getResult(True, u'创建公司新闻成功', sn.toJSON())
    except Exception as e:
        return getResult(False, u'创建公司新闻失败')


def set_company_admin(request, company_id=None):
    """
    设置公司管理员
    by：尚宗凯 at：2015-06-11
    完善接口
    by：尚宗凯 at：2015-06-12
    再完善接口
    by：尚宗凯 at：2015-06-19
    增加批量修改
    by:尚宗凯 at：2015-06-26
    """
    # user_id = request.REQUEST.get("user_id","")
    ids = request.REQUEST.getlist('id')
    do = request.REQUEST.get("do","")
    if not do:
        return getResult(False, u'参数错误, do不能为空')

    for user_id in ids:
        if user_id and company_id:
            if CompanyPerson.objects.filter(company_id=company_id, user_id=user_id).exists():
                cp = CompanyPerson.objects.get(company_id=company_id, user_id=user_id)
                if do == "manager":
                    # if cp.creator_type == 1:
                    #     return getResult(False, u'已经是管理员了')
                    # else:
                        cp.creator_type = 1
                elif do == "user":
                    # if cp.creator_type == 0:
                    #     return getResult(False, u'已经不是管理员了')
                    # else:
                        cp.creator_type = 0
                cp.save()
            # return getResult(True, u'设置公司管理员成功')
        # else:
        #     return getResult(False, u'参数错误')
    return getResult(True, '设置成功')


def get_company_news_index_by_flag(request, company_id=None):
    """
    返回html页面
    by：尚宗凯 at：2015-06-17
    优化接口
    by：尚宗凯 at：2015-06-17
    更改html位置
    by:王健 at:2015-06-19
    """
    result = CompanyColumn.objects.filter(company_id=company_id)
    return render_to_response('cp_manage/phone/company_column_index.html', {"data": result})


def get_contact_us_html(request, company_id=None):
    """
    联系我们html
    by:尚宗凯 at：2015-06-19
    修改html
    by：尚宗凯 at：2015-06-24
    修改联系我们html
    by:王健 at:2015-06-25
    """
    # company_id = 1
    result = Company.objects.get(pk=company_id)
    return render_to_response('cp_manage/phone/qiye_contact_us.html', RequestContext(request, {"data": result.toJSON()}))

# class ContactUs(BaseView):
#     """
#     联系我们html
#     by:尚宗凯 at：2015-06-19
#     """
#     view_id = 'contact_us'
#     template_name = 'cp_manage/phone/qiye_contact_us.html'
#     # title = u'天津依子轩科技有限公司'
#
#     def get_context_data(self, **kwargs):
#         # kwargs['products'] = Product.objects.filter(is_active=True).order_by('sorted')
#         return super(ContactUs, self).get_context_data(**kwargs)


def update_company(request):
    """
    修改公司
    by：尚宗凯 at：2015-06-18
    修改公司信息，提供参数的可修改
    by:王健 at:2015-06-22
    """
    id = request.REQUEST.get("id","")
    name = request.REQUEST.get("name","")
    address = request.REQUEST.get("address","")
    phone = request.REQUEST.get("phone","")
    logo = request.REQUEST.get("logo","")
    top_logo = request.REQUEST.get("top_logo","")
    c = Company.objects.get(pk=id)
    if name:
        c.name = name
    if address:
        c.address = address
    if phone:
        c.phone = phone
    if logo:
        c.logo = int(logo)
    if top_logo:
        c.top_logo = int(top_logo)
    c.save()
    return getResult(True, u'修改公司成功', c.toJSON())


def update_company_column_image(request, company_id):
    """
    修改栏目image
    by：尚宗凯 at：2015-06-18
    兼容有重复栏目的情况
    by：尚宗凯 at：2015-06-25
    """
    image = request.REQUEST.get("image","")
    flag = request.REQUEST.get("flag","")
    if not flag:
        return getResult(False, u'参数错误')
    if not CompanyColumn.objects.filter(company_id=company_id,flag=flag).exists():
        return getResult(False, u'错误无法获取公司栏目')
    cc = CompanyColumn.objects.filter(company_id=company_id, flag=flag)
    for i in cc:
        i.image = image
        i.save()
    return getResult(True, u'成功修改公司栏目image', cc[0].toJSON())


def update_sys_column(request):
    """
    修改公司栏目
    by：尚宗凯 at：2015-06-19
    修复一个bug
    by：尚宗凯 at：2015-06-25
    """
    sys_column_id = request.REQUEST.get("sys_column_id","")
    name = request.REQUEST.get("name","")
    index_num = request.REQUEST.get("index_num","")
    is_active = request.REQUEST.get("is_active","")
    flag = request.REQUEST.get("flag","")
    if sys_column_id:
        if SysColumn.objects.filter(pk=sys_column_id).exists():
            sc = SysColumn.objects.get(pk=sys_column_id)
            if name:
                sc.name = name
            if index_num:
                sc.index_num = index_num
            if is_active == "False":
                sc.is_active = False
            if is_active == "True":
                sc.is_active = True
                sc.flag = flag
                sc.timeline = int(time.time())
            sc.save()
            return getResult(True, u'修改系统栏目成功')
    else:
        return getResult(False, u'修改公司栏目失败')


def update_company_column(request):
    """
    修改公司栏目
    by：尚宗凯 at：2015-06-11
    完善接口
    by：尚宗凯 at：2015-06-12
    完善接口，不让这是父节点
    by：尚宗凯 at：2015-06-19
    优化接口，不让修改系统默认的flag
    by：尚宗凯 at:2015-06-19
    """
    company_id = request.REQUEST.get("company_id","")
    name = request.REQUEST.get("name","")
    columntype = request.REQUEST.get("columntype","")
    index_num = request.REQUEST.get("index_num","")
    is_active = request.REQUEST.get("is_active","")
    # father_id = request.REQUEST.get("father_id","")
    flag = request.REQUEST.get("flag","")
    company_column_id = request.REQUEST.get("company_column_id","")

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
            # if father_id:
            #     cc.father_id = father_id
            if flag and flag not in settings.DEFAULT_COMPANY_COLUMN:
                cc.flag = flag
            cc.timeline = timezone.now()
            cc.save()
            return getResult(True, u'修改公司栏目成功')
        else:
            return getResult(False, u'修改公司栏目失败')


class AppView(FrameView):
    '''
    后台app视图
    by:尚宗凯 at:2015-06-14
    '''
    template_name = 'cp_manage/app.html'
    title = u'Company'

def logout(request):
    '''
    退出登录
    by:范俊伟 at:2015-01-21
    修改退出后的网址
    by：尚宗凯 at：2015-06-22
    '''
    auth_logout(request)
    return http.HttpResponseRedirect(request.REQUEST.get('next', '/cp/manage'))



def get_user_by_company_id(request, company_id):
    """
    根据公司id查询公司下用户
    by：尚宗凯 at：2015-06-19
    修改一下接口，增加是否是管理员
    by：尚宗凯 at：2015-06-19
    优化公司成员查询
    by:王健 at:2015-6-19
    """
    key = request.REQUEST.get("key","")
    query = [{"id": x[0], "name": x[1], "tel": x[2], "creator_type":x[3]} for x in CompanyPerson.objects.filter(company_id=company_id,is_active=True).filter(Q(user__tel__icontains=key) | Q(user__name__icontains=key)).values_list("user_id","user__name","user__tel","creator_type")]
    return getResult(True, '成功', query)


# @login_company_customer_service_required
def query_user_name(request):
    """
    获取用户姓名
    by：尚宗凯 at：2015-06-19
    修改接口返回值
    by：尚宗凯 at：2015-06-19
    增加分页
    by：尚宗凯 at：2015-06-19
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    key = request.REQUEST.get("key","")
    # res = []
    if key:
        result = NSUser.objects.filter(Q(name__icontains=key)|Q(tel__icontains=key)).values('name',"id")
    else:
        result = NSUser.objects.all().values("name","id")
    result = list(result)[page_start:page_start+20]
    return getResult(True, '成功', result)


# @ns_manage_login_required
@login_company_customer_service_required
def delete_sys_banner(request):
    """
    删除系统banner接口
    by：尚宗凯 at：2015-06-16
    :param request:
    :return:
    """
    ids = request.REQUEST.getlist('id')
    if not ids:
        return getResult(False, '未选择banner')
    for id in ids:
        try:
            bc = SysBanner.objects.get(pk=id)
            bc.delete()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


@login_company_admin_required
def delete_company_banner(request, company_id=None):
    """
    删除公司banner
    by：尚宗凯 at：2015-06-23
    """
    ids = request.REQUEST.getlist('id')
    if not ids:
        return getResult(False, '未选择banner')
    for id in ids:
        try:
            bc = CompanyBanner.objects.get(pk=id)
            bc.delete()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


@login_company_admin_required
def set_company_banner_is_active(request, company_id=None):
    """
    设置公司banner生效
    by：尚宗凯 at：2015-06-23
    """
    ids = request.REQUEST.getlist('id')
    is_active = request.REQUEST.get('is_active')
    if is_active is None:
        return getResult(False, '未提供发布状态')
    elif is_active == 'false':
        is_active = False
    elif is_active == 'true':
        is_active = True
    if not ids:
        return getResult(False, '未选择banner')
    for id in ids:
        try:
            bc = CompanyBanner.objects.get(pk=id)
            bc.is_active = is_active
            bc.save()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


@ns_manage_login_required
def set_sys_banner_is_active(request):
    """
    设置系统banner生效
    by：尚宗凯 at：2015-06-16
    :param request:
    :return:
    """
    ids = request.REQUEST.getlist('id')
    is_active = request.REQUEST.get('is_active')
    if is_active is None:
        return getResult(False, '未提供发布状态')
    elif is_active == 'false':
        is_active = False
    elif is_active == 'true':
        is_active = True
    if not ids:
        return getResult(False, '未选择banner')
    for id in ids:
        try:
            bc = SysBanner.objects.get(pk=id)
            bc.is_active = is_active
            bc.save()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


def set_sys_column_is_active(request):
    """
    设置系统栏目状态
    by：尚宗凯 at：2015-06-17
    """
    ids = request.REQUEST.getlist('id')
    is_active = request.REQUEST.get('is_active')
    if is_active is None:
        return getResult(False, '未提供发布状态')
    elif is_active == 'false':
        is_active = False
    elif is_active == 'true':
        is_active = True
    if not ids:
        return getResult(False, '未选择栏目')
    for id in ids:
        try:
            bc = SysColumn.objects.get(pk=id)
            bc.is_active = is_active
            bc.save()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


# @ns_manage_login_required
def set_company_news_is_active(request):
    """
    批量设置公司新闻发布状态
    by：尚宗凯 at：2015-06-19
    去除权限校验
    by：尚宗凯 at：2015-06-19
    优化设置新闻发布的接口
    by:王健 at:2015-06-27
    优化新闻发布，解决发布不了的bug
    by:王健 at:2015-06-27
    """
    ids = request.REQUEST.getlist('id')
    is_active = request.REQUEST.get('is_active', '').lower()
    if is_active is None:
        return getResult(False, '未提供发布状态')
    elif is_active == 'false':
        is_active = False
    elif is_active == 'true':
        is_active = True
    if not ids:
        return getResult(False, '未选择新闻')
    successids = []
    for bc in CompanyNews.objects.filter(pk__in=ids):
        bc.is_active = is_active
        if is_active:
            bc.publish_time = timezone.now()
            bc.title = bc.pre_title
            bc.content = bc.pre_content
        else:
            bc.publish_time = None
        bc.save(update_fields=['is_active', 'publish_time', 'title', 'content'])
        successids.append(bc.pk)

    return getResult(True, '设置成功', successids)


@ns_manage_login_required
def set_sys_news_is_active(request):
    """
    设置系统新闻发布状态
    by：尚宗凯 at:2015-06-16
    优化语法，优化设置发布逻辑
    by：尚宗凯 at：2015-06-16
    """
    ids = request.REQUEST.getlist('id')
    is_active = request.REQUEST.get('is_active')
    if is_active is None:
        return getResult(False, '未提供发布状态')
    elif is_active == 'false':
        is_active = False
    elif is_active == 'true':
        is_active = True
    if not ids:
        return getResult(False, '未选择新闻')
    for id in ids:
        try:
            bc = SysNews.objects.get(pk=id)
            bc.is_active = is_active
            if is_active:
                bc.publish_time = timezone.now()
                bc.title = bc.pre_title
                bc.content = bc.pre_content
            else:
                bc.publish_time = None
            bc.save()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


@ns_manage_login_required
def set_big_company_display(request):
    """
    设置集团是否默认展示
    by：尚宗凯 at:2015-06-15
    修改设置失败
    by：尚宗凯 at：2015-06-16
    """
    ids = request.REQUEST.getlist('id')
    is_display = request.REQUEST.get('is_display')
    if is_display == None:
        return getResult(False, '未提供用户类型')
    elif is_display == 'false':
        is_display = False
    elif is_display == 'true':
        is_display = True
    if not ids:
        return getResult(False, '未选择集团')
    for id in ids:
        try:
            bc = BigCompany.objects.get(pk=id)
            bc.is_display = is_display
            bc.save()
        except Exception as e:
            return getResult(True, '设置失败')
    return getResult(True, '设置成功')


@ns_manage_login_required
def query_big_company(request):
    """
    查找集团
    by：尚宗凯 at:2015-06-15
    增加分页
    by：尚宗凯 at：2015-06-18
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    keyword = request.REQUEST.get('keyword', "")
    query = BigCompany.objects.filter(Q(name__icontains=keyword)).order_by('-id')
    result = []
    for i in query[page_start:page_start+20]:
        result.append(i.toJSON())
    return getResult(True, '', result)

@ns_manage_login_required
def get_all_company(request):
    """
    获取所有公司
    by：尚宗凯 at：2015-06-16
    增加获取公司管理员
    by：尚宗凯 at：2015-06-18
    增加分页显示
    by：尚宗凯 at：2015-06-18
    增加status筛选
    by：尚宗凯 at：2015-06-23
    修复公司管理员显示bug
    by：尚宗凯 at：2015-07-01
    修改查询，creator_type=1为公司管理员
    by: 范俊伟 at:2015-07-02
    """
    page_start = int(request.REQUEST.get('page_start', 0))
    keyword = request.REQUEST.get('keyword', "")
    if keyword != "":
        query = Company.objects.filter(Q(name__icontains=keyword)).filter(Q(status="1") | Q(status="0")).order_by('-id')
    else:
        query = Company.objects.all().filter(Q(status="1") | Q(status="0")).order_by('-id')
    result = []
    for i in query[page_start:page_start+20]:
        manage = ""
        try:
            cp = CompanyPerson.objects.filter(company_id=i.pk, creator_type=1)[0]
            # if int(cp.creator_type) == 1:
            manage = cp.user.name
        except Exception as e:
            pass
        res = i.toJSON()
        res["manager"] = manage
        result.append(res)
    return getResult(True, '', result)


# @ns_manage_login_required
def query_sys_news(request):
    """
    
    查找系统新闻
    by：尚宗凯 at：2015-06-16
    调整参数支持分页加载
    by:王健 at:2015-06-17
    增加根据sys_column_id筛选
    by：尚宗凯 at：2015-06-25
    最多显示5条
    by：尚宗凯 at：2015-06-25
    去掉5条限制
    by：尚宗凯 at：2015-06-26
    """
    keyword = request.REQUEST.get('keyword', "")
    sys_column_id = request.REQUEST.get("sys_column_id","")
    page_start = int(request.REQUEST.get('page_start', 0))
    if keyword != "":
        query = SysNews.objects.filter(Q(pre_title__icontains=keyword)|Q(title__icontains=keyword)|Q(pre_content__icontains=keyword)|Q(content__icontains=keyword)).order_by('-id')
    else:
        query = SysNews.objects.all().order_by('-id')
    if sys_column_id:
        query = query.filter(sys_column_id=sys_column_id)
    result = []
    for i in query[page_start:page_start+20]:
        result.append(i.toJSON())
    return getResult(True, '', result)


@ns_manage_login_required
def change_password(request):
    """
    修改密码
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    old_password = request.REQUEST.get('old_password')
    new_password = request.REQUEST.get('new_password')

    user = request.user
    if not user.check_password(old_password):
        return getResult(False, '原始密码错误')
    user.set_password(new_password)
    user.save()
    return getResult(True, '修改成功')


@ns_manage_login_required
def query_user(request):
    """
    查询用户
    by: 范俊伟 at:2015-06-12
    增加查询方式
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    keyword = request.REQUEST.get('keyword', "")
    user_type = request.REQUEST.get('user_type', "")
    query = get_user_model().objects.filter(Q(tel__icontains=keyword) | Q(name__icontains=keyword)).filter(
        is_staff=False)
    if user_type != "":
        query = query.filter(backuserinfo__user_type=user_type)

    result = []
    for i in query:
        res = i.toJSON()
        if i.icon_url:
            res['icon_url'] = i.icon_url.get_url('imageView2/5/w/80/h/80')
        else:
            res['icon_url'] = None

        if hasattr(i, 'backuserinfo'):
            backuserinfo = i.backuserinfo.toJSON()
            backuserinfo.update(res)
            res = backuserinfo

        result.append(res)

    return getResult(True, '', result)


@ns_manage_login_required
def query_all_big_company(request):
    """
    查询集团
    by：尚宗凯 at：2015-06-15
    """
    keyword = request.REQUEST.get('keyword', "")
    user_type = request.REQUEST.get('user_type', "")
    # query = get_user_model().objects.filter(Q(tel__icontains=keyword) | Q(name__icontains=keyword)).filter(
    #     is_staff=False)
    # if user_type != "":
    #     query = query.filter(backuserinfo__user_type=user_type)

    # result = []
    # for i in query:
    #     res = i.toJSON()
    #     if i.icon_url:
    #         res['icon_url'] = i.icon_url.get_url('imageView2/5/w/80/h/80')
    #     else:
    #         res['icon_url'] = None
    #
    #     if hasattr(i, 'backuserinfo'):
    #         backuserinfo = i.backuserinfo.toJSON()
    #         backuserinfo.update(res)
    #         res = backuserinfo
    #
    #     result.append(res)
    #
    # return getResult(True, '', result)

    result = []
    query = BigCompany.objects.filter(Q(tel__icontains=keyword))
    for i in query:
        res = i.toJSON()
        result.append(res)
    return getResult(True, '', result)


@ns_manage_admin_login_required
def set_user_type(request):
    """
    设置用户类型
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    ids = request.REQUEST.getlist('id')
    user_type = request.REQUEST.get('user_type')
    if user_type == None:
        return getResult(False, '未提供用户类型')
    if not ids:
        return getResult(False, '未选择用户')
    for id in ids:
        try:
            user = get_user_model().objects.get(id=id)
            if hasattr(user, 'backuserinfo'):
                backuserinfo = user.backuserinfo
            else:
                backuserinfo = BackUserInfo()
                backuserinfo.need_user = user
            backuserinfo.user_type = user_type
            backuserinfo.save()
        except get_user_model().DoesNotExist:
            pass

    return getResult(True, '设置成功')


def query_company_by_name(request):
    """
    通过关键词搜索公司名称
    by:尚宗凯 at：2015-06-17
    :param request:
    :return:
    """
    key = request.REQUEST.get("key","")
    start = int(request.REQUEST.get('start', '0'))
    if key:
        l = Company.objects.filter(Q(name__icontains=key))
    else:
        l = Company.objects.all()
    l = l.order_by('-create_time')[start:start + 20]
    l = MyEncoder.default(l)
    return getResult(True, u"success", l)


def query_company_by_bigcompnay(request):
    """
    通过集团id获取集团的公司
    by:尚宗凯 at：2015-06-17
    """
    bigcompany_id = request.REQUEST.get("bigcompany_id","")
    if not bigcompany_id:
        c = Company.objects.all()
    else:
        c = Company.objects.filter(bigcompany_id=bigcompany_id)
    c = MyEncoder.default(c)
    return getResult(True, u"success", c)


def query_company_pv(request, company_id=None):
    """
    返回公司pv
    by：尚宗凯 at：2015-06-17
    优化公司pv接口
    by：尚宗凯 at：2015-06-22.
    修复pv接口bug
    by：尚宗凯 at：2015-06-22
    修复接口bug
    by:王健 at:2015-06-30
    """
    if company_id:
        result = query_count_company_page_view(company_id)
        create_company_page_view(company_id, request.user.pk)
        if result is None or (isinstance(result, dict) and result.has_key("code")):
            return getResult(True, u"success", {"pv": 0})
        else:
            return getResult(True, u"success", {"pv": result['count']})

    else:
        return getResult(False, u"Fail")


@login_company_admin_required
def set_company_status(request, company_id):
    """
    设置公司状态
    by：尚宗凯 at：2015-06-23
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    status = request.REQUEST.get('status',"")
    if company_id and status:
        if Company.objects.filter(pk=company_id).exists():
            c = Company.objects.get(pk=company_id)
            c.status = int(status)
            c.save()
            return getResult(True, u'成功')
    else:
        return getResult(False, u'参数错误')


@login_company_admin_required
def get_company_detail_by_id(request, company_id):
    """
    # 通过公司id获取公司信息
    # by：尚宗凯 at：2015-06-23
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    if Company.objects.filter(pk=company_id).exists():
        c = Company.objects.get(pk=company_id)
        return getResult(True, u"success", c.toJSON())
    else:
        return getResult(False, u'公司不存在')


@login_company_admin_required
def delete_company_user(request, company_id):
    """
    删除公司成员
    by：尚宗凯 at：2015-06-24
    增加权限校验
    by：尚宗凯 at：2015-06-30
    修复接口bug
    by：尚宗凯 at：2015-07-03
    """
    user_id = request.REQUEST.get("user_id","")
    if not user_id:
        return getResult(False, u'参数错误')

    if CompanyPerson.objects.filter(user_id=user_id, company_id=company_id).exists():
        cp = CompanyPerson.objects.filter(user_id=user_id, company_id=company_id)[0]
        if cp.creator_type == 1:
            return getResult(False, u'不能删除管理员')
        else:
            cp.delete()
            return getResult(True, u"success")
    else:
        return getResult(False, u'用户不存在')


@login_company_admin_required
def get_permission(request, company_id):
    """
    获取当前用户作为管理员的公司的权限
    by:尚宗凯 at：2015-06-25
    修改权限传参数
    by：尚宗凯 at：2015-06-27
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    # if not CompanyPerson.objects.filter(user_id=request.user.pk, creator_type=1).exists():
    #     return getResult(False, u'非管理员不能操作')
    # company = CompanyPerson.objects.filter(user_id=request.user.pk, creator_type=1)[0].company
    p = Permission.objects.filter(company_id=company_id)
    result = []
    for i in p:
        result.append( str(CompanyColumn.objects.get(pk=i.column_id).flag)+"*"+str(i.group_flag)+"*"+str(i.perm) )
    return getResult(True, u"success", result)


@login_company_admin_required
def update_permission(request, company_id):
    """
    更改权限
    by：尚宗凯 at：2015-06-25
    权限设置
    by：尚宗凯 at：2015-06-27
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    power = request.REQUEST.getlist("power")
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
        result.append( str(CompanyColumn.objects.get(pk=i.column_id).flag)+"*"+str(i.group_flag)+"*"+str(i.perm) )
    return getResult(True, u"success", result)


def query_permission(request, company_id):
    """
    获取用户权限
    by：尚宗凯 at：2015-06-25
    完善权限接口
    by：尚宗凯 at：2015-07-01
    修改权限判断逻辑
    by：尚宗凯 at：2015-07-01
    """
    user_id = request.user.pk
    # if user_id is None:
    #     return getResult(False, u"未登录，请先登录")
    # if Project.objects.filter(company_id=company_id).exists():
    #     company_project_id_list = [i.pk for i in Project.objects.filter(company_id=company_id)]
    #     user_group_type_list = [i.type for i in Group.objects.filter(project_id__in=company_project_id_list, user_id=user_id)]
    #     user_group_type_list = list(set(user_group_type_list))
    #     if Permission.objects.filter(company_id=company_id, group_flag__in=user_group_type_list, perm__in=(1,2)).exists():
    #         zhgl = True
    #     else:
    #         zhgl = False
    if CompanyPerson.objects.filter(company_id=company_id, user_id=user_id).exists():
        zhgl = True
    else:
        zhgl = False
    if Person.objects.filter(user_id=user_id, is_active=True).exists():
        gcxmgl = True
    else:
        gcxmgl = False
    return getResult(True, u"success", {"zhgl":zhgl, "gcxmgl":gcxmgl})


@login_company_admin_required
def get_child_comapny_column_list(request, company_id=None):
    """
    根据flag查询子集栏目
    by:王健 at:2015-6-26
    增加权限校验
    by：尚宗凯 at：2015-06-30
    :return:
    """
    flag = request.REQUEST.get('flag', '')
    columns = [x.toJSON() for x in CompanyColumn.objects.filter(company_id=company_id, father__flag=flag, is_active=True).order_by('index_num')]
    return getResult(True, u"", columns)


def get_qiyezixun_news(request, company_id=None):
    """
    查询企业资讯下的新闻
    by:王健 at:2015-6-26
    :param request:
    :return:
    """
    key = request.REQUEST.get("key","")
    page_start = int(request.REQUEST.get('page_start', 0))
    is_active = request.REQUEST.get("is_active","")

    if company_id:
        news = CompanyNews.objects.filter(company_id=company_id)
        news = news.filter(company_column__flag='QIYEZIXUN')
        if key:
            news = news.filter(company_id=company_id).filter(Q(title__icontains=key) | Q(content__icontains=key)|Q(pre_title__icontains=key) | Q(pre_content__icontains=key))
            news = news.filter(company_column__flag='QIYEZIXUN')
        if is_active.lower() == "true":
            news = news.filter(is_active=True)
        elif is_active.lower() == 'false':
            news = news.filter(is_active=False)
        result = []
        news = news.order_by("-id")
        for i in news[page_start:page_start+20]:
            result.append(i.toJSON())
        return getResult(True, u'获取公司企业动态信息成功', result)
    else:
        return getResult(False, u'获取公司企业动态信息失败,参数错误')


@login_company_admin_required
def get_news_by_flag(request, company_id=None):
    """
    根据flag查询新闻
    by:王健 at:2015-6-26
    :param request:
    增加权限校验
    by：尚宗凯 at：2015-06-30
    :return:
    """
    key = request.REQUEST.get("key","")
    page_start = int(request.REQUEST.get('page_start', 0))
    is_active = request.REQUEST.get("is_active","")
    flag = request.REQUEST.get("flag","")

    if company_id:
        news = CompanyNews.objects.filter(company_id=company_id)
        news = news.filter(Q(company_column__flag=flag)|Q(company_column__father__flag=flag))
        if key:
            news = news.filter(company_id=company_id).filter(Q(title__icontains=key) | Q(content__icontains=key)|Q(pre_title__icontains=key) | Q(pre_content__icontains=key))
        if is_active.lower() == "true":
            news = news.filter(is_active=True)
        elif is_active.lower() == 'false':
            news = news.filter(is_active=False)
        result = []
        news = news.order_by("-id")
        for i in news[page_start:page_start+20]:
            result.append(i.toJSON())
        return getResult(True, u'获取公司企业动态信息成功', result)
    else:
        return getResult(False, u'获取公司企业动态信息失败,参数错误')


@login_company_admin_required
def company_info(request, company_id=None):
    """
    获取公司账户信息
    by:王健 at:2015-06-26
    先设置假数据
    by:王健 at:2015-06-26
    增加权限校验
    by：尚宗凯 at：2015-06-30
    修改项目成员总数
    by:王健 at:2015-07-02
    :param request:
    :return:
    """
    company = Company.objects.get(pk=company_id)
    company_infomation = {'price': 18650, 'person_num': Person.objects.filter(project__company__id=company.pk, is_active=True).count(), 'days': (18650 / 50) - (timezone.now() - company.create_time).days + 1, 'project_num': Project.objects.filter(company_id=company.pk).count()}
    return render_to_response('cp_manage/phone/company_info.html', RequestContext(request, {'company': company.toJSON(), 'company_info': company_infomation}))

@login_company_admin_required
def get_company_column_by_flag(request, company_id=None):
    """
    通过flag查询栏目id
    by:尚宗凯 at：2015-06-27
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    flag = request.REQUEST.get("flag","")
    if not flag:
        return getResult(False, u'参数错误')
    if not CompanyColumn.objects.filter(company_id=company_id, flag=flag):
        return getResult(False, u'栏目不存在')
    else:
        cc = CompanyColumn.objects.get(company_id=company_id, flag=flag)
        return getResult(True, u'获取公司企业动态信息成功', {"company_column_id":cc.pk})


@login_company_admin_required
def get_company_column_by_company(request, company_id=None):
    """
    通过公司id查询综合管理子节点的公司栏目id
    by:尚宗凯 at：2015-06-27
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    father_cc = CompanyColumn.objects.get(company_id=company_id, flag='ZONGHEGUANLI')
    cc = CompanyColumn.objects.filter(father_id=father_cc.pk)
    result = []
    for i in cc:
        result.append(i.toJSON())
    return getResult(True, u'success', result)


@login_company_admin_required
def delete_company_news(request):
    """
    删除公司新闻
    by:尚宗凯 at：2015-06-27
    删除多个新闻
    by：尚宗凯 at：2015-06-27
    参数修改为id
    by：尚宗凯 at：2015-06-29
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    news_id = request.REQUEST.getlist("id")
    for i in news_id:
        try:
            news = CompanyNews.objects.get(pk=i)
            news.delete()
        except Exception:
            return getResult(False, u'删除失败')
    return getResult(True, u'success')


@login_company_customer_service_required
def delete_sys_column(request):
    """
    删除系统栏目
    by：尚宗凯 at：2015-06-29
    增加权限校验
    by：尚宗凯 at：2015-06-30
    """
    sys_column_ids = request.REQUEST.getlist("id")
    for i in sys_column_ids:
        try:
            sc = SysColumn.objects.get(pk=i)
            sc.delete()
        except Exception:
            return getResult(False, u'删除失败')
    return getResult(True, u'success')


@login_company_admin_required
def query_company_project(request, company_id):
    """
    查找公司下面所有的项目
    by：尚宗凯 at：2015-06-30
    增加分页
    by：尚宗凯 at：2015-06-30
    """
    key = request.REQUEST.get("key","")
    page_start = int(request.REQUEST.get('page_start', 0))
    projects = Project.objects.filter(company_id=company_id).filter(Q(name__icontains=key) | Q(total_name__icontains=key))
    result = []
    for i in projects[page_start:page_start+20]:
        result.append(i.toJSON())
    return getResult(True, u'success', result)


@login_company_admin_required
def company_add_user_by_tel(request, company_id):
    """
    通过手机号加人到公司
    by：尚宗凯 at;2015-06-30
    优化存在判读
    by: 范俊伟 at:2015-06-30
    优化存在判读
    by: 范俊伟 at:2015-06-30
    """
    tel = request.REQUEST.get("tel","")
    tellist = []
    for c in str(tel).replace('+86', ''):
        try:
            int(c)
            tellist.append(c)
        except:
            return getResult(False, u'手机号有误')
    if len(tellist) == 11:
        tel = ''.join(tellist)
    else:
        return getResult(False, u'手机号错误')
    try:
        user = NSUser.objects.get(tel=tel)
        if CompanyPerson.objects.filter(user=user, company_id=company_id).exists():
           return getResult(False, u'用户已加入')
        else:
            cc = CompanyPerson()
            cc.user = user
            cc.company_id = company_id
            cc.is_active = True
            cc.creator_type = 0
            cc.create_time = timezone.now()
            cc.timeline = 0
            cc.save()
            return getResult(True, u'success')
    except NSUser.DoesNotExist:
        return getResult(False, u'用户不存在')


@login_company_admin_required
def close_project(request):
    """
    关闭项目
    by:尚宗凯 at：2015-06-30
    关闭项目发消息
    by：尚宗凯 at：2015-07-01
    """
    project_id = request.REQUEST.get("project_id","")
    if not project_id:
        return getResult(False, u'参数错误')
    if Project.objects.filter(id=project_id).exists():
        p = Project.objects.get(id=project_id)
        p.status = 2
        p.save()
        receiver_user_ids = [i.pk for i in p.group_set.filter(is_active=True)]
        NeedMessage.create_multiple_sys_message(receiver_user_ids, "title", SYS_MESSAGE['project_close'] % (p.total_name))
        p = MyEncoder.default(p)
        cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
        cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
        return getResult(True, u'成功关闭项目')
    else:
        return getResult(False, u'关闭项目失败')


@login_company_admin_required
def delete_project(request):
    """
    删除项目
    by:尚宗凯 at：2015-06-30
    删除项目发消息
    by：尚宗凯 at：2015-07-01
    """
    project_id = request.REQUEST.get("project_id","")
    if not project_id:
        return getResult(False, u'参数错误')
    if Project.objects.filter(id=project_id).exists():
        p = Project.objects.get(id=project_id)
        if p.status == 3:
            return getResult(False, u'项目已经是删除状态')
        elif p.status == 4:
            return getResult(False, u'项目已经处于删除公示期')
        elif p.status == 2:
            p.status = 5
            p.delete_project_time = datetime.datetime.now()
            p.save()
            receiver_user_ids = [i.pk for i in p.group_set.filter(is_active=True)]
            NeedMessage.create_multiple_sys_message(receiver_user_ids, "title", SYS_MESSAGE['project_delete'] % (p.total_name, DELETE_PROJECT_PUBLICITY_PERIOD))
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD)
        else:
            p.status = 4
            p.delete_project_time = datetime.datetime.now()
            p.save()
            receiver_user_ids = [i.pk for i in p.group_set.filter(is_active=True)]
            NeedMessage.create_multiple_sys_message(receiver_user_ids, "title", SYS_MESSAGE['project_delete'] % (p.total_name, DELETE_PROJECT_PUBLICITY_PERIOD))
            p = MyEncoder.default(p)
            cache.set(PROJECT_INFO % project_id, p, settings.CACHES_TIMEOUT)
            cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
            return getResult(True, u'项目公示期，%s日以后项目删除' % DELETE_PROJECT_PUBLICITY_PERIOD)
    else:
        return getResult(False, u'删除项目失败')


@login_company_admin_required
def cancel_delete_project(request):
    """
    # 取消删除项目
    # by:尚宗凯 at：2015-06-30
    """
    project_id = request.REQUEST.get("project_id","")
    if not project_id:
        return getResult(False, u'参数错误')
    if Project.objects.filter(id=project_id).exists():
        p = Project.objects.get(id=project_id)
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

