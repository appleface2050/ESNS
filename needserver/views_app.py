# coding=utf-8
# Date:2015/01/06
# Email:wangjian2254@gmail.com
import datetime
import json
import time

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings
from needserver.jifenutil import create_data_jifen
from django.core.cache import cache

from needserver.models import FileGroupJSON, FileGroup, \
    FileRecord, UserLastReadTimeline, Project
from nsbcs.models import File
from util import RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, RED_DOT_UNREAD_NUMBER, \
    RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE, RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD, \
    RED_DOT_USER_LAST_READ_TIMELINE, USER_ACTIVITY
from util.cache_handle import get_file_group_id_by_flag_from_cache
from util.jsonresult import getResult, MyEncoder
from util.loginrequired import client_login_project_required, app_power_permissions, login_project_status_zero_required
from util.needpush import NeedPush
from util.project_power_cache import get_alias_by_project_id_flag
from util.tools import find_file_type


__author__ = u'王健'


@client_login_project_required
@transaction.atomic()
def query_app_list(request, project_id=None):
    """
    根据缓存的json串，输出
    by:王健 at:2015-1-11
    组装成带有包含关系的json数据
    by:王健 at:2015-1-12
    组装成不带有包含关系的json数据，填充上project、timeline字段
    by:王健 at:2015-1-13
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    修改为网络图
    by:王健 at:2015-2-12
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    """
    timeline = int(request.REQUEST.get('timeline', '0'))
    if timeline:
        if FileGroupJSON.objects.filter(project_id=project_id, timeline=timeline).exists():
            return getResult(True, u'已经是最新的数据了')

    fgroupjson, create = FileGroupJSON.objects.get_or_create(project_id=project_id)
    if create:
        fgroupjson.timeline = int(time.time())
        filegroup = FileGroup.objects.filter(Q(project_id=project_id) | Q(project_id=None)).order_by('sorted')
        jsongroup = MyEncoder.default(filegroup)
        for g in jsongroup:
            if not g['project'] or not g['icon_url']:
                g['icon_url'] = 'http://needserver.duapp.com/static/icon/%s' % g['icon']
            g['project']=int(project_id)
            g['timeline'] = fgroupjson.timeline
        fgroupjson.jsontext = json.dumps(jsongroup)
        fgroupjson.save()
    return getResult(True, None, json.loads(fgroupjson.jsontext))

