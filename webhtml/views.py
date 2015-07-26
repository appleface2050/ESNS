# coding=utf-8
# Date: 15/2/11
# Time: 15:55
# Email:fanjunwei003@163.com
import urllib2
import json
import uuid,random
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from needserver.models import Group, Project, NSUser
from util.loginrequired import client_admin_login_required
from util.tools import common_except_log
from webhtml.base import tform
from webhtml.base.views import BaseView
from django.contrib.auth import logout as auth_logout
from django import http
from webhtml.models import Product, Tax, Order, Address, HelpContent, HelpMenu, HelpUsage
from django.contrib.auth import login as auth_login
from needserver.models import NeedHelper as NeedHelperModel
# from DjangoCaptcha import Captcha
from Need_Server.settings import ALI_OPEN_SEARCH,ALI_OPEN_SEARCH_ON

__author__ = u'范俊伟'


def logout(request):
    """
    退出
    by:范俊伟 at:2015-02-11
    :param request:
    :return:
    """
    auth_logout(request)
    return http.HttpResponseRedirect(request.REQUEST.get('next', reverse('home')))


class ForgetPassword(BaseView):
    """
    找回密码
    by: 尚宗凯 at:2015-03-27
    """
    view_id = 'get_password'

    def get_context_data(self, **kwargs):
        if self.request.browserGroup == 'smart_phone':
            self.template_name = 'webhtml/phone/phone_forget_password.html'
        else:
            self.template_name = 'webhtml/html/web_forget_password.html'
        return super(ForgetPassword, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 尚宗凯 at:2015-03-27
        """
        # if self.request.browserGroup == 'smart_phone':
        # template_name = 'webhtml/phone_forget_password.html'
        # else:
        # template_name = 'webhtml/html/web_forget_password.html'
        kwargs.update(self.request.POST.dict())
        tel = request.REQUEST.get('tel')
        sms_code = request.REQUEST.get('sms_code')
        password = request.REQUEST.get('password')
        re_password = request.REQUEST.get('re_password')

        if not tel:
            messages.error(request, '手机号码不能为空')
            return self.get(request, *args, **kwargs)
        if not sms_code:
            messages.error(request, '短信验证码不能为空')
            return self.get(request, *args, **kwargs)
        if not password:
            messages.error(request, '密码不能为空')
            return self.get(request, *args, **kwargs)
        if not re_password:
            messages.error(request, '确认密码不能为空')
            return self.get(request, *args, **kwargs)
        if re_password != password:
            messages.error(request, '密码不匹配')
            return self.get(request, *args, **kwargs)

        if not request.session.get('smscode', None):
            messages.error(request, '未发送短信验证码')
            return self.get(request, *args, **kwargs)
        if tel != request.session.get('smstel', None):
            messages.error(request, '发送验证码的手机号，和注册的手机号不符合')
            return self.get(request, *args, **kwargs)
        if sms_code != request.session.get('smscode', None):
            messages.error(request, '短信验证码错误')
            return self.get(request, *args, **kwargs)
        try:
            if not NSUser.objects.filter(tel=tel).exists():
                messages.error(request, '该账号不存在')
                return self.get(request, *args, **kwargs)
            else:
                user = NSUser.objects.get(tel=tel)
                user.set_password(password)
                user.save()
                request.session['smscode'] = None
                request.session['smstel'] = None
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)
                return HttpResponseRedirect('/')
        except:
            common_except_log()
            messages.error(request, '修改密码失败')
            return self.get(request, *args, **kwargs)


class HomeView(BaseView):
    '''
    前台web界面,首页
    by:范俊伟 at:2015-02-11
    修改基类,根据UserAgent使用不同模板
    by: 范俊伟 at:2015-03-11
    改版首页
    by:王健 at:2015-06-16
    '''
    view_id = 'home'

    def get_context_data(self, **kwargs):
        if self.request.browserGroup == 'smart_phone':
            # self.template_name = 'webhtml/phone/home.html'
            self.template_name = 'webhtml/phone/home_v2.html'
        else:
            self.template_name = 'webhtml/home4.html'
        return super(HomeView, self).get_context_data(**kwargs)


class ListView(BaseView):
    '''
    前台web界面,List框架
    by:范俊伟 at:2015-02-11
    修改基类
    by: 范俊伟 at:2015-03-11
    '''
    view_id = 'list'
    template_name = 'webhtml/list_item_1.html'


class DownloadView(BaseView):
    '''
    前台web界面,下载
    by:范俊伟 at:2015-02-11
    修改基类
    by: 范俊伟 at:2015-03-11
    '''
    view_id = 'download'
    template_name = 'webhtml/download.html'


class ReginsterView(BaseView):
    '''
    前台web界面,注册
    by:范俊伟 at:2015-02-11
    修改基类
    by: 范俊伟 at:2015-03-11
    '''

    template_name = 'webhtml/register.html'

    def post(self, request, *args, **kwargs):
        """
        post请求
        by: 范俊伟 at:2015-03-11
        修改注册界面
        by: 范俊伟 at:2015-03-17
        短信验证
        by: 范俊伟 at:2015-03-17
        """
        kwargs.update(self.request.POST.dict())
        tel = request.REQUEST.get('tel')
        sms_code = request.REQUEST.get('sms_code')
        password = request.REQUEST.get('password')
        re_password = request.REQUEST.get('re_password')
        name = request.REQUEST.get('name')
        if not tel:
            messages.error(request, '手机号码不能为空')
            return self.get(request, *args, **kwargs)
        if not sms_code:
            messages.error(request, '短信验证码不能为空')
            return self.get(request, *args, **kwargs)
        if not password:
            messages.error(request, '密码不能为空')
            return self.get(request, *args, **kwargs)
        if not re_password:
            messages.error(request, '确认密码不能为空')
            return self.get(request, *args, **kwargs)
        if not name:
            messages.error(request, '姓名不能为空')
            return self.get(request, *args, **kwargs)
        if re_password != password:
            messages.error(request, '密码不匹配')
            return self.get(request, *args, **kwargs)
        if NSUser.objects.filter(tel=tel).count() > 0:
            messages.error(request, '手机号已存在')
            return self.get(request, *args, **kwargs)
        if not request.session.get('smscode', None):
            messages.error(request, '未发送短信验证码')
            return self.get(request, *args, **kwargs)
        if tel != request.session.get('smstel', None):
            messages.error(request, '发送验证码的手机号，和注册的手机号不符合')
            return self.get(request, *args, **kwargs)
        if sms_code != request.session.get('smscode', None):
            messages.error(request, '短信验证码错误')
            return self.get(request, *args, **kwargs)
        try:
            user = NSUser(tel=tel, name=name)
            user.set_password(password)
            user.save()
            request.session['smscode'] = None
            request.session['smstel'] = None
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            return HttpResponseRedirect('/')
        except:
            common_except_log()
            messages.error(request, '注册失败')
            return self.get(request, *args, **kwargs)


class PhoneReginsterView(ReginsterView):
    """
    手机注册
    by: 尚宗凯 at:2015-03-19
    """
    template_name = 'webhtml/phone/register.html'


class UserCenterView(BaseView):
    '''
    用户中心
    by:范俊伟 at:2015-02-11
    修改基类
    by: 范俊伟 at:2015-03-11
    '''
    view_id = 'home'
    template_name = 'webhtml/user_center.html'
    need_site_permission = True

    def get_context_data(self, **kwargs):
        """
        获取参数
        by: 范俊伟 at:2015-02-14
        :param kwargs:
        :return:
        """
        orders = Order.objects.filter(user=self.request.user).order_by('-create_time')
        kwargs['orders'] = orders
        return super(UserCenterView, self).get_context_data(**kwargs)


class HtmlCommonView(BaseView):
    '''
    html页面通用视图
    by:范俊伟 at:2015-02-14
    修改基类
    by: 范俊伟 at:2015-03-11
    '''

    def get(self, request, *args, **kwargs):
        """
        get请求
        by: 范俊伟 at:2015-02-14
        增加kf_url模板参数
        by: 范俊伟 at:2015-05-11
        输出sessionid
        by: 范俊伟 at:2015-05-13
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        self.template_name = 'webhtml/html/' + kwargs.get('html_name') + '.html'
        kwargs['template_path'] = 'webhtml/templates/webhtml/html/' + kwargs.get('html_name') + '.html'
        kwargs['kf_url'] = settings.NEED_KF_BASE_URL
        kwargs['sessionid'] = request.session.session_key
        return super(HtmlCommonView, self).get(request, *args, **kwargs)


class HelpIndexAppleChecker(BaseView):
    """
    帮助首页,应付苹果审核
    by: 尚宗凯 at:2015-05-29
    """
    template_name = 'webhtml/phone/help/help_index_apple_checker.html'
    

class HelpIndex(BaseView):
    """
    帮助首页
    by: 尚宗凯 at:2015-04-24
    新版帮助
    by：尚宗凯 at：2015-05-27
    优化帮助页面
    by：尚宗凯 at：2015-05-28
    """
    template_name = 'webhtml/phone/help/help_index_v2.html'
    view_id = 'help'

    def get_context_data(self, **kwargs):
        agent = self.request.META.get("HTTP_USER_AGENT","")
        if agent.find("Android") != -1:
            help_menus = HelpMenu.objects.filter(parent_id=27, is_active=True)
        elif agent.find("iPhone") != -1:
            help_menus = HelpMenu.objects.filter(parent_id=63, is_active=True)
        else:
            help_menus = HelpMenu.objects.filter(parent_id=63, is_active=True)
        sub = []
        res = {"sub": sub}
        result = []
        for menu in help_menus:
            data = HelpContent.objects.filter(help_menu_id=menu.pk)
            if data.exists():
                if data.count() != 1:
                    sub.append({"is_menu":True,'menu_title': menu.title, 'menu_id': menu.pk, "menu_sorted": menu.sorted,"menu_desc": menu.desc, "menu_icon_url":menu.icon_url, "menu_parent_id":menu.parent_id })
                else:
                    content = HelpContent.objects.get(help_menu_id=menu.pk)
                    sub.append({'menu_title': menu.title, 'menu_id': menu.pk, "menu_sorted": menu.sorted, "menu_desc": menu.desc, "menu_icon_url":menu.icon_url, "menu_parent_id":menu.parent_id,
                                "content_title": content.title, "content_id": content.pk, "content_sorted": content.sorted,
                                })
        result.append(res)
        kwargs["result"] = result
        return super(HelpIndex, self).get_context_data(**kwargs)


class HelpVersion(BaseView):
    """
    版本介绍
    by: 尚宗凯 at:2015-04-24
    """
    template_name = 'webhtml/phone/help/help_version.html'
    view_id = 'help_version'

class HelpQuestion(BaseView):
    '''
    修改链接
    by: 尚宗凯 at:2015-04-20
    修改类名
    by: 尚宗凯 at:2015-04-24
    '''
    template_name = 'webhtml/phone/help/help3.html'
    # template_name = 'webhtml/phone/help/help_index.html'
    view_id = 'help_question'

    def get_context_data(self, **kwargs):
        result = []
        contents = HelpContent.objects.filter(is_active=True).values_list('id', 'title')
        sub = []
        res = { "sub": sub}
        for j in contents:
            sub.append({'title': j[1], 'id': j[0]})
        result.append(res)
        kwargs["result"] = result
        return super(HelpQuestion, self).get_context_data(**kwargs)


class HelpMenuDetailView(BaseView):
    """
    帮助详情
    by：尚宗凯 at：2015-05-05
    """
    template_name = 'webhtml/phone/help/help3.html'
    view_id = 'help_menu_detail'

    def get_context_data(self, **kwargs):
        help_menu_id = self.request.REQUEST['help_menu_id']
        result = []
        contents = HelpContent.objects.filter(help_menu_id=help_menu_id,is_active=True).values_list('id', 'title')
        sub = []
        res = {"sub": sub}
        for j in contents:
            sub.append({'title': j[1], 'id': j[0]})
        result.append(res)
        kwargs["result"] = result
        return super(HelpMenuDetailView, self).get_context_data(**kwargs)


class HelpSecondMenuView(BaseView):
    """
     四级目录中第二级目录
     by：尚宗凯 at：2015-05-12
    """
    # template_name = 'webhtml/phone/help/help3.html'
    template_name = 'webhtml/phone/help/help_second_menu.html'
    view_id = 'help_menu_parent'

    def get_context_data(self, **kwargs):
        """
        修改问题列表界面
        by:王健 at:2015-05-12
        :param kwargs:
        :return:
        """
        help_menu_parent_id = self.request.REQUEST.get('help_menu_parent_id')
        result = []
        menu = HelpMenu.objects.filter(parent_id=help_menu_parent_id,is_active=True).values_list('id', 'title', 'sorted')
        sub = []
        res = {"sub": sub}
        for j in menu:
            sub.append({'title': j[1], 'id': j[0], 'sorted': j[2], 'type': 'menu'})
        contents = HelpContent.objects.filter(help_menu_id=help_menu_parent_id, is_active=True).order_by('sorted').values_list('id', 'title', 'sorted')
        for j in contents:
            sub.append({'title': j[1], 'id': j[0], 'sorted': j[2], 'type': 'news'})
        sub.sort(lambda x, y: cmp(x['sorted'], y['sorted']))
        result.append(res)
        kwargs["result"] = result
        return super(HelpSecondMenuView, self).get_context_data(**kwargs)


class HelpThridMenuView(BaseView):
    """
     四级目录中第三级目录
     by：尚宗凯 at：2015-05-12
    """
    template_name = 'webhtml/phone/help/help_thrid_menu.html'
    view_id = 'help_thrid_menu_parent'

    def get_context_data(self, **kwargs):
        help_menu_parent_id = self.request.REQUEST['help_thrid_menu_parent_id']
        result = []
        menu = HelpMenu.objects.filter(parent_id=help_menu_parent_id,is_active=True).values_list('id', 'title')
        sub = []
        res = {"sub": sub}
        for j in menu:
            sub.append({'title': j[1], 'id': j[0]})
        result.append(res)
        kwargs["result"] = result
        return super(HelpThridMenuView, self).get_context_data(**kwargs)


# class HelpMenuView(BaseView):
#     """
#     帮助目录
#     by: 尚宗凯 at:2015-05-05
#     """
#     template_name = 'webhtml/phone/help/help_menu.html'
#     view_id = 'help_menu'
#
#     def get_context_data(self, **kwargs):
#         result = []
#         menu = HelpMenu.objects.filter(is_active=True).values_list('id', 'title')
#         sub = []
#         res = { "sub": sub}
#         for j in menu:
#             sub.append({'title': j[1], 'id': j[0]})
#         result.append(res)
#         kwargs["result"] = result
#         return super(HelpMenuView, self).get_context_data(**kwargs)


class HelpSearch(BaseView):
    """
    搜索结果页面
    by：尚宗凯 at：2015-04-19
    修改搜索不填内容时的结果
    by：尚宗凯 at：2015-05-07
    改为使用阿里云搜索
    by：尚宗凯 at：2015-06-01
    """
    template_name = 'webhtml/phone/help/search_result.html'
    view_id = 'help_search'

    def post(self, request, *args, **kwargs):
        w = request.REQUEST.get("w","")
        if not w:
            kwargs["result"] = None
            return self.get(request, *args, **kwargs)
        else:
            if ALI_OPEN_SEARCH_ON:
                url = "%s/ns/search?search_flag=help&query=%s" % (ALI_OPEN_SEARCH,w.strip())
                try:
                    jsonstr = urllib2.urlopen(url).read()
                    result = json.loads(jsonstr)
                    contents = result['result']['result'].get("items",[])
                except Exception as e:
                    print e
                    contents = []
            else:
                contents = HelpContent.search(w)
        result = []
        for i in contents:
            # help_menu_id = i.help_menu_id
            # menu_title = HelpMenu.objects.get(pk=help_menu_id).title
            if ALI_OPEN_SEARCH_ON:
                content_id = i["id"]
                content_title = i["title"]
            else:
                content_id = i.id
                content_title = i.title
            result.append({
                            # "menu_title": menu_title,
                           "content_id": content_id,
                           "content_title": content_title
                           })
        kwargs["result"] = result
        return self.get(request, *args, **kwargs)


class HelpDetail(BaseView):
    """
    手机帮助详情页
    by: 尚宗凯 at:2015-04-19
    更改展示方式
    by: 尚宗凯 at:2015-04-19
	优化代码
	by：尚宗凯 at：2015-06-01
    """

    template_name = 'webhtml/phone/help/help_detail.html'

    def get_context_data(self, **kwargs):
        help_content_id = self.request.REQUEST['help_content_id']
        if HelpContent.objects.filter(pk=help_content_id).exists():
            obj = HelpContent.objects.get(pk=help_content_id)
        else:
            obj = {"text":""}
        kwargs['obj'] = obj
        return super(HelpDetail, self).get_context_data(**kwargs)


class HelpMenuDetail(BaseView):
    """
    帮助menu页
    by：尚宗凯 at：2015-05-05
    """
    template_name = 'webhtml/phone/help/help_menu_detail.html'

    def get_context_data(self, **kwargs):
        help_menu_id = self.request.REQUEST['help_menu_id']
        obj = HelpMenu.objects.get(pk=help_menu_id)
        # kwargs['html'] = html
        kwargs['obj'] = obj
        return super(HelpMenuDetail, self).get_context_data(**kwargs)


def get_menu_by_father(menu_id, n, l, s):
    """
    根据父级菜单，查询子级菜单
    by:王健 at:2015-05-12
    优化获取菜单
    by:王健 at:2015-05-12
    :param menu_id:
    :param n:
    :param l:
    :param s:
    :return:
    """
    news = HelpContent.objects.filter(is_active=True, help_menu_id=menu_id).order_by('sorted')
    tmp_l = [(nn, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'*n, 'news') for nn in news]
    tl = []
    for m in HelpMenu.objects.filter(is_active=True, parent_id=menu_id).order_by('sorted'):
        if m.id not in s:
            tmp_l.append((m, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'*n, 'menu'))
            tl.append(m.id)
            s.add(m.id)
    tmp_l.sort(lambda x, y: cmp(x[0].sorted, y[0].sorted))
    if len(l) == 0:
        l.extend(tmp_l)
    else:
        flag = False
        for i, c in enumerate(l):
            if c[0].id == menu_id and isinstance(c[0], HelpMenu):
                for k, cc in enumerate(tmp_l):
                    l.insert(k+i+1, cc)
                flag = True
        if not flag:
            l.extend(tmp_l)
    for m_id in tl:
        get_menu_by_father(m_id, n + 1, l, s)
    return n+1


class HelpManager(BaseView):
    """
    使用帮助管理界面
    by:王健 at:2015-04-19
    """
    template_name = 'webhtml/phone/help/help_update.html'
    view_id = 'help_manager'

    def get_context_data(self, **kwargs):
        """
        组织菜单和新闻列表，优化缩进
        by:王健 at:2015-05-12
        :param kwargs:
        :return:
        """
        menulist = HelpMenu.objects.filter(is_active=True).order_by('sorted')
        l = []
        s = set()
        for m in menulist:
            if not m.parent_id:
                l.append((m, '', 'menu'))
                s.add(m.id)
                get_menu_by_father(m.pk, 1, l, s)

        kwargs['menulist'] = l
        return super(HelpManager, self).get_context_data(**kwargs)

    # @client_admin_login_required
    def get(self, request, *args, **kwargs):
        """
        get请求
        by:王健 at:2015-04-19
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        id = request.REQUEST.get('id')
        if not id:
            id = kwargs.get('id', '')
        if id:
            obj = HelpContent.objects.get(pk=id)
        else:
            obj = HelpContent()
        kwargs['obj'] = obj

        return super(HelpManager, self).get(request, *args, **kwargs)

    # @client_admin_login_required
    def post(self, request, *args, **kwargs):
        """
        post保存帮助信息
        by:王健 at:2015-04-19
        增加了一层目录结构
        by：尚宗凯 at：2015-05-12
        优化排序
        by:王健 at:2015-05-12
        """
        id = request.REQUEST.get('id')
        if id:
            obj = HelpContent.objects.get(pk=id)
        else:
            obj = HelpContent()
        obj.sorted = int(request.REQUEST.get('sorted', 0))
        obj.title = request.REQUEST.get('title')
        obj.text = request.REQUEST.get('content')
        obj.help_menu_id = request.REQUEST.get('menu_id')
        obj.save()
        kwargs['id'] = obj.pk
        return self.get(request, *args, **kwargs)


class HelpMenuManager(BaseView):
    """
    菜单管理接口
    by:王健 at:2015-05-12
    """
    template_name = 'webhtml/phone/help/help_menu_update.html'
    view_id = 'help_menu_manager'


    def get_context_data(self, **kwargs):
        """
        菜单获取列表
        by:王健 at:2015-05-12
        :param kwargs:
        :return:
        """
        menulist = HelpMenu.objects.filter(is_active=True).order_by('sorted')
        l = []
        s = set()
        for m in menulist:
            if not m.parent_id:
                l.append((m, '', 'menu'))
                s.add(m.id)
                get_menu_by_father(m.pk, 1, l, s)

        kwargs['menulist'] = l
        return super(HelpMenuManager, self).get_context_data(**kwargs)

    @client_admin_login_required
    def get(self, request, *args, **kwargs):
        """
        get请求
        by:王健 at:2015-05-12
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        id = request.REQUEST.get('id')
        if not id:
            id = kwargs.get('id', '')
        if id:
            obj = HelpMenu.objects.get(pk=id)
        else:
            obj = HelpContent()
        kwargs['obj'] = obj

        return super(HelpMenuManager, self).get(request, *args, **kwargs)

    @client_admin_login_required
    def post(self, request, *args, **kwargs):
        """
        post保存帮助信息
        by:王健 at:2015-05-12
        优化排序
        by:王健 at:2015-05-12
        加描述
        by：尚宗凯 at：2015-05-27
        """
        id = request.REQUEST.get('id')
        if id:
            obj = HelpMenu.objects.get(pk=id)
        else:
            obj = HelpMenu()
            # obj.sorted = HelpContent.objects.all().count()
        obj.sorted = int(request.REQUEST.get('sorted', 0))
        obj.title = request.REQUEST.get('title')
        obj.parent_id = request.REQUEST.get('menu_id')
        obj.desc = request.REQUEST.get('desc')
        obj.save()
        kwargs['id'] = obj.pk
        return self.get(request, *args, **kwargs)


@client_admin_login_required
def help_menu_delete(request):
    """
    帮助删除
    by:王健 at:2015-05-12
    """
    id = request.REQUEST.get("id")
    try:
        h = HelpMenu.objects.get(pk=id)
        if h.helpcontent_set.count() == 0:
            h.delete()
    except Exception as e:
        print e
    # return HttpResponseRedirect('/help_question')
    return HttpResponseRedirect('/helpupdate')


# def verification_code(request):
#     """
#     验证码功能
#     by:尚宗凯 at：2015-04-27
#     """
#     # ca =  Captcha(request)
#     # ca.words = ['hello','world','helloworld']
#     # ca.type = 'number'
#     # return ca.display()
#
#     figures = [1,2,3,4,5,6,7,8,9]
#     ca = Captcha(request)
#     ca.words = [''.join([str(random.sample(figures,1)[0]) for i in range(0,4)])]
#     ca.type = 'word'
#     if request.browserGroup == 'smart_phone':
#         ca.img_width = 100
#         ca.img_height = 30
#     else:
#         ca.img_width = 80
#         ca.img_height = 26
#     return ca.display()
#
#
# def check_verification_code(request):
#     _code = request.GET.get('code') or ''
#     if not _code:
#         return render('/',locals())
#     ca = Captcha(request)
#     if ca.check(_code):
#         return HttpResponse('验证成功')
#     else:
#         return HttpResponse('验证失败')

@client_admin_login_required
def help_delete(request):
    """
    帮助删除
    by：尚宗凯 at：2015-04-27
    修改跳转界面
    by:王健 at:2015-05-12
    """
    id = request.REQUEST.get("id")
    try:
        h = HelpContent.objects.get(pk=id)
        h.delete()
    except Exception as e:
        print e
    # return HttpResponseRedirect('/help_question')
    return HttpResponseRedirect('/helpupdate')


class NeedHelper(BaseView):
    """
    小助手
    by：尚宗凯 at：2015-04-03
    增加各种版本号适配
    by：尚宗凯 at：2015-04-07
    """
    # template_name = 'webhtml/phone/needhelper/gong_cheng_ri_zhi.html'

    view_id = 'need_helper'

    def get_context_data(self, **kwargs):
        flag = self.request.REQUEST['flag']
        version = self.request.REQUEST['version']
        # if version:
        # version = int(version)
        client_type = self.request.REQUEST['client_type']
        # if NeedHelperModel.get_url(file_group=flag, version=version, client_type=client_type):
        if version.find(".") != -1:  # 针对3.0.0这种版本号
            version = int(self.convert_version(version))
        elif int(version) >= 10000:  # 针对 30000处理方式
            version = int(version)
        else:  # 版本格式错误,返回一个默认版本
            version = 30000
        self.template_name = "webhtml/phone/needhelper/" + NeedHelperModel.get_url(file_group=flag, version=version,
                                                                                   client_type=client_type)
        return super(NeedHelper, self).get_context_data(**kwargs)

    def convert_version(self, version):
        tmp = version.split('.')
        try:
            a, b, c = tmp[0], tmp[1], tmp[2]
        except Exception as e:
            print e
            return ""
        if int(b) < 10:
            b = "0" + b
        if int(c) < 10:
            c = "0" + c
        return a + b + c






