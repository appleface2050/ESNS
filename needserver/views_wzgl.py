# coding=utf-8
# Date:2015/01/13
# Email:wangjian2254@icloud.com
import datetime
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Need_Server.settings import CREATE_DATA,JPUSH_MESSAGE
from needserver.forms import GYSAddressForm, WuZiRecordForm
from needserver.jifenutil import create_data_jifen
from django.core.cache import cache
from django.conf import settings

from needserver.models import FileGroup, \
    EngineCheck, GYSAddress, WuZiRecord, RecordDate, Project, UserLastReadTimeline
from nsbcs.models import File
from util import RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, RED_DOT_UNREAD_NUMBER, \
    RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE, RED_DOT_USER_LAST_READ_TIMELINE, USER_ACTIVITY
from util.cache_handle import get_file_group_id_by_flag_from_cache
from util.jsonresult import getResult, MyEncoder, getErrorFormResult
from util.loginrequired import client_login_project_required, app_power_permissions, login_project_status_zero_required
from util.needpush import NeedPush
from Need_Server.settings import JPUSH_MESSAGE
from util.project_power_cache import get_alias_by_project_id_flag,get_cache_project_power_timeline,get_power_group

__author__ = u'王健'


@login_project_status_zero_required
@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def create_gysaddress_by_group(request, project_id=None):
    """
    创建一个供应商名录
    by:王健 at:2015-1-14
    增加积分
    by:王健 at:2015-2-5
    修改权限校验 函数
    by:王健 at:2015-3-5
    增加修改时判断是否是当前用户创建的逻辑
    by:尚宗凯 at:2015-3-26
    增加极光推送
    by:尚宗凯 at:2015-4-8
    极光推送别名
    by:尚宗凯 at:2015-4-13
	极光推送IOS增加字段
	by:尚宗凯 at:2015-4-23
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
    添加用户活跃度缓存
    by：尚宗凯 at：2015-06-04
    """
    flag = request.REQUEST.get('flag')
    id = request.REQUEST.get('id')
    if id:
        ghsform = GYSAddressForm(request.POST, instance=GYSAddress.objects.get(pk=id))
        if ghsform.instance.user.pk != request.user.pk:
            return getResult(False, u'不是您发布的数据，不能修改', status_code=2)
    else:
        ghsform = GYSAddressForm(request.POST)
    if not ghsform.is_valid():
        return getErrorFormResult(ghsform)
    ghsform.instance.project_id = int(project_id)
    ghsform.instance.file_group = get_object_or_404(FileGroup, flag=flag)
    ghsform.instance.user = request.user
    gys = ghsform.save()
    # if flag:
    #     alias = list(set(get_alias_by_project_id_flag(project_id, flag)))
    #     NeedPush.send_jpush(flag=flag,
    #                     project_id=project_id,
    #                     title=Project.get_project_name_by_id(project_id),
    #                     msg=FileGroup.objects.get(flag=flag).name,
    #                     alias=alias,
    #                     file_group=FileGroup.objects.get(flag=flag).toJSON()
    #                     )

    from util.cache_handle import query_project_filegroup_data_
    all_flag = query_project_filegroup_data_(project_id)
    file_group_id = all_flag['flags2'][flag]
    alias = get_alias_by_project_id_flag(project_id, flag, file_group_id)
    alias = list(set(alias))
    NeedPush.send_jpush(flag=flag,
                        project_id=project_id,
                        title=Project.get_project_name_by_id(project_id),
                        msg=all_flag['file_group'][file_group_id]['name'],
                        alias=alias,
                        file_group=all_flag['file_group'][file_group_id]
    )

    # UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=request.user.pk)
    #更新项目应用节点最新数据时间
    user_id = request.user.pk
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, ghsform.instance.file_group_id), gys.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id, gys.timeline, settings.CACHES_TIMEOUT)
    cache.delete(USER_ACTIVITY % (user_id, project_id, ghsform.instance.create_time.strftime('%Y-%m-%d')))

    # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, ghsform.instance.file_group_id, user_id))
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    UserLastReadTimeline.update_last_read_timeline(project_id, 0, user_id)
    return getResult(True, u'创建供应商名录成功', MyEncoder.default(gys), jifen=create_data_jifen(request, CREATE_DATA))


@app_power_permissions(None, flag_name='flag')
def query_gysaddress_by_group(request, project_id=None):
    """
    查询供应商名录，根据应用节点，和时间戳
    by:王健 at:2015-1-14
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    记录最后阅读时间
    by：尚宗凯 at：2015-05-06
	增加根据开始时间结束时间搜索
	by：尚宗凯 at：2015-05-13
    优化查询
    by：尚宗凯 at：2015-05-20
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
        l = GYSAddress.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = GYSAddress.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__gt=int(timeline)).order_by('timeline')[:20]
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), 0, settings.CACHES_TIMEOUT)
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions(None, flag_name='flag')
def query_gysaddress_by_group_old(request, project_id=None):
    """
    查询供应商名录，根据应用节点，和时间戳 旧数据
    by:王健 at:2015-1-14
    修改排序错误
    by:王健 at:2015-1-26
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
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
        l = GYSAddress.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = GYSAddress.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__lt=int(timeline)).order_by('-timeline')[:20]
    return getResult(True, None, MyEncoder.default(l))



