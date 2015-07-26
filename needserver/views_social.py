# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import json
import urllib
import urllib2
import time

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone


# from riliusers.views_user import setLoginOrg
from needserver.jifenutil import create_data_jifen
from needserver.models import Social, Project, Person, Group
from util.jsonresult import getResult
from util.loginrequired import client_login_required, client_login_required_widthout_tel
from Need_Server.settings import BAE_AK, BAE_SK, FENXIANG

__author__ = u'王健'


def client_social_callback(request):
    """
    手机端 社会化注册
    by:王健 at:2015-1-15
    手机端 社会化注册，优化
    by:王健 at:2015-1-25
    :param request:
    :return:
    """
    result, social = social_callback(request, 'client')
    if result:
        return HttpResponseRedirect('/ns/client_social_result?result=true&media_type=%s&media_uid=%s&key=%s' % (social.media_type, social.media_uid, social.expires_in))

    else:
        return HttpResponseRedirect('/ns/client_social_result?result=false')


def client_social_result(request):
    """
    手机端 社会化注册, 结果页
    by:王健 at:2015-1-25
    :param request:
    :return:
    """
    return HttpResponse()



def client_add_social_callback(request):
    """
    手机端 社会化账号 绑定
    by:王健 at:2015-1-15
    手机端 社会化绑定，优化
    by:王健 at:2015-1-25
    :param request:
    :return:
    """
    result, social = social_callback(request, 'client_add')
    # result, social = social_callback(request, 'client')
    if result:
        return HttpResponseRedirect('/ns/client_social_result?result=true&media_type=%s&media_uid=%s&key=%s' % (social.media_type, social.media_uid, social.expires_in))

    else:
        return HttpResponseRedirect('/ns/client_social_result?result=false')



def web_social_callback(request):
    """
    web端社会化注册
    by:王健 at:2015-1-15
    :param request:
    :return:
    """
    result, social = social_callback(request, 'web')
    if result:
        if social.user.tel == None:
            return HttpResponseRedirect('/web/reg_tel')
        else:
            return HttpResponseRedirect('/web/')
    else:
        return HttpResponseRedirect(social)


@client_login_required
def web_add_social_callback(request):
    """
    web端社会化，绑定社会化账号
    by:王健 at:2015-1-16
    :param request:
    :return:
    """
    result, social = social_callback(request, 'web_add')
    if result:
        return HttpResponseRedirect('/web/')
    else:
        return HttpResponseRedirect(social)


def social_callback(request, client='client'):
    """
    社会化登陆的回调接口
    by:王健 at:2015-1-3
    设置失败后的 url，不同的客户端有不同的url
    by:王健 at:2015-1-15
    防止None被split
    by:王健 at:2015-3-18
    解决百度社会化登陆问题
    by:尚宗凯 at:2015-4-1
    百度社会化登陆去掉头像设置
    by:尚宗凯 at:2015-4-1
    根据客户端访问的 host变化
    by:尚宗凯 at:2015-4-3
    :param request:
    :return:
    """
    code = request.REQUEST.get('code')
    state = request.REQUEST.get('state', '')
    url = 'http://openapi.baidu.com/social/oauth/2.0/token'
    host = request.META.get('HTTP_HOST', '').lower()
    values = {'grant_type': 'authorization_code',
              'code': code,
              'client_id': BAE_AK,
              'client_secret': BAE_SK,
              # 'redirect_uri': 'http://needserver.duapp.com/ns/%s_social_callback' % client}
              'redirect_uri': 'http://%s/ns/%s_social_callback' % (host, client)
    }

    timeline = int(time.mktime(timezone.now().timetuple()))
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    html = response.read()
    result = json.loads(html)
    if result.has_key("error_code"):
        url = 'https://openapi.baidu.com/social/oauth/2.0/authorize?response_type=code&state=%s&client_id=SyeExPLiXrkTwBK9GUYFLAok&redirect_uri=http://%s/ns/%s_social_callback&media_type=%s' % (
            state, host, client, state.split('_')[0])
        return False, url


    #判断是否已经具有社会化登陆了，没有就新建
    if not Social.objects.filter(media_type=result.get('media_type'), media_uid=result.get('media_uid'),
                                 social_uid=result.get('social_uid')).exists():
        if request.user.is_authenticated():
            user = request.user
        else:
            user = get_user_model()()
            user.name = result.get('name')
            user.save()
        social = Social()
        social.user = user
        social.token = result.get('access_token')
        social.expires_in = timeline + result.get('expires_in', 0)
        social.media_type = result.get('media_type')
        social.media_uid = result.get('media_uid')
        social.social_uid = result.get('social_uid')
        social.session_key = result.get('session_key')
        social.session_secret = result.get('session_secret')
        social.save()
    else:
        social = Social.objects.get(media_type=result.get('media_type'), media_uid=result.get('media_uid'),
                                    social_uid=result.get('social_uid'))
        social.token = result.get('access_token')
        social.expires_in = timeline + result.get('expires_in', 0)
        social.session_key = result.get('session_key')
        social.session_secret = result.get('session_secret')
        social.save()
        user = social.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)
    # 判断是否带有 邀请标记，带有的话，就加入对应项目的root组
    if state.find('_project_') > 0 and len(state.split('_project_')) == 2:
        flag = state.split('_project_')[1]
        orgquery = Project.objects.filter(flag=flag)
        if orgquery.exists():
            org = orgquery[0]
            if Person.objects.filter(user=user, project=org, is_active=True).count() == 0:
                person, created = Person.objects.get_or_create(user=request.user, org=org)
                person.is_active = True
                person.save()
                group = Group.objects.get(project=org, flag='root')
                group.look_members.add(request.user)
                group.save()
    #如果用户没有头像，给用户下载一个头像
    # if not user.icon_url:
    #     userinfo_url = 'https://openapi.baidu.com/social/api/2.0/user/info?access_token=%s' % result.get('access_token')
    #     response_userinfo = urllib2.urlopen(userinfo_url)
    #     html_userinfo = response_userinfo.read()
    #     result_userinfo = json.loads(html_userinfo)
    #     if result_userinfo.has_key('tinyurl'):
    #         user.icon_url = result_userinfo.get('tinyurl')
    #         user.save()


    return True, social



