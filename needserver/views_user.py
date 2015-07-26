# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import json
import logging
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth import get_user_model
from django.db import transaction
import time
from needserver.forms import UserInfoForm
from needserver.jifenutil import login_jifen, query_fen_by_uid

from needserver.models import Social, Person, Project, Group, FileGroup, NSPersonTel, NSUser, SMSCounter, NeedMessage
from needserver.views_project import del_person_by_project
from nsbcs.models import BaseFile, QN_FRIENDS_ICON_BUCKET
from util import USERINFO_INFO, PROJECT_GROUP_LIST, PROJECT_PERSON_LIST, MY_PROJECT_QUERY_LIST, \
    RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE, PROJECT_GROUP_USER
from util.jsonresult import getResult, getErrorFormResult, MyEncoder
from util.loginrequired import client_login_required, client_login_required_widthout_tel, client_login_project_required, \
    login_project_manager_required
from submail.message_xsend import MESSAGEXsend
from submail.app_configs import MESSAGE_CONFIGS
from django.conf import settings
from needserver.models_view import VNSUseruUserInfoPersonBaseFile
from django.core.cache import cache
from Need_Server.settings import SYS_MESSAGE

__author__ = u'王健'

#修改个人信息
#by:王健 at:2015-3-2
#USERINFOATTR增加phrase
#by:尚宗凯 at:2015-3-24
USERINFOATTR = ('birthday', 'address', 'xueli', 'zhicheng', 'zhiyezigezheng', 'company', 'title', 'department', 'qq', 'email', 'phrase')
GROUP_TYPE = ['sys_manage', 'sys_xzzg', 'sys_jsdw', 'sys_sjdw', 'sys_kcdw', 'sys_jldw', 'sys_sgdw', 'sys_xmjl', 'sys_lwfbdw', 'sys_zyfbdw']
GROUP_TYPE_DW = ['sys_xzzg', 'sys_jsdw', 'sys_sjdw', 'sys_kcdw', 'sys_jldw', 'sys_sgdw', 'sys_lwfbdw', 'sys_zyfbdw']

def login_page(request):
    return render_to_response('login.html')


def logout(request):
    auth_logout(request)
    return getResult(True, '')


def login(request):
    """
    登陆, uuid_flag 是从社会化登陆跳转过来的登陆
    by:王健 at:2015-1-3
    所有username 都改为 tel
    by:王健 at:2015-1-8
    社会化登陆，校验手机号是否验证
    by:王健 at:2015-1-15
    登录后 返回用户信息
    by:王健 at:2015-1-16
    修改个人信息返回值
    by:王健 at:2015-1-20
    修改社会化登陆
    by:王健 at:2015-1-25
    :param request:
    :return:
    """
    media_type = request.REQUEST.get('media_type')
    media_uid = request.REQUEST.get('media_uid')
    key = request.REQUEST.get('key')
    if media_type and media_uid:
        social = Social.objects.get(media_type=media_type, media_uid=media_uid)
        if str(social.expires_in) != str(key):
            return getResult(False, u'社会化登陆过期,请重新登陆', None)
        user = social.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        if request.user.tel is None:
            return getResult(False, u'请登记手机号。', None, status_code=9)
        return getResult(True, u'登录成功', None)

    tel = request.REQUEST.get('tel')
    if not tel:
        return getResult(False, u'登录失败，请重新再试', None)
    try:
        int(tel)
        user = authenticate(tel=tel, password=request.REQUEST.get('password'))
    except:
        return getResult(False, u'用户名密码错误', None)
    if user and not user.is_active:
        return getResult(False, u'用户已经停止使用。')
    elif not user:
        return getResult(False, u'用户名密码错误', None)
    else:
        auth_login(request, user)
        return getResult(True, u'登录成功', request.user.get_user_map(True))


@client_login_required
@transaction.atomic()
def change_password(request):
    """
    修改密码
    by:王健 at:2015-1-3
    修改用户停用的逻辑
    by:尚宗凯 at:2015-5-5
    将修改密码成功改为重置密码成功
    by：尚宗凯 at:2015-05-14
	改一下文字
	by：尚宗凯 at:2015-05-14
    """
    # tel = request.REQUEST.get('tel')
    if not request.user.is_active:
        return getResult(False, u'用户已经停止使用。')
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        request.user.set_password(request.REQUEST.get('newpassword'))
        request.user.save(update_fields=['password'])

        return getResult(True, u'重置密码成功', None)
    else:
        return getResult(False, u'用户名密码错误', None)


