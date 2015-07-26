# coding=utf-8
# Date:2015/1/10
# Email:wangjian2254@gmail.com
from webappjs.base.views import LoginView
from webappjs.views import RegisterView, AppView, logout, add_django_message

__author__ = u'王健'

from django.conf.urls import patterns, url

# web端接口
# by:王健 at:2015-1-15

urlpatterns = patterns('web',
                       # 重新设计webappjs接口
                       # by:范俊伟 at:2015-02-06
                       url(r'^$', AppView.as_view(), name='home'),
                       url(r'login$', LoginView.as_view(), name='login'),
                       url(r'logout$', logout, name='logout'),
                       url(r'add_django_message$', add_django_message),
                       url(r'reg_tel$', RegisterView.as_view(), name='reg_tel', kwargs={"reg_tel": True}),
                       url(r'reg_user$', RegisterView.as_view(), name='register', kwargs={"reg_tel": False}),
)