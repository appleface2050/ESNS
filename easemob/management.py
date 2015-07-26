#coding=utf-8
#Date: 15-1-12
#Time: 上午11:48
from django.contrib.auth import models as django_user
from easemob.easemob_server import AppClientAuth
from easemob.models import HuanXin

# from needserver.models import FileGroup


__author__ = u'王健'

from django.db.models import signals
from django.conf import settings

def add_default_app(**kwargs):
    """
    环信id 和 username password 设置
    by:王健 at:2015-1-20
    使用settings中的 变量
    by:王健 at:2015-2-27
    根据环信的变更，取消掉了app管理员，改用 id 和 key 来获取token
    by:王健 at:2015-3-2
    数据初始化只在第一次运行
    by: 范俊伟 at:2015-06-29
    :param kwargs:
    :return:
    """
    if HuanXin.objects.all().count()==0:
        huanxin = HuanXin()
        huanxin.app = settings.HUANXIN_APP
        huanxin.org = settings.HUANXIN_ORG
        huanxin.username = settings.HUANXIN_USERNAME
        huanxin.password = settings.HUANXIN_PASSWORD
        huanxin.save()
        # app_admin_auth = AppAdminAccountAuth(huanxin.org, huanxin.app, huanxin.username, huanxin.password)
        app_admin_auth = AppClientAuth(huanxin.org, huanxin.app, huanxin.username, huanxin.password)
        token = app_admin_auth.acquire_token()
        if token:
            huanxin.token = token.token
            huanxin.exipres_in = token.exipres_in
            huanxin.save()




signals.post_syncdb.connect(add_default_app, sender=django_user, dispatch_uid='easemob.create_defaultapp')