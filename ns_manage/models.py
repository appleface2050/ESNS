# coding=utf-8
from django.conf import settings
from django.db import models

# Create your models here.
from util.basemodel import JSONBaseMixin

CONTRACT_STATUS_NO_ASSIGN = 0
CONTRACT_STATUS_ASSIGNED = 1
CONTRACT_STATUS_SIGNED = 2
CONTRACT_STATUS_PAYED_NO_ARRIVED = 3
CONTRACT_STATUS_PAYED_ARRIVED = 4
CONTRACT_STATUS_DROP = -1

CONTRACT_STATUS_CHOICES = (
    (CONTRACT_STATUS_NO_ASSIGN, u'未分配'),
    (CONTRACT_STATUS_ASSIGNED, u'已分配未签署'),
    (CONTRACT_STATUS_SIGNED, u'已签署未支付'),
    (CONTRACT_STATUS_PAYED_NO_ARRIVED, u'已支付未到账'),
    (CONTRACT_STATUS_PAYED_ARRIVED, u'已到账'),
    (CONTRACT_STATUS_DROP, u'作废'),
)


class BackUserInfo(models.Model, JSONBaseMixin):
    """
    后台用户信息扩展
    by: 范俊伟 at:2015-06-11
    修改user外键的写法，添加支付宝账号、身份证号、渠道代码
    by:王健 at:2015-06-11
    """
    USER_TYPE_CHOICES = (
        (-1, u'无效'),
        (0, u'客服'),
        (1, u'会计'),
        (2, u'推广员'),
    )
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, verbose_name=u"用户类型")
    need_user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, verbose_name=u'和NSUser关联')

    # 微信参数部分
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'微信昵称')
    wx_icon_url = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'微信头像')
    openid = models.CharField(max_length=50, db_index=True, unique=True, null=True, verbose_name=u'微信openid')
    language = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'语言')
    city = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'城市')
    province = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'省份')
    country = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'国家')
    subscribe_time = models.IntegerField(null=True, blank=True, verbose_name=u'关注时间戳')

    alipay_username = models.CharField(max_length=50, null=True, verbose_name=u'支付宝账号')
    id_num = models.CharField(max_length=20, null=True, verbose_name=u'身份证号')
    channel = models.CharField(max_length=20, unique=True, null=True, db_index=True, verbose_name=u'渠道代码')


class Contract(models.Model, JSONBaseMixin):
    """
    合同
    by: 范俊伟 at:2015-06-11
    修改user外键的写法
    by:王健 at:2015-06-11
    """
    # TODO: 字段未完成
    no = models.CharField(primary_key=True, max_length=255, verbose_name='合同编号')
    status = models.IntegerField(choices=CONTRACT_STATUS_CHOICES, default=CONTRACT_STATUS_NO_ASSIGN,
                                 verbose_name='合同状态')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name='关联推广员')
    project = models.ForeignKey('needserver.Project', null=True, verbose_name='关联项目')
    order = models.OneToOneField('webhtml.Order', null=True, verbose_name='订单')