@client_login_required
def get_user_social_list(request):
    p = []
    for social in request.user.social_set.all():
        p.append({'type': social.media_type, 'time': social.expires_in, 'token': social.token})
    return getResult(True, '', p)


@client_login_required
def send_social_success(request):
    """
    分享社交软件获取积分
    by:王健 at:2015-2-5
    :param request:
    :return:
    """
    return getResult(True, '', None, jifen=create_data_jifen(request, FENXIANG))

#
# @client_login_required
# def add_social_callback(request):
#     code = request.REQUEST.get('code')
#     state = request.REQUEST.get('state')
#     url = 'http://openapi.baidu.com/social/oauth/2.0/token'
#     values = {'grant_type': 'authorization_code',
#               'code': code,
#               'client_id': BAE_AK,
#               'client_secret': BAE_SK,
#               'redirect_uri': 'http://liyuoa.duapp.com/riliusers/add_social_callback'}
#     timeline = int(time.mktime(timezone.now().timetuple()))
#     data = urllib.urlencode(values)
#     req = urllib2.Request(url, data)
#     response = urllib2.urlopen(req)
#     html = response.read()
#     result = json.loads(html)
#     if state.find('_user_') > 0 and len(state.split('_user_')) == 2:
#         flag = state.split('_user_')[1]
#     if result.has_key("error_code"):
#         url = 'https://openapi.baidu.com/social/oauth/2.0/authorize?response_type=code&state=%s&client_id=SyeExPLiXrkTwBK9GUYFLAok&redirect_uri=http://liyuoa.duapp.com/riliusers/add_social_callback&media_type=%s&t=%s' % (
#             state, state.split('_')[0],timeline)
#         # return HttpResponse(u'请先登录账号，再绑定社交账号。<a href="%s">继续</a> %s'% (url, result.get('error_code')))
#         return HttpResponseRedirect(url)
#     try:
#         social = Social.objects.get(social_uid=result.get('social_uid'))
#     except:
#         social = Social()
#         social.user = chatlogin.person.user
#     # social, created = Social.objects.get_or_create(user_id=chatlogin.person.user_id,
#     #                                                media_type=result.get('media_type'),
#     #                                                media_uid=result.get('media_uid'),
#     #                                                social_uid=result.get('social_uid'))
#     if social.user == chatlogin.person.user:
#         user = social.user
#         social.token = result.get('access_token')
#         social.expires_in = timeline + result.get('expires_in', 0)
#         social.media_type = result.get('media_type')
#         social.media_uid = result.get('media_uid')
#         social.social_uid = result.get('social_uid')
#         social.session_key = result.get('session_key')
#         social.session_secret = result.get('session_secret')
#         social.save()
#     else:
#         return HttpResponse(u'该社交账号已经，绑定了另外一个账号。<a href="http://%s">返回首页</a>'% request.get_host())
#     if not user.icon:
#         userinfo_url = 'https://openapi.baidu.com/social/api/2.0/user/info?access_token=%s' % result.get('access_token')
#         response_userinfo = urllib2.urlopen(userinfo_url)
#         html_userinfo = response_userinfo.read()
#         result_userinfo = json.loads(html_userinfo)
#         if result_userinfo.has_key('tinyurl'):
#             user.icon = result_userinfo.get('tinyurl')
#             user.save()
#             for p in user.person_set.all():
#                 if not p.icon:
#                     p.icon = user.icon
#                     p.save()
#     from util.jsonresult import cache
#     import uuid
#     uuid_flag = str(uuid.uuid4())
#     cache.set(uuid_flag, social.social_uid, 60 * 10)
#     return HttpResponseRedirect('/?uuid_flag=%s' % uuid_flag)

#
# @client_login_required
# def add_social_code(request):
#     media_type = request.REQUEST.get('media_type')
#     from util.jsonresult import cache
#     import uuid
#
#     uuid_flag = str(uuid.uuid4())
#     cache.set(uuid_flag, request.user.id, 60 * 10)
#     url = 'https://openapi.baidu.com/social/oauth/2.0/authorize?response_type=code&state=%s_user_%s&client_id=SyeExPLiXrkTwBK9GUYFLAok&redirect_uri=http://liyuoa.duapp.com/riliusers/add_social_callback&media_type=%s' % (
#         media_type, uuid_flag, media_type)
#     return HttpResponseRedirect(url)

#
# def assk_callback(request):
#     return getResult(True, '', "assk_callback")
#
#
# def third_callback(request):
#     return getResult(True, '', "third_callback")
#
#
# def yanzheng(request):
#     return HttpResponse('87407z1pWYlOEwXaITaLuFVzBlA')