@transaction.atomic()
def enforce_reset_password(request):
    """
    强制重设密码
    by：尚宗凯 at：2015-05-14
    :param request:
    :return:
    """
    tel = request.REQUEST.get('tel')
    if not tel:
        return getResult(False, u'手机号不能为空。')
    try:
        if not NSUser.objects.filter(tel=tel).exists():
            return getResult(False, u'该账号不存在。')
        else:
            user = NSUser.objects.get(tel=tel)
            if not user.is_active:
                return getResult(False, u'用户已经停止使用。')
            user.set_password("123456")
            user.save()
            # user.backend = 'django.contrib.auth.backends.ModelBackend'
            # auth_login(request, user)
            return getResult(True, u'修改密码成功', None)
    except:
        return getResult(True, u'修改密码失败', None)

@transaction.atomic()
def forget_password(request):
    """
    重置密码接口
    by：尚宗凯 at：2015-05-05
    修改用户已停止使用bug
    by：尚宗凯 at：2015-05-05
    将修改密码成功改为重置密码成功
    by：尚宗凯 at:2015-05-14
	改一下文字
	by：尚宗凯 at:2015-05-14
    :param request:
    :return:
    """
    kwargs = {}
    kwargs.update(request.POST.dict())
    tel = request.REQUEST.get('tel')
    sms_code = request.REQUEST.get('sms_code')
    password = request.REQUEST.get('password')
    if not tel:
        return getResult(False, u'手机号不能为空。')
    if not sms_code:
        return getResult(False, u'短信验证码不能为空。')
    if not password:
        return getResult(False, u'密码不能为空。')

    if not request.session.get('smscode', None):
        return getResult(False, u'未发送短信验证码。')
    if tel != request.session.get('smstel', None):
        return getResult(False, u'发送验证码的手机号，和注册的手机号不符合。')
    if sms_code != request.session.get('smscode', None):
        return getResult(False, u'短信验证码错误。')
    try:
        if not NSUser.objects.filter(tel=tel).exists():
            return getResult(False, u'该账号不存在。')
        else:
            user = NSUser.objects.get(tel=tel)
            if not user.is_active:
                return getResult(False, u'用户已经停止使用。')
            user.set_password(password)
            user.save()
            request.session['smscode'] = None
            request.session['smstel'] = None
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            return getResult(True, u'重置密码成功', None)
    except:
        return getResult(True, u'修改密码失败', None)


@client_login_required
def get_upload_user_icon_url(request):
    """
    获取上传项目图标的url
    by：王健 at:2015-1-28
    上传到七牛
    by: 范俊伟 at:2015-04-14
    修改 获取url的函数，无需参数
    by: 王健 at:2015-04-14
    :param request:
    :param project_id:
    :return:
    """
    from nsbcs.views_bcsfile import create_user_icon_fileobj
    fileobj = create_user_icon_fileobj(request)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_post_url(), 'puturl': fileobj.get_put_url()})

@client_login_required
def get_qn_upload_user_icon_url(request):
    """
    七牛云存储接口,获取上传项目图标的url
    by: 范俊伟 at:2015-04-08
    :param request:
    :param project_id:
    :return:
    """
    from nsbcs.views_bcsfile import create_user_icon_fileobj
    fileobj = create_user_icon_fileobj(request,bucket=QN_FRIENDS_ICON_BUCKET)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})

@client_login_required
@transaction.atomic()
def update_user_icon_url(request):
    """
    获取上传项目图标的url
    by：王健 at:2015-1-28
    解决用户被删除的bug
    by:王健 at:2015-2-5
    解决用户被删除的bug
    by:范俊伟 at:2015-2-9
    :param request:
    :param project_id:
    :return:
    """
    fileid = request.REQUEST.get('fileid')
    if fileid:
        fileobj = get_object_or_404(BaseFile, pk=fileid)
        fileobj.file_status = True
        fileobj.save()
        old_icon = None
        if fileobj.user.icon_url:
            old_icon = fileobj.user.icon_url
        fileobj.user.icon_url = fileobj
        fileobj.user.save()
        if old_icon:
            old_icon.delete()
        return getResult(True, u'上传成功', None)
    else:
        return getResult(False, u'没有上传文件id', None)


