# coding=utf-8
import json
import logging
from django.conf import settings
import time
from needserver.models import Person
from django.utils import timezone

__author__ = 'wangjian'
import requests
import hashlib


API_HEADERS = {"X-APICloud-AppId": settings.APICLOUD_REPLAY_APP, "X-APICloud-AppKey": ''}


def get_appkey():
    """
    计算APICLOUD 的 appkey
    :return:
    """
    now = int(time.time()*1000)
    s = "%sUZ%sUZ%s" % (settings.APICLOUD_REPLAY_APP, settings.APICLOUD_REPLAY_AK, now)
    return '%s.%s' % (hashlib.sha1(s).hexdigest(), now)
    # s = "A6968565094002"+"UZ"+"62FB16B2-0ED6-B460-1F60-EB61954C823B"+"UZ"+now)+"."+now


def get_headers():
    """
    获取http请求头
    :return:
    """
    header = API_HEADERS.copy()
    header['X-APICloud-AppKey'] = get_appkey()
    return header


def get_api_url(url):
    """
    根据url 生成 接口url
    :param url:
    :return:
    """
    return '%s%s' % (settings.API_HOST_URL, url)


def get_result_json(result):
    """
    将str 转化为 json对象 返回
    :param result:
    :return:
    """
    try:
        if result.status_code == 200:
            r = json.loads(result.content)
        else:
            return None
    except:
        return None
    return r


def get(url, data):
    """
    get 提交
    捕获 错误异常
    by:王健 at:2015-06-03
    异常捕获 优化
    by:王健 at:2015-06-27
    :param url:
    :param data:
    :return:
    """
    try:
        return get_result_json(requests.get(get_api_url(url), json=data, headers=get_headers(), timeout=5))
    except Exception, e:
        log = logging.getLogger('django')
        log.error(str(e))
        return None


def post(url, data):
    """
    post 提交
    捕获 错误异常
    by:王健 at:2015-06-03
    异常捕获 优化
    by:王健 at:2015-06-27
    :param url:
    :param data:
    :return:
    """
    try:
        return get_result_json(requests.post(get_api_url(url), json=data, headers=get_headers(), timeout=5))
    except Exception, e:
        log = logging.getLogger('django')
        log.error(str(e))
        return None


def put(url, data):
    """
    put 提交
    捕获 错误异常
    by:王健 at:2015-06-03
    异常捕获 优化
    by:王健 at:2015-06-27
    :param url:
    :param data:
    :return:
    """
    try:
        return get_result_json(requests.put(get_api_url(url), json=data, headers=get_headers(), timeout=5))
    except Exception, e:
        log = logging.getLogger('django')
        log.error(str(e))
        return None


def delete(url, data=None):
    """
    get 提交
    捕获 错误异常
    by:王健 at:2015-06-03
    异常捕获 优化
    by:王健 at:2015-06-27
    :param url:
    :param data:
    :return:
    """
    try:
        return get_result_json(requests.delete(get_api_url(url), json=data, headers=get_headers(), timeout=5))
    except Exception, e:
        log = logging.getLogger('django')
        log.error(str(e))
        return None


def head(url, data):
    """
    get 提交
    捕获 错误异常
    by:王健 at:2015-06-03
    异常捕获 优化
    by:王健 at:2015-06-27
    :param url:
    :param data:
    :return:
    """
    try:
        return get_result_json(requests.head(get_api_url(url), json=data, headers=get_headers(), timeout=5))
    except Exception, e:
        log = logging.getLogger('django')
        log.error(str(e))
        return None


def has_replay(project_id, flag, filerecord_id, author):
    """
    根据参数获取所有的赞或者评论，判断单元测试是否成功
    获取最大值为1000
    by:王健 at:2015-06-02
    :param project_id:
    :param flag:
    :param filerecord_id:
    :param author:
    :return:
    """
    q = {
        "filter": {
            "where": {
                "project": project_id,
                "flag": flag,
                "filerecord": filerecord_id,
                "author": author,
                "is_zan": False
            },
            "skip": 0,
            "limit": 1000, "order": ["createdAt ASC"]
        }
    }
    result = get('/mcm/api/ReplayRecord', q)
    return result


