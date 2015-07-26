# coding=utf-8
# Date: 15/1/19
# Time: 15:12
# Email:fanjunwei003@163.com
from functools import update_wrapper
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.utils.decorators import classonlymethod
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.contrib import messages

from django.utils.http import urlencode
from webappjs.base import tform
from webhtml.base.views import PhoneLoginView, LoginView

__author__ = u'范俊伟'


def admin_view_decorator(func):
    '''
    登录检测装饰器函数
    by:范俊伟 at:2015-01-21
    :param func:
    :return:
    '''

    def admin_view(cls, cached=False, **kwargs):
        '''
        装饰器所产生的工厂函数
        by:范俊伟 at:2015-01-21
        :param cls: 传入的class类
        :param cached: 是否缓存
        '''
        view = func(cls, **kwargs)

        def has_permission(request):
            '''
            检测是否登录
            by:范俊伟 at:2015-01-21
            '''
            if request.user.is_active:
                return True
            else:
                return False

        def inner(request, *args, **kwargs):
            '''
            根据登录状态跳转页面
            by:范俊伟 at:2015-01-21
            使用webhtml的登录界面,根据UserAgent不同显示不同登录界面
            by: 范俊伟 at:2015-03-17
            '''
            if not has_permission(request) and getattr(cls, 'need_site_permission', True):
                if request.browserGroup == 'smart_phone':
                    return PhoneLoginView.as_view()(request, *args, **kwargs)
                else:
                    return LoginView.as_view()(request, *args, **kwargs)
            return view(request, *args, **kwargs)

        if not cached:
            inner = never_cache(inner)
        return update_wrapper(inner, view)

    return admin_view


class BaseView(TemplateView):
    '''
    后台管理View基类
    by:范俊伟 at:2015-01-21
    输出环信账号密码
    by:范俊伟 at:2015-02-04
    输出环信appkey
    by:范俊伟 at:2015-02-05
    '''

    # 是否需要登录,默认需要登录
    # by:范俊伟 at:2015-01-21
    need_site_permission = True

    # 页面模板
    # by:范俊伟 at:2015-01-21
    template_name = 'web/base.html'

    def get_context_data(self, **kwargs):
        '''
        获取模板所需的变量
        by:范俊伟 at:2015-01-21
        '''
        kwargs = super(BaseView, self).get_context_data(**kwargs)
        kwargs['url'] = self.request.get_full_path()
        if hasattr(self, 'form'):
            kwargs['form'] = self.form

        kwargs['is_debug'] = settings.DEBUG
        kwargs['hx_appkey'] = settings.HUANXIN_ORG + '#' + settings.HUANXIN_APP
        if self.request.user.is_active and self.request.user.hx_reg:
            kwargs['hx_username'] = self.request.user.pk
            kwargs['hx_password'] = self.request.user.hxpassword

        return kwargs

    def get_query_string(self, new_params=None, remove=None):
        '''
        返回当前url的查询参数(query string)
        by:范俊伟 at:2015-01-21
        :param new_params:所要添加的新参数,以dic形式提供
        :param remove:所要去除的字段,以array形式提供
        '''
        if new_params is None:
            new_params = {}
        if remove is None:
            remove = []
        p = dict(self.request.GET.items()).copy()
        for r in remove:
            for k in p.keys():
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                p[k] = v
        qs = urlencode(p)
        if qs:
            return '?%s' % qs
        else:
            return ''

    def isPhoneRequest(self):
        """
        判断是否为手机请求
        by: 范俊伟 at:2015-03-11
        """
        if self.kwargs.get('isPhone'):
            return True
        elif self.kwargs.get('isPC'):
            return False
        elif self.request.browserGroup == 'smart_phone' or self.request.browserGroup == 'feature_phone':
            return True
        else:
            return False

    @classonlymethod
    @admin_view_decorator
    def as_view(cls, **initkwargs):
        '''
        创建url文件中所需的view方法
        by:范俊伟 at:2015-01-21
        '''
        return super(BaseView, cls).as_view(**initkwargs)




class FrameView(BaseView):
    '''
    登录后页面布局基类
    by:范俊伟 at:2015-01-21
    菜单加载修改
    by: 范俊伟 at:2015-02-14
    '''

    def get_context_data(self, **kwargs):
        '''
        同父类
        by:范俊伟 at:2015-01-21
        菜单加载修改
        by: 范俊伟 at:2015-02-14
        '''
        kwargs = super(FrameView, self).get_context_data(**kwargs)
        return kwargs

    template_name = 'web/frame.html'