@client_login_required
@transaction.atomic()
def update_userinfo(request):
    """
    修改个人信息
    by:王健 at:2015-1-3
    修改个人相关的信息，新增加了UserInfo表
    by:王健 at:2015-1-18
    修复只传递一个参数时，把其他参数覆盖为空的bug
    by:王健 at:2015-1-19
    修改个人信息返回值
    by:王健 at:2015-1-20
    user 修改过后都更新person的timeline
    by:王健 at:2015-1-25
    user 修改导致的 person更新，插入到 user的save方法中
    by:王健 at:2015-1-28
    添加 nickname的修改
    by:王健 at:2015-3-2
    优化个人信息更新和获取
    by:王健 at:2015-3-9
    解决 缓存不一致问题
    by:王健 at:2015-3-10
    解决缩进错误
    by:尚宗凯 at:2015-3-26
    学历为空做特殊处理
    by：尚宗凯 at：2015-05-13
    项目的超级管理员名字改变，项目的信息也会变，项目的时间戳更新
    by:王健 at:2015-05-21
    is None 判断错误
    by:王健 at:2015-05-21
    增加realname设置
    by：尚宗凯 at：2015-06-26
    """
    user = request.user
    user_flag = False
    if request.REQUEST.has_key('name'):
        user.name = request.REQUEST.get('name')
        for p in Project.objects.filter(manager_id=user.pk):
            p.updatetimeline()
        user_flag = True
    if request.REQUEST.has_key('nickname'):
        user.nickname = request.REQUEST.get('nickname')
        user_flag = True
    if request.REQUEST.has_key('realname'):
        user.realname = request.REQUEST.get('realname')
        user_flag = True
    if request.REQUEST.has_key('sex'):
        if request.REQUEST.get('sex') == 'true':
            user.sex = True
        else:
            user.sex = False
        user_flag = True
    if user_flag:
        user.save()
    userinfo_flag = False
    if hasattr(user, 'userinfo') and user.userinfo:
        userinfo = user.userinfo
        post = {}
        for att in USERINFOATTR:
            if request.REQUEST.has_key(att):
                # setattr(userinfo,att, request.REQUEST.get(att))
                userinfo_flag = True
                post[att] = request.REQUEST.get(att)
            else:
                # setattr(request.POST, att, getattr(userinfo, att))
                if att == "xueli":
                    post[att] = None
                else:
                    post[att] = getattr(userinfo, att)
        userinfoform = UserInfoForm(post, instance=user.userinfo)
    else:
        userinfo_flag = True
        userinfoform = UserInfoForm(request.POST)

    if userinfo_flag:
        if not userinfoform.is_valid():
            return getErrorFormResult(userinfoform)
        userinfoform.instance.user = user
        userinfo = userinfoform.save()
        userinfo.save()
    if not user_flag and not userinfo_flag:
        u = cache.get(USERINFO_INFO % user.pk)
    else:
        u = None
        cache.delete(USERINFO_INFO % user.pk)
    if u is None:
        u = MyEncoder.default(userinfo)
        u.update(user.get_user_map(True))
        cache.set(USERINFO_INFO % user.pk, u, settings.CACHES_TIMEOUT)

    return getResult(True, u'修改个人信息成功', u)


@client_login_required_widthout_tel
@transaction.atomic()
def submit_user_tel(request):
    """
    提交手机号
    by:王健 at:2015-1-15
    提交手机号，只需要登录过，不需要已经有手机号，排除登陆者自己的手机号
    by:王健 at:2015-1-16
    改下提示内容
    by：尚宗凯 at：2015-05-12
    短信验证码使用后从session中删除
    by: 范俊伟 at:2015-07-01
    """
    user = request.user
    code = request.REQUEST.get('code', '')
    tel = request.REQUEST.get('tel', '')
    smsdebug = request.REQUEST.get('smsdebug', '')
    if not smsdebug and code != request.session.get('smscode', '1234'):
        return getResult(False, u'手机验证码不对，请重新输入。', None)
    if not smsdebug and tel != request.session.get('smstel', ''):
        return getResult(False, u'发送验证码的手机号，和注册的手机号不符合。请重新输入', None)
    user.tel = tel
    if get_user_model().objects.filter(tel=user.tel).exclude(id=user.id).exists():
        return getResult(False, u'手机号已经存在。请更换手机号', None)
    name = request.REQUEST.get('name', u'游客')
    if name:
        user.name = name
    user.save()
    request.session['smscode'] = None
    return getResult(True, u'验证手机号成功', None)


