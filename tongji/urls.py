# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
__author__ = u'王健'

from django.conf.urls import patterns, url

#统计接口开发
#by:王健 at:2015-4-3
urlpatterns = patterns('tongji',

                       url(r'^guest_app_url$', 'views_tongji.guest_app_url'),
                       url(r'^show_channel_tongji$', 'views_tongji.show_channel_tongji'),


)