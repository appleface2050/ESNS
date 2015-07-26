# coding=utf-8
# Date: 15/1/25'
# Email: wangjian2254@icloud.com
import datetime
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from Need_Server import settings
from needserver.models import Project, ProjectRechargeRecord
from util.basemodel import JSONBaseModel
from django.db.models import Q

__author__ = u'王健'

STATUS_CREATE = 0
STATUS_DROP = 1
STATUS_SUCCESS = 2
STATUS_REQUEST_REFUND = 3
STATUS_REFUNDING = 4
STATUS_REFUND_COMPLETE = 5
STATUS_PAYED_NO_ARRIVED = 6

STATUS_CHOICES = [
    (STATUS_CREATE, '刚创建订单'),
    (STATUS_DROP, '放弃订单'),
    (STATUS_PAYED_NO_ARRIVED, '已付款未到账'),
    (STATUS_SUCCESS, '订单付费成功'),
    (STATUS_REQUEST_REFUND, '订单付费申请退款'),
    (STATUS_REFUNDING, '订单正在退款'),
    (STATUS_REFUND_COMPLETE, '客户确认退款'),
]
PAY_TYPE_CHOICES = [
    (0, '支付宝'),
    (1, u'银行转账'),
    (2, u'现金'),
]

CONTRACT_WITHDRAWALS_STATUS_NO_APPLY = 0
CONTRACT_WITHDRAWALS_STATUS_APPLY = 1
CONTRACT_WITHDRAWALS_STATUS_TRANSFERRED = 2
CONTRACT_WITHDRAWALS_STATUS_COMPLETE = 3

CONTRACT_WITHDRAWALS_STATUS_CHOICES = (
    (CONTRACT_WITHDRAWALS_STATUS_NO_APPLY, u'未申请'),
    (CONTRACT_WITHDRAWALS_STATUS_APPLY, u'申请提现'),
    (CONTRACT_WITHDRAWALS_STATUS_TRANSFERRED, u'资金转出'),
    (CONTRACT_WITHDRAWALS_STATUS_COMPLETE, u'提现完成'),
)


class Product(JSONBaseModel):
    """
    产品信息，套餐信息
    by:王健 at:2015-1-25
    修改资金数据类型
    by: 范俊伟 at:2015-03-07
	增加赠送金币字段
	by: 尚宗凯 at:2015-04-22
    """
    flag = models.CharField(max_length=50, unique=True, verbose_name=u'标记', help_text=u'产品唯一标记')
    name = models.CharField(max_length=30, verbose_name=u'产品名称')
    desc = models.TextField(verbose_name=u'产品简介')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'是否可用')
    sorted = models.IntegerField(default=0, db_index=True, verbose_name=u'排序')
    price = models.BigIntegerField(default=0, verbose_name=u'实际价格', help_text=u'打折的情况，的实际价格，单位分')
    show_price = models.BigIntegerField(default=0, verbose_name=u'原价格', help_text=u'打折的情况，的原价格，单位分')
    gold = models.IntegerField(default=0, verbose_name=u'金币', help_text=u'每天消耗的金币, 按人每天消耗1个')
    gift = models.IntegerField(default=0, verbose_name=u'赠送金币', help_text=u'赠送金币, 每天消耗的金币, 按人每天消耗1个')


class Address(JSONBaseModel):
    """
    邮寄地址
    by:王健 at:2015-1-25
    固定电话 和 手机号 有一个可以为空
    by:王健 at:2015-3-8
    修改邮寄地址自选信息
    by:王健 at:2015-3-19
    为了部署，暂时放开注释
    by:王健 at:2015-3-20
    修改地址字段名称,使用京东地址数据,和之前的地址数据做区分
    by: 范俊伟 at:2015-03-19
    增加邮政编码
    by: 范俊伟 at:2015-05-12
    """
    # name = models.CharField(max_length=10, verbose_name=u'邮寄地址, 别名')
    username = models.CharField(max_length=30, verbose_name=u'收货人')
    address_v2 = models.IntegerField(verbose_name=u'所在地区')  # 使用京东数据,可根据数据做出联动效果
    address_detail = models.CharField(max_length=100, verbose_name=u'详细地址')
    zip_code = models.CharField(max_length=20, null=True)
    # tel = models.CharField(max_length=15, null=True, verbose_name=u'固定电话')
    phone = models.CharField(max_length=15, null=True, verbose_name=u'手机号或固定电话')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户', help_text=u'隶属于某个用户')


