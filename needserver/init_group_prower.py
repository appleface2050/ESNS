# coding=utf-8
# Date: 15/3/4'
# Email: wangjian2254@icloud.com
from needserver.models import Project, FileGroup

__author__ = u'王健'


def init_prower_by_group(group):
    """
    根据分组 设置 分组的默认权限
    by:王健 at:2015-3-4
    增加新节点
    by:尚宗凯 at:2015-4-13
    :param group:
    :return:
    """
    if group.project:
        project = group.project
    else:
        project = Project.objects.get(pk=group.project_id)
    if group.type == 'sys_manage':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du',
                                                     'gong_zuo_ying_xiang_ji_lu', 'gong_cheng_jian_cha',
                                                     'xing_xiang_zhan_shi', 'bao_guang_jing_gao', 'xiang_mu_wen_hua',
                                                     'wu_zi_guan_li', 'gong_cheng_jin_du', 'wen_jian_chuan_da',
                                                     'gong_cheng_yu_jue_suan', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'],
                                                    look=True, add=True, update=True, delete=True, app_add=True,
                                                    app_update=True, app_del=True)
    elif group.type == 'sys_xzzg':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_jsdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)

    elif group.type == 'sys_sjdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_kcdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_jldw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_sgdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'xing_xiang_zhan_shi', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_xmjl':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'gong_cheng_jian_cha', 'xing_xiang_zhan_shi', 'bao_guang_jing_gao', 'xiang_mu_wen_hua', 'wu_zi_guan_li', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'gong_cheng_yu_jue_suan', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True, add=True)
    elif group.type == 'sys_lwfbdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'gong_cheng_jian_cha', 'xing_xiang_zhan_shi', 'bao_guang_jing_gao', 'xiang_mu_wen_hua', 'wu_zi_guan_li', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)
    elif group.type == 'sys_zyfbdw':
        group.powers = get_prowerid_prower_by_flag(['gong_cheng_ri_zhi', 'gong_cheng_xing_xiang_jin_du', 'gong_zuo_ying_xiang_ji_lu',
                                                     'gong_cheng_jian_cha', 'xing_xiang_zhan_shi', 'bao_guang_jing_gao', 'xiang_mu_wen_hua', 'gong_cheng_jin_du',
                                                     'wen_jian_chuan_da', 'shi_ce_shi_liang', 'zhi_shi_ku','wo_xing_wo_xiu','shi_gong_zong_ping_mian_tu'], look=True)


def get_prowerid_by_flag(flags):
    a =  FileGroup.objects.filter(flag__in=flags).values_list('id')
    return [x[0]*100 for x in FileGroup.objects.filter(flag__in=flags).values_list('id')]


def get_prowerid_prower_by_flag(flags, look=False, add=False, update=False, delete=False, app_add=False,
                                app_update=False, app_del=False):
    """
    根据分组标记 和 参数 计算权限值
    long 改为 int
    by:王健 at:2015-3-6
    :param flags:
    :param look:
    :param add:
    :param update:
    :param delete:
    :param app_add:
    :param app_update:
    :param app_del:
    :return:
    """
    l = get_prowerid_by_flag(flags)
    rl = []
    if look:
        for i in l:
            rl.append(int(i+0))
    if add:
        for i in l:
            rl.append(int(i+1))

    if update:
        for i in l:
            rl.append(int(i+2))

    if delete:
        for i in l:
            rl.append(int(i+3))

    if app_add:
        for i in l:
            rl.append(int(i+4))

    if app_update:
        for i in l:
            rl.append(int(i+5))

    if app_del:
        for i in l:
            rl.append(int(i+6))
    return rl