@transaction.atomic()
def reg_user(request):
    """
    注册新用户
    by:王健 at:2015-1-3
    所有用户名都改为tel
    by:王健 at:2015-1-8
    手机校验码 校验
    by:王健 at:2015-1-14
    注册时带上手机校验码，和手机号匹配
    by:王健 at:2015-1-14
    修改个人信息返回值
    by:王健 at:2015-1-20
    修改默认姓名
    by:王健 at:2015-3-17
    添加注册的手机号已经被邀请过的逻辑
    by:尚宗凯 at:2015-3-25
    flag 拉人 暂时去掉
    by:王健 at:2015-3-25
    session中存在的用户，如果没有手机号，直接覆盖
    by:王健 at:2015-4-6
    可以拉多个人
    by:尚宗凯 at:2015-4-8
    增加发送系统消息
    by：尚宗凯 at：2015-04-10
    解决NSPersonTel里面 tel project_id 不唯一问题
    by：王健 at：2015-05-18
    修改发送need消息
    by：尚宗凯 at：2015-05-07
    改下提示内容
    by：尚宗凯 at：2015-05-12
    短信验证码使用后从session中删除
    by: 范俊伟 at:2015-07-01
    """
    flag = request.REQUEST.has_key('flag')
    if flag and not Project.objects.filter(flag=request.REQUEST.get('flag')).exists():
        return getResult(False, u'邀请链接已经失效，请联系项目管理员，重新获得邀请。')
    if request.user.is_anonymous() or (hasattr(request.user, 'tel') and request.user.tel):
        user = get_user_model()()
    elif not request.user.tel:
        user = request.user

    if request.REQUEST.has_key('password'):
        user.set_password(request.REQUEST.get('password'))

    code = request.REQUEST.get('code', '')
    tel = request.REQUEST.get('tel', '')
    smsdebug = request.REQUEST.get('smsdebug', '')
    if not smsdebug and code != request.session.get('smscode', '1234'):
        return getResult(False, u'手机验证码不对，请重新输入。', None)
    if not smsdebug and tel != request.session.get('smstel', ''):
        return getResult(False, u'发送验证码的手机号，和注册的手机号不符合。请重新输入', None)
    user.tel = tel
    if not user.tel or get_user_model().objects.filter(tel=user.tel).exists():
        return getResult(False, u'手机号已经存在。请更换手机号', None)
    # user.icon = request.REQUEST.get('userhead', '')
    user.name = request.REQUEST.get('name', u'')

    # {'success': True, 'message': u'用户名已经存在', 'result': None}


    user.save()
    request.session['smscode'] = None
    # send_mail(u'邮箱验证--%s' % APP_NAME, u'请点击下方链接，完成注册', user.email)
    # user.email_user(u'邮箱验证--%s' % APP_NAME, u'请点击下方链接，完成注册')


    if NSPersonTel.objects.filter(tel=tel).exists():
        pts = NSPersonTel.objects.filter(tel=tel)
        s = set()
        for pt in pts:
            if (pt.tel, pt.project_id) in s:
                continue
            person = Person()
            person.user = user
            person.project = pt.project
            person.save()
            s.add((pt.tel, pt.project_id))
            if Group.objects.filter(id=pt.group.pk).exists():
                group = pt.group
                group.look_members.add(person.user)
            pt.delete()
    # if flag:
    #     project = Project.objects.get(flag=request.REQUEST.get('flag'))
    #     person = Person()
    #     person.user = user
    #     person.project = project
    #     person.save()
    #     group = Group.objects.get(project=project, flag='root')
    #     group.look_members.add(person)
    #     group.save()
    NeedMessage.create_sys_message(user.pk,"title",SYS_MESSAGE['reg_user'])
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)

    return getResult(True, u'注册成功', user.get_user_map(True))


#
#
# @transaction.atomic()
# def addOrganization(request):
# """
# 加入项目
#     """
#     flag = request.REQUEST.has_key('flag')
#     username = request.REQUEST.get('username')
#     try:
#         int(username)
#         user = authenticate(tel=username, password=request.REQUEST.get('password'))
#     except:
#         user = authenticate(email=username, password=request.REQUEST.get('password'))
#     if user and not user.is_active:
#         return getResult(False, u'用户已经停止使用。')
#     elif not user:
#         return getResult(False, u'用户名密码错误', None)
#     else:
#         auth_login(request, user)
#
#     orgquery = Organization.objects.filter(flag=request.REQUEST.get('flag'))
#     if flag and orgquery.exists():
#         org = orgquery[0]
#         if Person.objects.filter(user=request.user, org=org, is_active=True).count() == 1:
#             person = Person.objects.get(user=request.user, org=org)
#             setLoginOrg(request, person, org)
#             return getResult(True, u'已经加入：%s了' % org.name)
#         person, created = Person.objects.get_or_create(user=request.user, org=org)
#         person.icon = request.user.icon
#         person.name = request.user.name
#         person.is_active = True
#         person.save()
#         department = Department.objects.get(org=org, flag='free')
#         department.members.add(person)
#         setLoginOrg(request, person, org)
#         return getResult(True, u'成功加入：%s' % org.name)
#     auth_logout(request)
#     return getResult(False, u'邀请链接已经失效，请联系（项目/公司）管理员，重新获得邀请。')
#
#
#
#
# @client_login_org_required
# def getContacts(request):
#     return getResult(True, '',
#                      [{'id': u.pk, 'icon': u.icon, 'name': u.name, 'is_active': u.is_active} for u in
#                       Person.objects.get(pk=get_current_person().get('pid', None)).contacts.all()])
#


