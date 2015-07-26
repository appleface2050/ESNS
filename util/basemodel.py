# coding=utf-8
# Date: 15/1/29'
# Email: wangjian2254@icloud.com
import json
from django.db import models
from django.db.models import DateTimeField, DateField, CommaSeparatedIntegerField, ImageField, DecimalField

__author__ = u'王健'

BASE_DATE_FROMATE = '%Y-%m-%d'
BASE_DATETIME_FROMATE = '%Y-%m-%d %H:%M:%S'

class JSONBaseModel(models.Model):
    """
    带json序列化的基础Model
    by:王健 at:2015-1-29
    """
    def toJSON(self):
        """
        序列化成 dict类型
        by:王健 at:2015-1-29
        修改 刚刚修改过 的字符串 日期 bug
        by:王健 at:2015-2-3
        对数组类型的字段，优化转化
        by:王健 at:2015-06-27
        :return:
        """

        fields = []
        for field in self._meta.fields:
            fields.append((field.name, field.attname, type(field)))

        d = {}
        for attr, attname, t in fields:
            if getattr(self, attname, None) == None:
                d[attr] = None
            else:
                if t == DateTimeField and not isinstance(getattr(self, attname), (str, unicode)):
                    d[attr] = getattr(self, attname).strftime(BASE_DATETIME_FROMATE)
                elif t == DateField and not isinstance(getattr(self, attname), (str, unicode)):
                    d[attr] = getattr(self, attname).strftime(BASE_DATE_FROMATE)
                elif t == CommaSeparatedIntegerField:
                    if isinstance(getattr(self, attname), (str,unicode)):
                        d[attr] = json.loads(getattr(self, attname, '[]'))
                    else:
                        d[attr] = getattr(self, attname)
                else:
                    d[attr] = getattr(self, attname)

        return d

    class Meta:
        abstract = True


class JSONBaseMixin(object):
    """
    model json序列化掺合类
    by: 范俊伟 at:2015-06-11
    """

    def toJSON(self):
        """
        序列化成 dict类型
        by:王健 at:2015-1-29
        修改 刚刚修改过 的字符串 日期 bug
        by:王健 at:2015-2-3
        :return:
        """
        fields = []
        for field in self._meta.fields:
            fields.append((field.name, field.attname, type(field)))
        d = {}
        for attr, attname, t in fields:
            if getattr(self, attname, None) == None:
                d[attr] = None
            else:
                if t == DateTimeField and not isinstance(getattr(self, attname), (str, unicode)):
                    d[attr] = getattr(self, attname).strftime(BASE_DATETIME_FROMATE)
                elif t == DateField and not isinstance(getattr(self, attname), (str, unicode)):
                    d[attr] = getattr(self, attname).strftime(BASE_DATE_FROMATE)
                elif t == ImageField:
                    if getattr(self, attname, {}):
                        d[attr] = getattr(self, attname, {}).url
                    else:
                        d[attr] = ''
                elif t == CommaSeparatedIntegerField:
                    d[attr] = json.loads(getattr(self, attname, '[]'))
                elif t == DecimalField:
                    d[attr] = float(getattr(self, attname))
                else:
                    d[attr] = getattr(self, attname)
        return d