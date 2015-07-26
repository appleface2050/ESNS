# coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from webhtml import urls as webhtml_url

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # 增加web模块，和默认首页
                       # by:王健 at:2015-1-15
                       # 改用webappjs模块,实现完全无刷新
                       # by:范俊伟 at:2015-02-06
                       # 修改web页面url的加载方式
                       # by:范俊伟 at:2015-02-11
                       url(r'^web/', include('webappjs.urls', namespace='web')),
                       # modify:范俊伟 at:2015-01-19 添加namespace,方便生成url
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^ns/', include('needserver.urls')),
                       # 添加文件上传模块
                       # by:王健 at:2015-1-10
                       url(r'^nf/', include('nsbcs.urls')),
                       # 环信刷新token
                       # by:王健 at:2015-1-20
                       url(r'^hx/', include('easemob.urls')),
                       # 统计模块
                       # by:王健 at:2015-4-3
                       url(r'^tj/', include('tongji.urls')),

                       # 客服模块,为客服系统提供接口
                       # by: 范俊伟 at:2015-05-14
                       url(r'^kf/', include('kf.urls')),
                       # 增加公司模块
                       # by:尚宗凯 at：2015-06-10
					   # 增加namespace
					   # by：尚宗凯 at：2015-06-14
                       url(r'^cp/', include('company.urls', namespace='cp_manage')),

                        # 添加在线编辑器模块
                        # by:王健 at:2015-06-14
                       url(r'^ueditor/', include('ueditor.urls')),

                       # 后台管理模块
                       # by: 范俊伟 at:2015-06-10
                       url(r'^ns_manage/', include('ns_manage.urls', namespace='ns_manage')),



                       url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += webhtml_url.urlpatterns
