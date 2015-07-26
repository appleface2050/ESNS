# coding=utf-8
# Date:2015/01/13
# Email:wangjian2254@icloud.com

import time
import urllib2
import json
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache

from needserver.models import SysMessage, Group, ProjectMessage, NeedMessage, NSUser,NeedMessageRead, \
    LastReadTimeProjectSysMessage
from util import RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE, RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER
from util.jsonresult import getResult, MyEncoder
from util.loginrequired import client_login_project_required, client_login_required_widthout_tel
from Need_Server.settings import NEED_MESSAGE_TYPE,NEED_MESSAGE_STATUS,CUSTOMER_SERVICE_MESSAGE


__author__ = u'王健'

def create_sysmessage_and_push(project_id, group_id, user_id, title, text):
    """
    创建系统消息并且推送给手机端，先做创建系统消息
    by:王健 at:2015-2-26
    :param project_id:
    :param group_id:
    :param user_id:
    :param title:
    :param text:
    :return:
    """
    msg = SysMessage()
    msg.project_id = int(project_id)
    if group_id:
        msg.to_group_id = int(group_id)
    if user_id:
        msg.user_id = int(user_id)
    msg.title = title
    msg.text = text
    msg.save()
    return msg

@client_login_required_widthout_tel
@transaction.atomic()
def create_sysmessage(request):
    """
    创建系统消息
    by:王健 at:2015-2-26
    """
    project_id = request.REQUEST.get('project_id')
    group_id = request.REQUEST.get('group_id')
    user_id = request.REQUEST.get('user_id')
    title = request.REQUEST.get('title')
    text = request.REQUEST.get('text')

    msg = create_sysmessage_and_push(project_id, group_id, user_id, title, text)

    return getResult(True, u'创建系统消息成功', MyEncoder.default(msg))



@client_login_project_required
def query_sysmessage(request, project_id=None):
    """
    根据项目查询系统消息
    by:王健 at:2015-2-26
    优化系统消息查询接口
    by:王健 at:2015-4-13
    增加刷新最后阅读系统消息时间
    by：尚宗凯 at：2015-05-08
    删除缓存
    by：尚宗凯 at：2105-05-22
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    group_id = request.REQUEST.get('group_id')
    l = SysMessage.objects.filter(project_id=project_id)
    if timeline:
        l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
    else:
        l = l.order_by('-timeline')
    if group_id:
        l = l.filter(Q(user_id=request.user.pk) | Q(user=None) | Q(to_group_id=group_id))
    else:
        l = l.filter(to_group_id=None).filter(Q(user_id=request.user.pk) | Q(user=None))
    user_id = request.user.pk
    LastReadTimeProjectSysMessage.update_last_read_timeline(type="sysmessage", user_id=user_id, project_id=project_id,group_id=group_id)
    cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("sysmessage", user_id, project_id, None))
    return getResult(True, u'获取系统消息', MyEncoder.default(l[:20]))


@client_login_project_required
def query_sysmessage_old(request, project_id=None):
    """
    根据项目查询系统消息旧数据
    by:王健 at:2015-2-26
    优化系统消息查询接口
    by:王健 at:2015-4-13
    增加刷新最后阅读系统消息时间
    by：尚宗凯 at：2015-05-08
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    group_id = request.REQUEST.get('group_id')
    l = SysMessage.objects.filter(project_id=project_id)
    if timeline:
        l = l.filter(timeline__lt=int(timeline)).order_by('-timeline')
    else:
        l = l.order_by('-timeline')

    if group_id:
        l = l.filter(Q(user_id=request.user.pk) | Q(user=None) | Q(to_group_id=group_id))
    else:
        l = l.filter(to_group_id=None).filter(Q(user_id=request.user.pk) | Q(user=None))
        LastReadTimeProjectSysMessage.update_last_read_timeline(type="sysmessage", user_id=request.user.pk, project_id=project_id,group_id=group_id)
    return getResult(True, u'获取系统消息', MyEncoder.default(l[:20]))


