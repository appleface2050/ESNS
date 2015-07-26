# coding=utf-8
# Date: 15/4/3'
# Email: wangjian2254@icloud.com
from django.utils import timezone

__author__ = u'王健'


from django.db import models


class TongJi(models.Model):
    """
    统计
    by:王健 at:2015-4-3
    """
    client_type = models.CharField(max_length=50, verbose_name=u'客户端类型')
    channel = models.CharField(max_length=20, default='web', verbose_name=u'推广途径')
    date = models.DateField(default=timezone.now, verbose_name=u'日期')
    num = models.IntegerField(default=0, verbose_name=u'数量')