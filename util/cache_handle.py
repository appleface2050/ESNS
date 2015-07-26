# coding=utf-8
import os
import datetime
from django.db.models import Q
from needserver.models import FileGroup, UserLastReadTimeline, SGlog, EngineCheck, GYSAddress, WuZiRecord, FileRecord, \
    Project
# from needserver.views_project import get_flag_unread_num

os.environ['DJANGO_SETTINGS_MODULE'] = 'Need_Server.settings'
from django.core.cache import cache
from django.conf import settings
# from needserver.models import FileGroup, Person
from util import PROJECT_FILEGROUP, PROJECT_USER_REALPOWERS, RED_DOT_UNREAD_NUMBER, \
    RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, PROJECT_FILEGROUP_NORMAL, \
    RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD, PROJECT_GROUP_USER, MY_PROJECT_QUERY_LIST, \
    PROJECT_INFO, USER_ACTIVITY


def get_file_group_id_by_flag_from_cache(project_id, flag):
    """
    通过flag获取file_group_id
    by:尚宗凯 at：2015-05-19
    优化函数
    by：尚宗凯 at：2015-05-20
    """
    data = query_project_filegroup_data_(project_id)
    return data['flags2'][flag]

def get_flag_by_file_group_id_from_cache(project_id, file_group_id):
    """
    通过file_group_id获取flag
    by:尚宗凯 at：2015-05-19
    优化函数
    by：尚宗凯 at：2015-05-20
    """
    data = query_project_filegroup_data_(project_id)
    return data['flags1'][file_group_id]


def query_project_filegroup_data_(project_id):
    """
    通过project_id从数据库查找缓存数据, 因为FileGroup里面数据库为空，所以当前没有用到project_id
    by:尚宗凯 at：2015-05-19
    FileGroup 当前project 为空，查询方法应当兼容。
    by:王健 at:2015-05-20
    优化函数
    by：尚宗凯 at：2015-05-20
    修改缓存默认项目应用节点
    by:王健 at:2015-05-21
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    优化函数
    by：尚宗凯 at：2015-05-20
    
    """
    result = cache.get(PROJECT_FILEGROUP % project_id)
    if result is None:
        result_normal = query_project_filegroup_data_normal()
        flags = result_normal['flags']
        flags2 = result_normal['flags2']
        file_group = result_normal['file_group']
        flag_father = result_normal['flag_father']
        flag_child = result_normal['flag_child']
        result = {}
        for filegroup in FileGroup.objects.filter(Q(project_id=project_id)):
            flags[filegroup.pk] = filegroup.flag
            flags2[filegroup.flag] = filegroup.pk
            file_group[filegroup.pk] = filegroup.toJSON()
            flag_child[filegroup.flag] = []
        for filegroup in file_group.values():
            if filegroup['father']:
                flag_father[filegroup['flag']] = file_group[filegroup['father']]['flag']
            else:
                flag_father[filegroup['flag']] = filegroup['flag']
        for filegroup in file_group.values():
            if flag_father[filegroup['flag']] != filegroup['flag']:
                flag_child[flag_father[filegroup['flag']]].append(filegroup['flag'])

        for flag in flag_child.keys():
            flag_child[flag] = list(set(flag_child[flag]))

        result["flags"] = flags
        result["flags2"] = flags2
        result["file_group"] = file_group
        result["flag_father"] = flag_father
        result["flag_child"] = flag_child
        cache.set(PROJECT_FILEGROUP % project_id, result, settings.CACHES_TIMEOUT)
    return result


def query_project_filegroup_data_normal():
    """
    查询默认的节点数据
    by:王健 at:2015-05-21
    :return:
    """
    result = cache.get(PROJECT_FILEGROUP_NORMAL)
    if result is None:
        result = {}
        flags, flags2, file_group, flag_father, flag_child = {}, {}, {}, {}, {}
        for filegroup in FileGroup.objects.filter(Q(project_id=None)):
            flags[filegroup.pk] = filegroup.flag
            flags2[filegroup.flag] = filegroup.pk
            file_group[filegroup.pk] = filegroup.toJSON()
            flag_child[filegroup.flag] = []
        for filegroup in file_group.values():
            if filegroup['father']:
                flag_father[filegroup['flag']] = file_group[filegroup['father']]['flag']
            else:
                flag_father[filegroup['flag']] = filegroup['flag']
        for filegroup in file_group.values():
            if flag_father[filegroup['flag']] != filegroup['flag']:
                flag_child[flag_father[filegroup['flag']]].append(filegroup['flag'])

        result["flags"] = flags
        result["flags2"] = flags2
        result["file_group"] = file_group
        result["flag_father"] = flag_father
        result["flag_child"] = flag_child
        cache.set(PROJECT_FILEGROUP_NORMAL, result, settings.CACHES_TIMEOUT)
    return result

