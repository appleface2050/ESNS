# coding=utf-8
# Date: 15/1/20'
# Email: wangjian2254@icloud.com
from django.db import transaction
from easemob.easemob_server import AppAdminAccountAuth, AppClientAuth
from easemob.models import HuanXin
from time import time
from util.jsonresult import getResult
from django.conf import settings

__author__ = u'王健'

@transaction.atomic()
def create_huanxin_token(request):
    """
    给最后一个环信账号 设置token值
    by:王健 at:2015-1-20
    修复 判断条件
    by:王健 at:2015-3-8
    修复没有环信 token的bug
    by:王健 at:2015-3-9
    """
    t = int(time())-3600*24
    if HuanXin.objects.filter(app=settings.HUANXIN_APP).exists():
        huanxinquery = HuanXin.objects.filter(app=settings.HUANXIN_APP, exipres_in__lt=t).order_by('exipres_in')[:1]
        if len(huanxinquery) > 0:
            huanxin = huanxinquery[0]
            app_admin_auth = AppClientAuth(huanxin.org, huanxin.app, huanxin.username, huanxin.password)
            token = app_admin_auth.acquire_token()
            if token:
                huanxin.token = token.token
                huanxin.exipres_in = token.exipres_in
                huanxin.save()
                return getResult(True, u'获取环信token成功')
            else:
                return getResult(False, u'获取环信token失败', huanxin.username)
        else:
            return getResult(True, u'没有过期的token')
    else:
        huanxin = HuanXin()
        huanxin.app = settings.HUANXIN_APP
        huanxin.org = settings.HUANXIN_ORG
        huanxin.username = settings.HUANXIN_USERNAME
        huanxin.password = settings.HUANXIN_PASSWORD
        app_admin_auth = AppClientAuth(huanxin.org, huanxin.app, huanxin.username, huanxin.password)
        token = app_admin_auth.acquire_token()
        if token:
            huanxin.token = token.token
            huanxin.exipres_in = token.exipres_in
            huanxin.save()