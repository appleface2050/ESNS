# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import hashlib
import time
import datetime
import json
import logging
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.cache import cache
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.conf import settings
import requests
import thread
from company.models import Company
from util import PROJECT_INFO, USERINFO_INFO, PROJECT_GROUP_LIST, PROJECT_PERSON_LIST, MY_PROJECT_QUERY_LIST, \
    PERSON_TIMELINE, PROJECT_IS_ACTIVE, RED_DOT_USER_LAST_READ_TIMELINE, RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE, \
    PROJECT_USER_REALPOWERS, RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE
from util.basemodel import JSONBaseModel
from util.jsonresult import MyEncoder
from util.needpush import NeedPush
from Need_Server.settings import JPUSH_MESSAGE, CACHES_TIMEOUT, CACHES_JPUSH_ALIAS_TIME_OUT, SHOW_USER_ID
from util import PROJECT_POWER_TIMELINE, PROJECT_ID_FLAG_OR_FILEGROUP_ID_ALIAS
from util.project_power_cache import get_alias_by_project_id_flag
# from util.tools import init_expired_date

__author__ = u'王健'


class NSUser(AbstractBaseUser, JSONBaseModel):
    """
    用户表
    by:王健 at:2015-1-3
    用户表 添加 性别字段，身份证id移到 个人信息里
    by:王健 at:2015-1-18
    环信账号是否注册过
    by:王健 at:2015-1-20
    添加索引
    by:王健 at:2015-1-25
    用户头像
    by:王健 at:2015-1-28
    添加关注项目
    by:王健 at:2015-1-30
    增加昵称 nickname 字段
    by:王健 at:2015-3-2
    配置字段，使之可以为空
    by:王健 at:2015-3-10
    增加 is_used 字段
    by:尚宗凯 at:2015-3-20
    去掉 is_used 字段
    by:尚宗凯 at:2015-3-25
    增加realname字段
    by：尚宗凯 at：2015-06-26
    """
    from nsbcs.models import BaseFile

    tel = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text=u'手机号')
    # password = models.CharField(_('password'), null=True, max_length=128)
    name = models.CharField(max_length=30, null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'昵称', help_text=u'昵称')
    realname = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'真实姓名', help_text=u'真实姓名',default="")
    sex = models.NullBooleanField(default=None, verbose_name=u'性别')
    icon_url = models.ForeignKey(BaseFile, null=True, blank=True, verbose_name=u'默认头像')

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    create_time = models.DateTimeField(_('date joined'), default=timezone.now)
    hxpassword = models.CharField(max_length=50, null=True, verbose_name=u'环信密码')
    hx_reg = models.BooleanField(default=False, db_index=True, verbose_name=u'是否注册过环信')

    guanzhu = models.ManyToManyField('Project', null=True, blank=True, verbose_name=u'关注项目')

    objects = BaseUserManager()

    USERNAME_FIELD = 'tel'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return unicode(self.name)

    def get_nickname(self):
        """
        获取昵称
        by:王健 at:2015-06-26
        :return:
        """
        if not self.name:
            return '%s****%' % (self.tel[:3], self.tel[-4:])
        else:
            return self.name

    def save(self, *args, **kwargs):
        """
        第一次保存时，创建一个环信账号和密码
        by:王健 at:2015-1-20
        取消打印消息，屏蔽错误
        by:王健 at:2015-1-30
        用户个人信息没有被修改，则不刷新 person表
        by:王健 at:2015-3-4
        添加缓存
        by:王健 at:2015-3-9
        修改环信注册失败的 处理
        by:王健 at:2015-3-12
        环信密码 在没有的时候 自动生成
        by:王健 at:2015-3-14
        解决 登陆时，不保存 hx_reg 和 hxpassword 问题
        by:王健 at:2015-3-16
        :param args:
        :param kwargs:
        :return:
        """
        if not self.pk:
            import uuid

            u = None
            self.hxpassword = str(uuid.uuid4()).replace('-', '')[:12]
        else:
            u = NSUser.objects.get(pk=self.pk)

        super(NSUser, self).save(*args, **kwargs)
        cache.delete(USERINFO_INFO % self.pk)
        if not u or self.name != u.name or self.nickname != u.nickname or self.sex != u.sex or u.icon_url_id != self.icon_url_id:
            for p in self.person_set.filter(is_active=True):
                p.save()
        if not self.hx_reg:
            if not self.hxpassword:
                import uuid

                self.hxpassword = str(uuid.uuid4()).replace('-', '')[:12]
                # if False and not self.hx_reg:    #测试用
            from easemob.client import register_new_user

            result, errormsg = register_new_user(self.pk, self.hxpassword)
            if result:
                self.hx_reg = True
                if kwargs.has_key('update_fields'):
                    kwargs['update_fields'].append('hx_reg')
                    kwargs['update_fields'].append('hxpassword')
                super(NSUser, self).save(*args, **kwargs)


    def get_user_map(self, myself=False):
        """
        组织用户的字典数据，根据参数放入密码
        by:王健 at:2015-1-20
        增加关注的项目的id列表，修复guanzhu 错误
        by:王健 at:2015-1-30
        修复bug icon_url 空值，变量名冲突
        by:王健 at:2015-1-31
        增加参与项目 id列表
        by:王健 at:2015-2-2
        修改了 昵称字段
        by:王健 at:2015-3-4
        游客账号 不输入环信密码
        by:王健 at:2015-4-8
        通过七牛处理功能,产生头像缩略图
        by: 范俊伟 at:2015-04-08
		增加realname
		by：尚宗凯 at：2015-06-26
        """
        p = {}
        p['tel'] = self.tel
        if self.name:
            p['name'] = self.name
        else:
            p['name'] = ''
        p['nickname'] = self.nickname
        if self.icon_url:
            p['icon_url'] = self.icon_url.get_url('imageView2/5/w/80/h/80')
            p['big_icon_url'] = self.icon_url.get_url()
        else:
            p['icon_url'] = ''
            p['big_icon_url'] = ''
        p['uid'] = self.pk
        p['sex'] = self.sex
        p['hx_reg'] = self.hx_reg
        p['realname'] = self.realname
        if myself:
            if self.pk != settings.SHOW_USER_ID:
                p['hxpassword'] = self.hxpassword
                p['guanzhuprojectlist'] = [u[0] for u in self.guanzhu.values_list('id')]
                if hasattr(self, 'person_set'):
                    p['canyuprojectlist'] = [u[0] for u in
                                             self.person_set.filter(is_active=True).values_list('project_id')]
                else:
                    p['canyuprojectlist'] = []
            else:
                p['canyuprojectlist'] = []
                p['guanzhuprojectlist'] = []
                p['hxpassword'] = []
                p['tel'] = ''
        return p

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # def email_user(self, subject, message, from_email=None):
    # """
    # Sends an email to this User.
    # """
    # send_mail(subject, message, from_email, [self.email])

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name


class UserInfo(JSONBaseModel):
    """
    用户的个人信息表
    by:王健 at:2015-1-18
    职务放在用户信息表
    by:王健 at:2015-2-12
    修改个人信息字段
    by:王健 at:2015-3-2
    添加缓存
    by:王健 at:2015-3-9
    增加phrase字段
    by:尚宗凯 at:2015-3-24
    """
    XUELI = ((0, u'未选择'), (5, u'高中'), (6, u'大专'), (7, u'本科'), (8, u'研究生'), (9, u'博士'))
    HUNYIN = (('wei', u'未婚'), ('yihun', u'已婚'), ('liyi', u'离异'))
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    # idnumber = models.CharField(max_length=20, blank=True, verbose_name=u'身份证号', help_text=u'3.2日决定不用')
    address = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'籍贯', help_text=u'3.2日决定改为籍贯')
    # address = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'现居住地', help_text=u'3.2日决定不用')
    xueli = models.IntegerField(default=0, null=True, blank=True, choices=XUELI, verbose_name=u'最高学历')
    # workage = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'参加工作的年份', help_text=u'3.2日决定不用')
    zhicheng = models.CharField(max_length=100, blank=True, verbose_name=u'职称')
    zhiyezigezheng = models.CharField(max_length=100, blank=True, verbose_name=u'职业资格证')
    # hunyin = models.CharField(max_length=5, blank=True, verbose_name=u'婚姻状况', help_text=u'3.2日决定不用')
    company = models.CharField(max_length=50, blank=True, verbose_name=u'所在公司名称')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'职务', help_text=u'职务')
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'部门', help_text=u'任职部门')
    email = models.EmailField(blank=True, verbose_name=u'电子邮件')
    qq = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'qq', help_text=u'qq号')
    phrase = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'心情短语', help_text=u'心情短语')

    def save(self, *args, **kwargs):
        """
        修改 id 为 user_id
        by:王健 at:2015-3-10
        修改个人信息，刷新 person表
        by:王健 at:2015-4-10
        """
        super(UserInfo, self).save(*args, **kwargs)
        cache.delete(USERINFO_INFO % self.user_id)
        for p in self.user.person_set.filter(is_active=True):
            p.save()

    def get_userinfo_map(self):
        """
        获取需要的userinfo dict信息
        by：尚宗凯 at：2015-05-11
        """
        userinfo = {}
        userinfo['birthday'] = self.birthday
        userinfo["address"] = self.address
        userinfo['xueli'] = self.xueli
        userinfo['zhicheng'] = self.zhicheng
        userinfo['zhiyezigezheng'] = self.zhiyezigezheng
        userinfo['company'] = self.company
        userinfo['title'] = self.title
        userinfo['department'] = self.department
        userinfo['email'] = self.email
        userinfo['qq'] = self.qq
        return userinfo


