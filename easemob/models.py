# coding=utf-8
# Date: 15/1/20'
# Email: wangjian2254@icloud.com
from django.db import models
__author__ = u'王健'


class HuanXin(models.Model):
    """
    用户的个人信息表
    by:王健 at:2015-1-18
    加大数据库字段长度
    by:王健 at:2015-3-8
    """
    token = models.CharField(max_length=100, blank=True, verbose_name=u'环信token')
    exipres_in = models.IntegerField(default=0, null=True, blank=True, db_index=True, verbose_name=u'过期时间')
    username = models.CharField(max_length=50, blank=True, unique=True, verbose_name=u'管理员用户名')
    password = models.CharField(max_length=50, blank=True, verbose_name=u'管理员密码')
    org = models.CharField(max_length=50, blank=True, verbose_name=u'环信组织id')
    app = models.CharField(max_length=50, blank=True, verbose_name=u'环信app')