@client_login_project_required
@transaction.atomic()
def create_project_message(request, project_id=None):
    """
    创建项目公告，根据分组
    by:王健 at:2015-2-26
    标题和内容不能为空
    by：尚宗凯 at：2015-05-04
    创建项目公告时刷新最后一次阅读时间
    by: 尚宗凯 at：2015-05-08
    创建项目公告更新最后阅读时间
    by：尚宗凯 at：2105-05-21
    """
    group_id = request.REQUEST.get('group_id')
    text = request.REQUEST.get('text')
    title = request.REQUEST.get('title')
    if title == "":
        return getResult(False, u'标题不能为空', status_code=2)
    if text == "":
        return getResult(False, u'内容不能为空', status_code=2)

    group = Group.objects.get(pk=group_id, project_id=project_id)
    if group.say_members.filter(id=request.user.id).exists():
        msg = ProjectMessage()
        msg.project_id = int(project_id)
        msg.to_group = group
        msg.user = request.user
        msg.title = title
        msg.text = text
        msg.save()
        LastReadTimeProjectSysMessage.update_last_read_timeline(type="project_message", user_id=request.user.pk, project_id=project_id,group_id=group_id)
        cache.set(RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE % ("project_message", project_id, group_id), msg.timeline, settings.CACHES_TIMEOUT)
        return getResult(True, u'发布公告成功', MyEncoder.default(msg))
    else:
        return getResult(False, u'您不具有发布公告的权限', status_code=8)


@client_login_project_required
def query_project_message(request, project_id=None):
    """
    根据项目查询分组公告消息
    by:王健 at:2015-2-26
    增加刷新最后一次阅读项目公告时间
    by：尚宗凯 at：2015-05-08
    删除缓存
    by：尚宗凯 at：2105-05-22
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    group_id = request.REQUEST.get('group_id')
    l = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id)
    if timeline:
        l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
    else:
        l = l.order_by('-timeline')
    user_id = request.user.pk
    LastReadTimeProjectSysMessage.update_last_read_timeline(type="project_message", user_id=user_id, project_id=project_id,group_id=group_id)
    cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message", user_id, project_id, None))
    return getResult(True, u'获取公告', MyEncoder.default(l[:20]))


@client_login_project_required
def query_project_message_old(request, project_id=None):
    """
    根据项目查询分组公告旧数据
    by:王健 at:2015-2-26
    增加刷新最后一次阅读项目公告时间
    by：尚宗凯 at：2015-05-08
    删除缓存
    by：尚宗凯 at：2105-05-22
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    group_id = request.REQUEST.get('group_id')
    l = ProjectMessage.objects.filter(project_id=project_id, to_group_id=group_id)
    if timeline:
        l = l.filter(timeline__lt=int(timeline)).order_by('-timeline')
    else:
        l = l.order_by('-timeline')
    user_id = request.user.pk
    LastReadTimeProjectSysMessage.update_last_read_timeline(type="project_message", user_id=user_id, project_id=project_id,group_id=group_id)
    cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER % ("project_message", user_id, project_id, group_id))
    return getResult(True, u'获取公告', MyEncoder.default(l[:20]))


# @client_login_required_widthout_tel
# @transaction.atomic()
# def create_needmessage(request):
#     """
#     创建用户消息
#     by:尚宗凯 at:2015-3-31
#     增加字段
#     by:尚宗凯 at:2015-4-1
#     修改返回结果
#     by:尚宗凯 at:2015-4-1
#     修改bug
#     by:尚宗凯 at:2015-4-1
#     增加消息自动回复
#     by：尚宗凯 at：2015-04-13
#     """
#     title = request.REQUEST.get('title', '')
#     text = request.REQUEST.get('text', '')
#     create_user_id = request.REQUEST.get('create_user_id', '')
#     to_user_id = request.REQUEST.get('to_user_id', '')
#     type = request.REQUEST.get('type', '')
#     if type != ' ':
#         type = int(type)
#     try:
#         assert type in NEED_MESSAGE_TYPE
#         msg = NeedMessage()
#         if type:
#             msg.type = type
#         if title:
#             msg.title = title
#         if text:
#             msg.text = text
#         if create_user_id:
#             msg.create_user = NSUser.objects.get(pk=create_user_id)
#         else:
#             user = request.user
#             msg.create_user = user
#         if to_user_id:
#             user = NSUser.objects.get(pk=int(to_user_id))
#             msg.to_user = user
#         msg.save()
#
#         NeedMessage.create_customer_service_message(user.pk,"title",CUSTOMER_SERVICE_MESSAGE['auto_reply'])
#         return getResult(True, u'创建NEED消息成功', MyEncoder.default(msg))
#     except Exception as e:
#         print e
#         return getResult(False, u'创建NEED消息失败', MyEncoder.default(msg))

@client_login_required_widthout_tel
def create_needmessage(request):
    """
    创建用户消息
    by:尚宗凯 at:2015-5-29
    """
    session_key = request.session.session_key
    text = request.REQUEST.get("text","")
    jsonstr = urllib2.urlopen(settings.NEED_KF_BASE_URL+'/kf/create_needmessage?sessionid=%s&text=%s' % (session_key, text)).read()
    result = json.loads(jsonstr)
    return getResult(result['success'], result['message'], result)


