# coding=utf-8
# Date: 14/11/5
# Time: 19:28
# Email:fanjunwei003@163.com
import uuid
from django.db.models.signals import post_syncdb
from webhtml.models import *
from webhtml import models as webhtml_models

__author__ = u'范俊伟'


def initData(**kwargs):
    """
    修改测试套餐
    by: 范俊伟 at:2015-03-07
    :param kwargs:
    :return:
    """
    if Product.objects.all().count() == 0:
        Product.objects.create(flag=str(uuid.uuid1()),
                               name='充值1分钱,得5000金豆',
                               desc='产品介绍',
                               price=1,
                               show_price=5000 * 100,
                               gold=5000
        )


post_syncdb.connect(initData, sender=webhtml_models)