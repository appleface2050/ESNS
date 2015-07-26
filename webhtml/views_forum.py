#coding=utf-8
from django.http import HttpResponseRedirect

__author__ = 'wangjian'


def forum_login(request):
    """
    论坛单点登录
    by:王健 at:2015-06-24
    :param request:
    :return:
    """
    return HttpResponseRedirect('http://forum.tjeasyshare.com')