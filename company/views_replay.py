# coding=utf-8
# Date:2015/01/13
# Email:wangjian2254@icloud.com
# from bson import ObjectId
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
from Need_Server.settings import CREATE_DATA
from company.models import SysNews, CompanyNews
from needserver import FILE_GROUP_FLAGS, FILE_GROUP_FLAGS_FILES, FILE_GROUP_FLAGS_BGIMAGES, FILE_GROUP_FLAGS_IMAGES
from needserver.jifenutil import create_data_jifen

from needserver.models import FileRecord,Reply, NSUser, EngineCheck
from util.cache_handle import query_project_filegroup_data_
from util.jsonresult import getResult, MyEncoder, is_success_mongodb_result
from util.loginrequired import client_login_project_required
from util.project_power_cache import whether_user_have_power_by_flag, all_flag_user_have_power_by_flag


__author__ = u'王健'
from util.apicloud import zan_news_by_id, del_zan_news_by_id, create_replay_by_news_id, query_replay_by_news_id, \
    query_replay_num_by_news_id, favorite_news_by_id, query_news_favorite_zan, del_favorite_news_by_id


def ding_news_by_id(request, company_id=''):
    """
    赞系统新闻
    by:王健 at:2015-06-18
    增加赞数量+1
    by：尚宗凯 at：2015-06-22
    修复栏目id错误的bug
    by:王健 at:2015-06-22
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = zan_news_by_id(request.user.id, company_id, news_id, news.company_column_id, int(time.time()), False)
            else:
                result = zan_news_by_id(request.user.id, company_id, news_id, news.sys_column_id, int(time.time()), True)
            news.add_zan_num()
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功对 %s 点了个赞。' % news.title, result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def delete_ding_news_by_id(request, company_id=''):
    """
    对一个记录发出顶的操作
    by:王健 at:2015-2-25
    删除点赞
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    解决enginecheck 没有title的bug
    by:王健 at:2015-06-01
    删除赞
    by:王健 at:2015-06-25
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = del_zan_news_by_id(request.user.id, news_id, False)
            else:
                result = del_zan_news_by_id(request.user.id, news_id, True)
            news.add_zan_num(-1)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功对 %s 取消了赞。' % news.title, result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def ding_favorite_by_id(request, company_id=''):
    """
    赞系统新闻
    by:王健 at:2015-06-18
    修复一个bug
    by：尚宗凯 at：2015-06-22
    修复栏目id错误的bug
    by:王健 at:2015-06-22
    修复dict 栏目id的bug
    by:王健 at:2015-06-23
    修复column_id
    by:王健 at:2015-06-25
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id).toJSON()
        else:
            news = SysNews.objects.get(pk=news_id).toJSON()
        if news:
            if company_id:
                result = favorite_news_by_id(request.user.id, company_id, news_id, news['company_column'], int(time.time()), False, news['title'], news['news_url'], news['icon_url'])
            else:
                result = favorite_news_by_id(request.user.id, company_id, news_id, news['sys_column'], int(time.time()), True, news['title'], news['news_url'], news['icon_url'])
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功收藏了新闻 %s 。' % news['title'], result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def delete_favorite_news_by_id(request, company_id=''):
    """
    对一个记录发出顶的操作
    by:王健 at:2015-2-25
    删除点赞
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    解决enginecheck 没有title的bug
    by:王健 at:2015-06-01
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = del_favorite_news_by_id(request.user.id, news_id, False)
            else:
                result = del_favorite_news_by_id(request.user.id, news_id, True)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功取消收藏 %s 。' % news.title, result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def replay_news_by_id(request, company_id=''):
    """
    对一条记录发出评论
    by:王健 at:2015-2-25
    去除 mongodb 影响
    by:王健 at:2015-3-8
    在某个节点下数据中发布评论
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    增加typeflag 字段
    by:王健 at:2015-06-03
    只取前一百评论内容
    by:王健 at:2015-06-04
    增加评论数量+1
    by：尚宗凯 at：2015-06-22
    修复bug
    by：尚宗凯 at：2015-06_22
    修复栏目id错误的bug
    by:王健 at:2015-06-22
    增加name参数
    by:王健 at:2015-06-24
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    获取昵称
    by:王健 at:2015-06-26
    """
    content = request.REQUEST.get('content', '')[:100]
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = create_replay_by_news_id(request.user.id, request.user.get_nickname(), company_id, news_id, news.company_column_id, int(time.time()), content, False)
            else:
                result = create_replay_by_news_id(request.user.id, request.user.get_nickname(), company_id, news_id, news.sys_column_id, int(time.time()), content, True)
            news.add_replay_num()
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功对 %s 发布了评论。' % news.title, result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def query_replay_news_by_id(request, company_id=''):
    """
    查询查询记录的评论信息
    by:王健 at:2015-2-25
    去除 mongodb 影响
    by:王健 at:2015-3-8
    获取某个节点数据下的所有评论
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    添加分页属性
    by:王健 at:2015-06-24
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    """
    news_id = request.REQUEST.get('id')
    start = int(request.REQUEST.get('start', 0))
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = query_replay_by_news_id(news_id, False, start)
            else:
                result = query_replay_by_news_id(news_id, True, start)

            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'获取评论成功。', result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def count_replay_by_news_id(request, company_id=''):
    """
    获取评论数量
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    :param request:
    :param company_id:
    :return:
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = query_replay_num_by_news_id(news_id, False)
            else:
                result = query_replay_num_by_news_id(news_id, True)

            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'获取评论数量成功。', result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


def query_favorite_zan_count_news_by_id(request, company_id=''):
    """
    查询新闻关注、赞、评论数量
    by:王健 at:2015-06-18
    查询用户是否赞过、收藏过和评论数量
    by:王健 at:2015-06-22
    增加company_id默认参数
    by：尚宗凯 at：2015-06-22
    适应性优化，公司id 从None改为''
    by:王健 at:2015-06-26
    :param request:
    :param company_id:
    :return:
    """
    news_id = request.REQUEST.get('id')
    if news_id:
        if company_id:
            news = CompanyNews.objects.get(pk=news_id)
        else:
            news = SysNews.objects.get(pk=news_id)
        if news:
            if company_id:
                result = query_news_favorite_zan(request.user.id, news_id, False)
            else:
                result = query_news_favorite_zan(request.user.id, news_id, True)

            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'获取评论数量成功。', result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')