def has_replay_or_zan(project_id, flag, filerecord_id):
    """
    根据参数获取所有的赞或者评论，判断单元测试是否成功
    获取最大值为1000
    by:王健 at:2015-06-02
    :param project_id:
    :param flag:
    :param filerecord_id:
    :return:
    """
    q = {
        "filter": {
            "where": {
                "project": project_id,
                "flag": flag,
                "filerecord": filerecord_id

            },
            "skip": 0,
            "limit": 1000, "order": ["createdAt ASC"]
        }
    }
    result = get('/mcm/api/ReplayRecord', q)
    return result


def has_replay_zan(project_id, flag, filerecord_id, author):
    """
    根据参数获取所有的赞或者评论，判断单元测试是否成功
    获取最大值为1000
    by:王健 at:2015-06-02
    :param project_id:
    :param flag:
    :param filerecord_id:
    :param author:
    :return:
    """
    q = {
        "filter": {
            "where": {
                "project": project_id,
                "flag": flag,
                "filerecord": filerecord_id,
                "author": author,
                "is_zan": True
            },
            "skip": 0,
            "limit": 1000
        }
    }
    result = get('/mcm/api/ReplayRecord', q)
    return result


def create_zan_by_filerecord(project_id, flag, filerecord_id, author, timeline, typeflag):
    """
    发出一条赞
    by:王健 at:2015-05-27
    添加create_time字段
    by:王健 at:2015-05-29
    获取最大值为1
    by:王健 at:2015-06-02
    :return:
    """
    q = {
        "filter": {
            "where": {
                "project": project_id,
                "flag": flag,
                "filerecord": filerecord_id,
                "author": author,
                "is_zan": True
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/ReplayRecord', q)
    if result is not None and isinstance(result, list):
        if len(result) == 0:
            result = post('/mcm/api/ReplayRecord',
                          {"project": project_id, 'flag': flag, 'filerecord': filerecord_id, 'author': author, 'is_zan': True, 'typeflag': typeflag,
                           'timeline': timeline, 'content': '', 'to_user': 0, 'create_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
        else:
            # result = delete('/mcm/api/ReplayRecord/%s' % result[0]['id'])
            result = result[0]

    return result


def create_replay_by_filerecord(project_id, flag, filerecord_id, author, timeline, content, typeflag, to_user=0):
    """
    发出一条赞
    by:王健 at:2015-05-27
    添加create_time字段
    by:王健 at:2015-05-29
    :return:
    """

    result = post('/mcm/api/ReplayRecord',
                  {"project": project_id, 'flag': flag, 'filerecord': filerecord_id, 'author': author, 'is_zan': False, 'typeflag': typeflag,
                   'timeline': timeline, 'content': content, 'to_user': to_user, 'create_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})

    return result


def delete_zan_by_filerecord(project_id, flag, filerecord_id, author):
    """
    取消赞
    by:王健 at:2015-05-27
    :param project_id:
    :param flag:
    :param filerecord_id:
    :param author:
    :param timeline:
    :return:
    """
    q = {
        "filter": {
            "fields": {
                "id": True
            },
            "where": {
                "project": project_id,
                "flag": flag,
                "filerecord": filerecord_id,
                "author": author,
                "is_zan": True
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/ReplayRecord', q)
    if result is not None:
        if len(result) > 0:
            result = delete('/mcm/api/ReplayRecord/%s' % result[0]['id'])

    return result


def query_replay_num_by_timeline(replay_timeline, user, project_id, all_have_power_flag):
    """
    根据数据信息，查询赞数量
    评论时间戳设置
    by:王健 at:2015-06-02
    日志记录查询参数
    by:王健 at:2015-06-02
    修复replay_timeline,只更新replay_timeline
    by:王健 at:2015-06-02
    :param project_id:
    :param flag:
    :param filerecord:
    :param timeline:
    :return:
    """

    if not replay_timeline:
        person = Person.objects.get(project_id=project_id, user_id=user)
        person.replay_timeline = int(time.time())
        person.save(update_fields=['replay_timeline'])
        timeline = person.replay_timeline
    else:
        timeline = replay_timeline
    q = {'filter': {"where": {"project": project_id, "timeline": {"gt": timeline}, "author": {"ne": user}, "flag": {"inq": all_have_power_flag}}}}
    if settings.ENVIRONMENT == 'baidu':
        log = logging.getLogger('django')
        log.error(json.dumps(q))
    return get('/mcm/api/ReplayRecord/count', q)


def get_last_replay_by_timeline(user, project_id, all_have_power_flag):
    """
    根据数据信息，查询赞数量
    修改排序字段
    by:王健 at:2015-06-02
    修改获取最后一个评论的bug
    by:王健 at:2015-06-02
    排除空数据的情况
    by:王健 at:2015-06-03
    :param project_id:
    :param flag:
    :param filerecord:
    :param timeline:
    :return:
    """

    q = {'filter': {"where": {"project": project_id, "author": {"ne": user}, "flag": {"inq": all_have_power_flag}}}, "skip": 0, "limit": 1, "order": ["createdAt DESC"]}
    result = get('/mcm/api/ReplayRecord', q)
    if isinstance(result, list) and len(result) > 0:
        return result[0]
    else:
        return None


def test_query_replay_by_timeline(replay_timeline, user, project_id, all_have_power_flag):
    """
    单元测试用，获取评论和赞列表
    by:王健 at:2015-05-28
    评论时间戳设置
    by:王健 at:2015-06-02
    修复replay_timeline,只更新replay_timeline
    by:王健 at:2015-06-02
    :return:
    """
    if not replay_timeline:
        person = Person.objects.get(project_id=project_id, user_id=user)
        person.replay_timeline = int(time.time())
        person.save(update_fields=['replay_timeline'])
        timeline = person.replay_timeline
    else:
        timeline = replay_timeline
    q = {'filter': {"where": {"project": project_id, "timeline": {"gt": timeline}, "author": {"ne": user}, "flag": {"inq": all_have_power_flag}}, "limit": 0, "order": ["createdAt DESC"]}}

    result = get('/mcm/api/ReplayRecord', q)
    return result

def query_replay_by_timeline(replay_timeline, user, project_id, all_have_power_flag):
    """
    根据timeline 获取评论列表
    评论时间戳设置
    by:王健 at:2015-06-02
    修复replay_timeline,只更新replay_timeline
    by:王健 at:2015-06-02
    修复查询不出的bug
    by:王健 at:2015-06-02
    :param replay_timeline:
    :param user:
    :param project_id:
    :return:
    """
    # result = get('/mcm/api/ReplayTimeline/%s' % replay_timeline, None)
    # if not result:
    #     timeline = int(time.time())
    #     result = post('/mcm/api/ReplayTimeline', {"project": project_id, "user": user, "timeline": timeline})
    #     if result:
    #         person = Person.objects.get(project_id=project_id, user_id=user)
    #         person.replay_timeline = result.get("id")
    #         person.save()
    #     return []
    # else:
    if not replay_timeline:
        person = Person.objects.get(project_id=project_id, user_id=user)
        person.replay_timeline = int(time.time())
        person.save(update_fields=['replay_timeline'])
        timeline = person.replay_timeline
    else:
        timeline = replay_timeline
    q = {'filter': {"where": {"project": project_id, "timeline": {"gt": timeline}, "author": {"ne": user}, "flag": {"inq": all_have_power_flag}}, "limit": 100, "order": ["createdAt DESC"]}}
    if settings.ENVIRONMENT == 'baidu':
        log = logging.getLogger('django')
        log.error(json.dumps(q))
    result = get('/mcm/api/ReplayRecord', q)
    if result is not None and len(result) > 0:
        person = Person.objects.get(project_id=project_id, user_id=user)
        person.replay_timeline = int(time.time())
        person.save(update_fields=['replay_timeline'])
    return result


def query_replay_by_filerecord_id(flag, filerecord_id, project_id):
    """
    根据数据，查询出所有评论
    默认查询1000条，省的分页
    by:王健 at:2015-06-01
    修改排序字段
    by:王健 at:2015-06-02
    :param flag:
    :param filerecord_id:
    :param project_id:
    :return:
    """

    q = {'filter': {"where": {"project": project_id, 'flag': flag, "filerecord": filerecord_id}, "limit": 1000, "order": ["createdAt ASC"]}}
    result = get('/mcm/api/ReplayRecord', q)
    return result


def zan_news_by_id(author, company_id, news_id, column_id, timeline, is_sys):
    """
    点赞
    :param author:
    :param company_id:
    :param news_id:
    :param column_id:
    :param is_sys:
    :return:
    """
    q = {
        "filter": {
            "where": {
                "company": company_id,
                "news": news_id,
                "column": column_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/ZanNews', q)
    if result is not None and isinstance(result, list):
        if len(result) == 0:
            result = post('/mcm/api/ZanNews',
                          {"company": company_id, 'news': news_id, 'column': column_id, 'author': author, 'is_sys': is_sys,
                           'timeline': timeline, 'create_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
        else:
            # result = delete('/mcm/api/ReplayRecord/%s' % result[0]['id'])
            result = result[0]

    return result


def del_zan_news_by_id(author, news_id, is_sys):
    """
    取消赞新闻
    :param author:
    :param news_id:
    :param is_sys:
    :return:
    """
    q = {
        "filter": {
            "fields": {
                "id": True
            },
            "where": {
                "news": news_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/ZanNews', q)
    if result is not None:
        if len(result) > 0:
            result = delete('/mcm/api/ZanNews/%s' % result[0]['id'])

    return result


def create_replay_by_news_id(author, nickname, company_id, news_id, column_id, timeline, content, is_sys):
    """
    创建评论
    by:王健 at:2015-06-18
    增加name属性
    by:王健 at:2015-06-24
    :param author:
    :param company_id:
    :param news_id:
    :param column_id:
    :param timeline:
    :param is_sys:
    :return:
    """
    result = post('/mcm/api/ReplayNews',
                  {"company": company_id, 'name': nickname, 'news': news_id, 'column': column_id, 'author': author, 'is_sys': is_sys,
                   'timeline': timeline, 'content': content, 'create_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})

    return result


def query_replay_by_news_id(news_id, is_sys, skip=0, limit=20):
    """
    根据新闻id查询评论列表
    添加分页属性
    by:王健 at:2015-06-24
    :param news_id:
    :param is_sys:
    :return:
    """

    q = {'filter': {"where": {"news": news_id, 'is_sys': is_sys}, "skip": skip, "limit": limit, "order": ["createdAt DESC"]}}
    result = get('/mcm/api/ReplayNews', q)
    return result


def query_replay_num_by_news_id(news_id, is_sys):
    """
    查询新闻评论数量
    :param news_id:
    :param is_sys:
    :return:
    """

    q = {'filter': {"where": {"news": news_id, 'is_sys': is_sys}}}
    return get('/mcm/api/ReplayNews/count', q)


def favorite_news_by_id(author, company_id, news_id, column_id, timeline, is_sys, title, url, icon_url):
    """
    点赞
    我的收藏，添加字段
    by:王健 at:2015-06-23
    :param author:
    :param company_id:
    :param news_id:
    :param column_id:
    :param is_sys:
    :return:
    """
    q = {
        "filter": {
            "where": {
                "news": news_id,
                "column": column_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/CollectNews', q)
    if result is not None and isinstance(result, list):
        if len(result) == 0:
            result = post('/mcm/api/CollectNews',
                          {'news': news_id, 'column': column_id, 'author': author, 'is_sys': is_sys, 'title': title, 'icon_url': icon_url,
                           'url': url, 'timeline': timeline, 'create_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')})
        else:
            # result = delete('/mcm/api/ReplayRecord/%s' % result[0]['id'])
            result = result[0]

    return result


def del_favorite_news_by_id(author, news_id, is_sys):
    """
    取消赞新闻
    :param author:
    :param news_id:
    :param is_sys:
    :return:
    """
    q = {
        "filter": {
            "fields": {
                "id": True
            },
            "where": {
                "news": news_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/CollectNews', q)
    if result is not None:
        if len(result) > 0:
            result = delete('/mcm/api/CollectNews/%s' % result[0]['id'])

    return result


def query_news_favorite_zan(author, news_id, is_sys):
    """
    根据新闻id查询用户是否赞过和收藏过
    :param author:
    :param news_id:
    :param is_sys:
    :return:
    """
    r = {'favorite': False, 'zan': False, 'count': 0}
    q = {
        "filter": {
            "fields": {
                "id": True
            },
            "where": {
                "news": news_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/CollectNews', q)
    if result is not None:
        if len(result) > 0:
            r['favorite'] = True
    q = {
        "filter": {
            "fields": {
                "id": True
            },
            "where": {
                "news": news_id,
                "author": author,
                "is_sys": is_sys
            },
            "skip": 0,
            "limit": 1
        }
    }
    result = get('/mcm/api/ZanNews', q)
    if result is not None:
        if len(result) > 0:
            r['zan'] = True

    q = {'filter': {"where": {"news": news_id, 'is_sys': is_sys}}}
    result = get('/mcm/api/ReplayNews/count', q)
    if result is None or (isinstance(result, dict) and result.has_key("code")):
        pass
    else:
        r['count'] = result.get('count', 0)
    return r


def create_company_page_view(company_id, user_id):
    """
    新增一条公司浏览记录
    by:尚宗凯 at:2015-06-22
    """
    result = post('/mcm/api/CompanyPageView',
                  {"company_id": company_id, 'user_id': user_id})
    return result

def create_news_page_view(is_sys_news, news_id, user_id):
    """
    新增一条公司浏览记录
    by:尚宗凯 at:2015-06-22
    """
    result = post('/mcm/api/NewsPageView',
                  {"is_sys_news":is_sys_news, "news_id": news_id, 'user_id': user_id})
    return result


def query_count_company_page_view(company_id):
    """
    查询公司浏览数量
    by：尚宗凯 at：2015-06-22
    """
    q = {'filter': {"where": {"company_id": company_id}}}
    return get('/mcm/api/CompanyPageView/count', q)


def query_count_news_page_view(is_sys_news, news_id):
    """
    查询新闻浏览数量
    by:尚宗凯 at：2015-06-22
    """
    q = {'filter': {"where": {"news_id": news_id, "is_sys_news":is_sys_news}}}
    return get('/mcm/api/NewsPageView/count', q)


def query_favorite_by_author(author):
    """
    根据用户查找我的收藏
    by:王健 at:2015-06-23
    设置排序
    by:王健 at:2015-06-30
    :param author:
    :return:
    """
    q = {
        "filter": {
            "fields": {
                "title": True,
                "icon_url": True,
                "create_time": True,
                "url": True
            },
            "where": {
                "author": author
            },
            "skip": 0,
            "limit": 1000,
            "order": ["createdAt DESC"]
        }
    }
    return get('/mcm/api/CollectNews', q)