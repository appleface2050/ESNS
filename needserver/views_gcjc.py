# coding=utf-8
# Date:2015/01/13
# Email:wangjian2254@icloud.com
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from needserver.jifenutil import create_data_jifen
from django.core.cache import cache

from needserver.models import FileGroup, \
    EngineCheck, UserLastReadTimeline, Project
from nsbcs.models import File
from util import RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, RED_DOT_UNREAD_NUMBER, \
    RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE, RED_DOT_USER_LAST_READ_TIMELINE, USER_ACTIVITY
from util.cache_handle import get_file_group_id_by_flag_from_cache
from util.jsonresult import getResult, MyEncoder
from util.loginrequired import client_login_project_required, app_power_permissions, login_project_status_zero_required

import datetime
from util.needpush import NeedPush
from util.project_power_cache import get_alias_by_project_id_flag

__author__ = u'王健'


@login_project_status_zero_required
@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def create_enginecheck_by_group(request, project_id=None):
    """
    创建一个工程检查
    by:王健 at:2015-1-13
    创建时 添加一个处理意见 参数“chuli”
    by:王健 at:2015-1-16
    处理意见，不在本接口填写
    by:王健 at:2015-1-21
    增加积分
    by:王健 at:2015-2-
    修改权限校验 函数
    by:王健 at:2015-3-5
    优化settings 使用
    by:王健 at:2015-3-9
    工程检查增加极光推送
    by:尚宗凯 at:2015-4-8
    提交日志时刷新阅读时间
    by：尚宗凯 at：2015-05-06
    增加最新数据时间缓存
    by：尚宗凯 at：2015-05-20
    修复小红点bug
    by：尚宗凯 at：2015-05-27
    增加项目状态为 0 装饰器
    by:尚宗凯 at：2015-05-31
	变更极光推送方法
	by：尚宗凯 at：2015-05-31
	上传图片增加长高比例
	by：尚宗凯 at：2015-06-02
    添加用户活跃度缓存
    by：尚宗凯 at：2015-06-04
    """
    fileid = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(File, pk=fileid, project_id=project_id)
    fileobj.file_status = True
    fileobj.save()

    flag = request.REQUEST.get('flag')
    # title = request.REQUEST.get('title')

    desc = request.REQUEST.get('desc')
    # path = request.REQUEST.get('path')
    enginecheck = EngineCheck()
    # enginecheck.title = title
    enginecheck.desc = desc

    enginecheck.project_id = int(project_id)
    enginecheck.user = request.user
    enginecheck.file_group = get_object_or_404(FileGroup, flag=flag)
    enginecheck.user = request.user
    # enginecheck.path = path
    enginecheck.pre_pic = fileobj
    try:
        tmp = fileobj.img_size.strip().split("x")
        x = float(tmp[0])
        y = float(tmp[1])
        enginecheck.pre_pic_scale = "%.02f" % (x/y)
    except Exception as e:
        pass
    enginecheck.save()


    from util.cache_handle import query_project_filegroup_data_
    all_flag = query_project_filegroup_data_(project_id)
    file_group_id = all_flag['flags2'][flag]

    #更新项目应用节点最新数据时间
    user_id = request.user.pk
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, enginecheck.file_group_id), enginecheck.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id, enginecheck.timeline, settings.CACHES_TIMEOUT)
    cache.delete(USER_ACTIVITY % (user_id, project_id, enginecheck.create_time.strftime('%Y-%m-%d')))
    # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, enginecheck.file_group_id, user_id))
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    UserLastReadTimeline.update_last_read_timeline(project_id, 0, user_id)

    alias = get_alias_by_project_id_flag(project_id, flag, file_group_id)
    alias = list(set(alias))
    NeedPush.send_jpush(flag=flag,
                        project_id=project_id,
                        title=Project.get_project_name_by_id(project_id),
                        msg=all_flag['file_group'][file_group_id]['name'],
                        alias=alias,
                        file_group=all_flag['file_group'][file_group_id]
    )

    return getResult(True, u'创建工程检查成功', MyEncoder.default(enginecheck), jifen=create_data_jifen(request, settings.CREATE_DATA))


