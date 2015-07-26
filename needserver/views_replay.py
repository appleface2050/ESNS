# coding=utf-8
# Date:2015/01/13
# Email:wangjian2254@icloud.com
# from bson import ObjectId
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
from Need_Server.settings import CREATE_DATA
from needserver import FILE_GROUP_FLAGS, FILE_GROUP_FLAGS_FILES, FILE_GROUP_FLAGS_BGIMAGES, FILE_GROUP_FLAGS_IMAGES
from needserver.jifenutil import create_data_jifen

from needserver.models import FileRecord,Reply, NSUser, EngineCheck
from util.cache_handle import query_project_filegroup_data_
from util.jsonresult import getResult, MyEncoder, is_success_mongodb_result
from util.loginrequired import client_login_project_required
from util.project_power_cache import whether_user_have_power_by_flag, all_flag_user_have_power_by_flag


__author__ = u'王健'
# from mango import database as db
from util.apicloud import create_zan_by_filerecord, delete_zan_by_filerecord, create_replay_by_filerecord, \
    query_replay_by_filerecord_id, query_replay_by_timeline, query_replay_num_by_timeline, get_last_replay_by_timeline


@client_login_project_required
@transaction.atomic()
def ding_filerecord_by_id(request, project_id=None):
    """
    对一个记录发出顶的操作
    by:王健 at:2015-2-25
    点赞
    by:王健 at:2015-05-28
    修改提示语
    by:王健 at:2015-05-28
    解决enginecheck 没有title的bug
    by:王健 at:2015-06-01
    添加typeflag 字段
    by:王健 at:2015-06-02
    """
    filerecord_id = request.REQUEST.get('id')
    flag = request.REQUEST.get('flag')
    if filerecord_id and flag:
        title = None
        typeflag = 'images'
        if flag in FILE_GROUP_FLAGS_FILES:
            typeflag = 'files'
        elif flag in FILE_GROUP_FLAGS_BGIMAGES:
            typeflag = 'bgimages'
        elif flag in FILE_GROUP_FLAGS_IMAGES:
            typeflag = 'images'
        else:
            typeflag = 'jc'

        if flag in FILE_GROUP_FLAGS:
            filerecord = get_object_or_404(FileRecord, pk=filerecord_id, project_id=project_id)
            title = filerecord.title
        elif flag in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
            filerecord = get_object_or_404(EngineCheck, pk=filerecord_id, project_id=project_id)
            title = filerecord.desc
        else:
            filerecord = None
            title = ''

        if filerecord:
            result = create_zan_by_filerecord(project_id, flag, filerecord_id, request.user.pk, int(time.time()), typeflag)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')

            return getResult(True, u'成功对 %s 点了个赞。' % title, result, jifen=create_data_jifen(request, CREATE_DATA))
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


@client_login_project_required
@transaction.atomic()
def delete_ding_filerecord_by_id(request, project_id=None):
    """
    对一个记录发出顶的操作
    by:王健 at:2015-2-25
    删除点赞
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    解决enginecheck 没有title的bug
    by:王健 at:2015-06-01
    """
    filerecord_id = request.REQUEST.get('id')
    flag = request.REQUEST.get('flag')
    if filerecord_id and flag:
        if flag in FILE_GROUP_FLAGS:
            filerecord = get_object_or_404(FileRecord, pk=filerecord_id, project_id=project_id)
            title = filerecord.title
        elif flag in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
            filerecord = get_object_or_404(EngineCheck, pk=filerecord_id, project_id=project_id)
            title = filerecord.desc
        else:
            filerecord = None
            title = ''

        if filerecord:
            result = delete_zan_by_filerecord(project_id, flag, filerecord_id, request.user.pk)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'成功 %s 取消了赞。' % title, result)
        return getResult(False, u'数据不存在')
    else:
        return getResult(False, u'请提供正确的参数')


@client_login_project_required
@transaction.atomic()
def replay_filerecord_by_id(request, project_id=None):
    """
    对一条记录发出评论
    by:王健 at:2015-2-25
    去除 mongodb 影响
    by:王健 at:2015-3-8
    在某个节点下数据中发布评论
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    增加typeflag 字段
    by:王健 at:2015-06-03
    只取前一百评论内容
    by:王健 at:2015-06-04
    """
    filerecord_id = request.REQUEST.get('id')
    flag = request.REQUEST.get('flag')
    content = request.REQUEST.get('content', '')[:100]
    to_user = request.REQUEST.get('to_user', '0')
    if flag and filerecord_id and content:
        typeflag = 'images'
        if flag in FILE_GROUP_FLAGS_FILES:
            typeflag = 'files'
        elif flag in FILE_GROUP_FLAGS_BGIMAGES:
            typeflag = 'bgimages'
        elif flag in FILE_GROUP_FLAGS_IMAGES:
            typeflag = 'images'
        else:
            typeflag = 'jc'
        if flag in FILE_GROUP_FLAGS:
            filerecord = get_object_or_404(FileRecord, pk=filerecord_id, project_id=project_id)
        elif flag in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
            filerecord = get_object_or_404(EngineCheck, pk=filerecord_id, project_id=project_id)
        else:
            filerecord = None
        if filerecord:
            result = create_replay_by_filerecord(project_id, flag, filerecord_id, request.user.pk, int(time.time()), content, typeflag, to_user)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'发布评论成功。', result, jifen=create_data_jifen(request, CREATE_DATA))
    else:
        return getResult(False, u'请提供正确的参数')


