#coding=utf-8
#author:u'王健'
#Date: 14-5-21
#Time: 上午7:56
from django.db import models
from django.forms import ModelForm

__author__ = u'王健'


class CustomModelForm(ModelForm):
    """
    可以返回json格式 错误信息的 基础表单
    by:王健 at:2015-1-3
    追踪回Model 中 获取verbose_name 值
    by:王健 at:2015-1-18
    对外键的label 获取
    by:王健 at:2015-1-29
    优化错误信息 提示
    by:王健 at:2015-4-8
    """
    def json_error(self,s='\n'):
        msg = []
        for k in self.errors.keys():
            label = u''
            for field in self.Meta.model._meta.fields:
                if field.attname == k or (field.attname[0:len(k)] == k and field.attname.find('id') > 0):
                    label = field.verbose_name
            # label = self.fields.get(k).label
            error = u"、".join(self.errors.get(k))
            msg.append(u'%s : %s'%(label,error))
            sorted(msg)
        return s.join(msg)

    def clean(self):
        """
        对文字字段，清空前后空格
        by:王健 at:2015-4-10
        :return:
        """
        v = super(CustomModelForm, self).clean()
        for field in self.Meta.model._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                if v.has_key(field.name):
                    v[field.name] = v[field.name].strip()
        return v