class Tax(JSONBaseModel):
    """
    发票信息
    by:王健 at:2015-1-25
    发票信息，去除无用字段
    by:王健 at:2015-3-8
    修改发票字段信息
    by:王健 at:2015-3-19
    为了部署，暂时放开注释
    by:王健 at:2015-3-20
    """
    # TAXTYPE = (('putong', u'增值税普通发票'), ('zhuan', u'增值税专用发票'))
    fptt = models.CharField(max_length=100, verbose_name=u"发票抬头")
    # username = models.CharField(max_length=10, verbose_name=u'联系人')
    # tel = models.CharField(max_length=15, verbose_name=u'联系人电话')
    address = models.ForeignKey(Address, verbose_name=u'寄送地址')
    # taxtype = models.CharField(max_length=10, choices=TAXTYPE, verbose_name=u'发票种类')
    # taxnum = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'税号')
    # companyaddress = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'公司地址')
    # companytel = models.CharField(max_length=15, blank=True, null=True, verbose_name=u'公司电话')
    # banknum = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'银行账号')
    # bankaddress = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'开户行')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户', help_text=u'隶属于某个用户')


class Order(JSONBaseModel):
    """
    订单
    by:王健 at:2015-1-25
    字段修改
    by: 范俊伟 at:2015-02-14
    修改资金数据类型,删除flash字段
    by: 范俊伟 at:2015-03-07
    修改字段
    by: 范俊伟 at:2015-03-07
    修改字段
    by: 范俊伟 at:2015-06-11
    """

    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'项目创建日期',
                                       help_text=u'在系统中创建项目的日期')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户', help_text=u'隶属于某个用户')
    status = models.IntegerField(default=STATUS_CREATE, choices=STATUS_CHOICES, db_index=True, verbose_name=u'订单状态')
    product = models.ForeignKey(Product, verbose_name=u'产品')
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'备注')
    price = models.BigIntegerField(verbose_name=u'价格', help_text=u'根据订单，计算出的价格,单位分')
    real_price = models.BigIntegerField(verbose_name=u'实际价格', blank=True, null=True, help_text=u'最终客户付出的金额,单位分')
    pay_date = models.DateTimeField(null=True, db_index=True, verbose_name=u'付费日期', help_text=u'付费日期')
    pay_type = models.IntegerField(blank=True, null=True, db_index=True, verbose_name=u'付款方式', choices=PAY_TYPE_CHOICES)
    is_mail = models.BooleanField(default=True, db_index=True, verbose_name=u'是否邮寄发票', help_text=u"是否吧发票快递邮寄")
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=u'发票邮寄地址')
    tax = models.ForeignKey(Tax, blank=True, null=True, verbose_name=u'发票信息')
    project = models.ForeignKey(Project, verbose_name=u'充值项目')

    mail = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'快递公司')
    mail_number = models.CharField(max_length=20, db_index=True, verbose_name=u'快递单号', blank=True, null=True)
    mail_status = models.IntegerField(default=0, db_index=True, verbose_name=u'快递状态',
                                      help_text=u'0：无快递 1：尚未发送快递 2：等待收快递 3：快递到达 4：快递遗失')
    mail_price = models.DecimalField(max_digits=5, null=True, decimal_places=2, verbose_name=u'快递费')
    mail_date = models.DateTimeField(db_index=True, blank=True, null=True, verbose_name=u'快递发出时间')
    mail_place = models.TextField(verbose_name=u'快递地理位置变化')

    bz = models.TextField(null=True, verbose_name=u'工作人员处理的日志')
    payer_bank_account = models.CharField(max_length=255, null=True, verbose_name='付款者银行账号')
    into_bank_account = models.CharField(max_length=255, null=True, verbose_name='转入银行账号')
    trade_no = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name=u'交易流水号,支付生成或会计标记')
    withdrawals_status = models.IntegerField(choices=CONTRACT_WITHDRAWALS_STATUS_CHOICES,
                                             default=CONTRACT_WITHDRAWALS_STATUS_NO_APPLY, verbose_name='提现状态')

    def create_pay_order(self, pay_type):
        """
        根据订单创建支付订单
        by: 范俊伟 at:2015-03-07
        pay_type判断bug
        by: 范俊伟 at:2015-03-07
        """
        payOrder = PayOrder()
        payOrder.order = self
        prefix = None
        if (int(pay_type) == 0):
            prefix = "zhifubao"
        payOrder.flag = payOrder.create_flag(prefix)
        while PayOrder.objects.filter(flag=payOrder.flag).count() > 0:
            payOrder.flag = payOrder.create_flag(prefix)
        payOrder.real_price = self.real_price
        payOrder.pay_type = pay_type
        payOrder.save()
        return payOrder

    def success(self, payOrder):
        """
        支付成功
        by: 范俊伟 at:2015-03-07
        修改支付处理
        by: 王健 at:2015-03-17
        """
        update = Order.objects.filter(id=self.id).exclude(status=STATUS_SUCCESS).update(pay_date=payOrder.close_time,
                                                                                        pay_type=payOrder.pay_type,
                                                                                        trade_no=payOrder.trade_no,
                                                                                        payer_bank_account=payOrder.payer_bank_account,
                                                                                        into_bank_account=payOrder.into_bank_account,
                                                                                        status=STATUS_SUCCESS)
        if update:
            projectRechargeRecord = ProjectRechargeRecord()
            projectRechargeRecord.project = self.project
            projectRechargeRecord.date = payOrder.close_time
            projectRechargeRecord.order_id = self.id
            projectRechargeRecord.price0 = self.product.gold
            projectRechargeRecord.price_type = 0
            projectRechargeRecord.save(user_id=self.user_id)

            if hasattr(self, 'contract'):
                from ns_manage.models import CONTRACT_STATUS_PAYED_ARRIVED

                contract = self.contract
                contract.status = CONTRACT_STATUS_PAYED_ARRIVED
                contract.save()

    def cancel(self):
        """
        取消订单
        by: 范俊伟 at:2015-03-20
        """
        self.status = STATUS_DROP
        self.save()