class Project(JSONBaseModel):
    """
    项目表
    by:王健 at:2015-1-3
    项目表 添加 项目创建日期
    by:王健 at:2015-1-8
    create_date 改为 create_time
    by:王健 at:2015-1-12
    部分字段设置为可为空， 添加一个 是否允许游客进入的字段
    by:王健 at:2015-1-18
    添加索引
    by:王健 at:2015-1-25
    项目头像
    by:王健 at:2015-1-28
    关注数量 和 成员数量
    by:王健 at:2015-1-30
    项目名称 改为项目简称
    by:王健 at:2015-2-4
    全称 创建唯一索引
    by:王健 at:2015-3-4
    默认都是付过帐的 项目
    by:王健 at:2015-3-9
    建筑层数 修改为字符
    by:王健 at:2015-3-15
    变更部分字段的长度
    by:尚宗凯 at:2015-3-17
    项目建设单位负责人，提示文字不对
    by:王健 at:2015-4-18
    增加渠道代码字段
    by:尚宗凯 at:2015-5-13
    增加删除公示期状态
    by：尚宗凯 at：2015-06-01
    增加5项目从关闭进入删除公示期
    by：尚宗凯 at：2015-06-05
    增加过期日期字段
    by：尚宗凯 at：2015-06-08
    去掉过期日期字段
    by：尚宗凯 at：2015-06-10
    """
    from nsbcs.models import File

    name = models.CharField(max_length=8, db_index=True, blank=True, verbose_name=u'项目简称', help_text=u'项目名称')
    total_name = models.CharField(max_length=50, unique=True, db_index=True, blank=True, verbose_name=u'项目全称',
                                  help_text=u'项目全称')
    flag = models.CharField(max_length=50, blank=True, unique=True, verbose_name=u'邀请码', help_text=u'邀请其他用户加入本组织')
    icon_url = models.ForeignKey(File, related_name='project_icon', verbose_name=u'头像', null=True, blank=True,
                                 help_text=u'项目头像')
    # icon_url = models.CharField(max_length=200, verbose_name=u'头像', null=True, blank=True, help_text=u'项目头像')
    address = models.IntegerField(default=0, db_index=True, verbose_name=u'地址')
    jzmj = models.IntegerField(verbose_name=u'建筑面积', help_text=u'单位平米')
    jglx = models.CharField(max_length=30, verbose_name=u'结构类型')
    jzcs = models.CharField(max_length=30, verbose_name=u'建筑层数')
    htzj = models.BigIntegerField(verbose_name=u'合同造价')
    kg_date = models.DateField(verbose_name=u'开工日期')
    days = models.IntegerField(verbose_name=u'总工期')

    jsdw = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u'建设单位')
    jsdw_fzr = models.CharField(max_length=30, blank=True, verbose_name=u'建设单位负责人')
    kcdw = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u'勘察单位')
    kcdw_fzr = models.CharField(max_length=30, blank=True, verbose_name=u'勘察单位负责人')
    sjdw = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u'设计单位')
    sjdw_fzr = models.CharField(max_length=30, blank=True, verbose_name=u'设计单位负责人')
    sgdw = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u'施工单位')
    sgdw_fzr = models.CharField(max_length=30, blank=True, verbose_name=u'施工单位负责人')
    jldw = models.CharField(max_length=30, db_index=True, blank=True, verbose_name=u'监理单位')
    jldw_fzr = models.CharField(max_length=30, blank=True, verbose_name=u'监理单位负责人')

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=u'超级管理员')
    is_active = models.NullBooleanField(default=True, db_index=True, verbose_name=u'是否可用',
                                        help_text=u'None 表示没付费，True 表示项目付费了可用，False表示项目终结了')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'项目资料修改时间线')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'项目创建日期',
                                       help_text=u'在系统中创建项目的日期')

    is_guest = models.NullBooleanField(default=None, db_index=True, null=True, blank=True, verbose_name=u'是否接受游客')

    guanzhu_num = models.IntegerField(default=0, verbose_name=u'关注数量')
    chengyuan_num = models.IntegerField(default=0, verbose_name=u'成员数量')

    channel = models.CharField(max_length=20, db_index=True, null=True, verbose_name=u'渠道代码')
    status = models.IntegerField(default=0, db_index=True, null=True, verbose_name=u'项目状态 0正常 1欠费 2关闭 3已删除 4删除公示期 5项目从关闭进入删除公示期')
    delete_project_time = models.DateTimeField(db_index=True, verbose_name=u'系统删除时间',null=True,
                                       help_text=u'系统删除时间')
    pay_type = models.IntegerField(default=0, db_index=True, verbose_name=u'付费类型 0试用项目 1自费项目 2企业付费项目')
    company = models.ForeignKey(Company, verbose_name=u'隶属公司', null=True)

    # expired_date = models.DateField(verbose_name=u'过期日期', default=init_expired_date)

    def __unicode__(self):
        """
        修改total_name
        by:王健 at:2015-1-8
        :return:
        """
        return unicode(self.total_name)

    def save(self, *args, **kwargs):
        """
        第一次保存时，创建一个不会重复的，flag，用于以后邀请人加入标记
        by:王健 at:2015-1-3
        初次创建项目时，默认添加600金币
        by:王健 at:2015-3-2
        添加缓存
        by:王健 at:2015-3-9
        添加系统消息
        by:王健 at:2015-3-16
        更新话术
        by:王健 at:2015-3-17
        :param args:
        :param kwargs:
        :return:
        """
        add = False
        if not self.pk:
            import uuid

            add = True
            self.flag = str(uuid.uuid4())
        self.timeline = int(time.time())
        super(Project, self).save(*args, **kwargs)
        if add:
            sys = SysMessage()
            sys.project = self
            sys.title = u'系统消息'
            sys.text = settings.CREATE_PROJECT_SYSMESSAGE % self.total_name
            sys.user = self.manager
            sys.save()

            pr = ProjectRechargeRecord()
            pr.project = self
            pr.date = timezone.now()
            pr.order_id = None
            pr.price0 = 600
            pr.price_type = 1
            pr.save(sysmessage=sys)

        cache.delete(PROJECT_INFO % self.pk)

    def updatetimeline(self):
        self.save(update_fields=['timeline'])

    @staticmethod
    def get_project_name_by_id(project_id):
        """
        通过project id获得项目名称
        by：尚宗凯 at：2015-04-08
        返回total_name
        by：尚宗凯 at：2015-04-16
        :param project_id:
        :return:
        """
        try:
            p = Project.objects.get(pk=project_id)
            return p.total_name
        except Exception as e:
            pass

    def toJSON(self):
        """
        自定义 json函数
        by:王健 at:2015-2-5
        修改 icon_url 没有值时的默认值
        by:王健 at:2015-2-14
        修改新图
        by:王健 at:2015-2-15
        添加管理员名称显示
        by:王健 at:2015-3-4
        解决 修改数据时，id是字符串 无法 取模 的bug
        by:王健 at:2015-3-11
        修改项目头像的url
        by:王健 at:2015-4-10
        delete_project_time为None改为""
        by：尚宗凯 at：2015-06-03
        """
        d = super(Project, self).toJSON()
        d['manager_name'] = self.manager.name
        if self.icon_url:
            d['icon_url'] = self.icon_url.get_url()
        else:
            d['icon_url'] = 'http://%s/static/icon/xiangmu2%s.png' % (settings.HOST_URL, int(self.id) % 14)
        if d["delete_project_time"] is None:
            d['delete_project_time'] = ""
        return d

    # def get_status(self):
    #     """
    #     获取项目状态
    #     by：尚宗凯 at：2015-06-01
    #     """
    #     project = cache.get(PROJECT_INFO % self.pk)
    #     if project is None or not project['delete_project_time']:
    #         project = MyEncoder.default(self)
    #     if project['status'].status == 4:
    #         from Need_Server.settings import DELETE_PROJECT_PUBLICITY_PERIOD
    #         if (datetime.datetime.now() - project['delete_project_time']) >= datetime.timedelta(days=DELETE_PROJECT_PUBLICITY_PERIOD):
    #             self.status = 3
    #             self.save()
    #             cache.set(PROJECT_INFO % self.pk, MyEncoder.default(self), settings.CACHES_TIMEOUT)
    #     return project.status

    class Meta():
        verbose_name = u'项目信息'


