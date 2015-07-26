# coding=utf-8
# Date: 15/4/15
# Time: 16:38
# Email:fanjunwei003@163.com
from bson import Timestamp
from django.conf import settings
from django.shortcuts import render_to_response

import time

__author__ = u'范俊伟'
# 非阿里云环境这段代码无法通过
# by：尚宗凯 at：2015-04-16
# mongodb用户验证
# by: 范俊伟 at:2015-04-16
try:
    import pymongo

    LOGGING_MONGODB_CONFIG = settings.LOGGING_MONGODB_CONFIG

    conn = pymongo.Connection(LOGGING_MONGODB_CONFIG.get('host'), LOGGING_MONGODB_CONFIG.get('port'))
    db = conn[LOGGING_MONGODB_CONFIG.get('name')]
    if LOGGING_MONGODB_CONFIG.get('username') and LOGGING_MONGODB_CONFIG.get('password'):
        db.authenticate(LOGGING_MONGODB_CONFIG.get('username'), LOGGING_MONGODB_CONFIG.get('password'))
except:
    pass


def logging(request):
    """
    日志显示
    by: 范俊伟 at:2015-04-15
    日志正序排列
    by: 范俊伟 at:2015-04-16
    日志改为反序排列
    by:王健 at:2015-04-19
    :param request:
    :return:
    """
    begin_time = time.time() - 60 * 60 * 24 * 3
    ts = Timestamp(int(begin_time), 0)
    docs = db.logs.find({"timestamp": {"$gt": ts}}).sort("timestamp", pymongo.DESCENDING)
    res = []
    for i in docs:
        timestamp = i.get('timestamp')
        datetime = None
        if timestamp:
            datetime = timestamp.as_datetime()
        i.update({"datetime": datetime})
        res.append(i)
    return render_to_response('needserver/logging.html', {"list": res})


def logging_count(request):
    """
    显示日志统计
    by: 范俊伟 at:2015-05-06
    :param request:
    :return:
    """
    sort = request.REQUEST.get('sort', 'last_time')
    query = db['count_logs'].find({})
    if sort == 'last_time':
        query = query.sort("last_time", pymongo.DESCENDING)
    elif sort == 'first_time':
        query = query.sort("first_time", pymongo.DESCENDING)
    elif sort == 'count':
        query = query.sort("count", pymongo.DESCENDING)
    else:
        query = query.sort("last_time", pymongo.DESCENDING)
    return render_to_response('needserver/logging_count.html', {"list": query})