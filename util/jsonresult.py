#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
import collections
import logging
import json
from django import db

from django.core.serializers import deserialize, serialize
from django.db.models.query import QuerySet
from django.db import models
from django.http import HttpResponse
from util.basemodel import JSONBaseModel


__author__ = u'王健'

# 如果百度的缓存不可用，则用默认的缓存
# try:
#     from bae_memcache.cache import BaeMemcache
#     # cache = BaeMemcache(CACHE_ID, CACHE_ADDR, BAE_API_KEY, BAE_SECRET_KEY)
#     raise u'暂时没有使用百度缓存'
# except:
#     logging.error("bae cache error")
from django.core.cache import cache


def getErrorFormResult(form):
    msg = form.json_error()
    return getResult(False, msg, None)


def getCacheResult(cache_name):
    """
    返回缓存的数据
    by:王健 at:2015-1-3
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    :param cache_name:
    :return:
    """
    cache_result = cache.get(cache_name)
    if cache_result is not None:
        return HttpResponse(cache_result)
    else:
        return


def is_success_mongodb_result(result):
    """
    根据mongo的返回信息，判断本次是否成功
    by:王健 at:2015-1-3
    :param result:
    :return:
    """
    if hasattr(result, 'err') and result['err'] is not None:
        return False
    else:
        return True

def getResult(success, message, result=None, status_code=0, cachename=None, dialog=0, jifen=None):
    """
    0 正常返回 code
    1 登录过期，需要重新登录
    2 项目id错误
    3 需要提供用户名和密码
    4 error
    5 用户禁止使用
    6 用户离开了当前组织
    7 组织余额不足，需要充值后继续使用
    8 权限不足
    9 手机号校验

    dialog 客户端提示类型
    0： 红字 3秒 提示
    1：Alert 提示
    by:王健 at:2015-1-3
    返回值，加上content-type = json
    by:王健 at:2015-1-6
    优化返回结构的 status_code
    by:王健 at:2015-1-10
    增加手机号没有校验的提示
    by:王健 at:2015-1-15
    增加积分
    by:王健 at:2015-2-5
    """
    map = {'success': success, 'message': message, 'status_code': status_code, 'dialog':dialog}
    if result:
        map['result'] = result
    if not success and status_code == 0:
        map['status_code'] = 4
    if jifen and jifen[0]:
        map['jifen'] = jifen[1]
        map['jifen_msg'] = jifen[2]
    jsonstr = json.dumps(map)
    if cachename:
        cache.set(str(cachename), jsonstr, 3600 * 24)
    return HttpResponse(jsonstr, u'application/json')


def getTestResult(success, message, result=None, status_code=0, cachename=None, dialog=0, jifen=None):
    '''
    单元测试 使用
    by:王健 at:2015-1-3
    优化返回结构的 status_code
    by:王健 at:2015-1-10
    增加积分
    by:王健 at:2015-2-5
    '''
    map = {'success': success, 'message': message, 'status_code': status_code, 'dialog':dialog}
    if result:
        map['result'] = result
    if not success and status_code == 0:
        map['status_code'] = 4
    if jifen and jifen[0]:
        map['jifen'] = jifen[1]
        map['jifen_msg'] = jifen[2]
    return map


class MyEncoder():
    """
    继承自simplejson的编码基类，用于处理复杂类型的编码
    by:王健 at:2015-1-3
    对list类型的不做处理，view中还是主要以返回QuerySet为主
    by:王健 at:2015-1-7
    不再继承一个class了，直接用json模块
    by:王健 at:2015-1-13
    """


    @staticmethod
    def default(obj):
        """
        优化Model 序列化 功能
        by:王健 at:2015-1-29
        优化 序列化算法
        by:王健 at:2015-3-9
        :param obj:
        :return:
        """
        if not isinstance(obj, dict) and isinstance(obj, collections.Iterable):
            l = []
            for o in obj:
                if isinstance(o, JSONBaseModel):
                    l.append(o.toJSON())
                else:
                    l.append(o)
            return l
        if isinstance(obj, JSONBaseModel):
            return obj.toJSON()
        return obj