def send_sms_code(request):
    """
    发送手机验证信息
    by:王健 at:2015-1-14
    session里记录手机号和code
    by:王健 at:2015-1-14
    限制短信发送次数
    by: 范俊伟 at:2015-04-09
    根据短信的返回结果，记录日志
    by:王健 at:2015-05-18
    :param request:
    :return:
    """
    tel = request.REQUEST.get("tel")
    try:
        telnum = int(tel)
        if telnum < 10000000000 or telnum > 20000000000:
            return getResult(False, u'手机号不正确', None)
    except:
        return getResult(False, u'手机号不正确', None)
    if tel:
        if request.session.has_key("sms_num_%s" % str(tel)):
            num = request.session["sms_num_%s" % str(tel)]
        else:
            num = 0
        if request.session.has_key("sms_sendtime_%s" % str(tel)):
            sendtime = request.session["sms_sendtime_%s" % str(tel)]
        else:
            sendtime = None
        from datetime import datetime

        if sendtime:
            sendtime = datetime(int(sendtime[:4]), int(sendtime[4:6]), int(sendtime[6:8]), int(sendtime[8:10]),
                                int(sendtime[10:12]), int(sendtime[12:14]))
            if (datetime.now() - sendtime).seconds < 60:
                return getResult(False, u'每分钟只能发送一次验证码', None)
        else:
            num = 0

        check_res = SMSCounter.check_count(tel, 0)
        if check_res == -1:
            return getResult(False, u'该手机号今天已超过最大发送次数', None)
        elif check_res == -2:
            return getResult(False, u'每个手机号每分钟只能发送一次验证码', None)

        import random

        code = random.randint(1000, 9999)
        request.session["smscode"] = str(code)
        request.session["smstel"] = str(tel)
        request.session["sms_num_%s" % str(tel)] = num + 1
        request.session["sms_sendtime_%s" % str(tel)] = datetime.now().strftime("%Y%m%d%H%M%S")
        print code
        submail = MESSAGEXsend(MESSAGE_CONFIGS)
        submail.add_to(tel)
        submail.set_project('03tQD1')
        submail.add_var('code', code)
        result = submail.xsend()
        if result['status'] == 'success':
            SMSCounter.add_tel(tel, 0)
            return getResult(True, u'验证码已经发往手机。', None)
        else:
            log = logging.getLogger('django')
            log.error(u'tel:%s, %s' % (tel, json.dumps(result)))
            return getResult(False, u'验证码短信发送失败，请稍等片刻再操作。', None)

    else:
        return getResult(False, u'每分钟只能发送一次验证码', None)

# @client_login_required
def current_user(request):
    """
    所有用户名 都改为 tel
    by:王健 at:2015-1-8
    修改个人信息返回值
    by:王健 at:2015-1-20
    增加积分
    by:王健 at:2015-2-5
    未登录用户自动生成测试账号
    by:尚宗凯 at:2015-3-26
    添加时间戳，防止 批量重复创建用户
    by:王健 at:2015-4-6
    无账号调用，则使用游客账号
    by:王健 at:2015-4-8
    :param request:
    :return:
    """
    if not request.user.is_anonymous():
    # if request.user.is_anonymous():
        if request.user.is_active:
            # if request.user.tel == None:
            #     return getResult(False, u'请登记手机号。', None, status_code=9)
            return getResult(True, '', request.user.get_user_map(True), jifen=login_jifen(request))
        else:
            return getResult(False, u'用户已被禁用。', None, 5)
    # else:
    #     return getResult(False, u'请先登录', None, 1)
    else:
        # t = int(request.REQUEST.get('t', '0'))
        # timeline = int(time.time())
        # if (t + 20) < timeline:
        #     return getResult(False, u'校验不通过。', None, 5)
        user = get_user_model().objects.get(pk=settings.SHOW_USER_ID)
        # # user = NSUser()
        # user.tel = None
        # user.set_password('123456')
        # user.name = u"测试账号"
        # user.nickname = "测试账号"
        # user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        return getResult(True, '', request.user.get_user_map(True), jifen=login_jifen(request))


