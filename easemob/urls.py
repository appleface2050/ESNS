# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
__author__ = u'王健'

from django.conf.urls import patterns, url

#url添加$结束符
#by:王健 at:2015-1-21
urlpatterns = patterns('easemob',
                       url(r'^create_huanxin_token$', 'views.create_huanxin_token'),



)