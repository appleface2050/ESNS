# coding=utf-8
# Date: 15/4/16
# Time: 14:02
# Email:fanjunwei003@163.com
from django.conf import settings
import datetime
import mongoengine

__author__ = u'范俊伟'
mongoengine.connect(settings.NEED_MONGODB_CONFIG.get('name'),
                    host=settings.NEED_MONGODB_CONFIG.get('host', 27017),
                    port=settings.NEED_MONGODB_CONFIG.get('port'),
                    username=settings.NEED_MONGODB_CONFIG.get('username'),
                    password=settings.NEED_MONGODB_CONFIG.get('password')
                    )


class RequestCounter(mongoengine.Document):
    """
    接口请求计数表
    by: 范俊伟 at:2015-04-16
    """
    uid = mongoengine.IntField()
    key = mongoengine.StringField(max_length=255)
    create_time = mongoengine.DateTimeField(default=datetime.datetime.now)


class DangerUser(mongoengine.Document):
    """
    危险用户记录
    by: 范俊伟 at:2015-04-16
    """
    uid = mongoengine.IntField()
    count = mongoengine.IntField()
    flag = mongoengine.IntField()  # 0:警告,1:禁用账号
    create_time = mongoengine.DateTimeField(default=datetime.datetime.now)