@client_login_project_required
def get_userinfo(request, project_id):
    """
    根据id获取用户基础信息
    by:王健 at:2015-1-16
    修改个人信息返回值
    by:王健 at:2015-1-20
    修复id值不对的bug
    by:王健 at:2015-2-17
    查询视图替代查询表
    by:尚宗凯 at:2015-3-6
    查询表替代视图
    by:尚宗凯 at:2015-3-8
    :param request:
    :return:
    """
    userid = request.REQUEST.get('user_id')
    if Person.objects.filter(user_id=userid, project_id=project_id).exists():
        person = Person.objects.get(user_id=userid, project_id=project_id)
        user = person.user
        p = user.get_user_map()
        if hasattr(user, 'userinfo') and user.userinfo:
            p.update(MyEncoder.default(user.userinfo))
        p['id'] = user.pk
        return getResult(True, '', p)
    else:
        return getResult(False, u'不是项目组内成员')

    # userid = request.REQUEST.get('user_id')
    # try:
    #     print userid,project_id
    #     p = VNSUseruUserInfoPersonBaseFile.objects.get(user_id=userid,project_id=project_id)
    #     p = p.toJSON()
    #     p['id'] = p['user_id']
    #     return getResult(True, '', p)
    # # except VNSUseruUserInfoPersonBaseFile.DoesNotExist:
    # except Exception as e:
    #     print e
    #     return getResult(False, u'不是项目组内成员')

def person_2_dict(person):
    """
    个人数据 转换为 字典数据
    by:王健 at:2015-1-16
    icon_url 修改
    by:王健 at:2015-1-30
    修复bug icon_url 空值
    by:王健 at:2015-1-31
    输出 权限
    by:王健 at:2015-3-5
    添加 职务 属性
    by:王健 at:2015-3-6
    输出个人的真实权限
    by:王健 at:2015-05-07
    优化名称
    by：尚宗凯 at：2015-05-14
    项目联系人名称为空则显示手机号
    by：尚宗凯 at：2015-05-14
    修改name不为空时逻辑错误
    by：尚宗凯 at:2015-05-15
    """
    d = {'id': person.user_id, 'timeline': person.timeline, 'project': person.project_id, 'name': person.user.name or person.user.tel[:3]+"****"+person.user.tel[-3:],
          'is_active': person.is_active}
    if person.user.icon_url:
        d['icon_url'] = person.user.icon_url.get_url()
    else:
        d['icon_url'] = ''
    if person.is_active:
        # d['title'] = person.title
        # person.init_powers()
        d['powers'] = person.real_powers()
        try:
            d['title'] = person.user.userinfo.title
        except:
            d['title'] = ''
        d['create_time'] = person.create_time.strftime('%Y-%m-%d %H:%M:%S')
    return d


def person_show_project_2_dict(user):
    """
    示例项目，中获取的本人信息
    修改示例项目 中 本人的权限
    by:王健 at:2015-4-9
    :param user:
    :return:
    """
    d = {'id': user.pk, 'timeline': 0, 'project': settings.SHOW_PROJECT_ID, 'name': user.name, 'is_active': True,
         'create_time': '2015-03-25 00:00:00', 'powers': [x[0] * 100 for x in FileGroup.objects.filter(
        Q(project_id=settings.SHOW_PROJECT_ID) | Q(project_id=None)).filter(
        father=None).values_list('id')]}
    d['powers'].extend([x + 1 for x in d['powers']])
    return d

