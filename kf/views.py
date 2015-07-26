# coding=utf-8
from django.shortcuts import render

# Create your views here.
from needserver.models import NSUser, Project
from util.jsonresult import getResult, MyEncoder


def query_user(request):
    """
    查询用户列表
    by: 范俊伟 at:2015-05-14
    :param request:
    :return:
    """
    last_id = request.REQUEST.get('last_id', None)
    if last_id == None:
        query = NSUser.objects.all().order_by('id')[:100]
    else:
        query = NSUser.objects.filter(id__gt=last_id).order_by('id')[:100]

    return getResult(True, '', MyEncoder.default(query))


def query_project(request):
    """
    查询项目列表
    by: 范俊伟 at:2015-05-14
    :param request:
    :return:
    """
    last_id = request.REQUEST.get('last_id', None)
    if last_id == None:
        query = Project.objects.all().order_by('id')[:100]
    else:
        query = Project.objects.filter(id__gt=last_id).order_by('id')[:100]

    return getResult(True, '', MyEncoder.default(query))


def get_project_info(request):
    """
    查询项目信息
    by: 范俊伟 at:2015-05-14
    :param request:
    :return:
    """
    id = request.REQUEST.get('id')
    if not id:
        return getResult(False, '未提供项目id')
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return getResult(False, '项目不存在')

    return getResult(True, '', MyEncoder.default(project))