@login_project_status_zero_required
@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def create_wuzirecord_by_group(request, project_id=None):
    """
    创建一个物资记录
    by:王健 at:2015-1-14
    num bug修复
    by:王健 at:2015-2-3
    增加积分
    by:王健 at:2015-2-5
    优化物资记录 增加方法
    by:王健 at:2015-2-10
    修改权限校验 函数
    by:王健 at:2015-3-5
    增加采购出库入库修改记录
    by:尚宗凯 at:2015-3-26
    添加极光推送
    by:尚宗凯 at:2015-4-8
	极光推送别名
	by:尚宗凯 at:2015-4-13
	极光推送IOS增加字段
	by:尚宗凯 at:2015-4-23
    提交日志时刷新阅读时间
    by：尚宗凯 at：2015-05-06
    优化查询
    by：尚宗凯 at：2015-05-20
    增加项目状态为 0 装饰器
    by:尚宗凯 at：2015-05-31
    添加用户活跃度缓存
    by：尚宗凯 at：2015-06-04
    """
    flag = request.REQUEST.get('flag')
    id = request.REQUEST.get('id')
    create = False
    if id:
        ghsform = WuZiRecordForm(request.POST, instance=WuZiRecord.objects.get(pk=id))
        record = ghsform.instance.record_date
        if ghsform.instance.user.pk != request.user.pk:
            return getResult(False, u'不是您发布的数据，不能修改', status_code=2)
        now = datetime.datetime.now().date()
        if record.date + datetime.timedelta(days=1) < now:
             return getResult(False, u'已超过24小时，不能修改', status_code=2)
    else:
        ghsform = WuZiRecordForm(request.POST)
        record, create = RecordDate.objects.get_or_create(project_id=project_id, file_group=FileGroup.objects.get(flag=flag), date=timezone.now())
        ghsform.instance.record_date = record
        record.num += 1
        record.last_create_user = request.user

    if not ghsform.is_valid():
        if create:
            record.delete()
        return getErrorFormResult(ghsform)
    ghsform.instance.project_id = int(project_id)
    ghsform.instance.file_group = get_object_or_404(FileGroup, flag=flag)
    ghsform.instance.user = request.user
    gys = ghsform.save()

    record.save()
    result = MyEncoder.default(record)
    result.update(MyEncoder.default(gys))

    # if flag:
        # alias = list(set(get_alias_by_project_id_flag(project_id, flag)))
        # NeedPush.send_jpush(flag=flag,
        #                 project_id=project_id,
        #                 title=Project.get_project_name_by_id(project_id),
        #                 msg=FileGroup.objects.get(flag=flag).name,
        #                 alias=alias,
        #                 file_group=FileGroup.objects.get(flag=flag).toJSON()
        #                 )
    from util.cache_handle import query_project_filegroup_data_
    all_flag = query_project_filegroup_data_(project_id)
    file_group_id = all_flag['flags2'][flag]
    alias = get_alias_by_project_id_flag(project_id, flag, file_group_id)
    alias = list(set(alias))
    NeedPush.send_jpush(flag=flag,
                        project_id=project_id,
                        title=Project.get_project_name_by_id(project_id),
                        msg=all_flag['file_group'][file_group_id]['name'],
                        alias=alias,
                        file_group=all_flag['file_group'][file_group_id]
    )

    # UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=request.user.pk)
    #更新项目应用节点最新数据时间
    user_id = request.user.pk
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, ghsform.instance.file_group_id), record.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id, record.timeline, settings.CACHES_TIMEOUT)
    cache.delete(USER_ACTIVITY % (user_id, project_id, ghsform.instance.create_time.strftime('%Y-%m-%d')))

    # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, ghsform.instance.file_group_id, user_id))
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    UserLastReadTimeline.update_last_read_timeline(project_id, 0, user_id)
    return getResult(True, u'创建物资记录成功', result, jifen=create_data_jifen(request, CREATE_DATA))


