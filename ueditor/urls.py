# coding=utf-8
'''
Created on 2012-9-3

@author: 王健
'''
from django.conf.urls import patterns, url


urlpatterns = patterns('ueditor',
                       # 系统图片位置
                       # by:王健 at:2015-06-14
					   # 解决urlbug
                       # by：尚宗凯 at：2015-06-15
                       # 修改函数名，符合规范
                       # by:王健 at:2015-06-17
                       url(r'^imageUp$', 'views.image_up'),
                       # url(r'^fileUp$', 'views.fileUp'),
                       # url(r'^getRemoteImage$', 'views.getRemoteImage'),
                       # 修改函数名，符合规范
                       # by:王健 at:2015-06-17
                       url(r'^imageManager$', 'views.image_manager'),
                       # url(r'^getMovie$', 'views.getMovie'),

                        # 公司图片位置
                        # by:王健 at:2015-06-14
                       # 修改函数名，符合规范
                       # by:王健 at:2015-06-17
                       url(r'^(?P<company_id>\d+)/imageUp$', 'views.image_up'),
                       # url(r'^(?P<company_id>\d+)/fileUp$', 'views.fileUp'),
                       # url(r'^(?P<company_id>\d+)/getRemoteImage$', 'views.getRemoteImage'),
                       # 修改函数名，符合规范
                       # by:王健 at:2015-06-17
                       url(r'^(?P<company_id>\d+)/imageManager$', 'views.image_manager'),
                       # url(r'^(?P<company_id>\d+)/getMovie$', 'views.getMovie'),

)