# coding=utf-8
from django import http
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from needserver.models import NSUser
from ns_manage.base.views import FrameView
from django.contrib.auth import logout as auth_logout, get_user_model
from ns_manage.models import BackUserInfo
from util.jsonresult import getResult
from util.loginrequired import ns_manage_login_required, ns_manage_admin_login_required


def logout(request):
    '''
    退出登录
    by:范俊伟 at:2015-01-21
    '''
    auth_logout(request)
    return http.HttpResponseRedirect(request.REQUEST.get('next', '/ns_manage/'))


@ns_manage_login_required
def change_password(request):
    """
    修改密码
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    old_password = request.REQUEST.get('old_password')
    new_password = request.REQUEST.get('new_password')

    user = request.user
    if not user.check_password(old_password):
        return getResult(False, '原始密码错误')
    user.set_password(new_password)
    user.save()
    return getResult(True, '修改成功')


class AppView(FrameView):
    '''
    后台app视图
    by:范俊伟 at:2015-02-06
    '''
    template_name = 'ns_manage/app.html'
    title = u'Need'


@ns_manage_login_required
def query_user(request):
    """
    查询用户
    by: 范俊伟 at:2015-06-12
    增加查询方式
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    keyword = request.REQUEST.get('keyword', "")
    user_type = request.REQUEST.get('user_type', "")
    query = get_user_model().objects.filter(Q(tel__icontains=keyword) | Q(name__icontains=keyword)).filter(
        is_staff=False)
    if user_type != "":
        query = query.filter(backuserinfo__user_type=user_type)

    result = []
    for i in query:
        res = i.toJSON()
        if i.icon_url:
            res['icon_url'] = i.icon_url.get_url('imageView2/5/w/80/h/80')
        else:
            res['icon_url'] = None

        if hasattr(i, 'backuserinfo'):
            backuserinfo = i.backuserinfo.toJSON()
            backuserinfo.update(res)
            res = backuserinfo

        result.append(res)

    return getResult(True, '', result)


@ns_manage_admin_login_required
def set_user_type(request):
    """
    设置用户类型
    by: 范俊伟 at:2015-06-12
    :param request:
    :return:
    """
    ids = request.REQUEST.getlist('id')
    user_type = request.REQUEST.get('user_type')
    if user_type == None:
        return getResult(False, '未提供用户类型')
    if not ids:
        return getResult(False, '未选择用户')
    for id in ids:
        try:
            user = get_user_model().objects.get(id=id)
            if hasattr(user, 'backuserinfo'):
                backuserinfo = user.backuserinfo
            else:
                backuserinfo = BackUserInfo()
                backuserinfo.need_user = user
            backuserinfo.user_type = user_type
            backuserinfo.save()
        except get_user_model().DoesNotExist:
            pass

    return getResult(True, '设置成功')
