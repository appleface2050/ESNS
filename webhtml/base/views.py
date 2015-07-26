# coding=utf-8
# Date: 15/1/19
# Time: 15:12
# Email:fanjunwei003@163.com
from django.conf import settings
from django.core.urlresolvers import reverse
from functools import update_wrapper
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import HttpResponseRedirect

from django.utils.decorators import classonlymethod
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

from django.utils.http import urlencode
from webhtml.base import tform
from needserver.models import NSUser

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
            根据UserAgent跳转到不同登录页面
            by: 范俊伟 at:2015-03-06
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
    前台界面基类，默认不需要登录
    by:王健 at:2015-01-25
    '''

    # 是否需要登录,默认需要登录
    # by:范俊伟 at:2015-01-21
    # 默认不需要登录
    # by:范俊伟 at:2015-01-21
    need_site_permission = False

    # 页面模板
    # by:范俊伟 at:2015-01-21
    template_name = 'webhtml/base.html'

    def get_context_data(self, **kwargs):
        '''
        获取模板所需的变量
        by:范俊伟 at:2015-01-21
        客服系统所需变量
        by: 范俊伟 at:2015-05-21
        '''
        kwargs = super(BaseView, self).get_context_data(**kwargs)
        kwargs['url'] = self.request.get_full_path()
        kwargs['kf_url'] = settings.NEED_KF_BASE_URL
        kwargs['sessionid'] = self.request.session.session_key
        if hasattr(self, 'form'):
            kwargs['form'] = self.form
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

    def isSmartPhone(self):
        """
        判断是否是智能手机
        by: 尚宗凯 at: 2015-03-27
        """
        if self.request.browserGroup == 'smart_phone':
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


def login(request, *args, **kwargs):
    """
    根据UserAgent不同显示不同登录界面
    by: 范俊伟 at:2015-03-17
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if request.browserGroup == 'smart_phone':
        return PhoneLoginView.as_view()(request, *args, **kwargs)
    else:
        return LoginView.as_view()(request, *args, **kwargs)


class LoginView(BaseView):
    '''
    登录视图
    by:范俊伟 at:2015-01-21
    登录视图，用于前台界面
    by:范俊伟 at:2015-01-26
    简单登录界面
    by: 范俊伟 at:2015-03-11
    增加 next 参数的配置
    by: 王健 at:2015-03-16
    '''
    need_site_permission = False
    template_name = 'webhtml/html/login.html'

    def get_context_data(self, **kwargs):
        '''
        获取模板所需的变量
        by:范俊伟 at:2015-01-21
        '''
        kwargs = super(BaseView, self).get_context_data(**kwargs)
        kwargs['next'] = self.request.REQUEST.get('next', '')
        return kwargs


    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 范俊伟 at:2015-03-11
        修改登录界面
        by: 范俊伟 at:2015-03-11
        修改默认跳转地址
        by: 范俊伟 at:2015-03-17
        NSUser增加is_used字段
        by: 尚宗凯 at:2015-03-20
        NSUser删除is_used字段
        by: 尚宗凯 at:2015-03-25
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tel = request.REQUEST.get('tel')
        password = request.REQUEST.get('password')
        if not tel:
            messages.error(request, u'账号不能为空')
            return self.get(request, *args, **kwargs)
        if not password:
            messages.error(request, u'密码不能为空')
            return self.get(request, *args, **kwargs)

        user = authenticate(tel=tel, password=request.REQUEST.get('password'))
        if user and not user.is_active:
            messages.error(request, u'用户已经停止使用')
            return self.get(request, *args, **kwargs)
        elif not user:
            messages.error(request, u'用户名密码错误')
            return self.get(request, *args, **kwargs)
        else:
            auth_login(request, user)
            next_url = request.REQUEST.get('next', None)
            if next_url:
                return HttpResponseRedirect(next_url)
            current_url = request.path
            login_url = reverse('login')
            if current_url == login_url:
                current_url = reverse('web:home')
            current_url = '%s%s' % (current_url, self.get_query_string())
            return HttpResponseRedirect(current_url)


class PhoneLoginView(BaseView):
    """
    手机登录视图类
    by: 范俊伟 at:2015-03-06
    """
    need_site_permission = False
    template_name = 'webhtml/phone/login.html'

    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 范俊伟 at:2015-03-06
        登录跳转需要携带之前的queryString参数
        by: 范俊伟 at:2015-03-11
        修改默认跳转地址
        by: 范俊伟 at:2015-03-17
        NSUser增加is_used字段
        by: 尚宗凯 at:2015-03-20
        NSUser删除is_used字段
        by: 尚宗凯 at:2015-03-25
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        tel = request.REQUEST.get('tel')
        password = request.REQUEST.get('password')
        if not tel:
            messages.error(request, u'账号不能为空')
            return self.get(request, *args, **kwargs)
        if not password:
            messages.error(request, u'密码不能为空')
            return self.get(request, *args, **kwargs)

        user = authenticate(tel=tel, password=request.REQUEST.get('password'))
        if user and not user.is_active:
            messages.error(request, u'用户已经停止使用')
            return self.get(request, *args, **kwargs)
        elif not user:
            messages.error(request, u'用户名密码错误')
            return self.get(request, *args, **kwargs)
        else:
            auth_login(request, user)
            next_url = request.REQUEST.get('next', None)
            if next_url:
                return HttpResponseRedirect(next_url)
            current_url = request.path
            login_url = reverse('login')
            if current_url == login_url:
                current_url = reverse('web:home')
            current_url = '%s%s' % (current_url, self.get_query_string())
            return HttpResponseRedirect(current_url)


def format_money(value, has_comma=False):
    """
    格式化以分位单位的金额
    by: 范俊伟 at:2015-03-07
    控制是否带千分位
    by: 范俊伟 at:2015-03-20
    :param value:
    :return:
    """
    try:
        value = int(value)
        if has_comma:
            return format(float(value) / 100.0, ',.2f')
        else:
            return format(float(value) / 100.0, '.2f')
    except:
        return None




