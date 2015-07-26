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
from company.models import CompanyPerson
from util.jsonresult import getResult

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
        权限控制
        by: 范俊伟 at:2015-06-11
        '''
        view = func(cls, **kwargs)

        def has_permission(request):
            '''
            检测是否登录
            by:范俊伟 at:2015-01-21
            '''
            if request.user.is_active:
                if request.user.is_staff:
                    return True
                if CompanyPerson.objects.filter(user=request.user, creator_type=1).exists():
                    return True
                # elif hasattr(request.user, 'backuserinfo'):
                #     backuserinfo = request.user.backuserinfo
                #     if backuserinfo.user_type >= 0:
                #         return True

            return False

        def inner(request, *args, **kwargs):
            '''
            根据登录状态跳转页面
            by:范俊伟 at:2015-01-21
            使用webhtml的登录界面,根据UserAgent不同显示不同登录界面
            by: 范俊伟 at:2015-03-17
            '''
            if not has_permission(request) and getattr(cls, 'need_site_permission', True):
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
        权限控制
        by: 范俊伟 at:2015-06-11
        增加参数输出
        by: 范俊伟 at:2015-06-12
        增加登陆判断
        by：尚宗凯 at：2015-06-18
        '''
        kwargs = super(BaseView, self).get_context_data(**kwargs)
        kwargs['url'] = self.request.get_full_path()
        if hasattr(self, 'form'):
            kwargs['form'] = self.form
        kwargs['is_debug'] = settings.DEBUG
        if self.request.user.is_active:
            if self.request.user.is_staff:
                kwargs['user_type'] = 'admin'
            elif CompanyPerson.objects.filter(user=self.request.user, creator_type=1).exists():
                cp = CompanyPerson.objects.filter(user=self.request.user, creator_type=1)[0]
                kwargs['company'] = cp.company.toJSON()
                kwargs['user_type'] = 'company_manager'
            elif hasattr(self.request.user, 'backuserinfo'):
                backuserinfo = self.request.user.backuserinfo
                if backuserinfo.user_type == 0:
                    kwargs['user_type'] = 'kf'
                elif backuserinfo.user_type == 1:
                    kwargs['user_type'] = 'accountancy'
                elif backuserinfo.user_type == 2:
                    kwargs['user_type'] = 'promoter'

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
        去除测试代码
        by:王健 at:2015-06-27
        '''
        # from needserver.models import NSUser
        # user = NSUser.objects.get(tel='18262283559')
        # user.set_password('123456')
        # user.save()
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
        输出用户头像
        by: 范俊伟 at:2015-06-10
        '''
        kwargs = super(FrameView, self).get_context_data(**kwargs)
        if self.request.user.icon_url:
            kwargs['user_icon_url'] = self.request.user.icon_url.get_url('imageView2/5/w/60/h/60')
        return kwargs

    template_name = 'web/frame.html'


class LoginView(BaseView):
    '''
    登录视图
    by:范俊伟 at:2015-01-21
    '''
    need_site_permission = False
    template_name = 'cp_manage/login.html'

    def get_context_data(self, **kwargs):
        '''
        同父类
        by:范俊伟 at:2015-01-21
        '''
        return super(LoginView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 范俊伟 at:2015-04-21
        修改登陆跳转地址
        by: 范俊伟 at:2015-05-04
        修改链接
        by: 范俊伟 at:2015-06-10
        权限控制
        by: 范俊伟 at:2015-06-11
        增加登陆权限控制
        by：尚宗凯 at：2015-06-18
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.REQUEST.get('username')
        password = request.REQUEST.get('password')
        if not username:
            return getResult(False, u"账号不能为空")
        if not password:
            return getResult(False, u"密码不能为空")
        user = authenticate(username=username, password=request.REQUEST.get('password'))
        if user and not user.is_active:
            return getResult(False, u"用户已经停止使用")
        elif not user:
            return getResult(False, u"用户名密码错误")
        else:
            can_login = False
            if user.is_staff or CompanyPerson.objects.filter(user=user, creator_type=1).exists():
                can_login = True
            elif hasattr(user, 'backuserinfo'):
                backuserinfo = user.backuserinfo
                if backuserinfo.user_type >= 0:
                    can_login = True
            if not can_login:
                return getResult(False, u"无权登录后台")
            auth_login(request, user)
            next_url = request.REQUEST.get('next', None)
            if next_url:
                return HttpResponseRedirect(next_url)
            current_url = request.path
            login_url = reverse('cp_manage:login')
            if current_url == login_url:
                current_url = reverse('cp_manage:cp_manage')
                # current_url = reverse('cp_manage:manage')

            current_url = '%s%s' % (current_url, self.get_query_string())
            return getResult(True, "", result={"url": current_url})