class ProjectPersonChangeRecord(JSONBaseModel):
    """
    项目成员变动记录
    by:王健 at:2015-3-15
    时间默认值bug修改
    by: 范俊伟 at:2015-06-29
    """
    project = models.ForeignKey(Project, verbose_name=u'项目', related_name='projectpersonchangerecord')
    date = models.DateTimeField(default=timezone.now, verbose_name=u'日期')
    create_date = models.DateField(default=timezone.now, verbose_name=u'日期')
    price = models.IntegerField(default=0, verbose_name=u'货币扣款')
    members = models.IntegerField(default=0, verbose_name=u'当日成员数量')
    pre_members = models.IntegerField(default=0, verbose_name=u'前日成员数量')
    stop_days = models.IntegerField(default=0, verbose_name=u'报停日子数')
    end_date = models.DateTimeField(verbose_name=u'使用终止日期')

    def save(self, *args, **kwargs):
        """
        保存人员变动记录，计算使用终止日期
        by:王健 at:2015-3-15
        不到一天的 不算做一天
        by:王健 at:2015-4-6
        修复计算余额的bug
        by:王健 at:2015-05-08
        充值后应清空项目是否可用的缓存
        by:王健 at:2015-05-21
        设置新的计费方式
        by:王健 at:2015-06-24
        """
        add = True

        self.date = self.create_date
        if self.pk:
            add = False
        if self.members == 0:
            self.members = 1
        if add:

            pr = ProjectPersonChangeRecord.objects.filter(project_id=self.project_id).order_by('-create_date')[:1]
            if len(pr) == 1:
                pr = pr[0]
            if pr:
                self.members = self.project.person_set.filter(is_active=True).count()
                self.pre_members = pr.members
                if pr.stop_days < (self.date - pr.date).days:
                    # self.price += pr.price - (pr.members * ((self.date - pr.date).days - pr.stop_days))
                    self.price += pr.commit_value()
                else:
                    self.price = pr.price
                    self.stop_days += pr.stop_days - (self.date - pr.date).days

        # if self.members > self.pre_members:
        #     days = (self.price - self.members) / self.members
        #     # if ((self.price - self.members) % self.members) > 0:
        #     # days = int(days) + 1
        # else:
        #     days = (self.price - self.pre_members) / self.members
        #     # if ((self.price - self.pre_members) % self.members) > 0:
        #     # days = int(days) + 1
        days = self.price / settings.DEFAULT_PRICE_EVERYDAY
        if days < 0:
            days = 0
        self.end_date = self.date + datetime.timedelta(days=(days + self.stop_days))
        super(ProjectPersonChangeRecord, self).save(*args, **kwargs)
        cache.delete(PROJECT_IS_ACTIVE % (self.project_id, timezone.now().strftime('%Y-%m-%d')))

    def commit_value(self, date=None, today=True):
        """
        根据提供的时间 计算 余额
        by:王健 at:2015-3-15
        优化计算余额的算法
        by:王健 at:2015-05-08
        设置新的计费方式
        by:王健 at:2015-06-24
        """
        if not self.pk:
            return 0
        if not date:
            date = timezone.now()
        if not today:
            date += datetime.timedelta(days=-1)
        if (date - self.date).days >= self.stop_days:
            r = self.price - settings.DEFAULT_PRICE_EVERYDAY * ((date - self.date).days - self.stop_days + 1)
            if r >= 0:
                return r
            else:
                return self.price % settings.DEFAULT_PRICE_EVERYDAY
            #
            # if self.members > self.pre_members:
            #     r = self.price - self.members - self.members * ((date - self.date).days - self.stop_days)
            #
            #     if r >= 0:
            #         return r
            #     else:
            #         return (self.price - self.members) % self.members
            #
            #
            # r = self.price - self.pre_members - self.members * ((date - self.date).days - self.stop_days)
            # if r >= 0:
            #     return r
            # else:
            #     return (self.price - self.pre_members) % self.members
        else:
            return self.price

    def commit_days_real(self, date=None):
        """
        计算真实的剩余天数
        by:王健 at:2015-05-08
        当天也算一天
        by:王健 at:2015-07-01
        :param date:
        :return:
        """
        if not date:
            used = (timezone.now() - datetime.datetime(self.date.year, self.date.month, self.date.day)).days + 1
        else:
            used = (date - datetime.datetime(self.date.year, self.date.month, self.date.day)).days + 1
        if used < 0:
            used = 0
        return (datetime.datetime(self.end_date.year, self.end_date.month, self.end_date.day) - datetime.datetime(
            self.date.year, self.date.month, self.date.day)).days - used

    def commit_days(self, date=None):
        """
        根据提供的日期，计算距离此日，还有多少天可用
        by:王健 at:2015-3-15
        优化计算剩余天数的算法
        by:王健 at:2015-05-08
        计算友好的剩余天数
        by:王健 at:2015-05-08
        """
        r = self.commit_days_real(date)
        if r >= 0:
            return r
        else:
            return 0

    class Meta():
        verbose_name = u'项目每日付款记录'
        unique_together = [('create_date', 'project')]


class ProjectRechargeRecord(JSONBaseModel):
    """
    项目充值记录
    by:王健 at:2015-2-28
    date 改为 DateTimeField 防止出现一天内多次充值 无效的bug
    by:王健 at:2015-3-8
    """
    project = models.ForeignKey(Project, verbose_name=u'项目')
    date = models.DateTimeField(default=timezone.now, verbose_name=u'日期')
    order_id = models.IntegerField(null=True, unique=True, verbose_name=u'订单id')
    price0 = models.IntegerField(default=0, verbose_name=u'充值资金')
    price1 = models.IntegerField(default=0, verbose_name=u'余额')
    price2 = models.IntegerField(default=0, verbose_name=u'总值')
    price_type = models.IntegerField(default=0, verbose_name=u'充值类型', help_text=u'0：付费充值，1：注册赠送，2：管理员设置')

    def save(self, sysmessage=None, user_id=None, **kwargs):
        """
        添加新充值记录时，计算总值
        by:王健 at:2015-3-2
        冲了值的项目 都改为 可用
        by:王健 at:2015-3-10
        修改 扣费算法，计算余额
        by:王健 at:2015-3-15
        """
        if not sysmessage and not user_id:
            import logging

            log = logging.getLogger('django')
            log.error(u'创建充值记录，必须提供 系统消息类 或 充值人id，错误订单id：%s' % self.order_id)
            raise u'创建充值记录，必须提供 系统消息类 或 充值人id，错误订单id：%s' % self.order_id
        ppcr = ProjectPersonChangeRecord.objects.filter(project_id=self.project_id).order_by('-create_date')[:1]
        if len(ppcr) == 1:
            ppcr = ppcr[0]
        else:
            ppcr = ProjectPersonChangeRecord()
            ppcr.price = 0
        self.price1 = ppcr.commit_value(today=False)

        if self.price1 < 0:
            self.price1 = 0
        self.price2 = self.price0 + self.price1
        self.project.is_active = True
        self.project.save()
        super(ProjectRechargeRecord, self).save(kwargs)

        ppcr, created = ProjectPersonChangeRecord.objects.get_or_create(project_id=self.project_id,
                                                                        create_date=self.date)
        if created:
            ppcr.members = self.project.person_set.filter(is_active=True).count()
        ppcr.price = self.price2
        ppcr.save()
        if not sysmessage:
            sysmessage = SysMessage()
            sysmessage.project_id = self.project_id
            sysmessage.title = u"充值完成"
            sysmessage.text = u"您的项目“%s”已经成功充值%s金豆，您当前项目有%s人，预计还可用%s天。" % (self.project.total_name,
                                                                           self.price0, ppcr.members,
                                                                           ppcr.commit_days())
            sysmessage.user_id = user_id
            sysmessage.save()

    class Meta():
        verbose_name = u'项目每日付款记录'


