# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
from django.contrib.auth import get_user_model
from django.db import transaction
from util.jsonresult import getResult
from util.loginrequired import client_login_required


__author__ = u'王健'

@client_login_required
@transaction.atomic()
def admin_init_password(request):
    """
    初始化密码为 手机号后六位
    by:王健 at:2015-3-20
    """
    tel = request.REQUEST.get('tel')
    if not request.user.is_staff:
        return getResult(False, u'您不是系统管理员。')
    try:
        user = get_user_model().objects.get(tel=tel)
        user.set_password(user.tel[-6:])
        user.save()
        return getResult(True, u'初始化成功', None)
    except:
        return getResult(False, u'账号不存在。')




