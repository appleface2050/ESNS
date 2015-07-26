# coding=utf-8
# Date:2015/01/06
# Email:wangjian2254@gmail.com
import datetime
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.utils import timezone
from Need_Server.settings import CREATE_DATA
from needserver.jifenutil import create_data_jifen
from django.core.cache import cache
from django.conf import settings

from needserver.models import SGTQlog, SGlog, FileGroup, UserLastReadTimeline, Project
from util import RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, PROJECT_FILEGROUP, RED_DOT_UNREAD_NUMBER, \
    RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE, RED_DOT_USER_LAST_READ_TIMELINE, USER_ACTIVITY
from util.cache_handle import get_file_group_id_by_flag_from_cache
from util.jsonresult import getResult, MyEncoder
from util.loginrequired import client_login_project_required, app_power_permissions, \
    login_project_status_zero_required
from util.needpush import NeedPush
from util.project_power_cache import get_alias_by_project_id_flag


__author__ = u'王健'


@app_power_permissions('gong_cheng_ri_zhi')
def query_log_date_list(request, project_id=None):
    """
    查询项目的日志天气列表
    by:王健 at:2015-1-6
    根据date字段排序，分页
    by:王健 at:2015-1-8
    修改Model名字，去除下划线， 优化带有日期查询的排序问题，防止隔过数据
    by:王健 at:2015-1-13
    改用时间戳 筛选
    by:王健 at:2015-1-20
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-4
    """
    date = int(request.REQUEST.get('timeline', '0'))
    if not date:
        l = SGTQlog.objects.filter(project_id=project_id).order_by('-date')[0:20]
    else:
        l = SGTQlog.objects.filter(project_id=project_id, timeline__gt=int(date)).order_by('date')[:20]
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions('gong_cheng_ri_zhi')
def query_log_date_list_old(request, project_id=None):
    """
    根据date字段排序，分页,查询旧数据
    by:王健 at:2015-1-8
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    改用时间戳 筛选
    by:王健 at:2015-1-20
    修改排序错误
    by:王健 at:2015-1-26
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-4
    """
    date = int(request.REQUEST.get('timeline', '0'))
    if not date:
        l = SGTQlog.objects.filter(project_id=project_id).order_by('-date')[0:20]
    else:
        l = SGTQlog.objects.filter(project_id=project_id, timeline__lt=int(date)).order_by('-date')[:20]
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions('gong_cheng_ri_zhi')
def query_log_list_by_date(request, project_id=None):
    """
    查询项目的施工日志根据日期
    by:王健 at:2015-1-6
    datetime 进行时间点刷新
    by:王健 at:2015-1-8
    有datetime的情况下 查询日志
    by:王健 at:2015-1-12
    datetime 改为 create_time
    by:王健 at:2015-1-12
    修改Model名字，去除下划线， 优化带有日期查询的排序问题，防止隔过数据
    by:王健 at:2015-1-13
    没有时间参数时，一次获取全部数据
    by:王健 at:2015-1-20
    日志正序输出
    by:王健 at:2015-1-30
    日志也使用timeline
    by:王健 at:2015-2-10
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-4
    增加最后阅读时间
    by：尚宗凯 at：2015-05-06
	增加根据开始时间结束时间搜索
	by：尚宗凯 at：2015-05-13
    优化查询
    by：尚宗凯 at：2015-05-20
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """
    sg_tq_id = request.REQUEST.get('sg_tq_id', '0')
    timeline = int(request.REQUEST.get('timeline', '0'))
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = SGlog.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = SGlog.objects.all()
    if not timeline:
        l = l.filter(project_id=project_id, sg_tq_log_id=sg_tq_id).order_by('timeline')
    else:
        l = l.filter(project_id=project_id, sg_tq_log_id=sg_tq_id, timeline__gt=int(timeline)).order_by('timeline')[:20]
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag="gong_cheng_ri_zhi").pk, user_id=user_id)
    cache.set(RED_DOT_UNREAD_NUMBER % ("gong_cheng_ri_zhi", user_id, project_id), 0, settings.CACHES_TIMEOUT)
    return getResult(True, None, MyEncoder.default(l))