class Group(JSONBaseModel):
    """
    分组表
    by:王健 at:2015-1-3
    index改为sorted
    by:王健 at:2015-1-13
    添加是否可用的字段
    by:王健 at:2015-1-16
    sorted 字段 默认值为0
    by:王健 at:2015-1-18
    添加索引
    by:王健 at:2015-1-25
    添加环信群组id，和是否应该注册环信群组标记
    by:王健 at:2015-2-26
    添加权限 属性
    by:王健 at:2015-3-4
    分组名称 长度要和 项目全称长度限制一样
    by:王健 at:2015-3-10
    """
    from nsbcs.models import File

    name = models.CharField(max_length=50, verbose_name=u'名称', help_text=u'分组名称')
    icon_url = models.ForeignKey(File, related_name='group_icon', verbose_name=u'头像', null=True, blank=True,
                                 help_text=u'项目头像')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    say_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_say_members',
                                         verbose_name=u'可发言成员成员', help_text=u'分组成员')
    look_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_look_members',
                                          verbose_name=u'无发言权限成员', help_text=u'分组成员')
    type = models.CharField(max_length=10, db_index=True, default='custom', verbose_name=u'分组标签',
                            help_text=u'“custom”是用户自建的分组，其他的为系统创建。组织中必须存在的分组（根组（root）），所有新加入的人都归属根组')
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    sorted = models.IntegerField(default=0, db_index=True, blank=True, null=True, verbose_name=u'排序字段')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=u'创建者')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'是否在用')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    hxgroup_id = models.CharField(max_length=50, null=True, verbose_name=u'环信群组id', help_text=u'系统注册的环信群组id')
    is_needhx = models.BooleanField(default=False, verbose_name=u'是否需要注册环信群组')
    hx_timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    powers = models.CommaSeparatedIntegerField(max_length=1000, null=True, verbose_name=u'权限值')

    def __unicode__(self):
        return unicode(self.name)

    def append_prower(self, prower):
        """
        追加权限
        by:王健 at:2015-3-4
        追加权限 时，清空项目权限缓存
        by:王健 at:2015-4-10
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []
        if int(prower) not in self.powers:
            self.powers.append(int(prower))
            cache.delete(PROJECT_POWER_TIMELINE % self.project_id)
            return True
        return False

    def remove_prower(self, prower):
        """
        移除权限
        by:王健 at:2015-3-4
        修改删除权限的bug
        by:王健 at:2015-3-27
        追加权限 时，清空项目权限缓存
        by:王健 at:2015-4-10
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []
        if int(prower) in self.powers:
            self.powers.remove(int(prower))
            cache.delete(PROJECT_POWER_TIMELINE % self.project_id)
            return True
        return False

    def has_prower(self, prower):
        """
        权限判断
        by:王健 at:2015-3-4
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []
            return False
        if int(prower) in self.powers:
            return True
        return False

    def init_powers(self):
        """
        json 转 list
        by:王健 at:2015-3-5
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []


    def is_user_is_sysmanager(self, project_id, user_id):
        """
        判断user_id是否在管理员分组
        :param user_id:
        :return:
        """
        # p = Project.objects.get(pk=project_id)
        group = Project.objects.get(pk=project_id).group_set.filter(type='sys_manage')[0]
        if user_id in [i['id'] for i in group.look_members.values("id")] or user_id in [i['id'] for i in group.say_members.values("id")]:
            return True
        else:
            return False

    # @staticmethod
    # def whether_user_have_power_by_flag(user_id, project_id, flag):
    #     """
    #     解决示例项目中Person为空的bug
    #     by:尚宗凯 at：2015-05-18
    #     """
    #     # if not Person.objects.filter(user_id=user_id,project_id=project_id).exists():
    #     if int(project_id) == settings.SHOW_PROJECT_ID:
    #         return False
    #     # p = Person.objects.get(user_id=user_id,project_id=project_id)
    #     file_group_id = FileGroup.get_father_flag(flag).pk
    #     # if 100*int(file_group_id) in p.real_powers():
    #     if 100*int(file_group_id) in Group.get_real_power_by_project_user(project_id=project_id,user_id=user_id):
    #         return True
    #     else:
    #         return False


    # @staticmethod
    # def get_real_power_by_project_user(project_id, user_id):
    #     """
    #     通过project_id user_id返回用户的真实权限
    #     by: 尚宗凯 at：2015-05-20
    #     """
    #     powers = cache.get(PROJECT_USER_REALPOWERS % (project_id, user_id))
    #     if not powers:
    #         powers = Person.objects.get(user_id=user_id,project_id=project_id).real_powers()
    #         cache.set(PROJECT_USER_REALPOWERS % (project_id, user_id), powers, settings.CACHES_TIMEOUT)
    #     return powers


    @staticmethod
    def whether_user_have_power_by_multi_flag(user_id, project_id, flags):
        """
        多个flag是否有权限，有一个有权限即返回True
        by：尚宗凯 at：2015-05-20
        增加权限缓存
        by：尚宗凯 at：2015-05-20
        """
        # p = Person.objects.get(user_id=user_id,project_id=project_id)
        for flag in flags:
            file_group_id = FileGroup.get_father_flag(flag).pk
            # if 100*int(file_group_id) in p.real_powers():
            if 100*int(file_group_id) in Group.get_real_power_by_project_user(project_id=project_id,user_id=user_id):
                return True
            else:
                continue
        return False

    def toJSON(self):
        """
        为解决环信 群组注册错误的bug， 在群组注册错误时，返回 is_needhx =False，防止手机端出问题
        同时，再次请求环信，注册群组。
        by:王健 at:2015-4-10
        :return:
        """
        d = super(Group, self).toJSON()
        if d['is_needhx'] and not d['hxgroup_id']:
            self.save()
            if self.is_needhx and not self.hxgroup_id:
                d['is_needhx'] = False
            else:
                d['hxgroup_id'] = self.hxgroup_id
        return d


    def save(self, *args, **kwargs):
        """
        修改群组信息，不修改项目的时间戳
        by:王健 at:2015-2-6
        保存分组信息是 判断是否应该注册环信群
        by:王健 at:2015-2-26
        优化环信群组修改的变更
        by:王健 at:2015-2-27
        环信群聊调试，修改添加成员的接口
        by:王健 at:2015-2-28
        保存时，把list保存为字符串
        by:王健 at:2015-3-4
        添加缓存
        by:王健 at:2015-3-9
        环信取消 管理员用户 不可用了
        by:王健 at:2015-3-13
        """
        if isinstance(self.powers, list):
            import json

            self.powers = json.dumps(self.powers).replace('L', '')
        if not self.pk:
            from init_group_prower import init_prower_by_group

            init_prower_by_group(self)
        timeline = int(time.time())
        self.timeline = timeline
        if self.pk and self.is_needhx:
            # if False and self.pk and self.is_needhx:        #测试用
            say_members = [str(u[0]) for u in self.say_members.values_list('id')]
            look_members = [str(u[0]) for u in self.look_members.values_list('id')]
            members = list(set(say_members) | set(look_members))
            if not self.hxgroup_id:
                from easemob.client import register_new_group

                result, errormsg = register_new_group({'groupname': self.name, 'desc': self.name, 'public': False,
                                                       'maxusers': len(members) + 1, 'approval': True,
                                                       'owner': settings.HUANXIN_ADMIN, 'members': members})
                if result:
                    self.hxgroup_id = errormsg['data']['groupid']
                    self.hx_timeline = timeline
            elif self.timeline != self.hx_timeline:
                flag = True
                from easemob.client import get_group_members, delete_group_member, add_group_member, update_group_info

                result, hx_members_data = get_group_members(self.hxgroup_id)
                if result:
                    hx_members = []
                    for h_dict in hx_members_data['data']:
                        if h_dict.has_key('member'):
                            hx_members.append(h_dict['member'])
                    for hx_uname in hx_members:
                        if hx_uname not in members:
                            result, errormsg = delete_group_member(self.hxgroup_id, hx_uname)
                            if not result:
                                flag = False
                    result, errormsg = update_group_info(self.hxgroup_id,
                                                         {'groupname': self.name, 'description': self.name,
                                                          'maxusers': len(members) + 1})
                    if not result:
                        flag = False
                    for hx_uname in members:
                        if hx_uname not in hx_members:
                            result, errormsg = add_group_member(self.hxgroup_id, hx_uname)
                            if not result:
                                flag = False
                    if flag:
                        self.hx_timeline = timeline
        super(Group, self).save(*args, **kwargs)
        cache.delete(PROJECT_GROUP_LIST % self.project_id)

    @staticmethod
    def get_user_id_by_group_ids(group_id_list):
        """
        通过group_id list 返回 user_id_list
        by:尚宗凯 at：2015-04-09
        优化代码
        by：王健 at：2015-05-07
        """
        res = []
        if not group_id_list:
            return res
        for g in Group.objects.filter(id__in=group_id_list):
        # for id in group_id_list:
        #     g = Group.objects.get(pk=id)
            # u_id = g.look_members
            u_id_list = g.look_members.values_list("id")
            u_id_list2 = g.say_members.values_list("id")
            for i in u_id_list:
                res.append(str(i[0]))
            for i in u_id_list2:
                res.append(str(i[0]))
        return res

    class Meta():
        verbose_name = u'分组信息'


class Person(JSONBaseModel):
    """
    项目与用户的关联表，附带写用户在项目中的信息
    by:王健 at:2015-1-3
    Person 不再提供默认分组字段
    by:王健 at:2015-1-8
    添加索引
    by:王健 at:2015-1-25
    去除title属性
    by:王健 at:2015-2-12
    增加权限属性
    by:王健 at:2015-3-4
    添加逆权限属性
    by:王健 at:2015-05-06
    增加评论id的字段，评论模块需要使用
    by:王健 at:2015-05-27
    优化评论数据库设计
    by:王健 at:2015-06-02
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    is_active = models.BooleanField(default=True, verbose_name=u'是否在用')
    create_time = models.DateTimeField(_('date joined'), default=timezone.now)
    # group = models.ForeignKey(Group, verbose_name=u'分组')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    powers = models.CommaSeparatedIntegerField(max_length=1000, null=True, verbose_name=u'权限值')
    dispowers = models.CommaSeparatedIntegerField(max_length=1000, null=True, verbose_name=u'权限值')
    replay_timeline = models.IntegerField(default=0, verbose_name=u'评论回复阅读，时间戳')
    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.old_is_active = self.is_active

    def __unicode__(self):
        """
        person 模型 没有了 name字段，改为输出 名字加岗位
        by:王健 at:2015-1-5
        删除title
        by:尚宗凯 at:2015-3-25
        """
        return u'%s' % (self.user.name)

    def real_powers(self):
        """
        获取真实权限
        by:王健 at:2015-05-11
        :return:
        """
        self.init_powers()
        self.init_dispowers()
        powers_set = set(self.powers)
        for group in Group.objects.filter(project_id=self.project_id).filter(Q(say_members=self.user_id) | Q(look_members=self.user_id)):
            group.init_powers()
            powers_set.update(set(group.powers))
        powers_set = powers_set - set(self.dispowers)
        return list(powers_set)

    def append_disprower(self, prower):
        """
        追加逆权限
        by:王健 at:2015-5-6
        :param prower:
        :return:
        """
        if isinstance(self.dispowers, (str, unicode)):
            import json

            self.dispowers = json.loads(self.dispowers)
        elif self.dispowers is None:
            self.dispowers = []
        if int(prower) not in self.dispowers:
            self.dispowers.append(int(prower))
            return True
        return False

    def remove_disprower(self, prower):
        """
        移除逆权限
        by:王健 at:2015-5-6
        :param prower:
        :return:
        """
        if isinstance(self.dispowers, (str, unicode)):
            import json

            self.dispowers = json.loads(self.dispowers)
        elif self.dispowers is None:
            self.dispowers = []
        if int(prower) in self.dispowers:
            self.dispowers.remove(int(prower))
            return True
        return False

    def has_disprower(self, prower):
        """
        权限是否具有逆判断
        by:王健 at:2015-5-6
        :param prower:
        :return:
        """
        if isinstance(self.dispowers, (str, unicode)):
            import json

            self.dispowers = json.loads(self.dispowers)
        elif self.dispowers is None:
            self.dispowers = []
            return False
        if int(prower) in self.dispowers:
            return True
        return False

    def init_dispowers(self):
        """
        json 转 list
        by:王健 at:2015-5-6
        """
        if isinstance(self.dispowers, (str, unicode)):
            import json

            self.dispowers = json.loads(self.dispowers)
        elif self.dispowers is None:
            self.dispowers = []
        return self.dispowers

    def append_prower(self, prower):
        """
        追加权限
        by:王健 at:2015-3-4
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers is None:
            self.powers = []
        if int(prower) not in self.powers:
            self.powers.append(int(prower))
            return True
        return False

    def remove_prower(self, prower):
        """
        移除权限
        by:王健 at:2015-3-4
        修改删除权限的bug
        by:王健 at:2015-3-27
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers is None:
            self.powers = []
        if int(prower) in self.powers:
            self.powers.remove(int(prower))
            return True
        return False

    def has_prower(self, prower):
        """
        权限判断
        by:王健 at:2015-3-4
        :param prower:
        :return:
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []
            return False
        if int(prower) in self.powers:
            return True
        return False

    def init_powers(self):
        """
        json 转 list
        by:王健 at:2015-3-5
        返回数组
        by:王健 at:2015-3-9
        """
        if isinstance(self.powers, (str, unicode)):
            import json

            self.powers = json.loads(self.powers)
        elif self.powers == None:
            self.powers = []
        return self.powers

    def save(self, *args, **kwargs):
        """
        添加新成员时，增加成员数
        by:王健 at:2015-1-30
        添加 chengyuan 参数来对移出又加入的成员 增加关注和成员
        by:王健 at:2015-2-6
        保存时，把list保存为字符串
        by:王健 at:2015-3-4
        添加缓存
        by:王健 at:2015-3-9
        清除 person 时间线缓存
        by:王健 at:2015-3-14
        人员变动时，新增、删除时，重新计算余额和剩余日期
        by:王健 at:2015-3-15
        人员变动，新增、删除、重新加入，person 变动，会产生 关注列表变化 和 参与列表变化
        by:王健 at:2015-3-16
        跟新个人信息后，必须刷新 我的项目 缓存
        by:王健 at:2015-4-9
        增加发送need消息，用户加入项目
        by：尚宗凯 at：2015-04-14
        添加项目成员发送的推送，改由view函数实现
        by:王健 at:2015-04-19
        取消修改人员导致的项目被更新，去除对chengyuan_num 和 guanzhu_num 的维护
        by:王健 at:2015-05-07
        添加成员更新项目的时间戳
        by:王健 at:2015-05-21
        """
        add = True
        remove_or_readd = False
        if self.pk:
            add = False
            if self.old_is_active != self.is_active:
                remove_or_readd = True

        if isinstance(self.powers, list):
            import json

            self.powers = json.dumps(self.powers).replace('L', '')
        self.timeline = int(time.time())
        # if not self.pk or kwargs.has_key('chengyuan'):
        #     if kwargs.has_key('chengyuan'):
        #         del kwargs['chengyuan']
        #     self.project.chengyuan_num += 1
        #     if not self.project.nsuser_set.filter(id=self.user.id).exists():
        #         self.project.nsuser_set.add(self.user)
        #         self.project.guanzhu_num += 1
        #     self.project.save()
        super(Person, self).save(*args, **kwargs)
        cache.delete(PERSON_TIMELINE % (self.project_id, self.user_id))
        # self.project.updatetimeline()
        cache.delete(MY_PROJECT_QUERY_LIST % self.user_id)
        if add or remove_or_readd:
            self.project.updatetimeline()
            ppcr, created = ProjectPersonChangeRecord.objects.get_or_create(project_id=self.project_id,
                                                                            create_date=timezone.now())
            ppcr.members = self.project.person_set.filter(is_active=True).count()
            ppcr.save()
            cache.delete(USERINFO_INFO % self.user_id)
            cache.delete(PROJECT_PERSON_LIST % self.project_id)



    class Meta():
        unique_together = [('user', 'project')]
        verbose_name = u'项目中的个人信息'


