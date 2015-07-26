# coding=utf-8
import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import RequestContext
from company.models import SysNews, SysColumn, CompanyPerson, Company
from submail.app_configs import MESSAGE_CONFIGS
from submail.message_xsend import MESSAGEXsend
from util.jsonresult import getResult

__author__ = 'wangjian'
from django.shortcuts import render_to_response, get_object_or_404


def add_user_to_company(request):
    """
    添加用户到公司里
    by:王健 at:2015-06-19
    解决REQUEST getlist 函数bug
    by:王健 at:2015-06-19
    :param request:
    :return:
    """
    user_ids = [int(x) for x in request.REQUEST.getlist('id')]
    company_id = request.REQUEST.get('company_id')
    ids = [x[0] for x in CompanyPerson.objects.filter(user_id__in=user_ids, company_id=company_id).values_list('user_id')]

    for user in get_user_model().objects.filter(pk__in=set(user_ids)-set(ids)):
        cp,created = CompanyPerson.objects.get_or_create(user=user, company_id=company_id)

    return getResult(True, u'添加成员成功', )


def check_user_registered(request):
    """
    返回已注册用户手机号
    by: 范俊伟 at:2015-06-24
    :param request:
    :return:
    """
    tels = request.REQUEST.getlist('tel')
    query = get_user_model().objects.filter(tel__in=tels)
    result = []
    for i in query:
        result.append(i.tel)
    return getResult(True, '', result)


def add_user_by_tel_to_company(request, company_id):
    """
    通过手机号添加用户
    by: 范俊伟 at:2015-06-25
    :param request:
    :param company_id:
    :return:
    """
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return getResult(False, '公司不存在')
    tels = request.REQUEST.getlist('tel')
    success_tels = []
    error_tels = []
    send_sms_tels = []
    for tel in set(tels):
        try:
            user = get_user_model().objects.get(tel=tel)
            CompanyPerson.objects.get_or_create(user=user, company=company)
            success_tels.append(tel)
        except get_user_model().DoesNotExist:
            tellist = []
            for c in tel.replace('+86', ''):
                try:
                    int(c)
                    tellist.append(c)
                except:
                    pass
            if len(tellist) == 11:
                new_tel = ''.join(tellist)
                submail = MESSAGEXsend(MESSAGE_CONFIGS)
                submail.add_to(new_tel)
                submail.set_project('rT7w11')
                submail.add_var('from', (True and [request.user.name] or [request.user.tel])[0])
                submail.add_var('project', company.name)
                submail.add_var('url', '%s?v=%s' % (settings.MESSAGE_URL, random.randint(0, 100)))
                submail.xsend()
                send_sms_tels.append(tel)
            else:
                error_tels.append(tel)
                continue

    return getResult(True, '', {"success_tels": success_tels, "error_tels": error_tels, "send_sms_tels": send_sms_tels})


def manage_com_user(request, company_id):
    """
    管理企业的员工
    by:王健 at:2015-06-22
    :param request:
    :param company_id:
    :return:
    """
    return render_to_response('cp_manage/phone/company_user_manage.html', RequestContext(request, {"data": None, 'company_id': company_id}))


def manage_com_user_html(request, company_id):
    """
    添加员工、删除员工、权限管理
    by:王健 at:2015-06-23
    显示员工列表
    by:王健 at:2015-07-01
    员工删除开发
    by:王健 at:2015-07-02
    :param request:
    :param company_id:
    :return:
    """
    users = []
    for x in get_user_model().objects.filter(companyperson__company__id=company_id, companyperson__is_active=True).order_by('-id'):
        d = x.toJSON()
        if x.icon_url:
            d['icon_url'] = x.icon_url.get_url('imageView2/5/w/80/h/80')
        else:
            d['icon_url'] = ''
        users.append(d)

    return render_to_response('cp_manage/phone/company_members.html', RequestContext(request, {'company_id': company_id, 'users': users}))