@client_login_project_required
def query_person(request, project_id=None):
    """
    获取所有联系人
    by:王健 at:2015-1-16
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    使用缓存
    by:王健 at:2015-3-9
    针对示例项目优化，获取成员接口
    by:王健 at:2015-3-25
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    if not timeline:
        l = cache.get(PROJECT_PERSON_LIST % project_id)
        if l is None:
            l = Person.objects.filter(project_id=project_id).order_by('-timeline')
        else:
            if int(project_id) == settings.SHOW_PROJECT_ID:
                l.append(person_show_project_2_dict(request.user))
            return getResult(True, None, l)
    else:
        l = Person.objects.filter(project_id=project_id, timeline__gt=int(timeline)).order_by('timeline')
    ul = []
    for person in l:
        ul.append(person_2_dict(person))

    if not timeline:
        cache.set(PROJECT_PERSON_LIST % project_id, ul, settings.CACHES_TIMEOUT)
        if int(project_id) == settings.SHOW_PROJECT_ID:
                ul.append(person_show_project_2_dict(request.user))
    return getResult(True, None, ul)


def group_2_dict(group):
    """
    群组数据转换为 字典数据
    by:王健 at:2015-1-16
    icon_url 修改
    by:王健 at:2015-1-30
    修复bug icon_url 空值
    by:王健 at:2015-1-31
    分组信息 添加新字段
    by:王健 at:2015-2-27
    输出 权限
    by:王健 at:2015-3-5
    :param group:
    :return:
    """
    d = {'id': group.id, 'timeline': group.timeline, 'project': group.project_id, 'name': group.name,
         'is_active': group.is_active, 'hxgroup_id': group.hxgroup_id, 'is_needhx': group.is_needhx}
    if group.is_active:
        if group.icon_url:
            d['icon_url'] = group.icon_url.get_url()
        else:
            d['icon_url'] = ''
        group.init_powers()
        d['powers'] = group.powers
        d['type'] = group.type
        d['sorted'] = group.sorted
        d['user'] = group.user_id
        d['say_members'] = [x[0] for x in group.say_members.values_list('id')]
        d['look_members'] = [x[0] for x in group.look_members.values_list('id')]
    return d


@client_login_project_required
def query_group(request, project_id=None):
    """
    获取所有分组
    by:王健 at:2015-1-16
    排除root 组
    by:王健 at:2015-2-2
    不排除 root 组，方便客户端 组织“未分组” 。
    by:王健 at:2015-2-3
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    使用缓存
    by:王健 at:2015-3-9
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    if not timeline:
        l = cache.get(PROJECT_GROUP_LIST % project_id)
        if l is None:
            l = Group.objects.filter(project_id=project_id).filter(is_active=True).order_by('-timeline')
        else:
            return getResult(True, None, l)
    else:
        l = Group.objects.filter(project_id=project_id, timeline__gt=int(timeline)).filter(is_active=True).order_by('timeline')
    ul = []
    for person in l:
        ul.append(group_2_dict(person))
    if not timeline:
        cache.set(PROJECT_GROUP_LIST % project_id, ul, settings.CACHES_TIMEOUT)
    return getResult(True, None, ul)


@client_login_required
def guanzhu_project(request):
    """
    关注项目
    by:王健 at:2015-1-30
    元祖改为字符串
    by:王健 at:2015-1-31
    增加缓存
    by:王健 at:2015-3-9
    清空个人信息
    by:王健 at:2015-3-16
    """
    cache.delete(MY_PROJECT_QUERY_LIST % request.user.pk)
    project_id = request.REQUEST.get('project_id', '')
    do = request.REQUEST.get('do', 'join')
    try:
        project = Project.objects.get(id=project_id)
        if do == 'join':
            if not project.nsuser_set.filter(id=request.user.id).exists():
                project.nsuser_set.add(request.user)
                project.guanzhu_num += 1
                project.save()
                msg = u'关注%s成功'
                cache.delete(USERINFO_INFO % request.user.pk)
            else:
                msg = u'已经关注过%s'
            return getResult(True, msg % project.name, {'project': MyEncoder.default(project), 'guanzhuprojectlist': [p[0] for p in request.user.guanzhu.values_list('id')]})
        else:
            if project.nsuser_set.filter(id=request.user.id).exists():
                project.nsuser_set.remove(request.user)
                project.guanzhu_num -= 1
                project.save()
                cache.delete(USERINFO_INFO % request.user.pk)
            return getResult(True, u'取消关注%s成功' % project.name, {'project': MyEncoder.default(project), 'guanzhuprojectlist': [p[0] for p in request.user.guanzhu.values_list('id')]})
    except Project.DoesNotExist:
        return getResult(False, u'项目不存在')
    except ValueError:
        return getResult(False, u'参数格式错误')


@client_login_required
def query_my_jifen(request):
    """
    查询我的积分值
    by:王健 at:2015-2-6
    :param request:
    :return:
    """
    return getResult(True, u'', query_fen_by_uid(request))