class ProjectApply(JSONBaseModel):
    """
    申请，申请加入项目
    by:王健 at:2015-1-3
    项目申请，添加时间戳
    by:王健 at:2015-1-7
    create_date 改为 create_time
    by:王健 at:2015-1-12
    添加索引
    by:王健 at:2015-1-25
    处理申请或添加申请，则删除对应用户的 my_project 的缓存
    by:王健 at:2015-4-14
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    checker = models.ForeignKey(Person, null=True, blank=True, verbose_name=u'审核人', help_text=u'隶属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    content = models.CharField(max_length=100, verbose_name=u'申请')
    status = models.NullBooleanField(default=None, db_index=True, verbose_name=u'是否同意',
                                     help_text=u'None 未处理, True 同意，False 不同意')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'申请发出时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(ProjectApply, self).save(*args, **kwargs)
        cache.delete(MY_PROJECT_QUERY_LIST % self.user_id)


class Social(JSONBaseModel):
    """
    社会化登陆
    by:王健 at:2015-1-3
    添加索引
    by:王健 at:2015-1-25
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    media_type = models.CharField(max_length=10, db_index=True, verbose_name=u'第三方网站')
    media_uid = models.CharField(max_length=50, db_index=True, verbose_name=u'第三方网站账号')
    social_uid = models.CharField(max_length=30, unique=True, verbose_name=u'百度社会化id')
    session_key = models.CharField(max_length=200, verbose_name=u'百度社会化 key')
    session_secret = models.CharField(max_length=50, verbose_name=u'百度社会化 秘钥')
    token = models.CharField(max_length=100, verbose_name=u'第三方网站授权信息', help_text=u'token')
    expires_in = models.IntegerField(blank=True, null=True, verbose_name=u'第三方网站授权信息，有效期', help_text=u'以秒为单位')

    def __unicode__(self):
        return unicode(self.user)

    class Meta():
        verbose_name = u'第三方网站授权'


class RecordDate(JSONBaseModel):
    """
    按天记录
    by:王健 at:2015-1-29
    增加最后上传人
    by:王健 at:2015-2-10
    修改def __unicode__
    by:尚宗凯 at:2015-2-19
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    file_group = models.ForeignKey('FileGroup', verbose_name=u'隶属应用')
    date = models.DateField(default=timezone.now, db_index=True, verbose_name=u'日期')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'最后修改时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'时间戳')
    num = models.IntegerField(default=0, verbose_name=u'记录数量')
    last_create_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'最后上传人')

    def __unicode__(self):
        return unicode(self.date)
        # return unicode(self.user)

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        self.create_time = timezone.now()
        super(RecordDate, self).save(*args, **kwargs)

    class Meta():
        verbose_name = u'每日记录'
        unique_together = (("project", "file_group", "date"),)


class SGTQlog(RecordDate):
    """
    施工日志的日期
    by:王健 at:2015-1-5
    日期加上索引, 地点使用项目的地点
    by:王健 at:2015-1-6
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    添加 create_time 、timeline 、num 字段
    by:王健 at:2015-1-20
    添加索引
    by:王健 at:2015-1-25
    继承每日记录
    by:王健 at:2015-1-29
    """
    weather = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'天气')
    wind = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'风力')
    qiwen = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'气温')

    def toJSON(self):
        """
        没有天气值时，使用未知替代
        by:王健 at:2015-3-5
        """
        d = super(SGTQlog, self).toJSON()
        if not d['weather']:
            d['weather'] = u'未知'
        if not d['wind']:
            d['wind'] = u'未知'
        if not d['qiwen']:
            d['qiwen'] = u'未知'
        return d


    def __unicode__(self):
        return unicode(self.date.strftime('%Y-%M-%D'))

    class Meta():
        verbose_name = u'施工工作日天气'


class SGlog(JSONBaseModel):
    """
    施工日志
    by:王健 at:2015-1-5
    datetime 改为 create_time
    by:王健 at:2015-1-12
    修改Model名字，去除下划线，
    by:王健 at:2015-1-13
    添加索引
    by:王健 at:2015-1-25
    增加是否删除属性，增加timeline属性
    by:王健 at:2015-2-10
    修改日志的 text 字段长度
    by:王健 at:2015-2-11
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    sg_tq_log = models.ForeignKey(SGTQlog, verbose_name=u'施工日期')
    text = models.CharField(max_length=50, verbose_name=u'日志')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'日志时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    is_active = models.BooleanField(default=True, verbose_name=u'是否删除')

    def __unicode__(self):
        return unicode(self.text)

    def save(self, *args, **kwargs):
        """
        保存日志时，更新天气信息的num数据
        by:王健 at:2015-2-14
        极光推送修改内容
        by：尚宗凯 at：2015-04-07
        极光推送ios适配
        by：尚宗凯 at：2015-04-07
        #变更工程日志极光推送
        #by:尚宗凯 at:2015-4-9
        #极光推送IOS增加字段
        #by:尚宗凯 at:2015-4-23
		变更极光推送方法
		by：尚宗凯 at：2015-05-31
        """
        self.timeline = int(time.time())
        super(SGlog, self).save(*args, **kwargs)
        self.sg_tq_log.num = self.sg_tq_log.sglog_set.filter(is_active=True).count()
        self.sg_tq_log.save()
        # data = {"title":"施工日志有了新变化","message":"施工日志有了新变化","project_id":self.project_id,"type":"refresh", "flag":"gong_cheng_ri_zhi"}
        # NeedPush.new().send(msg_content=u"施工日志有了新变化",title=u"施工日志有了新变化",content_type=u"content_type",extras=data,tag="p_"+str(self.project_id))



    class Meta():
        verbose_name = u'施工日志'


class FileGroupJSON(JSONBaseModel):
    """
    客户端的app json数据，缓存成一个数据
    by:王健 at:2015-1-11
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    添加索引
    by:王健 at:2015-1-25
    """
    project = models.OneToOneField(Project, verbose_name=u'隶属项目')
    jsontext = models.TextField(verbose_name=u'应用模块的 json 数据')
    timeline = models.IntegerField(null=True, blank=True, db_index=True, verbose_name=u'时间戳')


