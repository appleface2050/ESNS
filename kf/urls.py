# coding=utf-8
# Date: 15/5/14
# Time: 14:36
# Email:fanjunwei003@163.com
from django.conf.urls import patterns, url

__author__ = u'范俊伟'
urlpatterns = patterns('kf',
                       url(r'^query_user$', 'views.query_user'),
                       url(r'^query_project$', 'views.query_project'),
                       url(r'^get_project_info$', 'views.get_project_info'),
                       )