def get_last_new_data_timeline(project_id, file_group_id, flag):
    """
    获取某项目某节点最新数据的时间
    by:尚宗凯 at：2015-05-20
    修复小红点bug
    by：尚宗凯 at:2015-05-21
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    timeline = cache.get(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, file_group_id))
    if timeline is None:
        if flag == "gong_cheng_ri_zhi":
            sglog_list = SGlog.objects.filter(project_id=project_id, is_active=True).order_by("-timeline").values_list('timeline')[:1]     # 施工日志
            if len(sglog_list) != 0:
                timeline = sglog_list[0][0]
            else:
                timeline = 0
        elif flag in ["gong_cheng_jian_cha", "zhi_liang_jian_cha", "an_quan_wen_ming_jian_cha"]:
            ec_list = EngineCheck.objects.filter(project_id=project_id, is_active=True, file_group_id=file_group_id).order_by("-timeline").values_list('timeline')[:1]
            if len(ec_list) != 0:
                timeline = ec_list[0][0]
            else:
                timeline = 0
        elif flag in ["wu_zi_guan_li"]:
            gysa_list = GYSAddress.objects.filter(project_id=project_id, is_active=True, file_group_id=file_group_id).order_by("-timeline").values_list('timeline')[:1]
            if len(gysa_list) != 0:
                timeline = gysa_list[0][0]
            else:
                timeline = 0
        elif flag in ["wu_zi_cai_gou_ji_lu","wu_zi_ru_ku_ji_lu","wu_zi_chu_ku_ji_lu"]:
            wzr_list = WuZiRecord.objects.filter(project_id=project_id, is_active=True, file_group_id=file_group_id).order_by("-timeline").values_list('timeline')[:1]
            if len(wzr_list) != 0:
                timeline = wzr_list[0][0]
            else:
                timeline = 0
        else:
            fr_list = FileRecord.objects.filter(project_id=project_id, is_active=True, file_group_id=file_group_id).order_by("-timeline").values_list('timeline')[:1]
            if len(fr_list) != 0:
                timeline = fr_list[0][0]
            else:
                timeline = 0
        cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, file_group_id), timeline, settings.CACHES_TIMEOUT)
    return timeline


def get_last_filerecord_timeline_by_project(project_id):
    """
    filerecord节点的时间戳判断
    by:王健 at:2015-05-21
    修改控制校验
    by:王健 at:2015-05-21
    """
    timeline = cache.get(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD % project_id)
    if timeline is None:
        from needserver import FILE_GROUP_FLAGS
        fr_list = FileRecord.objects.filter(project_id=project_id, is_active=True, file_group__flag__in=FILE_GROUP_FLAGS).order_by("-timeline").values_list('timeline')[:1]
        if len(fr_list) != 0:
            timeline = fr_list[0][0]
        else:
            timeline = 0
        cache.set(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD % project_id, timeline, settings.CACHES_TIMEOUT)
    return timeline
        #
        # # elif SysMessage.has_new_message(project_id=project_id, last_read_time=last_read_time, user_id=user_id):
        # #     return True
        # elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="gong_cheng_jian_cha") and EngineCheck.objects.filter(project_id=project_id, is_active=True,
        #                                 timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # enginecheck              #日常巡查虽然属于工程检查但是数据保存在filerecord里面
        #     return True
        # elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="wu_zi_guan_li") and GYSAddress.objects.filter(project_id=project_id, timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # gysaddress
        #     return True
        # elif Group.whether_user_have_power_by_flag(user_id, project_id, flag="wu_zi_guan_li") and WuZiRecord.objects.filter(project_id=project_id, is_active=True,
        #                                timeline__gt=last_read_time).exclude(user_id=user_id).exists():  # wuzirecord
        #     return True
        # elif Group.whether_user_have_power_by_multi_flag(user_id, project_id,flags=file_record_flags) and FileRecord.objects.filter(project_id=project_id, is_active=True,timeline__gt=last_read_time).exclude(user_id=user_id).exists():
        #     return True
        # else:
        #     return False




# def get_flag_unread_num_use_cache(flag, user_id, project_id):
#     """
#     根据flag获取未读数量
#     by: 尚宗凯 at：2015-05-20
#     """
#     num = cache.get(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id))
#     last_read_time = UserLastReadTimeline.get_last_read_timeline(project_id=project_id,
#                                                                  file_group_id=FileGroup.objects.get(flag=flag).pk,
#                                                                  user_id=user_id)
#     last_new_data_time = cache.get(RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE % (project_id, get_file_group_id_by_flag_from_cache(project_id=project_id, flag=flag)))
#     if num and last_new_data_time and last_read_time and last_read_time > last_new_data_time:
#         return num
#     else:
#         num = get_flag_unread_num(flag, user_id, project_id)
#         cache.set(RED_DOT_UNREAD_NUMBER % (flag, user_id, project_id), num, settings.CACHES_TIMEOUT)
#         return num