class FileGroup(JSONBaseModel):
    """
    应用模块的“节点”
    by:王健 at:2015-1-11
    修改Model名字，去除下划线，index改为sorted
    by:王健 at:2015-1-13
    添加is_pub 字段，以后用来标记该字段是否允许游客可见
    by:王健 at:2015-1-18
    添加索引
    by:王健 at:2015-1-25
    添加icon_url 字段
    by:王健 at:2015-1-28
    """
    CREATE_TYPE = (('sys', u'系统创建'), ('c', u'用户自定义'))
    from nsbcs.models import File

    project = models.ForeignKey(Project, verbose_name=u'隶属项目', null=True, blank=True, help_text=u'隶属项目')
    name = models.CharField(max_length=30, verbose_name=u'名称')
    flag = models.CharField(max_length=50, unique=True, verbose_name=u'功能标记')
    icon = models.CharField(max_length=100, blank=True, verbose_name=u'图标', help_text=u'手机端本地的图片')
    icon_url = models.ForeignKey(File, related_name='file_group_icon', verbose_name=u'头像', null=True, blank=True,
                                 help_text=u'应用头像')
    typeflag = models.CharField(max_length=15, verbose_name=u'展示类型')
    father = models.ForeignKey('FileGroup', null=True, blank=True, verbose_name=u'应用模块的节点')
    sorted = models.IntegerField(db_index=True, verbose_name=u'排序')
    status = models.CharField(max_length=5, db_index=True, choices=CREATE_TYPE, verbose_name=u'应用类型',
                              help_text=u'系统创建为：sys，用户自定义为：c')
    is_pub = models.BooleanField(default=False, db_index=True, verbose_name=u'是否对外公开')

    def __unicode__(self):
        return unicode(self.name)


    def save(self, *args, **kwargs):
        FileGroupJSON.objects.filter(project_id=self.project_id).delete()
        super(FileGroup, self).save(*args, **kwargs)

    def toJSON(self):
        """
        自定义 json函数
        by:王健 at:2015-2-6
        """
        d = super(FileGroup, self).toJSON()
        if not self.project and not self.icon_url:
            d['icon_url'] = 'http://needserver.duapp.com/static/icon/%s' % self.icon
        if self.project and self.icon_url:
            d['icon_url'] = self.icon_url.get_url()
        return d

    @staticmethod
    def is_flag_is_a_father_flag(flag):
        """
        判断是否是父级节点
        by:尚宗凯 at：2015-05-06
        使用缓存
        by：尚宗凯 at：2015-05-20
        """
        fg = FileGroup.objects.get(flag=flag)
        father_flag_id_list = [i['father_id'] for i in FileGroup.objects.filter(father_id__gt=1).distinct().values("father_id")]  #可以放缓存里
        if fg.pk in father_flag_id_list:
            return True
        else:
            return False

    @staticmethod
    def get_father_flag(flag):
        """
        获取节点的父节点
        by:尚宗凯 at：2015-05-15
        """
        if FileGroup.is_flag_is_a_father_flag(flag) or FileGroup.is_single_flag(flag):
            return FileGroup.objects.get(flag=flag)
        else:
            return FileGroup.objects.get(flag=flag).father


    @staticmethod
    def get_child_flag(flag):
        """
        获取子节点
        by:尚宗凯 at：2015-05-06
        """
        if not FileGroup.is_flag_is_a_father_flag(flag):
            return False
        else:
            fg = FileGroup.objects.filter(flag=flag)
            child_fg = FileGroup.objects.filter(father=fg)
            return child_fg

    @staticmethod
    def get_child_flag2(flag):
        """
        子节点定义为：这个节点存在father_id
        by:尚宗凯 at：2015-05-19
        优化查询
        by：尚宗凯 at：2015-05-20
        """
        file_group = FileGroup.objects.get(flag=flag)
        if file_group.father:
            return []
        else:
            return [x[0] for x in FileGroup.objects.filter(father_id=file_group.pk).values_list("flag")]

    @staticmethod
    def is_single_flag(flag):
        """
        判断节点是否非父节点非子节点
        by:尚宗凯 at：2015-05-06
        """
        if FileGroup.is_flag_is_a_father_flag(flag):
            return False
        elif FileGroup.objects.get(flag=flag).father_id > 1:
            return False
        else:
            return True

    @staticmethod
    def get_father_flag2(flag):
        """
        按照父节点定义为：如果节点没有子节点就是父节点，通过flag返回父节点的flag
        by:尚宗凯 at：2015-05-15
        """
        file_group = FileGroup.objects.get(flag=flag)
        if file_group.father:
            return file_group.father.flag
        else:
            return flag

    class Meta():
        verbose_name = u'应用'


class FileRecord(JSONBaseModel):
    """
    应用的内容项
    by:王健 at:2015-1-11
    date字段 改为datetime字段
    by:王健 at:2015-1-12
    修改Model名字，去除下划线
    by:王健 at:2015-1-13
    添加索引
    by:王健 at:2015-1-25
    添加多文件记录字段
    by:王健 at:2015-1-29
    增加赞、踩 评论数量 字段，优化files存取
    by:王健 at:2015-1-31
    无效嗲吗清除
    by:王健 at:2015-2-25
    修改字段长度限制
    by:王健 at:2015-3-11
    增加status字段
    by:尚宗凯 at:2015-3-27
    修改字段名称
    by:尚宗凯 at:2015-3-30
    增加filetype字段
    by:尚宗凯 at:2015-3-30
    增加极光推送
    by:尚宗凯 at:2015-4-8
    flag为空不需要发送极光推送
    by:尚宗凯 at:2015-4-8
    filetype可空
    by: 范俊伟 at:2015-04-14
    删除一些无效的字段
    by:王健 at:2015-05-27
    变更极光推送方法
    by：尚宗凯 at：2015-05-31
    增加图片的比例
    by:尚宗凯 at：2015-06-02
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', null=True, blank=True, help_text=u'隶属项目')
    title = models.CharField(max_length=300, verbose_name=u'标题')
    file_group = models.ForeignKey(FileGroup, verbose_name=u'隶属应用')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'创建日期')
    text = models.CharField(max_length=500, null=True, blank=True, verbose_name=u'内容')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    files = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True, verbose_name=u'文件存储数组')
    files_scale = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True, verbose_name=u'文件长高比例存储数组')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    is_active = models.BooleanField(default=True, verbose_name=u'状态', help_text=u'True 未删除,False 已删除')
    filetype = models.CharField(max_length=20, null=True, verbose_name=u'文件类型')

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        if isinstance(self.files, list):
            import json

            self.files = json.dumps(self.files).replace('L', '')
        super(FileRecord, self).save(*args, **kwargs)
        # 增加极光推送
        #by:尚宗凯 at:2015-4-8
        #极光推送改为按照别名推送
        #by：尚宗凯 at：2015-04-13
        #极光推送IOS增加字段
        #by:尚宗凯 at:2015-4-23
        #修改极光推送方式
        #by:尚宗凯 at：2015-05-07
        # if flag:
        #     alias = list(set(get_alias_by_project_id_flag(self.project_id, flag, self.file_group.pk)))
        #     # alias = list(set(get_alias_by_project_id_filegroup_id(self.project_id, self.file_group.pk)))
        #     NeedPush.send_jpush(flag=flag,
        #                         project_id=self.project_id,
        #                         title=Project.get_project_name_by_id(self.project_id),
        #                         msg=FileGroup.objects.get(flag=flag).name,
        #                         alias=alias,
        #                         file_group=FileGroup.objects.get(flag=flag).toJSON()
        #     )

    def append_file(self, fileid):
        if isinstance(self.files, (str, unicode)):
            import json

            self.files = json.loads(self.files)
        elif self.files == None:
            self.files = []
        if int(fileid) not in self.files:
            self.files.append(int(fileid))

    def set_is_active_false(self):
        # 设置status
        #by 尚宗凯 at：2015-03-27
        #修改字段名称
        #by:尚宗凯 at:2015-3-30
        self.is_active = False

    class Meta():
        verbose_name = u'应用'


class EngineCheck(JSONBaseModel):
    """
    工程检查, 部分字段设为 可为空
    by:王健 at:2015-1-13
    增加了创建时间
    by:王健 at:2015-1-15
    添加索引
    by:王健 at:2015-1-25
    完成时间属性
    by:王健 at:2015-2-10
    增加is_active字段
    by:尚宗凯 at:2015-3-30
    工程检查增加极光推送
    by:尚宗凯 at:2015-4-8
    上传图片增加长高比例
    by：尚宗凯 at：2015-06-02
    """
    from nsbcs.models import File

    project = models.ForeignKey(Project, verbose_name=u'隶属项目', null=True, blank=True, help_text=u'隶属项目')
    file_group = models.ForeignKey(FileGroup, verbose_name=u'隶属应用')
    # title = models.CharField(max_length=50, verbose_name=u'标题')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    # path = models.CharField(max_length=50, verbose_name=u'位置')
    pre_pic = models.ForeignKey(File, related_name='pre_pic', verbose_name=u'整改前照片')
    desc = models.CharField(max_length=300, verbose_name=u'问题描述')
    chuli = models.CharField(max_length=300, null=True, blank=True, verbose_name=u'处理意见')
    chuli_pic = models.ForeignKey(File, null=True, blank=True, related_name='chuli_pic', verbose_name=u'处理结果')
    fucha = models.CharField(max_length=300, null=True, blank=True, verbose_name=u'复查意见')
    status = models.BooleanField(default=False, verbose_name=u'状态', help_text=u'是否处理完成')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'发布日期')
    finish_time = models.DateTimeField(null=True, verbose_name=u'发布日期')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    is_active = models.BooleanField(default=True, verbose_name=u'状态', help_text=u'True 未删除,False 已删除')
    pre_pic_scale = models.FloatField(default=None, null=True, verbose_name=u'整改前照片长高比例')
    chuli_pic_scale = models.FloatField(default=None, null=True, verbose_name=u'整改后照片长高比例')

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(EngineCheck, self).save(*args, **kwargs)
        # 增加极光推送
        #by:尚宗凯 at:2015-4-8
        #增加flag默认值
        #by:尚宗凯 at:2015-4-9
        #极光推送改为用别名
        #by：尚宗凯 at：2015-04-13
        #极光推送IOS增加字段
        #by:尚宗凯 at:2015-4-23
        #修改极光推送
        #by：尚宗凯 at：2015-05-07
        # if flag:
        #     alias = list(set(get_alias_by_project_id_flag(self.project_id, flag, self.file_group.pk)))
        #     # alias = list(set(get_alias_by_project_id_filegroup_id(self.project_id, self.file_group.pk)))
        #
        #     NeedPush.send_jpush(flag=flag,
        #                         project_id=self.project_id,
        #                         title=Project.get_project_name_by_id(self.project_id),
        #                         msg=FileGroup.objects.get(flag=flag).name,
        #                         alias=alias,
        #                         file_group=FileGroup.objects.get(flag=flag).toJSON()
        #     )

    def set_is_active_false(self):
        # 设为False
        #by:尚宗凯 at:2015-3-30
        self.is_active = False


class GYSAddress(JSONBaseModel):
    """
    供应商名录
    by:王健 at:2015-1-13
    增加记录人字段
    by:王健 at:2015-1-14
    增加了创建时间
    by:王健 at:2015-1-15
    添加索引
    by:王健 at:2015-1-25
    去除是否合同、付款方式 字段
    by:王健 at:2015-2-4
    增加极光推送
    by:尚宗凯 at:2015-4-8
    修改提示文字
    by:尚宗凯 at:2015-4-8
    修改提示文字
    by:尚宗凯 at:2015-4-20
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', null=True, blank=True, help_text=u'隶属项目')
    file_group = models.ForeignKey(FileGroup, verbose_name=u'隶属应用')
    name = models.CharField(max_length=50, db_index=True, verbose_name=u'物资名称')
    ghs = models.CharField(max_length=50, db_index=True, verbose_name=u'供应商')
    ghs_fzr = models.CharField(max_length=10, db_index=True, verbose_name=u'供应商负责人')
    ghs_fzr_tel = models.CharField(max_length=15, db_index=True, verbose_name=u'供应商负责人电话')
    # is_hetong = models.BooleanField(default=False, verbose_name=u'是否签了合同')
    # pay_type = models.CharField(max_length=15, verbose_name=u'付款方式')
    shr = models.CharField(max_length=10, db_index=True, verbose_name=u'送货联系人')
    shr_tel = models.CharField(max_length=15, db_index=True, verbose_name=u'送货联系人电话')
    bz = models.CharField(max_length=200, verbose_name=u'备注')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'记录人')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'发布日期')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(GYSAddress, self).save(*args, **kwargs)