@client_login_project_required
def query_replay_filerecord_by_id(request, project_id=None):
    """
    查询查询记录的评论信息
    by:王健 at:2015-2-25
    去除 mongodb 影响
    by:王健 at:2015-3-8
    获取某个节点数据下的所有评论
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    """
    filerecord_id = request.REQUEST.get('id')
    flag = request.REQUEST.get('flag')
    if flag and filerecord_id:
        if flag in FILE_GROUP_FLAGS:
            filerecord = get_object_or_404(FileRecord, pk=filerecord_id, project_id=project_id)
        elif flag in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
            filerecord = get_object_or_404(EngineCheck, pk=filerecord_id, project_id=project_id)
        else:
            filerecord = None
        if filerecord:
            result = query_replay_by_filerecord_id(flag, filerecord_id, project_id)
            if result is None or (isinstance(result, dict) and result.has_key("code")):
                return getResult(False, u'操作失败，请稍后再试')
            return getResult(True, u'获取评论成功。', {'pinglun': result, 'filerecord': filerecord.toJSON()})
    else:
        return getResult(False, u'请提供正确的参数')


@client_login_project_required
def query_replay_filerecord_by_timeline(request, project_id=None):
    """
    根据时间戳，获取所有评论
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    优化评论时间戳设计
    by:王健 at:2015-06-02
    优化返回值格式
    by:王健 at:2015-06-02
    """
    person = request.user.person_set.filter(project_id=project_id)[0]
    all_flag = query_project_filegroup_data_(project_id)
    all_have_power_flag = all_flag_user_have_power_by_flag(request.user.pk, project_id, None, all_flag)
    result = query_replay_by_timeline(person.replay_timeline, request.user.pk, project_id, all_have_power_flag)
    if result is None or (isinstance(result, dict) and result.has_key("code")):
        return getResult(False, u'操作失败，请稍后再试')
    if isinstance(result, list):
        l = {'images': [], 'jc': [], 'files': [], 'bgimages': []}
        dl = {'images': [], 'jc': [], 'files': [], 'bgimages': []}
        for p in result:
            if p['flag'] in FILE_GROUP_FLAGS_FILES:
                l['files'].append(p['filerecord'])
            elif p['flag'] in FILE_GROUP_FLAGS_BGIMAGES:
                l['bgimages'].append(p['filerecord'])
            elif p['flag'] in FILE_GROUP_FLAGS_IMAGES:
                l['images'].append(p['filerecord'])
            elif p['flag'] in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
                l['jc'].append(p['filerecord'])
            else:
                pass
        if l['images']:
            dl['images'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['images'], project_id=project_id)])
        if l['bgimages']:
            dl['bgimages'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['bgimages'], project_id=project_id)])
        if l['files']:
            dl['files'].extend([f.toJSON() for f in FileRecord.objects.filter(pk__in=l['files'], project_id=project_id)])
        if l['jc']:
            dl['jc'].extend([f.toJSON() for f in EngineCheck.objects.filter(pk__in=l['jc'], project_id=project_id)])
        for r in dl.values():
            for f in r:
                f['flag'] = all_flag['flags'][f['file_group']]
        dl['pinglun'] = result
        return getResult(True, u'获取评论成功。', dl)
    else:
        return getResult(False, u'获取评论失败')


@client_login_project_required
def count_replay_filerecord_by_timeline(request, project_id=None):
    """
    查询未读评论的数量
    by:王健 at:2015-05-28
    修改错误提示语
    by:王健 at:2015-05-28
    优化评论数据
    by:王健 at:2015-05-28
    优化评论时间戳设计
    by:王健 at:2015-06-02
    结果中添加typeflag字段，解决pinglun，bug
    by:王健 at:2015-06-02
    :param request:
    :param project_id:
    :return:
    """
    person = request.user.person_set.filter(project_id=project_id)[0]
    all_flag = query_project_filegroup_data_(project_id)
    all_have_power_flag = all_flag_user_have_power_by_flag(request.user.pk, project_id, None, all_flag)
    result = query_replay_num_by_timeline(person.replay_timeline, request.user.pk, project_id, all_have_power_flag)
    if result is None or (isinstance(result, dict) and result.has_key("code")):
        return getResult(False, u'操作失败，请稍后再试')
    p = get_last_replay_by_timeline(request.user.pk, project_id, all_have_power_flag)
    result['pinglun'] = p
    if p:
        if p['flag'] in FILE_GROUP_FLAGS:
            result['filerecord'] = FileRecord.objects.get(pk=p['filerecord']).toJSON()
        elif p['flag'] in ('zhi_liang_jian_cha', 'an_quan_wen_ming_jian_cha'):
            result['filerecord'] = EngineCheck.objects.get(pk=p['filerecord']).toJSON()
        result['filerecord']['flag'] = all_flag['flags'][result['filerecord']['file_group']]
        if p['flag'] in FILE_GROUP_FLAGS_BGIMAGES:
            result['filerecord']['typeflag'] = 'bgimages'
        elif p['flag'] in FILE_GROUP_FLAGS_FILES:
            result['filerecord']['typeflag'] = 'files'
        elif p['flag'] in FILE_GROUP_FLAGS_IMAGES:
            result['filerecord']['typeflag'] = 'images'
        else:
            result['filerecord']['typeflag'] = 'jc'

    return getResult(True, u'获取评论数量成功。', result)

