# coding=utf-8
# Date: 15/4/10'
# Email: wangjian2254@icloud.com
import json
from django.conf import settings
from django.db.models import Q
from Need_Server.settings import CACHES_JPUSH_ALIAS_TIME_OUT

from util import PROJECT_ID_FLAG_OR_FILEGROUP_ID_ALIAS, PROJECT_POWER_TIMELINE, PROJECT_USER_REALPOWERS



__author__ = u'王健'

from django.core.cache import cache


def get_alias_by_project_id_flag(project_id, flag, file_group_id=None):
    """
    通过缓存查找alias
    by：尚宗凯 at：2015-04-09
    修复bug
    by：尚宗凯 at：2015-04-09
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修复逻辑bug
    by：尚宗凯 at：2015-05-21
    修改获取alias逻辑
    by：尚宗凯 at：2015-05-31
    """
    cache_key = PROJECT_ID_FLAG_OR_FILEGROUP_ID_ALIAS % (project_id, flag)
    alias = cache.get(cache_key)
    if alias is None:
        if file_group_id is None:
            from util.cache_handle import query_project_filegroup_data_
            result = query_project_filegroup_data_(project_id)
            file_group_id = result['flags2'][flag]
        alias = []
        users = []
        from util.cache_handle import get_project_user_group_use_cache
        project_user_group = get_project_user_group_use_cache(project_id)
        for user_list in project_user_group.values():
            users.extend(user_list)
        users = list(set(users))
        for user_id in users:
            powers = get_real_power_by_project_user(project_id,user_id)
            if int(file_group_id)*100 in powers:
                alias.append(user_id)
    cache.set(cache_key, alias, CACHES_JPUSH_ALIAS_TIME_OUT)
    return alias

# def get_alias_by_project_id_filegroup_id(project_id, filegroup_id):
#     """
#     根据project_id filegroup_id获取alias
#     by：王健 at：2015-05-07
#     优化缓存结果的非空判断
#     by:王健 at:2015-05-21
#     修改控制校验
#     by:王健 at:2015-05-21
#     """
#     from needserver.models import Group
#
#     cache_key = PROJECT_ID_FLAG_OR_FILEGROUP_ID_ALIAS % (project_id, filegroup_id)
#     alias = cache.get(cache_key)
#     if alias is None:
#         project_powers = get_cache_project_power_timeline(project_id)[0]
#         flag = project_powers['pks'][str(filegroup_id)]
#         alias = Group.get_user_id_by_group_ids(get_power_group(flag, project_powers))
#         cache.set(cache_key, alias, CACHES_JPUSH_ALIAS_TIME_OUT)
#     return alias


def get_cache_project_power_timeline(project_id):
    """
    获取缓存中的project_power_timeline
    by：尚宗凯 at：2015-04-09
    修改返回值，兼容 权限 观察者模块
    by：王健 at：2015-04-10
    修改极光推送方式
    by：尚宗凯 at：2015-05-07
    优化缓存结果的非空判断
    by:王健 at:2015-05-21
    修改逻辑错误
    by：尚宗凯 at：2015-05-21
    """
    from needserver.models import Group, FileGroup

    cache_key_project = PROJECT_POWER_TIMELINE % project_id
    project_powers = cache.get(cache_key_project)
    project_powers_flag = False

    if project_powers is None:
        project_powers_flag = True
        flag_dict = {}
        flag_pk_dict = {}
        flag_pk_dict = {}
        powers_dict = {}
        power_timeline = 0
        project_powers = {'flag': flag_dict, 'powers': powers_dict, 'pks': flag_pk_dict}
        for file_group in FileGroup.objects.filter(Q(project_id=project_id) | Q(project=None)):
            if file_group.father_id:
                flag_dict[file_group.flag] = file_group.father_id
            else:
                flag_dict[file_group.flag] = file_group.pk
            flag_pk_dict[str(file_group.pk)] = file_group.flag
        for f in flag_dict.keys():
            for k in flag_pk_dict.keys():
                if flag_pk_dict[k] == f:
                    flag_pk_dict[k] = flag_pk_dict[str(flag_dict[f])]


        for x in Group.objects.filter(project_id=project_id).exclude(type='root').values_list('powers', 'timeline',
                                                                                              'id'):
            if x[0] and isinstance(x[0], (str, unicode)):
                powers = json.loads(x[0])
                powers_dict[str(x[2])] = powers
            if power_timeline < int(x[1]):
                power_timeline = int(x[1])
        project_powers['timeline'] = power_timeline
        cache.set(cache_key_project, project_powers, settings.CACHES_TIMEOUT)
    return project_powers, project_powers_flag


def get_power_group(flag, project_powers):
    """
    获取当前flag有权限的group
    by:尚宗凯 at：2015-04-09
    修改获取group方式
    by：王健 at：2015-05-07
    """
    from needserver.models import FileGroup

    power = project_powers['flag'].get(flag) * 100
    grps = []
    for p in project_powers['powers']:
        if power in project_powers['powers'][p]:
            grps.append(p)
    return grps


def get_real_power_by_project_user(project_id, user_id):
    """
    通过project_id user_id返回用户的真实权限
    by: 尚宗凯 at：2015-05-20
    """
    powers = cache.get(PROJECT_USER_REALPOWERS % (project_id, user_id))
    if powers is None:
        from needserver.models import Person
        powers = Person.objects.get(user_id=user_id, project_id=project_id).real_powers()
        cache.set(PROJECT_USER_REALPOWERS % (project_id, user_id), powers, settings.CACHES_TIMEOUT)
    return powers


def whether_user_have_power_by_flag(user_id, project_id, flags_or_flag, all_flag_dict=None):
    """
    通过user_id project_id flag判断是否具有权限
    by：尚宗凯 at：2015-05-20
    针对示例项目对powers做特殊处理
    by：尚宗凯 at：2015-05-21
    使用外部参数，避免一次 cache操作
    by:王健 at:2015-05-28
    """
    if int(project_id) == settings.SHOW_PROJECT_ID:
        powers = []
    else:
        powers = get_real_power_by_project_user(project_id, user_id)
    from util.cache_handle import query_project_filegroup_data_
    if all_flag_dict is None:
        all_flag_dict = query_project_filegroup_data_(project_id)
    if isinstance(flags_or_flag,(str,unicode)):
        file_group_id = all_flag_dict['flags2'][all_flag_dict['flag_father'][flags_or_flag]]
        if int(file_group_id)*100 in powers:
            return True
        else:
            return False
    else:
        result = {}
        for flag in flags_or_flag:
            file_group_id = all_flag_dict['flags2'][all_flag_dict['flag_father'][flag]]
            if int(file_group_id)*100 in powers:
                result[flag] = True
            else:
                result[flag] = False
        return result


def all_flag_user_have_power_by_flag(user_id, project_id, flags_or_flag, all_flag_dict=None):
    """
    根据flag 获取 具有权限的所有flag
    :param user_id:
    :param project_id:
    :param flags_or_flag:
    :param all_flag_dict:
    :return:
    """
    if all_flag_dict is None:
        from util.cache_handle import query_project_filegroup_data_
        all_flag_dict = query_project_filegroup_data_(project_id)
    if not flags_or_flag:
        flags_or_flag = all_flag_dict['flags2'].keys()
    m = whether_user_have_power_by_flag(user_id, project_id, flags_or_flag, all_flag_dict)
    tmp = []
    for k in m:
        if m[k]:
            if not all_flag_dict["flag_child"][k]:
                tmp.append(k)
            else:
                tmp.extend(all_flag_dict["flag_child"][k])
    all_have_power_flag = list(set(tmp))
    return all_have_power_flag