def query_need_message(request):
    """
    查询用户消息
    by:尚宗凯 at:2015-5-29
    """
    session_key = request.session.session_key
    jsonstr = urllib2.urlopen(settings.NEED_KF_BASE_URL+'/kf/create_needmessage?sessionid=%s' % (session_key)).read()
    result = json.loads(jsonstr)
    return getResult(result['success'], result['message'], result)


# def query_need_message(request):
#     """
#     查询用户消息
#     by:尚宗凯 at:2015-3-31
#     增加字段
#     by:尚宗凯 at:2015-4-1
# 	添加默认使用登陆用户查询
# 	by:尚宗凯 at:2015-4-1
# 	增加返回字段
# 	by:尚宗凯 at:2015-4-2
# 	修改warning, 完善代码
# 	by：尚宗凯 at：2015-4-3
# 	增加query后标明已读功能
# 	by：尚宗凯 at：2015-4-9
# 	去掉已读功能
# 	by：尚宗凯 at：2015-4-10
# 	增加不显示已阅读信息功能
# 	by：尚宗凯 at：2015-4-14
# 	解决存在的bug
# 	by：尚宗凯 at：2015-4-14
#     """
#     timeline = request.REQUEST.get('timeline', '0')
#     if timeline != '':
#         timeline = int(timeline)
#     create_user = request.REQUEST.get('create_user_id', '')
#     to_user = request.REQUEST.get('to_user_id', '')
#     title = request.REQUEST.get('title', '')
#     status = request.REQUEST.get('status', '')
#
#     if not create_user:
#         create_user = request.user
#     else:
#         create_user = NSUser.objects.get(pk=create_user)
#     if not to_user:
#         to_user = request.user
#     else:
#         to_user = NSUser.objects.get(pk=to_user)
#     if status != '':
#         status = int(status)
#     type = request.REQUEST.get('type', '')
#     if type != '':
#         type = int(type)
#     l = NeedMessage.objects.all()
#     if status:
#         l = l.filter(status=status)
#     if type:
#         l = l.filter(type=type)
#     if title:
#         l = l.filter(title=title)
#     if create_user and to_user:
#         l = l.filter(Q(create_user=create_user)|Q(to_user=to_user))
#     elif create_user:
#         l = l.filter(create_user=create_user)
#     elif to_user:
#         l = l.filter(to_user=to_user)
#     create_user_read_timeline = NeedMessageRead.get_user_timeline(create_user.pk)
#     to_user_read_timeline = NeedMessageRead.get_user_timeline(to_user.pk)
#
#     if create_user_read_timeline:
#         l = l.filter(timeline__gt=int(create_user_read_timeline))
#     if to_user_read_timeline:
#         l = l.filter(timeline__gt=int(to_user_read_timeline))
#
#     if timeline:
#         l = l.filter(timeline__gt=int(timeline)).order_by('timeline')
#     else:
#         l = l.order_by('-timeline')
#     res = []
#     if l:
#         for i in l[:20]:
#             tmp = i.toJSON()
#             # if tmp['create_user'] and NSUser.objects.get(pk=tmp['create_user']).icon_url:
#             if i.create_user and i.create_user.icon_url:
#                 tmp['create_user_icon_url'] = i.create_user.icon_url.get_url()
#                 tmp['create_user_name'] = i.create_user.name
#             else:
#                 tmp['create_user_icon_url'] = ""
#
#             if i.to_user and i.to_user.icon_url:
#                 tmp['to_user_icon_url'] = i.to_user.icon_url.get_url()
#                 tmp['to_user_name'] = i.to_user.name
#             else:
#                 tmp['to_user_icon_url'] = ""
#             res.append(tmp)
#             # i.set_status_read()
#     return getResult(True, u'获取NEED消息', res)
#     # return getResult(True, u'获取NEED消息', MyEncoder.default(l[:20]))

@client_login_required_widthout_tel
@transaction.atomic()
def read_needmessage(request):
    """
    读取need消息
    by：尚宗凯 at：2015-04-14
    """
    try:
        nmr ,create = NeedMessageRead.objects.get_or_create(user_id=request.user.pk)
        if create:
            nmr = NeedMessageRead()
            nmr.user = NSUser.objects.get(pk=request.user.pk)
            nmr.timeline = int(time.time())
            nmr.save()
        else:
            nmr.timeline = int(time.time())
            nmr.save()
        return getResult(True, u'成功上传刷新阅读时间', MyEncoder.default(nmr))
    except Exception as e:
        print e
        return getResult(False, u'上传刷新阅读时间失败', status_code=4)