@client_login_project_required
@transaction.atomic()
def del_wuzirecord_by_id(request, project_id=None):
    """
    不超过24小时的日志，可以由发布者 删除
    by:王健 at:2015-2-10
    修改权限校验 函数
    by:王健 at:2015-3-5
    删除项目应用节点最新数据时间
    by:尚宗凯 at：2015-05-20
    删除时间改为30日之内
    by：尚宗凯 at：2015-05-27
    """
    pk = request.REQUEST.get('id')
    if pk:
        wuzirecord = WuZiRecord.objects.get(pk=pk)
        if wuzirecord.project_id != int(project_id) or wuzirecord.user_id != request.user.pk:
            return getResult(False, u'不是您发布的数据，不能删除', status_code=2)
        if (wuzirecord.create_time + datetime.timedelta(days=30)) < timezone.now():
            return getResult(False, u'超过30日的数据，不能删除')
        wuzirecord.record_date.num -= 1
        wuzirecord.record_date.save()
        wuzirecord.is_active = False
        wuzirecord.save()
        #删除项目应用节点最新数据时间
        cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, wuzirecord.file_group_id))
        cache.delete(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
        return getResult(True, u'删除物资记录成功', pk)
    else:
        return getResult(False, u'参数不正确')


@client_login_project_required
@transaction.atomic()
def del_gysaddress_by_id(request, project_id):
    """
    删除供应商地址
    by:尚宗凯 at:2015-3-26
    删除项目应用节点最新数据时间
    by:尚宗凯 at：2015-05-20
    修复一个bug
    by：尚宗凯 at：2015-05-20
    删除时间改为30日之内
    by：尚宗凯 at：2015-05-27
    """
    # flag = request.REQUEST.get('flag')
    id = request.REQUEST.get('id')
    if id:
        ghsform = GYSAddressForm(request.POST, instance=GYSAddress.objects.get(pk=id))
        if ghsform.instance.user.pk != request.user.pk or ghsform.instance.project_id != int(project_id):
            return getResult(False, u'不是您发布的数据，不能删除', status_code=2)
        if (ghsform.instance.create_time + datetime.timedelta(days=1)) < timezone.now():
            return getResult(False, u'超过30日的数据，不能删除', status_code=2)
        ghsform.instance.delete()
        #删除项目应用节点最新数据时间
        cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, ghsform.instance.file_group_id))
        cache.delete(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
        return getResult(True, u'删除供应商记录成功', id)
    else:
        return getResult(False, u'参数不正确')


@app_power_permissions(None, flag_name='flag')
def query_wuzirecord_by_group(request, project_id=None):
    """
    查询物资记录，根据应用节点，和时间戳
    by:王健 at:2015-1-14
    添加记录日期id,获取全部信息
    by:王健 at:2015-1-31
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    增加开始结束时间搜索
    by：尚宗凯 at：2015-05-14
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """
    flag = request.REQUEST.get('flag')
    timeline = int(request.REQUEST.get('timeline', '0'))
    record_date_id = request.REQUEST.get('record_date_id')
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = WuZiRecord.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = WuZiRecord.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, record_date_id=record_date_id, file_group__flag=flag).order_by('-timeline')
    else:
        l = l.filter(project_id=project_id, record_date_id=record_date_id, file_group__flag=flag, timeline__gt=int(timeline)).order_by('timeline')
    return getResult(True, None, MyEncoder.default(l))



#
# @client_login_project_required
# def query_wuzirecord_by_group_old(request, project_id=None):
#     """
#     查询物资记录，根据应用节点，和时间戳 旧数据
#     by:王健 at:2015-1-14
#     修改排序错误
#     by:王健 at:2015-1-26
#     添加记录日期id
#     by:王健 at:2015-1-31
#     """
#     flag = request.REQUEST.get('flag')
#     timeline = int(request.REQUEST.get('timeline', '0'))
#     record_date_id = request.REQUEST.get('record_date_id')
#     if not timeline:
#         l = WuZiRecord.objects.filter(project_id=project_id, record_date_id=record_date_id, file_group__flag=flag).order_by('-timeline')[:20]
#     else:
#         l = WuZiRecord.objects.filter(project_id=project_id, record_date_id=record_date_id, file_group__flag=flag, timeline__lt=int(timeline)).order_by('-timeline')[:20]
#     return getResult(True, None, MyEncoder.default(l))




@app_power_permissions(None, flag_name='flag')
def query_record_date_by_group(request, project_id=None):
    """
    查询供应商名录，根据应用节点，和时间戳
    by:王健 at:2015-1-29
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    记录最后阅读时间
    by：尚宗凯 at：2015-05-06
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
        l = RecordDate.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = RecordDate.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__gt=int(timeline)).order_by('timeline')[:20]
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), 0, settings.CACHES_TIMEOUT)
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions(None, flag_name='flag')
def query_record_date_by_group_old(request, project_id=None):
    """
    查询供应商名录，根据应用节点，和时间戳 旧数据
    by:王健 at:2015-1-14
    修改排序错误
    by:王健 at:2015-1-29
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    """
    flag = request.REQUEST.get('flag')
    timeline = int(request.REQUEST.get('timeline', '0'))
    if not timeline:
        l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = RecordDate.objects.filter(project_id=project_id, file_group__flag=flag, timeline__lt=int(timeline)).order_by('-timeline')[:20]
    return getResult(True, None, MyEncoder.default(l))