@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def update_enginecheck_by_group(request, project_id=None):
    """
    修改一个工程检查
    by:王健 at:2015-1-13
    修改时 不用提交处理意见
    by:王健 at:2015-1-16
    处理意见，在本接口填写
    by:王健 at:2015-1-21
    完成工程检查，保存完成时间
    by:王健 at:2015-2-10
    修改权限校验 函数
    by:王健 at:2015-3-5
	工程检查回复添加极光推送
	by：尚宗凯 at：2015-4-8
    """
    fileid = request.REQUEST.get('fileid')
    if fileid:
        fileobj = get_object_or_404(File, pk=fileid, project_id=project_id)
        fileobj.file_status = True
        fileobj.save()

    pk = request.REQUEST.get('id')
    fucha = request.REQUEST.get('fucha')
    status = request.REQUEST.get('status')
    chuli = request.REQUEST.get('chuli')
    enginecheck = get_object_or_404(EngineCheck, pk=pk, project_id=project_id)
    flag = False
    if fileid:
        enginecheck.chuli_pic = fileobj
        flag = True
    if fucha:
        enginecheck.fucha = fucha
        flag = True
    if chuli:
        enginecheck.chuli = chuli
        flag = True
    if status == 'true':
        enginecheck.status = True
        if not enginecheck.finish_time:
            enginecheck.finish_time = timezone.now()
        flag = True
    if flag:
        try:
            tmp = fileobj.img_size.strip().split("x")
            x = float(tmp[0])
            y = float(tmp[1])
            enginecheck.chuli_pic_scale = "%.02f" % (x/y)
        except Exception as e:
            pass
        enginecheck.save()
    return getResult(True, None, MyEncoder.default(enginecheck))


@app_power_permissions(None, flag_name='flag')
def query_enginecheck_by_group(request, project_id=None):
    """
    查询工程检查，根据应用节点，和时间戳
    by:王健 at:2015-1-13
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    记录最后阅读时间
    by：尚宗凯 at：2015-05-06
	增加开始结束时间搜索
	by：尚宗凯 at:2015-05-06
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """
    flag = request.REQUEST.get('flag')
    timeline = int(request.REQUEST.get('timeline', '0'))
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = EngineCheck.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = EngineCheck.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__gt=int(timeline)).order_by('timeline')[:20]
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), 0, settings.CACHES_TIMEOUT)
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions(None, flag_name='flag')
def query_enginecheck_by_group_old(request, project_id=None):
    """
    查询工程检查，根据应用节点，和时间戳 旧数据
    by:王健 at:2015-1-13
    修改排序错误
    by:王健 at:2015-1-26
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
	增加根据开始时间结束时间搜索
	by：尚宗凯 at：2015-05-13
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """

    flag = request.REQUEST.get('flag')
    timeline = int(request.REQUEST.get('timeline', '0'))
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = EngineCheck.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = EngineCheck.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__lt=int(timeline)).order_by('-timeline')[:20]
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def delete_enginecheck_by_enginecheck_id(request, project_id=None):
    """
    删除工程检查，本人 24小时内有效
    by:尚宗凯 at:2015-3-30
    删除项目应用节点最新数据时间
    by：尚宗凯 at：2105-05-20
    删除时间改为30日之内
    by：尚宗凯 at：2015-05-27
    """
    enginecheck_id = request.REQUEST.get('enginecheck_id', '')
    if enginecheck_id:
        ec = EngineCheck.objects.get(pk=enginecheck_id)
        if ec.user_id != request.user.pk:
            return getResult(False, u'不是您发布的数据，不能删除', status_code=2)
        if ec.create_time + datetime.timedelta(days=30) < timezone.now():
            return getResult(False, u'超过30日的数据，不能删除', status_code=2)
        ec.set_is_active_false()
        ec.save()
        #删除项目应用节点最新数据时间
        cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, ec.file_group_id))
        cache.delete(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
        return getResult(True, u'成功删除工程检查', enginecheck_id)
    return getResult(False, u'记录不存在,删除失败', status_code=2)

