#coding=utf-8
#author:u'王健'
#Date: 14-5-21
#Time: 上午8:00
from django import forms

from needserver.models import Project, Group, GYSAddress, WuZiRecord, UserInfo
from util.CustomForm import CustomModelForm


__author__ = u'王健'


class UserInfoForm(CustomModelForm):
    """
    用户个人信息表单
    by:王健 at:2015-1-18
    增加 title 属性
    by:王健 at:2015-2-13
    修改属性，新增了部门、qq 去掉了 居住地、婚姻、身份证号
    by:王健 at:2015-3-4
    增加phrase字段
    by:尚宗凯 at:2015-3-24
    """
    birthday = forms.DateField(required=False)
    qq = forms.CharField(required=False)
    address = forms.IntegerField(required=False)
    xueli = forms.IntegerField(required=False)
    zhicheng = forms.CharField(required=False)
    zhiyezigezheng = forms.CharField(required=False)
    hunyin = forms.CharField(required=False)
    company = forms.CharField(required=False)
    department = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phrase = forms.CharField(required=False)

    class Meta:
        model = UserInfo
        fields = ('birthday', 'qq', 'department', 'address', 'xueli', 'zhicheng', 'zhiyezigezheng', 'company', 'title', 'email' ,'phrase')


class ProjectForm(CustomModelForm):
    """
    项目表单
    by:王健 at:2015-1-3
    部分数字类型的值，需要使用数字型的字段
    by:王健 at:2015-1-5
    项目添加图标字段
    by:王健 at:2015-1-29
    添加字段限制
    by:王健 at:2015-2-15
    建筑层数 改为字符
    by:王健 at:2015-3-15
    修改name属性为非必填
    by:王健 at:2015-4-10
    修改address必填属性
    by:王健 at:2015-04-19
    修改name属性为必填项
    by:王健 at:2015-05-07
	增加渠道代码字段
	by:王健 at:2015-05-13
    """
    icon_url = forms.IntegerField(required=False)
    address = forms.IntegerField()
    jzmj = forms.IntegerField()
    jzcs = forms.CharField(max_length=30)
    htzj = forms.IntegerField()
    kg_date = forms.DateField()
    days = forms.IntegerField()

    name = forms.CharField(max_length=8)
    jsdw = forms.CharField()
    jsdw_fzr = forms.CharField()
    kcdw = forms.CharField()
    kcdw_fzr = forms.CharField()
    sjdw = forms.CharField()
    sjdw_fzr = forms.CharField()
    sgdw = forms.CharField()
    sgdw_fzr = forms.CharField()
    jldw = forms.CharField()
    jldw_fzr = forms.CharField()

    channel = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ('name', 'icon_url', 'total_name', 'address', 'jzmj', 'jglx', 'jzcs', 'htzj', 'kg_date', 'days', 'jsdw', 'jsdw_fzr', 'kcdw', 'kcdw_fzr', 'sjdw', 'sjdw_fzr', 'sgdw', 'sgdw_fzr', 'jldw', 'jldw_fzr', 'channel')


class GroupForm(CustomModelForm):
    """
    分组表单
    by:王健 at:2015-1-3
    """
    icon_url = forms.CharField(required=False)

    class Meta:
        model = Group
        fields = ('name', 'icon_url', 'project')


class GYSAddressForm(CustomModelForm):
    """
    供货商表单
    by:王健 at:2015-1-14
    booleanField 会认为False型为为负值，所以改为可选参数
    by:王健 at:2015-1-22
    去除合同、付款方式字段
    by:王健 at:2015-2-4
    """
    bz = forms.CharField(required=False)
    # is_hetong = forms.BooleanField(required=False)
    class Meta:
        model = GYSAddress
        fields = ('name', 'ghs', 'ghs_fzr', 'ghs_fzr_tel', 'shr', 'shr_tel', 'bz')


class WuZiRecordForm(CustomModelForm):
    """
    物资记录
    by:王健 at:2015-1-14
    去除num ，count 改为数量字段
    by:王健 at:2015-2-4
    """
    company = forms.CharField(required=False)
    lingliaoren = forms.CharField(required=False)
    # count = forms.IntegerField()
    class Meta:
        model = WuZiRecord
        fields = ('name', 'gg', 'company', 'lingliaoren', 'count')