class PayOrder(JSONBaseModel):
    """
    支付订单,每次点击支付按钮基于Order表创建
    by: 范俊伟 at:2015-03-07
    修改字段
    by: 范俊伟 at:2015-03-07
    trade_no初始值为空
    by: 范俊伟 at:2015-03-08
    修改字段
    by: 范俊伟 at:2015-06-11
    """
    order = models.ForeignKey(Order, verbose_name='订单')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'项目创建日期',
                                       help_text=u'在系统中创建项目的日期')
    close_time = models.DateTimeField(db_index=True, null=True, verbose_name=u'记录关闭或完成时间')
    flag = models.CharField(max_length=50, unique=True, verbose_name=u'订单id')
    trade_no = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name=u'交易流水号,由支付宝生成')
    status = models.IntegerField(default=STATUS_CREATE, choices=STATUS_CHOICES, db_index=True, verbose_name=u'订单状态')
    real_price = models.BigIntegerField(verbose_name=u'实际价格', blank=True, null=True, help_text=u'最终客户付出的金额,单位分')
    pay_type = models.IntegerField(blank=True, null=True, db_index=True, verbose_name=u'付款方式', choices=PAY_TYPE_CHOICES)
    payer_bank_account = models.CharField(max_length=255, null=True, verbose_name='付款者银行账号')
    into_bank_account = models.CharField(max_length=255, null=True, verbose_name='转入银行账号')

    def create_flag(self, prefix, length=50):
        """
        生成支付ID,前缀
        by: 范俊伟 at:2015-03-07
        :param prefix:id前缀
        :param length:
        :return:
        """
        now = datetime.datetime.now()
        res = prefix + now.strftime('%Y%m%d%H%M%S')
        res += get_random_string(length - len(res))
        return res

    def success(self, trade_no=None):
        """
        支付成功操作
        by: 范俊伟 at:2015-03-07
        优化,在trade_no为空字串时设置为None
        by: 范俊伟 at:2015-03-08
        :param trade_no:
        :return:
        """
        if not trade_no:
            trade_no = None
        update = PayOrder.objects.filter(id=self.id).exclude(status=STATUS_SUCCESS).update(close_time=timezone.now(),
                                                                                           trade_no=trade_no,
                                                                                           status=STATUS_SUCCESS)
        payOrder = PayOrder.objects.get(id=self.id)
        if update:
            self.order.success(payOrder)