class WuZiRecord(JSONBaseModel):
    """
    物资记录
    by:王健 at:2015-1-13
    增加记录人字段
    by:王健 at:2015-1-14
    领料单位、领料人、库存量 可以为空
    by:王健 at:2015-1-17
    添加索引
    by:王健 at:2015-1-25
    添加“记录日期”字段
    by:王健 at:2015-1-29
    去除 num 字段，count 改为数量
    by:王健 at:2015-2-4
    is_active 字段
    by:王健 at:2015-2-10
    修改 gg字段长度，count字段类型
    by:王健 at:2015-2-12
    修改gg 和 count 字段的 长度
    by:王健 at:2015-3-11
    增加极光推送
    by:尚宗凯 at:2015-4-8
    尺寸规格 修改名字
    by:王健 at:2015-4-10
    """
    # TYPESTATUS = (('buy', u'物资购买记录'), ('come', u'物资入库记录'), ('out', u'物资出库记录'))
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', null=True, blank=True, help_text=u'隶属项目')
    file_group = models.ForeignKey(FileGroup, verbose_name=u'隶属应用')
    record_date = models.ForeignKey(RecordDate, verbose_name=u'哪一天')
    name = models.CharField(max_length=50, db_index=True, verbose_name=u'物资名称')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name=u'日期')
    gg = models.CharField(max_length=200, verbose_name=u'尺寸规格')
    # status = models.CharField(max_length=5, db_index=True, choices=TYPESTATUS, verbose_name=u'类型')
    company = models.CharField(max_length=20, db_index=True, null=True, blank=True, verbose_name=u'领料单位')
    lingliaoren = models.CharField(max_length=10, db_index=True, null=True, blank=True, verbose_name=u'领料人')
    count = models.CharField(max_length=200, verbose_name=u'数量', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'记录人')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'是否删除')

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(WuZiRecord, self).save(*args, **kwargs)


class MessageBase(JSONBaseModel):
    """
    消息基类
    by:王健 at:2015-2-25
    修复save函数bug
    by:王健 at:2015-2-26
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    title = models.CharField(max_length=30, verbose_name=u'标题')
    text = models.TextField(verbose_name=u'系统消息内容')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'日志时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'时间戳')

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(MessageBase, self).save(*args, **kwargs)


    class Meta():
        abstract = True
        verbose_name = u'消息基类'


class SysMessage(MessageBase):
    """
    针对项目的系统消息
    by:王健 at:2015-2-25
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'针对个人')
    to_group = models.ForeignKey(Group, null=True, verbose_name=u'针对项目的分组')

    class Meta():
        verbose_name = u'系统消息'


class ProjectMessage(MessageBase):
    """
    针对项目的系统消息
    by:王健 at:2015-2-25
    添加公告的发布人
    by:王健 at:2015-2-26
    """
    to_group = models.ForeignKey(Group, verbose_name=u'针对项目的分组')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'发布人')

    class Meta():
        verbose_name = u'分组公告消息'


class NeedMessage(JSONBaseModel):
    """
    针对用户的消息
    by：尚宗凯 at：2015-03-31
    增加status type字段
    by：尚宗凯 at：2015-04-01
    增加一些功能
    by：尚宗凯 at：2015-04-09
    修改一些功能
    by：尚宗凯 at：2015-04-09
    消息自动回复
    by：尚宗凯 at：2015-04-13
    为多人发送系统消息
    by：尚宗凯 at：2015-04-13
    修改多人发送系统消息bug
    by：尚宗凯 at：2015-04-14
    增加发送need消息时发送极光推送
    by：尚宗凯 at：2015-04-14
    接口存在的bug
    by：尚宗凯 at：2015-04-14
    发送系统消息时发送极光推送
    by：尚宗凯 at：2015-04-14
    极光推送IOS增加字段
    by:尚宗凯 at:2015-4-23
    修改极光推送need消息文本
    by:尚宗凯 at:2015-4-27
    """
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'发布人', related_name=u"create_user",
                                    null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'接收人', related_name=u"to_user", null=True)
    title = models.CharField(max_length=30, verbose_name=u'标题', null=True)
    text = models.TextField(verbose_name=u'消息内容', null=True)
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'日志时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'时间戳')
    status = models.IntegerField(default=1, verbose_name=u'消息状态')  # NEED_MESSAGE_STATUS
    type = models.IntegerField(default=1, verbose_name=u'消息类型')  # NEED_MESSAGE_TYPE

    def __unicode__(self):
        return unicode(self.title)

    def save(self, *args, **kwargs):
        self.timeline = int(time.time())
        super(NeedMessage, self).save(*args, **kwargs)

    @staticmethod
    def create_sys_message(to_user_id, title, text, type=1):
        """
        Need系统消息创建
        by: 范俊伟 at:2015-05-07
        增加网路请求超时时间,改为同步调用
        by: 范俊伟 at:2015-05-07
        """
        try:
            to_user = NSUser.objects.get(pk=to_user_id)
        except NSUser.DoesNotExist:
            return
        try:
            u = MyEncoder.default(to_user)
            u.update(to_user.get_user_map(True))
            data = {"user": u, "text": text}
            data = json.dumps(data)
            sign = hashlib.md5(data + 'sdfasdnasldkfj1293sdlnfld').hexdigest()
            url = settings.NEED_KF_BASE_URL + '/kf/create_sys_message'
            requests.post(url, {"data": data, "sign": sign}, timeout=5)
        except:
            from util.tools import common_except_log

            common_except_log()


    def set_status_read(self):
        self.status = 0
        self.save()

    @staticmethod
    def create_customer_service_message(to_user, title, text, type=2):
        msg = NeedMessage()
        try:
            if to_user:
                msg.to_user = NSUser.objects.get(pk=to_user)
            if title:
                msg.title = title
            if text:
                msg.text = text
            if type:
                msg.type = type
            msg.create_user = NSUser.objects.get(pk=SHOW_USER_ID)
            msg.save()
        except Exception as e:
            print

    @staticmethod
    def create_multiple_sys_message(multi_to_user_ids, title, text, type=1):
        for user_id in multi_to_user_ids:
            NeedMessage.create_sys_message(user_id, title, text, type=type)

    class Meta():
        verbose_name = u'用户公告消息'


