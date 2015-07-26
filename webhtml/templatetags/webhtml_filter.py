# coding=utf-8
# Date: 15/3/7
# Time: 16:44
# Email:fanjunwei003@163.com
from django import template
from util.address_v2_data import counties
from webhtml.base.views import format_money

__author__ = u'范俊伟'
register = template.Library()


@register.filter(name='money')
def money(value):
    """
    格式化资金的模板filter
    by: 范俊伟 at:2015-03-07
    千分位控制
    by: 范俊伟 at:2015-03-20
    :param value:
    :return:
    """
    return format_money(value, True)


@register.filter(name='address_v2')
def address_v2(value):
    """
    转换地址信息
    by: 范俊伟 at:2015-03-20
    :param value:
    :return:
    """
    address = ''
    try:
        id = str(value)
        for i in counties:
            ddd = str(i.get('id'))
            if str(i.get('id')) == id:
                address = u'%s %s %s' % (i.get('province_name'), i.get('city_name'), i.get('name'))
                break
    except:
        pass
    return address
