# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import datetime
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import timezone

from needserver.forms import ProjectForm
from needserver.models import Group, Person, ProjectApply, Project, ProjectRechargeRecord, \
    ProjectPersonChangeRecord
from nsbcs.models import File
from submail.app_configs import MESSAGE_CONFIGS
from submail.message_xsend import MESSAGEXsend
from tongji.models import TongJi
from util import PROJECT_INFO, PROJECT_QUERY_LIST, MY_PROJECT_QUERY_LIST, USERINFO_INFO
from util.jsonresult import getResult, MyEncoder, getErrorFormResult
from util.loginrequired import client_login_required, login_project_manager_required, client_login_project_required
from django.conf import settings
from needserver.models import SGlog, ProjectMessage, FileRecord, RecordDate, GYSAddress, FileGroup, FileGroupJSON, \
    WuZiRecord, NSUser, NSPersonTel
from nsbcs.models import BaseFile, File
from webhtml.models import Order

__author__ = u'王健'


def guest_app_url(request):
    """
    根据用户使用的操作系统，来判断显示什么页面。
    ios手机端浏览器，跳转到 打开app或app store页面
    android 手机跳转到，打开app或 apk下载页面
    pc 浏览器，跳转到首页
    by：王健 at:2015-1-25
    名片二维码识别
    by：王健 at:2015-4-7
    测试服务器的 跳转到 住服务器
    by：王健 at:2015-4-16
    :param request:
    :return:
    """
    H_URL = 'www.tjeasyshare.com'
    agent = request.META.get('HTTP_USER_AGENT', '').lower()
    host = request.META.get('HTTP_HOST', '').lower()
    if host != H_URL:
        channel = request.REQUEST.get('channel', '')
        # return HttpResponseRedirect('http://%s/ns/guest_app_url?channel=%s' % (H_URL, channel))

    url = 'http://%s' % H_URL
    client_type = 'web'
    channel = request.REQUEST.get('channel', 'web')
    if agent.find('android') >= 0:
        url = settings.APK_DOWNLOAD_URL
        if channel != 'web' and channel != 'mingpian':
            url = settings.APK_DOWNLOAD_CHANNEL_URL % channel
        client_type = 'android'
    elif agent.find('iphone') >= 0 or agent.find('ipad') >= 0:
        url = settings.IOS_DOWNLOAD_URL
        client_type = 'ios'
    date = timezone.now()
    tongji, created = TongJi.objects.get_or_create(client_type=client_type, date=date, channel=channel)
    tongji.num += 1
    tongji.save(update_fields=['num'])
    if agent.find('micromessenger') >= 0:
        url = settings.WECHAT_DOWNLOAD_URL
    return HttpResponseRedirect(url)


def show_channel_tongji(request):
    """
    显示各个频道的统计
    by:王健 at:2015-4-3
    :param request:
    :return:
    """
    now_date = request.REQUEST.get('date', '')
    days = int(request.REQUEST.get('days', '7'))
    if not now_date:
        now_date = timezone.now()
    else:
        now_date = datetime.datetime.strptime(now_date, "%Y-%m-%d")
    start_date = now_date - datetime.timedelta(days=days)

    l = TongJi.objects.filter(date__gt=start_date, date__lte=now_date).order_by('-date')
    return render_to_response('tongji/tongji.html', {'tjlist': l})