@login_project_manager_required
@transaction.atomic()
def change_user_group(request, project_id):
    """
    把某个用户 放入、移出某个群, 如果在九个预制群组，则只能隶属一个分组
    by:王健 at:2015-2-6
    如果从某个分组移出某人，如果他同时不是管理员，则也会被移出项目
    by:王健 at:2015-2-13
    不恩能够加入社会大众通道
    by:王健 at:2015-2-15
    默认修改为移动都改为say_members 成员
    by:王健 at:2015-2-27
    关闭 9个特殊分组的移出 功能
    by:王健 at:2015-3-11
    移入9个分组时，在其他组，也消失，移入管理员组时，在其他组，不消失， 保存一下Person，更新时间线缓存
    by:王健 at:2015-3-14
    如果是超级管理员，不能从管理员组移出。
    by:王健 at:2015-3-16
    项目经理部的人 被移入管理员组，则修改为可发布项目公告
    by:王健 at:2015-3-16
    增加系统消息
    by：尚宗凯 at：2015-04-10
    不发消息了
    by：尚宗凯 at：2015-04-14
    移入管理员组的成员，自动移入项目经理部
    by:王健 at:2015-05-11
    切换分组时，清空所有的个人权限，和逆权限
    by:王健 at:2015-05-15
    设置为非管理员组，则管理员身份去掉
    by:王健 at:2015-05-20
    删除用户最后阅读系统消息项目公告缓存
    by：尚宗凯 at：2015-05-21
    设置项目经理部时，可能已经加入，但要去掉管理员
    by:王健 at:2015-05-22
    :param request:
    :param project_id:
    :return:
    """
    uid = request.REQUEST.get('user_id')
    gid = request.REQUEST.get('group_id')
    do = request.REQUEST.get('do', 'join')
    if uid and gid:
        group = Group.objects.get(pk=gid, project_id=project_id)
        if group.type == 'sys_shdztd':
            return getResult(False, u'项目成员无需加入 社会大众通道 。')

        user = get_user_model().objects.get(pk=uid)
        is_in = Group.objects.filter(pk=gid, project_id=project_id).filter(Q(say_members=uid) | Q(look_members=uid)).exists()
        if do == 'join':
            #加入分组
            if not is_in or group.type == 'sys_xmjl':
                #不在分组内
                group.look_members.add(user)
                group.save()
                person = Person.objects.get(user=user, project_id=group.project_id)
                person.powers = []
                person.dispowers = []
                person.save()
                if group.type in GROUP_TYPE and group.type != 'sys_manage':
                    #分组是 特殊分组，并且不是管理员组，则从其他组中删除，
                    for g in Group.objects.filter(project_id=project_id, type__in=GROUP_TYPE).filter(Q(say_members=uid) | Q(look_members=uid)):
                        if g.pk != group.pk:
                            if g.project.manager_id == user.id:
                                #如果此人还是超级管理员，则不能移出管理员组
                                continue
                            g.look_members.remove(user)
                            g.say_members.remove(user)
                            g.save()
                elif group.type == 'sys_manage':
                    xmjlgroup = Group.objects.get(project_id=project_id, type='sys_xmjl')
                    xmjlgroup.look_members.remove(user)
                    xmjlgroup.say_members.add(user)
                    xmjlgroup.save()
                    #如果是从别的组移入管理员组
                    for g in  Group.objects.filter(project_id=project_id, type__in=GROUP_TYPE_DW).filter(Q(look_members=uid) | Q(say_members=uid)):
                        g.look_members.remove(user)
                        g.say_members.remove(user)
                        g.save()



                if group.type == 'sys_xmjl' and Group.objects.filter(project_id=project_id, type='sys_manage').filter(Q(say_members=uid)| Q(look_members=uid)).exists():
                    #如果是从别的组移入项目组，同时又是管理员组成员
                    #判断是否还在项目经理部组的 look_members 权限，如果是，则移到say_members 里
                    group.look_members.remove(user)
                    group.say_members.add(user)
                    group.save()

        else:
            if group.type in GROUP_TYPE and group.type != 'sys_manage':
                #如果不是管理员，则不可以从其他分组里直接移出
                return getResult(False, u'错误操作，成员不能从分组里直接移出，可以删除成员，或移入其他分组')
            if is_in:
                group.look_members.remove(user)
                group.say_members.remove(user)
                group.save()
                person = Person.objects.get(user=user, project_id=group.project_id)
                person.save()

        cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("project_message", uid, project_id, gid))
        cache.delete(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % ("sysmessage", uid, project_id, gid))
        cache.delete(PROJECT_GROUP_USER % project_id)
        # NeedMessage.create_sys_message(user.pk,"title",SYS_MESSAGE['change_user_group'])
        return getResult(True, u'操作成功', None)
    else:
        return getResult(False, u'错误操作，参数不正确')

