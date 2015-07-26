# coding=utf-8
# Date: 15/5/14
# Time: 14:36
# Email:fanjunwei003@163.com
from django.conf.urls import patterns, url
from ns_manage import views
from ns_manage.base import views as base_views

__author__ = u'范俊伟'
urlpatterns = patterns('ns_manage',
                       url(r'^$', views.AppView.as_view(), name='home'),
                       url(r'^login$', base_views.LoginView.as_view(), name='login'),
                       url(r'^logout$', views.logout, name='logout'),
                       url(r'^query_user$', views.query_user),
                       url(r'^set_user_type$', views.set_user_type),
                       url(r'^change_password$', views.change_password),
                       )
