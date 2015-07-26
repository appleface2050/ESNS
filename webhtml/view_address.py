# coding=utf-8
# Date: 15/3/20
# Time: 12:17
# Email:fanjunwei003@163.com
from util.address_v2_data import provinces, cities, counties
from util.jsonresult import getResult

__author__ = u'范俊伟'


def get_provinces(request):
    """
    获取省份
    by: 范俊伟 at:2015-03-20
    :param request:
    :return:
    """
    return getResult(True, '', result=provinces)


def get_cities(request):
    """
    根据省份ID获取城市信息
    by: 范俊伟 at:2015-03-20
    :param request:
    :return:
    """
    province_id = request.REQUEST.get('province_id')
    res = []
    for i in cities:
        if str(i.get('province_id')) == province_id:
            res.append(i)
    return getResult(True, '', result=res)


def get_counties(request):
    """
    根据城市ID获取城镇信息
    by: 范俊伟 at:2015-03-20
    :param request:
    :return:
    """
    city_id = request.REQUEST.get('city_id')
    res = []
    for i in counties:
        if str(i.get('city_id')) == city_id:
            res.append(i)
    return getResult(True, '', result=res)


def get_address_by_id(request):
    """
    根据地址id获取地址信息
    by: 范俊伟 at:2015-03-20
    :param request:
    :return:
    """
    id = request.REQUEST.get('id')
    for i in counties:
        if str(i.get('id')) == id:
            return getResult(True, '', i)
    return getResult(False, '无此记录')