@login_project_status_zero_required
@app_power_permissions('gong_cheng_ri_zhi', add=True)
@transaction.atomic()
def update_log_by_date(request, project_id=None):
    """
    更新或添加新的施工日志根据日期、天气
    by:王健 at:2015-1-6
    修改属性名
    by:王健 at:2015-1-8
    修改属性名，天气和风力
    by:王健 at:2015-1-12
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    天气表增加 timeline、num、create_time 字段
    by:王健 at:2015-1-20
    返回的数据，包括施工天气信息
    by:王健 at:2015-1-28
    增加积分
    by:王健 at:2015-2-5
    记录日志最后上传人
    by:王健 at:2015-2-10
    修改权限校验 函数
    by:王健 at:2015-3-4
    提交日志时刷新阅读时间
    by：尚宗凯 at：2015-05-06
    增加最新数据时间缓存
    by：尚宗凯 at：2015-05-20
    修复小红点bug
    by:尚宗凯 at：2015-05-27
    增加项目状态为 0 装饰器
    by:尚宗凯 at：2015-05-31
	变更极光推送方法
	by：尚宗凯 at：2015-05-31
	添加用户活跃度缓存
    by：尚宗凯 at：2015-06-04
    """
    if not request.REQUEST.get('text'):
        return getResult(False, u'日志内容不能为空', None)
    sg_tq_id = request.REQUEST.get('sg_tq_id', '')
    if not sg_tq_id:
        sg_tq_log, create = SGTQlog.objects.get_or_create(project_id=project_id, file_group=FileGroup.objects.get(flag='gong_cheng_ri_zhi'), date=timezone.now())

    else:
        sg_tq_log = SGTQlog.objects.get(pk=sg_tq_id)
    f = False
    if not sg_tq_log.weather:
        sg_tq_log.weather = request.REQUEST.get('weather', '')
        f = True
    if not sg_tq_log.wind:
        sg_tq_log.wind = request.REQUEST.get('wind')
        f = True
    if not sg_tq_log.qiwen:
        sg_tq_log.qiwen = request.REQUEST.get('qiwen')
        f = True
    if f:
        sg_tq_log.save()
    pk = request.REQUEST.get('id')
    if pk:
        sg_log = SGlog.objects.get(pk=pk)
        if sg_log.project_id != int(project_id) or sg_log.user_id != request.user.pk:
            return getResult(False, u'不是一个项目的日志', status_code=2)
    else:
        sg_log = SGlog()
        sg_tq_log.create_time = timezone.now()
        sg_tq_log.num += 1
        sg_tq_log.last_create_user = request.user
        sg_tq_log.save()
    sgtqlog = MyEncoder.default(sg_tq_log)
    sg_log.project_id = int(project_id)
    sg_log.sg_tq_log = sg_tq_log
    sg_log.text = request.REQUEST.get('text', '')
    sg_log.user = request.user
    sg_log.save()
    sgtqlog.update(MyEncoder.default(sg_log))

    #更新项目应用节点最新数据时间
    user_id = request.user.pk
    flag = "gong_cheng_ri_zhi"
    from util.cache_handle import query_project_filegroup_data_
    all_flag = query_project_filegroup_data_(project_id)

    # file_group_id = get_file_group_id_by_flag_from_cache(project_id=project_id, flag="gong_cheng_ri_zhi")
    file_group_id = all_flag['flags2'][flag]
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, file_group_id), sg_log.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id, sg_log.timeline, settings.CACHES_TIMEOUT)
    # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id))
    UserLastReadTimeline.update_last_read_timeline(project_id, file_group_id, user_id)
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
    cache.delete(USER_ACTIVITY % (user_id, project_id, sg_log.create_time.strftime('%Y-%m-%d')))
    return getResult(True, u'保存日志成功', sgtqlog, jifen=create_data_jifen(request, CREATE_DATA))


@client_login_project_required
@transaction.atomic()
def del_log_by_id(request, project_id=None):
    """
    不超过24小时的日志，可以由发布者 删除
    by:王健 at:2015-2-10
    清除最新数据事件缓存
    by：尚宗凯 at：2015-05-20
    删除时间改为30日之内
    by：尚宗凯 at：2015-05-27
    """
    pk = request.REQUEST.get('id')
    if pk:
        sg_log = SGlog.objects.get(pk=pk)
        if sg_log.project_id != int(project_id) or sg_log.user_id != request.user.pk:
            return getResult(False, u'不是您发布的数据，不能删除', status_code=2)
        if (sg_log.create_time + datetime.timedelta(days=30)) < timezone.now():
            return getResult(False, u'超过30日的数据，不能删除')
        sg_log.sg_tq_log.num -= 1
        sg_log.sg_tq_log.save()
        sg_log.is_active = False
        sg_log.create_time = timezone.now()
        sg_log.save()
        #删除项目应用节点最新数据时间
        cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, get_file_group_id_by_flag_from_cache(project_id=project_id, flag="gong_cheng_ri_zhi")))
        cache.delete(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
        return getResult(True, u'删除日志成功', pk)
    else:
        return getResult(False, u'参数不正确')
