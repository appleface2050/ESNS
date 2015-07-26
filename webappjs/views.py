# coding=utf-8
# Date: 15/1/19
# Time: 18:23
# Email:fanjunwei003@163.com
"""
后台管理视图
"""
from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout
from util.jsonresult import getResult
from webappjs.base import tform
from webappjs.base.views import BaseView, FrameView

__author__ = u'范俊伟'


def logout(request):
    '''
    退出登录
    by:范俊伟 at:2015-01-21
    '''
    auth_logout(request)
    return http.HttpResponseRedirect(request.REQUEST.get('next', reverse('web:home')))


class RegisterView(BaseView):
    '''
    用户注册视图,通过reg_tel参数区分是否为通过社会化第三方平台第一次登录的注册请求
    by:范俊伟 at:2015-01-21
    '''
    need_site_permission = False
    template_name = 'web/register.html'

    def get_context_data(self, **kwargs):
        '''
        同父类
        by:范俊伟 at:2015-01-21
        '''
        if not kwargs.get('reg_tel', False):
            kwargs["tform"] = [
                tform.TextField(label='电话', name='tel', input_check='checkTel()',
                                template='web/include/register/field_tel.html'),
                tform.TextField(label='短信验证码', name='code', template='web/include/register/field_text.html'),
                tform.TextField(label='密码', name='password', template='web/include/register/field_password.html'),
                tform.TextField(label='确认密码', name='password_re', input_check='checkPasswordRe()',
                                template='web/include/register/field_password.html'),
                tform.TextField(label='真实姓名', name='name', template='web/include/register/field_text.html'),
                # tform.HiddenField(name='smsdebug', value='smsdebug'),
            ]
        else:
            kwargs["tform"] = [
                tform.TextField(label='电话', name='tel', input_check='checkTel()',
                                template='web/include/register/field_tel.html'),
                tform.TextField(label='短信验证码', name='code', template='web/include/register/field_text.html'),
                tform.TextField(label='真实姓名', name='name', template='web/include/register/field_text.html'),
                # tform.HiddenField(name='smsdebug', value='smsdebug'),
            ]
        return super(RegisterView, self).get_context_data(**kwargs)


class AppView(FrameView):
    '''
    后台app视图
    by:范俊伟 at:2015-02-06
    '''
    template_name = 'web/app.html'
    title = u'Need'


def logout(request):
    """
    退出
    by:范俊伟 at:2015-02-06
    修改登出的界面
    by:范俊伟 at:2015-03-16
    :param request:
    :return:
    """
    auth_logout(request)
    return http.HttpResponseRedirect(request.REQUEST.get('next', reverse('home')))


def add_django_message(request):
    '''
    添加跨页显示消息
    by:范俊伟 at:2015-02-10
    :param request:
    :return:
    '''
    message = request.REQUEST.get('message')
    tag = request.REQUEST.get('tag')
    if message and tag:
        if tag == 'success':
            messages.success(request, message)
        elif tag == 'error':
            messages.error(request, message)
        elif tag == 'info':
            messages.info(request, message)

    return getResult(True, '')
