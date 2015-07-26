# coding=utf-8
# Date: 15/3/20
# Time: 12:17
# Email:fanjunwei003@163.com
from django.conf import settings

__author__ = '范俊伟'


def base(request):
    """
    通用模版参数
    by: 范俊伟 at:2015-06-24
    :param request:
    :return:
    """
    return {"is_debug":settings.DEBUG}