class HelpMenu(JSONBaseModel):
    """
    手机web帮助目录
    by:尚宗凯 at：2015-04-17
    改为父级菜单可以为空
    by:尚宗凯 at：2015-04-19
    去掉title唯一索引
    by:尚宗凯 at：2015-04-19
    数据库增加字段
    by：尚宗凯 at：2015-05-27
    """
    title = models.CharField(max_length=50, verbose_name=u'目录')
    is_active = models.NullBooleanField(default=True, db_index=True, verbose_name=u'是否可用',
                                        help_text=u'True表示生效，False表示无效')
    sorted = models.IntegerField(default=0, db_index=True, blank=True, null=True, verbose_name=u'顺序')
    parent = models.ForeignKey('HelpMenu', verbose_name=u'父级菜单', help_text=u'父级菜单', null=True)
    icon_url = models.CharField(max_length=200, null=True, verbose_name=u'图标的url')
    desc = models.CharField(max_length=100, null=True, verbose_name=u'描述')

    class Meta():
        ordering = ['sorted']


class HelpContent(JSONBaseModel):
    """
    手机web帮助内容
    by:尚宗凯 at：2015-04-17
    手机搜索
    by:尚宗凯 at：2015-04-19
    删除menu外键
    by:王健 at:2015-04-24
	增加一级目录外键
	by:尚宗凯 at：2015-05-05
    """
    title = models.CharField(max_length=50, verbose_name=u'目录')
    is_active = models.NullBooleanField(default=True, db_index=True, verbose_name=u'是否可用',
                                        help_text=u'True表示生效，False表示无效')
    sorted = models.IntegerField(default=0, db_index=True, blank=True, null=True, verbose_name=u'顺序')
    text = models.TextField(default="", blank=True, verbose_name=u'html代码')
    tags = models.CharField(max_length=100, verbose_name=u'标签', db_index=True)
    help_menu = models.ForeignKey(HelpMenu, verbose_name=u'隶属目录', help_text=u'隶属目录', null=True, blank=True)

    @staticmethod
    def search(w):
        hc = HelpContent.objects.filter(Q(title__icontains=w) | Q(text__icontains=w) | Q(tags__icontains=w))
        return hc

    class Meta():
        ordering = ['sorted']


class HelpUsage(JSONBaseModel):
    """
    使用帮助
    by：尚宗凯 at：2015-05-04
    """
    title = models.CharField(max_length=50, verbose_name=u'目录')
    is_active = models.NullBooleanField(default=True, db_index=True, verbose_name=u'是否可用',
                                        help_text=u'True表示生效，False表示无效')
    sorted = models.IntegerField(default=0, db_index=True, blank=True, null=True, verbose_name=u'顺序')
    text = models.TextField(default="", blank=True, verbose_name=u'html代码')
    tags = models.CharField(max_length=100, verbose_name=u'标签', db_index=True)

    @staticmethod
    def search(w):
        hu = HelpUsage.objects.filter(Q(title__icontains=w) | Q(text__icontains=w) | Q(tags__icontains=w))
        return hu