class NeedMessageRead(JSONBaseModel):
    """
    need消息阅读时间
    by:尚宗凯 at：2014-04-14
    通过用户id获取timeline
    by:尚宗凯 at：2014-04-14
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'接收人', primary_key=True)
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'时间戳')

    @staticmethod
    def get_user_timeline(user_id):
        try:
            nmr = NeedMessageRead.objects.get(pk=user_id)
            return nmr.timeline
        except Exception as e:
            print e
            return None


class NSJiFen(JSONBaseModel):
    """
    用户积分
    by 尚宗凯 at:2015-3-7
    """
    id = models.CharField(max_length=200, verbose_name=u'积分唯一标示', primary_key=True)
    days = models.IntegerField(verbose_name=u'连续登陆天数', default=0)
    type = models.CharField(max_length=200, verbose_name=u'积分类型', blank=True, null=True)
    fen = models.IntegerField(verbose_name=u'积分数值', default=0)

    class Meta():
        verbose_name = u'积分'


class NSPersonTel(JSONBaseModel):
    """
    通过手机号加人，手机号保存表
    null 属性修改
    by:王健 at:2015-03-25
    改为tel可以重复
    by：尚宗凯 at：2015-04-08
    """
    tel = models.CharField(max_length=20, null=True, blank=True, help_text=u'手机号')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'用户')
    project = models.ForeignKey(Project, null=True, verbose_name=u'项目')
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=u'分组')
    create_time = models.DateTimeField(verbose_name=u'创建时间', default=timezone.now)


class NeedHelper(JSONBaseModel):
    """
    Need的小助手的 数据
    by:王健 at:2015-3-31
    增加客户端类型
    by:王健 at:2015-4-3
    增加获取跳转url方法
    by：尚宗凯 at：2015-04-03
    """
    file_group = models.CharField(max_length=50, verbose_name=u'应用节点')
    min_version = models.IntegerField(default=0, verbose_name=u'最低版本')
    max_version = models.IntegerField(default=0, verbose_name=u'最高版本支持')
    client_type = models.CharField(max_length=20, default="", verbose_name=u'客户端类型')
    url = models.URLField(verbose_name=u'跳转url')
    name = models.CharField(max_length=50, verbose_name=u'应用节点中文名')

    @staticmethod
    def get_url(file_group, version="", client_type=""):
        nh = NeedHelper.objects.all()
        if file_group:
            nh = nh.filter(file_group=file_group)
        if version:
            nh = nh.filter(max_version__gte=int(version)).filter(min_version__lte=int(version))
        # if client_type:
        # nh = nh.filter(client_type=client_type)

        if nh.exists():
            return nh[0].url
        else:
            return False


class SMSCounter(JSONBaseModel):
    """
    短信计数
    by: 范俊伟 at:2015-04-09
    bae测试服务器发送数量改为99次
    by: 范俊伟 at:2015-05-07
    """
    TYPE_CHOICES = (
        (0, u'注册'),
        (1, u'找回密码')
    )
    tel = models.CharField(max_length=20, null=True, blank=True, help_text=u'手机号')
    flag = models.IntegerField(verbose_name='接口标记')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    @staticmethod
    def add_tel(tel, flag):
        sms_counter = SMSCounter()
        sms_counter.tel = tel
        sms_counter.flag = flag
        sms_counter.save()

    @staticmethod
    def check_count(tel, flag):
        # return 0
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(1)
        query = SMSCounter.objects.filter(tel=tel, flag=flag, time__gt=start_time).order_by('-time')[:5]
        if settings.ENVIRONMENT == "baidu":
            if query.count() >= 99:
                return -1
        else:
            if query.count() >= 5:
                return -1
            elif query.count() > 0:
                last_tel = query[0]
                delta = now - last_tel.time
                if delta.seconds < 60:
                    return -2
            return 0

    @staticmethod
    def check_count_and_add_tel(tel, flag):
        res = SMSCounter.check_count(tel, flag)
        if res == 0:
            SMSCounter.add_tel(tel, flag)
            return 0
        else:
            return res


class Reply(JSONBaseModel):
    """
    评论
    by：尚宗凯 at：2015-04-29
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    content = models.CharField(max_length=300, verbose_name=u'评论内容')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"reply_user", verbose_name=u'评论的人')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u"reply_to_user", verbose_name=u'被评论的人')
    file_record = models.ForeignKey(FileRecord, verbose_name=u'file_record', help_text=u'file_record', related_name=u"reply_file_record")
    file_group = models.ForeignKey(FileGroup, verbose_name=u'file_group', help_text=u'file_group')
    create_time = models.DateTimeField(default=timezone.now,verbose_name=u'项目评论日期',
                                       help_text=u'项目评论日期')


class UserLastReadTimeline(JSONBaseModel):
    """
    记录用户最后一次刷新某节点的时间
    by：尚宗凯 at：2015-05-05
    修改数据库
    by：尚宗凯 at：2015-05-08
    在百度环境下添加，输出日志
    by:王健 at:2015-05-18
    修改输入日志
    by：尚宗凯 at：2015-05-18
    优化代码，去掉记录日志
    by：尚宗凯 at：2015-05-18
    """
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目')
    file_group_id = models.IntegerField(default=0, verbose_name=u'file_group', help_text=u'file_group')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'最后一次阅读的时间')

    @staticmethod
    def update_last_read_timeline(project_id, file_group_id, user_id):
        """
        在百度环境下添加，输出日志
        by:王健 at:2015-05-18
        bug解决，屏蔽日志
        by:王健 at:2015-05-18
        删除多余内容,增加缓存删除操作
        by：尚宗凯 at：2015-05-19
        """
        if not file_group_id:
            file_group_id = 0
        # cache.delete(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id))
        ulrt, created = UserLastReadTimeline.objects.get_or_create(project_id=project_id,file_group_id=file_group_id,user_id=user_id)
        # if created:
            # ulrt.project_id = project_id
            # ulrt.file_group_id = file_group_id
            # ulrt.user_id = user_id
        ulrt.timeline = int(time.time())
        cache.set(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id), ulrt.timeline, settings.CACHES_TIMEOUT)
        ulrt.save()

    @staticmethod
    def get_last_read_timeline(project_id, file_group_id, user_id):
        """
        获取最后一次阅读时间
        by：尚宗凯 at：2015-05-06
        新加入用户将对方最后一次阅读时间设置为创建的时间
        by: 尚宗凯 at：2015-05-18
        增加缓存
        by：尚宗凯 at：2015-05-19
        优化缓存结果的非空判断
        by:王健 at:2015-05-21
        """
        timeline = cache.get(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id))
        if timeline is not None:
            return timeline
        else:
            if UserLastReadTimeline.objects.filter(project_id=project_id,file_group_id=file_group_id,user_id=user_id).exists():
                timeline = UserLastReadTimeline.objects.get(project_id=project_id,file_group_id=file_group_id,user_id=user_id).timeline
                cache.set(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id),timeline,settings.CACHES_TIMEOUT)
                return timeline
            else:
                if Person.objects.filter(user_id=user_id, project_id=project_id).exists():
                    timeline = Person.objects.get(user_id=user_id,project_id=project_id).timeline
                    cache.set(RED_DOT_USER_LAST_READ_TIMELINE % (project_id, file_group_id, user_id),timeline,settings.CACHES_TIMEOUT)
                    return timeline
                else:
                    return 0


class LastReadTimeProjectSysMessage(JSONBaseModel):
    """
    系统消息，项目公告最后一次阅读时间
    by：尚宗凯 at：2015-05-08
    系统消息由于没有group_id,特殊处理
    by：尚宗凯 at：2015-05-11
    update_last_read_timeline针对没有group_id,特殊处理
    by：尚宗凯 at：2015-05-11
    增加缓存
    by：尚宗凯 at：2015-05-21
    """
    type = models.CharField(max_length=100, verbose_name=u'缓存的类型',null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目',null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户',null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, verbose_name=u'消息针对分组')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'最后一次阅读的时间')

    @staticmethod
    def update_last_read_timeline(type, user_id, project_id, group_id):
        if not group_id:
            lrtpmsm, created = LastReadTimeProjectSysMessage.objects.get_or_create(type=type, project_id=project_id, user_id=user_id)
        else:
            lrtpmsm, created = LastReadTimeProjectSysMessage.objects.get_or_create(type=type, project_id=project_id, user_id=user_id, group_id=group_id)
        if created:
            lrtpmsm.project_id = project_id
            lrtpmsm.type = type
            lrtpmsm.user_id = user_id
        lrtpmsm.timeline = int(time.time())
        lrtpmsm.save()
        cache.set(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % (type, user_id, project_id, group_id), lrtpmsm.timeline, settings.CACHES_TIMEOUT)

    @staticmethod
    def get_last_read_timeline(type, user_id, project_id, group_id):
        assert type in ("sysmessage","project_message")
        timeline = cache.get(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % (type, user_id, project_id, group_id))
        if timeline != None:
            return timeline
        else:
            if type == "sysmessage":
                if LastReadTimeProjectSysMessage.objects.filter(type=type,user_id=user_id,project_id=project_id).exists():
                    timeline = LastReadTimeProjectSysMessage.objects.get(type=type,user_id=user_id,project_id=project_id).timeline
                else:
                    timeline = 0
            else:
                if LastReadTimeProjectSysMessage.objects.filter(type=type,user_id=user_id,project_id=project_id,group_id=group_id).exists():
                    timeline = LastReadTimeProjectSysMessage.objects.get(type=type,user_id=user_id,project_id=project_id,group_id=group_id).timeline
                else:
                    timeline = 0
            cache.set(RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE % (type, user_id, project_id, group_id), timeline, settings.CACHES_TIMEOUT)
            return timeline


# class RechargeRecord(JSONBaseModel):
#     """
#     充值记录
#     by：尚宗凯 at：2015-06-08
#     """
#     order_id = models.IntegerField(null=True, unique=True, verbose_name=u'订单id')
#     contract_code = models.CharField(max_length=30, null=True, unique=True, verbose_name=u'合同编号')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户', help_text=u'隶属于某个用户')
#     project = models.ForeignKey(Project, verbose_name=u'隶属项目', help_text=u'隶属项目',null=True, blank=True)
#     price = models.BigIntegerField(default=0, verbose_name=u'付费金额', help_text=u'付费金额')
#     expired_date = models.DateField(verbose_name=u'过期时间')
#     recharge_type = models.IntegerField(null=True, verbose_name=u'充值类型', help_text=u'充值类型 0客服操作 1用户自身操作')
#     create_time = models.DateTimeField(verbose_name=u'创建时间', default=timezone.now)