@login_project_status_zero_required
@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def create_file_by_group(request, project_id=None):
    """
    根据应用标记，创建文件
    by:王健 at:2015-1-12
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    fileid字段优化为可为一个id也可为‘,’分隔的id字符串
    by:王健 at:2015-1-31
    增加积分
    by:王健 at:2015-2-5
    修改权限校验 函数
    by:王健 at:2015-3-5
    优化settings 使用
    by:王健 at:2015-3-9
    增加filetype字段
    by:尚宗凯 at:2015-3-30
    增加判断filetype
    by:尚宗凯 at:2015-3-30
    增加极光推送
    by:尚宗凯 at:2015-4-8
    逻辑修改,将update改为save,以调用save重载获取图片分辨率
    by: 范俊伟 at:2015-04-09
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    提交日志时刷新阅读时间
    by：尚宗凯 at：2015-05-06
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    增加最新数据时间缓存
    by：尚宗凯 at：2015-05-19
    增加filerecord节点的缓存管理
    by:王健 at:2015-05-21
    修复项目超级管理员新建项目出现小红点bug
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
    fileids = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    # num = File.objects.filter(project_id=project_id, pk__in=fileids).update(file_status=True)
    # if num == 0:
    #     return getResult(False, u'文件不存在', None)
    query = File.objects.filter(project_id=project_id, pk__in=fileids)
    if query.count() == 0:
        return getResult(False, u'文件不存在', None)
    for i in query:
        i.file_status = True
        i.save()

    flag = request.REQUEST.get('flag')
    title = request.REQUEST.get('title')
    text = request.REQUEST.get('text')
    filetype = request.REQUEST.get('filetype')
    id = request.REQUEST.get('id', None)
    if not id:
        filerecord = FileRecord()
        filerecord.file_group = get_object_or_404(FileGroup, flag=flag)
    else:
        filerecord = FileRecord.objects.get(pk=id)
    if request.REQUEST.has_key('title'):
        filerecord.title = title
    if request.REQUEST.has_key('text'):
        filerecord.text = text
    if request.REQUEST.has_key('filetype'):
        filerecord.filetype = filetype
    else:
        f = File.objects.get(id=int(fileids[0]))
        filerecord.filetype = find_file_type(f.name)

    filerecord.project_id = int(project_id)
    filerecord.user = request.user
    files_scale = []
    for fid in fileids:
        filerecord.append_file(fid)
        fileobj = get_object_or_404(File, pk=fid, project_id=project_id)
        try:
            tmp = fileobj.img_size.strip().split("x")
            x = float(tmp[0])
            y = float(tmp[1])
            files_scale.append(float("%.02f" % (x/y)))
        except Exception as e:
            pass
    filerecord.files_scale = str(files_scale)
    filerecord.save()

    from util.cache_handle import query_project_filegroup_data_
    all_flag = query_project_filegroup_data_(project_id)

    #更新项目应用节点最新数据时间
    user_id=request.user.pk
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, filerecord.file_group_id), filerecord.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD % project_id, filerecord.timeline, settings.CACHES_TIMEOUT)
    cache.set(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id, filerecord.timeline, settings.CACHES_TIMEOUT)
    cache.delete(USER_ACTIVITY % (user_id, project_id, filerecord.create_time.strftime('%Y-%m-%d')))

    # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, filerecord.file_group_id, user_id))
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    UserLastReadTimeline.update_last_read_timeline(project_id, 0, user_id)

    file_group_id = filerecord.file_group_id
    alias = get_alias_by_project_id_flag(project_id, flag, file_group_id)
    alias = list(set(alias))
    NeedPush.send_jpush(flag=flag,
                        project_id=project_id,
                        title=Project.get_project_name_by_id(project_id),
                        msg=all_flag['file_group'][file_group_id]['name'],
                        alias=alias,
                        file_group=all_flag['file_group'][file_group_id]
    )

    return getResult(True, None, MyEncoder.default(filerecord), jifen=create_data_jifen(request, settings.CREATE_DATA))


@app_power_permissions(None, flag_name='flag', add=True)
@transaction.atomic()
def delete_file_by_filerecord_id(request, project_id):
    """
    删除上传的文件信息 ,将FileRecord状态设为False,删除File内容
    by:尚宗凯 at:2015-3-27
    修改方法名称
    by:尚宗凯 at:2015-3-30
    极光推送不发送
    by:尚宗凯 at:2015-4-8
    删除项目应用节点最新数据时间
    by:尚宗凯 at：2015-05-20
    增加filerecord节点的缓存管理
    by:王健 at:2015-05-21
    删除时间改为30日之内
    by：尚宗凯 at：2015-05-27
	变更极光推送方法
	by：尚宗凯 at：2015-05-31
    """
    filerecord_id = request.REQUEST.get('filerecord_id', '')
    if filerecord_id:
        fr = FileRecord.objects.get(pk=filerecord_id)
        fileids_str = fr.files
        fileids_str = fileids_str.strip("[").strip("]").split(",")
        fileids = []
        for i in fileids_str:
            fileids.append(int(i))
        if fileids:
            files = File.objects.filter(project_id=project_id, pk__in=fileids)
            for file in files:
                if request.user.pk != file.user_id:
                    return getResult(False, u'不是您发布的数据，不能删除', status_code=2)
                if file.create_time + datetime.timedelta(days=30) < timezone.now():
                    return getResult(False, u'超过30日的数据，不能删除', status_code=2)
                file.delete()
            fr.set_is_active_false()
            fr.save()
            #删除项目应用节点最新数据时间
            cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, fr.file_group_id))
            cache.delete(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD % project_id)
            cache.delete(RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE % project_id)
            return getResult(True, u'成功删除上传的文件信息', filerecord_id)
    return getResult(False, u'记录不存在,删除失败', status_code=2)


@app_power_permissions(None, flag_name='flag')
def query_file_by_group(request, project_id=None):
    """
    根据应用标记，查询应用内容
    by:王健 at:2015-1-12
    修改Model名字，去除下划线， 优化带有日期查询的排序问题，防止隔过数据
    by:王健 at:2015-1-13
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    过滤is_active字段
    by:尚宗凯 at:2015-3-30
    去掉过滤is_active字段
    by:尚宗凯 at:2015-3-30
    记录最后阅读时间
    by：尚宗凯 at：2015-05-06
    增加开始结束时间搜索
    by：尚宗凯 at:2015-05-14
    更新用户项目应用节点未读数量缓存
    by：尚宗凯 at：2105-05-20
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """
    flag = request.REQUEST.get('flag')
    dt = int(request.REQUEST.get('timeline', '0'))
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = FileRecord.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = FileRecord.objects.all()
    if not dt:
        l = l.filter(project_id=project_id, file_group__flag=flag).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__gt=int(dt)).order_by('timeline')[:20]
    user_id = request.user.pk
    UserLastReadTimeline.update_last_read_timeline(project_id=project_id, file_group_id=FileGroup.objects.get(flag=flag).pk, user_id=user_id)
    cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), 0, settings.CACHES_TIMEOUT)
    return getResult(True, None, MyEncoder.default(l))


@app_power_permissions(None, flag_name='flag')
def query_file_by_group_old(request, project_id=None):
    """
    根据应用标记，查询应用内容。查询旧数据
    by:王健 at:2015-1-12
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    修改排序错误
    by:王健 at:2015-1-26
    优化URL参数 timeline 0 和空 一致
    by:王健 at:2015-2-26
    修改权限校验 函数
    by:王健 at:2015-3-5
    过滤is_active字段
    by:尚宗凯 at:2015-3-30
	修改搜索结束时间逻辑
	by：尚宗凯 at：2015-05-28
    """
    flag = request.REQUEST.get('flag')
    dt = int(request.REQUEST.get('timeline', '0'))
    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    if start_date and end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')
        l = FileRecord.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    else:
        l = FileRecord.objects.all()
    if not dt:
        l = l.filter(project_id=project_id, file_group__flag=flag,is_active=True).order_by('-timeline')[:20]
    else:
        l = l.filter(project_id=project_id, file_group__flag=flag, timeline__lt=int(dt), is_active=True).order_by('-timeline')[:20]
    return getResult(True, None, MyEncoder.default(l))