def get_project_user_group_use_cache(project_id):
    """
    获取project user group
    by：尚宗凯 at：2015-05-21
    """
    project_user_group = cache.get(PROJECT_GROUP_USER % project_id)
    if project_user_group is None:
        project_user_group = {}
        from needserver.models import Group
        for group in Group.objects.filter(project_id=project_id):
            project_user_group[group.pk] = [i['id'] for i in group.look_members.values("id")] + [i['id'] for i in group.say_members.values("id")]
        cache.set(PROJECT_GROUP_USER % project_id, project_user_group, settings.CACHES_TIMEOUT)
    return project_user_group


def get_my_project_query_list(user_id, project_ids):
    """
    my_project2使用，获取项目的信息
    by：尚宗凯 at：2015-06-01
    修复公示期存在的一个bug
    by：尚宗凯 at：2015-06-02
    status 4 变为 3 时增加删除内容
    by：尚宗凯 at：2015-06-03
	修复bug
	by：尚宗凯 at：2015-06-04
	增加了5 为公示期状态
	by：尚宗凯 at：2015-06-05
    """
    from Need_Server.settings import DELETE_PROJECT_PUBLICITY_PERIOD
    resultlist = cache.get(MY_PROJECT_QUERY_LIST % user_id)
    if resultlist is None:
        l = Project.objects.filter(pk__in=project_ids).order_by('-id')
        resultlist = []
        myprojectids = []
        for p in l:
            if p.status in (4,5) and p.delete_project_time and ((datetime.datetime.now() - p.delete_project_time) >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD)):
                p.status = 3
                p.save()
                cache.delete(PROJECT_INFO % p.pk)
            myprojectids.append(p.pk)
            pd = p.toJSON()
            pd['is_guanzhu'] = False
            if p.status in (4,5) and p.delete_project_time and ((datetime.datetime.now() - p.delete_project_time) >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD)):
                pd['delete'] = True
                pd['is_active'] = False
            resultlist.append(pd)
    else:
        for p in resultlist:
            if p['status'] in (4,5) and p['delete_project_time'] and (datetime.datetime.now() - datetime.datetime.strptime(p['delete_project_time'],'%Y-%m-%d %H:%M:%S') >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD)):
                project = Project.objects.get(pk=p['id'])
                project.status = 3
                project.save()
                cache.delete(PROJECT_INFO % project.pk)
                p['status'] = 3
                p['delete'] = True
                p['is_active'] = False
    cache.set(MY_PROJECT_QUERY_LIST % user_id, resultlist, 60)
    return resultlist


def get_user_activity(user_id, project_id, start_date, end_date):
    """
    获取用户活跃
    by：尚宗凯 at：2016-06-04
    """
    assert start_date <= end_date
    assert user_id is not None
    assert  project_id is not None
    result = {}
    start = start_date
    while start <= end_date:
        num = cache.get(USER_ACTIVITY % (user_id, project_id, start.strftime('%Y-%m-%d')))
        if num is None:
            num = get_user_one_day_data_number(user_id, project_id, start)
            cache.set(USER_ACTIVITY % (user_id, project_id, start.strftime('%Y-%m-%d')), num, settings.CACHES_TIMEOUT)
        result[start.strftime('%Y-%m-%d')] = num
        start += datetime.timedelta(days=1)
    return result


def get_user_one_day_data_number(user_id, project_id, day):
    """
    从数据库中获取用户某天提交数据条数
    by:尚宗凯 at：2016-06-04
    """
    end_day = day + datetime.timedelta(days=1)
    num = 0
    num += SGlog.objects.filter(user_id=user_id, project_id=project_id, create_time__gt=day, create_time__lt=end_day).count()
    num += FileRecord.objects.filter(user_id=user_id, project_id=project_id, create_time__gt=day, create_time__lt=end_day).count()
    num += EngineCheck.objects.filter(user_id=user_id, project_id=project_id, create_time__gt=day, create_time__lt=end_day).count()
    num += WuZiRecord.objects.filter(user_id=user_id, project_id=project_id, create_time__gt=day, create_time__lt=end_day).count()
    num += GYSAddress.objects.filter(user_id=user_id, project_id=project_id, create_time__gt=day, create_time__lt=end_day).count()
    return num
