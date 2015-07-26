# coding=utf-8
# Date: 15/1/19'
# Email: wangjian2254@icloud.com
import threading
from requests.auth import AuthBase
from easemob.models import HuanXin
from django.conf import settings

__author__ = u'王健'


import requests
import json
from time import time

JSON_HEADER = {'content-type': 'application/json'}
# EASEMOB_HOST = "http://localhost:8080"#
EASEMOB_HOST = "https://a1.easemob.com/%s/%s/" % (settings.HUANXIN_ORG, settings.HUANXIN_APP)

EASEMOB_HOST_USERS = '%susers' % EASEMOB_HOST
EASEMOB_HOST_GROUPS = '%schatgroups' % EASEMOB_HOST

DEBUG = False

def put(url, payload, auth=None):
    """
    put 方法访问
    by:王健 at:2015-2-27
    :param url:
    :param payload:
    :param auth:
    :return:
    """
    r = requests.put(url, data=json.dumps(payload), headers=JSON_HEADER, auth=auth)
    return http_result(r)


def post(url, payload, auth=None):
    """
    post 方法访问
    by:王健 at:2015-1-20
    :param url:
    :param payload:
    :param auth:
    :return:
    """
    r = requests.post(url, data=json.dumps(payload), headers=JSON_HEADER, auth=auth)
    return http_result(r)


def get(url, auth=None):
    """
    get 方法访问
    by:王健 at:2015-1-20
    :param url:
    :param auth:
    :return:
    """
    r = requests.get(url, headers=JSON_HEADER, auth=auth)
    return http_result(r)


def delete(url, auth=None):
    """
    delete 方法访问
    by:王健 at:2015-1-20
    :param url:
    :param auth:
    :return:
    """
    r = requests.delete(url, headers=JSON_HEADER, auth=auth)
    return http_result(r)


def http_result(r):
    """
    结果处理
    by:王健 at:2015-1-20
    记录错误日志
    by:王健 at:2015-3-12
    :param r:
    :return:
    """
    if DEBUG:
        error_log = {
                    "method": r.request.method,
                    "url": r.request.url,
                    "request_header": dict(r.request.headers),
                    "response_header": dict(r.headers),
                    "response": r.text
                }
        if r.request.body:
            error_log["payload"] = r.request.body
        print json.dumps(error_log)

    if r.status_code == requests.codes.ok:
        return True, r.json()
    else:
        import logging
        log = logging.getLogger('django')
        log.error(r.text)
        return False, r.text

def register_new_user(username, password):
    """
    注册新的app用户
    POST /{org}/{app}/users {"username":"xxxxx", "password":"yyyyy"}
    by:王健 at:2015-1-20
    """
    payload = {"username": username, "password":password}
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return post(EASEMOB_HOST_USERS, payload, token)

def reset_password(username, password=''):
    """
    重置环信密码
    POST /{org}/{app}/users {"username":"xxxxx", "password":"yyyyy"}
    by:尚宗凯 at:2015-3-19
    修改函数名称，改为put方法
    by:尚宗凯 at:2015-3-19
    """
    payload = {"username": username, "password":password}
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return put(EASEMOB_HOST_USERS, payload, token)

def get_group_members(group_id):
    """
    更新群组成员
    GET /{org}/{app}/chatgroups/group_id/users
    by:王健 at:2015-2-27
    """
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return get(EASEMOB_HOST_GROUPS + '/%s/users' % group_id, token)


def add_group_member(group_id, usernames):
    """
    更新群组成员
    POST /{org}/{app}/chatgroups/group_id/users
    by:王健 at:2015-2-27
    修改为添加单个用户
    by:王健 at:2015-2-28
    """
    # payload = {"usernames": usernames}
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return post(EASEMOB_HOST_GROUPS + '/%s/users/%s' % (group_id, usernames), None, token)


def delete_group_member(group_id, username):
    """
    更新群组成员
    DELETE /{org}/{app}/chatgroups/group_id/users/username
    by:王健 at:2015-2-27
    """
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return delete(EASEMOB_HOST_GROUPS + '/%s/users/%s' % (group_id, username), token)


def register_new_group(payload):
    """
    注册新的app用户
    POST /{org}/{app}/chatgroups
    by:王健 at:2015-2-27
    """
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return post(EASEMOB_HOST_GROUPS, payload, token)


def update_group_info(group_id, payload):
    """
    注册新的app用户
    PUT /{org}/{app}/chatgroups/group_id
    by:王健 at:2015-2-27
    """
    if token.is_not_valid():
        return False, u'系统错误（HX_Token），请联系管理员'
    return put(EASEMOB_HOST_GROUPS + '/%s' % group_id, payload, token)



class Token(AuthBase):
    """
    从数据库中获取 token
    by:王健 at:2015-1-20
    """

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.get_token()
        return r

    def get_token(self):
        """
        获取token信息
        by:王健 at:2015-1-20
        :return:
        """
        return self.token

    def __init__(self,):
        self.token = None
        self.exipres_in = 0
        self.authing = False

    def make_token(self):
        """
        从数据库中获取一个token
        by:王健 at:2015-1-20
        修复 环信 token bug
        by:王健 at:2015-3-9
        """
        tl = HuanXin.objects.filter(app=settings.HUANXIN_APP).order_by('-exipres_in')[:1]
        for t in tl:
            self.token = str(t.token)
            self.exipres_in = t.exipres_in
            self.authing = False

    def is_not_valid(self):
        """这个token是否还合法, 或者说, 是否已经失效了, 这里我们只需要
        检查当前的时间, 是否已经比或者这个token的时间过去了exipreis_in秒

        即  current_time_in_seconds < (expires_in + token_acquired_time)
        by:王健 at:2015-1-20
        """
        return self.get_authimg(time() > self.exipres_in)

    def get_authimg(self, valid):
        """
        自动去获取，新的token
        :param valid:
        :return:
        """
        if valid:
            if not self.authing:
                self.authing = True
                AuthThread().start()
        return valid




class AuthThread(threading.Thread):
    """
    异步执行获取token的函数
    by:王健 at:2015-1-20
    修复bug，去除无用参数
    by:王健 at:2015-3-8
    :return:
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        执行获取token的函数
        by:王健 at:2015-1-20
        :return:
        """
        import views
        views.create_huanxin_token(None)
        token.make_token()

token = Token()
token.make_token()