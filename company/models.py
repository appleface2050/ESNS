#coding=utf-8
from django.conf import settings
from django.db import models
from django.utils import timezone
from util.basemodel import JSONBaseModel

__author__ = 'wangjian'


class BigCompany(JSONBaseModel):
    """
    集团
    by:王健 at:2015-06-10
    增加是否展示字段
    by：尚宗凯 at：2015-06-15
    """
    name = models.CharField(max_length=30, verbose_name=u'公司或集团')
    logo = models.IntegerField(default=0, verbose_name=u'公司或集团logo， 图片id')
    is_display = models.BooleanField(default=False, verbose_name=u'是否默认展示')

    def toJSON(self):
        """
        自定义 json函数
        by:王健 at:2015-06-10
        完善一下
        by：尚宗凯 at：2015-06-11
        添加测试图片地址
        by:王健 at:2015-06-16
        修改测试图片地址
        by:尚宗凯 at:2015-06-16
        修改测试图片地址
        by:尚宗凯 at:2015-06-16
        去掉测试图片地址
        by:尚宗凯 at：2015-06-22
        去掉测试地址
        by:王健 at:2015-06-27
        修改集团logo无法显示的bug
        by:王健 at:2015-06-27
        """
        d = super(BigCompany, self).toJSON()
        d['logo_url'] = ''
        if self.logo:
            from nsbcs.models import SysFile
            try:
                d['logo_url'] = SysFile.objects.get(pk=self.logo).get_url('imageView2/5/w/%s/h/%s' % (200, 88))
            except SysFile.DoesNotExist, e:
                pass
        return d


class Company(JSONBaseModel):
    """
    企业，与项目可关联的企业
    by:王健 at:2015-06-08
    设置公司状态
    by:王健 at:2015-06-22
    增加集团字段为空
    by:尚宗凯 at：2015-06-24
    去除无用参数
    by:王健 at:2015-06-27
    """
    bigcompany = models.ForeignKey(BigCompany, verbose_name=u'隶属集团或公司',null=True)
    name = models.CharField(max_length=30, verbose_name=u'公司', db_index=True)
    logo = models.IntegerField(default=0, verbose_name=u'公司logo，图片id')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'加入的时间')
    expired_date = models.DateField(default=timezone.now, verbose_name=u'公司过期时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    address = models.CharField(max_length=100, verbose_name=u'公司地址', db_index=True, null=True)
    phone = models.CharField(max_length=15, null=True, verbose_name=u'手机号或固定电话')
    top_logo = models.IntegerField(default=0, verbose_name=u'公司toplogo，图片id')
    status = models.IntegerField(default=0, verbose_name=u'状态', help_text=u'客服后台管理 0：试用 1：正式试用 2：删除')

    def __unicode__(self):
        """
        修改total_name
        by:王健 at:2015-1-8
        :return:
        """
        return unicode(self.name)

    def toJSON(self):
        """
        自定义 json函数
        by:王健 at:2015-06-10
        完善 json函数
        by：尚宗凯 at：2015-06-11
        测试logo_url
        by：尚宗凯 at：2015-06-16
        增加bigcompany_name字段
        by：尚宗凯 at：2015-06-16
        增加top_logo_url
        by:尚宗凯 at：2015-06-19
        固定logo和top_logo的图片高度
        by:王健 at:2015-06-23
        完善top logo url逻辑
        by：尚宗凯 at：2015-06-24
        固定logo和top_logo的图片高度
        by:王健 at:2015-06-24
        显示真实logo数据
        by:王健 at:2015-06-26
        """
        d = super(Company, self).toJSON()
        d['logo_url'] = ''
        from nsbcs.models import ComFile
        if self.logo > 0:
            try:
                d['logo_url'] = ComFile.objects.get(pk=self.logo).get_url('imageView2/5/w/%s/h/%s' % (40, 40))
            except ComFile.DoesNotExist, e:
                pass
            # if settings.ENVIRONMENT == 'baidu':
            #     d['logo_url'] = 'http://www.tjeasyshare.com/static/headicon/001.jpg'
        if self.top_logo > 0:
            try:
                d['top_logo_url'] = ComFile.objects.get(pk=self.top_logo).get_url('imageView2/5/w/%s/h/%s' % (200, 88))
            except Exception as e:
                d['top_logo_url'] = ""
        else:
            d['top_logo_url'] = ""
        # if settings.ENVIRONMENT == 'baidu':
        #     d['top_logo_url'] = 'http://7xj20h.com2.z0.glb.qiniucdn.com//sys_bigcom/6fdaab2e-41fd-4956-98c5-fd522f1a1151.png?attname=top_zhongtianlogo%402x.png'
        if self.bigcompany:
            d["bigcompany_name"] = self.bigcompany.name
        return d


class SysBanner(JSONBaseModel):
    """
    系统banner
    by：尚宗凯 at：2015-06-11
    """
    image = models.IntegerField(default=0, verbose_name=u'公司logo，图片id')
    url = models.CharField(max_length=200, null=True, verbose_name=u'链接地址')
    index_num = models.IntegerField(default=0, verbose_name=u'排序字段')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    def toJSON(self):
        """
        获取系统banner的数据
        by:王健 at:2015-06-22
        输出系统banner 的字典
        by:王健 at:2015-06-22
        设置默认测试image_url
        by:王健 at:2015-06-22
        修改banner逻辑
        by：尚宗凯 at:2015-06-25
        设置banner的默认高度
        by:王健 at:2015-07-01
        """
        from nsbcs.models import SysFile
        d = super(SysBanner, self).toJSON()
        d['image_url'] = ''
        if self.image:
            try:
                d['image_url'] = SysFile.objects.get(pk=self.image).get_url('imageView2/5/w/%s/h/%s' % (960, 322))
            except Exception as e:
                d['image_url'] = "http://needserver.duapp.com/static/icon/shigongrizhi3.png"
        return d


class CompanyBanner(JSONBaseModel):
    """
    公司banner 数据
    by:王健 at:2015-06-10
    """
    company = models.ForeignKey(Company, verbose_name=u'隶属公司')
    image = models.IntegerField(default=0, verbose_name=u'公司logo，图片id')
    url = models.CharField(max_length=200, null=True, verbose_name=u'链接地址')
    index_num = models.IntegerField(default=0, verbose_name=u'排序字段')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    def toJSON(self):
        """
        获取公司banner的数据
        by:王健 at:2015-06-22
        输出公司banner的字典
        by:王健 at:2015-06-22
        设置默认测试image_url
        by:王健 at:2015-06-22
        修复image_url bug
        by:王健 at:2015-07-01
        设置banner的默认高度
        by:王健 at:2015-07-01
        """
        from nsbcs.models import ComFile
        d = super(CompanyBanner, self).toJSON()
        d['image_url'] = ''
        if self.image:
            try:
                d['image_url'] = ComFile.objects.get(pk=self.image).get_url('imageView2/5/w/%s/h/%s' % (960, 322))
            except Exception as e:
                d['image_url'] = "http://needserver.duapp.com/static/icon/shigongrizhi3.png"
        return d


class CompanyColumn(JSONBaseModel):
    """
    公司资讯栏目
    by:王健 at:2015-06-10
    修改flag字段长度
    by：尚宗凯 at：2015-06-18
    添加可自定义的新闻栏目类型
    by:王健 at:2015-06-19
    """
    company = models.ForeignKey(Company, verbose_name=u'隶属公司')
    name = models.CharField(max_length=10, verbose_name=u'栏目')
    columntype = models.IntegerField(default=1, verbose_name=u'栏目类型', help_text=u'1为普通型，栏目下可以有很多新闻，0为特殊型，只可以有一个新闻；2为企业咨询，可自定义。')
    index_num = models.IntegerField(default=0, verbose_name=u'排序字段')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    father = models.ForeignKey('CompanyColumn', null=True, verbose_name=u'父级栏目')
    flag = models.CharField(max_length=100, null=True, verbose_name=u'栏目标示')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    image = models.IntegerField(default=0, verbose_name=u'公司栏目图片id')

    def toJSON(self):
        """
        自定义json
        by:王建 at:2015-06-25
        :return:
        """
        d = super(CompanyColumn,self).toJSON()
        d['image_url'] = ''
        if self.image > 0:
            from nsbcs.models import ComFile
            try:
                d['image_url'] = ComFile.objects.get(pk=self.image).get_url()
            except ComFile.DoesNotExist, e:
                pass
        return d

    class Meta:
        """
        添加栏目约束
        by:王健 at:2015-06-19
        """
        unique_together = (('company', 'flag'),)


    @staticmethod
    def init_company_column(company):
        """
        初始化公司的栏目
        by：尚宗凯 at：2015-06-18
        增加企业新闻资讯的栏目
        by:王健 at:2015-06-19
        名字改了
        by：尚宗凯 at：2015-06-24
        增加权限
        by：尚宗凯 at：2015-06-25
        修改了几个栏目
        by：尚宗凯 at：2015-06-25
        领导关怀修改
        by：尚宗凯 at：2015-06-26
        修改核心层介绍为领导介绍
        by:王健 at:2015-06-27
        去掉授权管理
        by：尚宗凯 at：2015-06-30
        """
        c1 = CompanyColumn()
        c1.company = company
        c1.name = u"公司简介"
        c1.columntype = 1
        c1.index_num = 0
        c1.flag = "GONGSIJIANJIE"
        c1.save()

        c11 = CompanyColumn()
        c11.company = company
        c11.name = u"公司介绍"
        c11.columntype = 0
        c11.index_num = 0
        c11.flag = "GONGSIJIESHAO"
        c11.father = c1
        c11.save()

        c12 = CompanyColumn()
        c12.company = company
        c12.name = u"企业荣誉"
        c12.columntype = 1
        c12.index_num = 1
        c12.flag = "QIYERONGYU"
        c12.father = c1
        c12.save()

        c13 = CompanyColumn()
        c13.company = company
        c13.name = u"领导介绍"
        c13.columntype = 1
        c13.index_num = 2
        c13.flag = "HEXINCENGJIESHAO"
        c13.father = c1
        c13.save()

        # c14 = CompanyColumn()
        # c14.company = company
        # c14.name = u"领导关怀"
        # c14.columntype = 1
        # c14.index_num = 3
        # c14.flag = "LINGDAOGUANHUAI"
        # c14.father = c1
        # c14.save()

        c15 = CompanyColumn()
        c15.company = company
        c15.name = u"组织架构"
        c15.columntype = 0
        c15.index_num = 4
        c15.flag = "ZUZHIJIAGOU"
        c15.father = c1
        c15.save()

        c2 = CompanyColumn()
        c2.company = company
        c2.name = u"企业文化"
        c2.columntype = 1
        c2.index_num = 1
        c2.flag = "QIYEWENHUA"
        c2.save()

        c21 = CompanyColumn()
        c21.company = company
        c21.name = u"文化简介"
        c21.columntype = 0
        c21.index_num = 0
        c21.flag = "WENHUAJIANJIE"
        c21.father = c2
        c21.save()

        c22 = CompanyColumn()
        c22.company = company
        c22.name = u"公司活动"
        c22.columntype = 1
        c22.index_num = 1
        c22.flag = "GONGSIHUODONG"
        c22.father = c2
        c22.save()

        c23 = CompanyColumn()
        c23.company = company
        c23.name = u"员工风采"
        c23.columntype = 1
        c23.index_num = 2
        c23.flag = "YUANGONGFENGCAI"
        c23.father = c2
        c23.save()

        c24 = CompanyColumn()
        c24.company = company
        c24.name = u"领导关怀"
        c24.columntype = 1
        c24.index_num = 3
        c24.flag = "LINGDAOGUANHUAI"
        c24.father = c2
        c24.save()

        c3 = CompanyColumn()
        c3.company = company
        c3.name = u"公司业绩"
        c3.columntype = 1
        c3.index_num = 2
        c3.flag = "GONGSIYEJI"
        c3.save()

        c31 = CompanyColumn()
        c31.company = company
        c31.name = u"工程业绩"
        c31.columntype = 1
        c31.index_num = 0
        c31.flag = "GONGCHENGYEJI"
        c31.father = c3
        c31.save()

        c32 = CompanyColumn()
        c32.company = company
        c32.name = u"创优业绩"
        c32.columntype = 1
        c32.index_num = 1
        c32.flag = "CHUANGYOUYEJI"
        c32.father = c3
        c32.save()

        c33 = CompanyColumn()
        c33.company = company
        c33.name = u"在施工程介绍"
        c33.columntype = 1
        c33.index_num = 2
        c33.flag = "ZAISHIGONGCHENGJIESHAO"
        c33.father = c3
        c33.save()

        c4 = CompanyColumn()
        c4.company = company
        c4.name = u"综合管理"
        c4.columntype = 1
        c4.index_num = 3
        c4.flag = "ZONGHEGUANLI"
        c4.save()

        # c41 = CompanyColumn()
        # c41.company = company
        # c41.name = u"授权管理"
        # c41.columntype = 1
        # c41.index_num = 1
        # c41.flag = "SHOUQUANGUANLI"
        # c41.father = c4
        # c41.save()
        # Permission.add_all_permissoin(c41)

        c42 = CompanyColumn()
        c42.company = company
        c42.name = u"文件传达"
        c42.columntype = 1
        c42.index_num = 2
        c42.flag = "WENJIANCHUANDA"
        c42.father = c4
        c42.save()
        Permission.add_all_permissoin(c42)

        c43 = CompanyColumn()
        c43.company = company
        c43.name = u"通知公告"
        c43.columntype = 1
        c43.index_num = 3
        c43.flag = "TONGZHIGONGGAO"
        c43.father = c4
        c43.save()
        Permission.add_all_permissoin(c43)

        c44 = CompanyColumn()
        c44.company = company
        c44.name = u"宣传报道"
        c44.columntype = 1
        c44.index_num = 4
        c44.flag = "XUANCHUANBAODAO"
        c44.father = c4
        c44.save()
        Permission.add_all_permissoin(c44)

        c45 = CompanyColumn()
        c45.company = company
        c45.name = u"技术指导"
        c45.columntype = 1
        c45.index_num = 5
        c45.flag = "JISHUZHIDAO"
        c45.father = c4
        c45.save()
        Permission.add_all_permissoin(c45)

        c46 = CompanyColumn()
        c46.company = company
        c46.name = u"工程管理"
        c46.columntype = 1
        c46.index_num = 6
        c46.flag = "GONGCHENGGUANLI"
        c46.father = c4
        c46.save()
        Permission.add_all_permissoin(c46)

        c47 = CompanyColumn()
        c47.company = company
        c47.name = u"信息发布"
        c47.columntype = 1
        c47.index_num = 7
        c47.flag = "XINXIFABU"
        c47.father = c4
        c47.save()
        Permission.add_all_permissoin(c47)

        c48 = CompanyColumn()
        c48.company = company
        c48.name = u"报审资料"
        c48.columntype = 1
        c48.index_num = 8
        c48.flag = "BAOSHENZILIAO"
        c48.father = c4
        c48.save()
        Permission.add_all_permissoin(c48)

        c5 = CompanyColumn()
        c5.company = company
        c5.name = u"企业资讯"
        c5.columntype = 1
        c5.index_num = 4
        c5.flag = "QIYEZIXUN"
        c5.save()


class CompanyNews(JSONBaseModel):
    """
    公司资讯
    by:王健 at:2015-06-10
    增加数量字段
    by：尚宗凯 at：2015-06-22
    将publish_time变为可为空
    by：尚宗凯 at：2015-06-23
    增加type_flag字段
    by：尚宗凯 at：2015-06-25
    增加文件字段
    by：尚宗凯 at：2015-06-27
    """
    company_column = models.ForeignKey(CompanyColumn, verbose_name=u'所属的栏目')
    company = models.ForeignKey(Company, verbose_name=u'隶属公司')
    pre_title = models.CharField(max_length=100, verbose_name=u'标题', help_text=u'预览版')
    title = models.CharField(max_length=100, verbose_name=u'标题')
    pre_content = models.TextField(verbose_name=u'新闻内容', help_text=u'预览版')
    content = models.TextField(verbose_name=u'新闻内容')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者')
    is_active = models.BooleanField(default=True, verbose_name=u'是否发布')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=u'发布时间',null=True)
    pv = models.IntegerField(default=0, verbose_name=u'page view')
    zan_num = models.IntegerField(default=0, verbose_name=u'赞数量')
    replay_num = models.IntegerField(default=0, verbose_name=u'评论数量')
    type_flag = models.CharField(max_length=30, verbose_name=u'类型 news、files、images', null=True)
    files = models.CommaSeparatedIntegerField(max_length=200, blank=True, null=True, verbose_name=u'文件存储数组')

    def toJSON2(self):
        """
        精简tojson
        by:王健 at:2015-07-01
        :return:
        """
        d = super(CompanyNews, self).toJSON()
        d['news_url'] = 'http://%s/cp/show_phone_news/%s/%s/%s' % (settings.HOST_URL, self.company_id, self.company_column_id, self.pk)
        imglist = []
        import re
        for img in re.findall('(?i)<img[^\'\"]+[\'\"]([^>]+)[\'\"][^\'\"]+/>', self.content):
            imglist.append(img)
        if len(imglist) > 0:
            d['icon_url'] = imglist[0]
        else:
            d['icon_url'] = ''

        # d['icon_url'] = 'http://www.tjeasyshare.com/static/headicon/001.jpg'
        if self.author:
            d['author_name'] = self.author.name
        d['is_sys'] = 'false'
        return d


    def toJSON(self):
        """
        获取赞评论数量
        by:王健 at:2015-06-11
        新闻图片测试版
        by:王健 at:2015-06-16
        修改测试图片地址
        by:尚宗凯 at:2015-06-16
        修改公司新闻的url
        by:王健 at:2015-06-19
        优化公司id
        by:王健 at:2015-06-22
        修复column_id
        by：尚宗凯 at：2015-06-22
        修改新闻阅读数属性
        by:王健 at:2015-06-25
        增加栏目名称
        by:王健 at:2015-06-25
        增加公司名称
        by:王健 at:2015-06-27
        """
        d = self.toJSON2()
        d['column_name'] = self.company_column.name
        d['company_name'] = self.company.name
        return d

    def append_file(self, fileid):
        """
        增加附件
        by：尚宗凯 at：2015-06-27
        """
        if isinstance(self.files, (str, unicode)):
            import json
            self.files = json.loads(self.files)
        elif self.files == None:
            self.files = []
        if int(fileid) not in self.files:
            self.files.append(int(fileid))

    def add_pv(self):
        self.pv += 1
        self.save(update_fields=['pv'])

    def add_zan_num(self, i=1):
        """
        增加减赞数量操作
        by:王健 at:2015-06-25
        """
        self.zan_num += i
        self.save(update_fields=['zan_num'])

    def add_replay_num(self):
        self.replay_num +=1
        self.save(update_fields=['replay_num'])

class SysColumn(JSONBaseModel):
    """
    系统栏目
    by:王健 at:2015-06-10
    修改flag字段长度
    by：尚宗凯 at：2015-06-18
    修复括号
    by:尚宗凯 at：2015-06-26
    """
    name = models.CharField(max_length=10, verbose_name=u'栏目')
    index_num = models.IntegerField(default=0, verbose_name=u'排序字段')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')
    father = models.ForeignKey('CompanyColumn', null=True, verbose_name=u'父级栏目')
    flag = models.CharField(max_length=100, null=True, verbose_name=u'栏目标示')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')


class SysNews(JSONBaseModel):
    """
    系统消息
    by:王健 at:2015-06-10
    发布时间可为空
    by：尚宗凯 at：2015-06-11
    修改toJSON函数
    by:王健 at:2015-06-24
    """
    sys_column = models.ForeignKey(SysColumn, verbose_name=u'所属的栏目')
    company = models.ForeignKey(Company, null=True, verbose_name=u'隶属公司')
    pre_title = models.CharField(max_length=100, verbose_name=u'标题', help_text=u'预览版')
    title = models.CharField(max_length=100, verbose_name=u'标题')
    pre_content = models.TextField(verbose_name=u'新闻内容', help_text=u'预览版')
    content = models.TextField(verbose_name=u'新闻内容')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者')
    is_active = models.BooleanField(default=True, verbose_name=u'是否发布')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name=u'发布时间', null=True)
    pv = models.IntegerField(default=0, verbose_name=u'page view')
    zan_num = models.IntegerField(default=0, verbose_name=u'赞数量')
    replay_num = models.IntegerField(default=0, verbose_name=u'评论数量')

    def toJSON(self):
        """
        获取赞评论数量
        by:王健 at:2015-06-11
        新闻图片 测试版
        by:王健 at:2015-06-16
        新闻的图片，正则过滤出第一个来
        by:王健 at:2015-06-18
        修改阅读数属性名
        by:王健 at:2015-06-25
        增加栏目名称
        by:王健 at:2015-06-25
        """
        d = super(SysNews, self).toJSON()
        d['news_url'] = 'http://%s/cp/show_sys_phone_news/%s/%s' % (settings.HOST_URL, self.sys_column_id, self.pk)
        imglist = []
        import re
        for img in re.findall('(?i)<img[^\'\"]+[\'\"]([^>]+)[\'\"][^\'\"]+/>', self.content):
            imglist.append(img)
        if len(imglist) > 0:
            d['icon_url'] = imglist[0]
        else:
            d['icon_url'] = ''
        if self.author:
            d['author_name'] = self.author.name
        d['is_sys'] = 'true'
        d['column_name'] = self.sys_column.name
        return d

    def add_pv(self):
        self.pv += 1
        self.save()

    def add_zan_num(self, i=1):
        """
        增加减赞数量操作
        by:王健 at:2015-06-25
        """
        self.zan_num += i
        self.save()

    def add_replay_num(self):
        self.replay_num +=1
        self.save()


class CompanyPerson(JSONBaseModel):
    """
    公司和user对应关系
    by：尚宗凯 at：2015-06-10
    修改字段名称
    by：尚宗凯 at：2015-06-11
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    company = models.ForeignKey(Company, verbose_name=u'隶属公司',help_text=u'隶属公司')
    is_active = models.BooleanField(default=True, verbose_name=u'是否在用')
    creator_type = models.IntegerField(default=0, verbose_name=u'身份 0普通成员 1管理员')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'加入的时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')
    powers = models.CommaSeparatedIntegerField(max_length=1000, null=True, verbose_name=u'权限值')
    dispowers = models.CommaSeparatedIntegerField(max_length=1000, null=True, verbose_name=u'权限值')
    replay_timeline = models.IntegerField(default=0, verbose_name=u'评论回复阅读，时间戳')

    class Meta:
        """
        用户和公司的约束
        by:王健 at:2015-06-19
        """
        unique_together = (('company', 'user'),)


class SaveNews(JSONBaseModel):
    """
    用户收藏新闻
    by：尚宗凯 at：2015-06-10
    修改注释
    by：尚宗凯 at：2015-06-22
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    news_id = models.IntegerField(max_length=11, verbose_name=u'收藏的新闻')
    news_type = models.CharField(max_length=30, verbose_name=u'新闻类型 0系统新闻 1用户新闻')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'加入的时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')


class FollowCompany(JSONBaseModel):
    """
    关注公司
    by：尚宗凯 at：2015-06-10
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'账户')
    company = models.ForeignKey(Company, verbose_name=u'关注',help_text=u'关注')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'加入的时间')


class Permission(JSONBaseModel):
    """
    权限设置（栏目是否可见）
    by：尚宗凯 at：2015-06-25
    修改增加权限方法
    by：尚宗凯 at：2015-06-26
    """
    company = models.ForeignKey(Company, verbose_name=u'隶属公司',help_text=u'隶属公司')
    column = models.ForeignKey('CompanyColumn', null=True, verbose_name=u'栏目id')
    group_flag = models.CharField(max_length=100, verbose_name=u'FLAG')
    perm = models.IntegerField(default=0, verbose_name=u'权限 0无权限 1阅读权限 2阅读更新权限')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'加入的时间')
    timeline = models.IntegerField(default=0, db_index=True, verbose_name=u'修改版本，时间戳')

    @staticmethod
    def add_all_permissoin(company_column):
        from needserver.models import Group
        group_flags = [i.type for i in Group.objects.filter(project_id=settings.SHOW_PROJECT_ID)]
        group_flags.append("staff")
        for i in group_flags:
            p = Permission()
            p.company_id = company_column.company.pk
            p.column_id = company_column.pk
            p.create_time = timezone.now()
            p.group_flag = i
            p.perm = 1
            p.save()

    @staticmethod
    def update_perm(company_id, flag, group_flag, perm):
        try:
            cc = CompanyColumn.objects.get(company_id=company_id, flag=flag)
            p = Permission.objects.get(column_id=cc.pk, group_flag=group_flag)
            p.perm = perm
            p.save()
        except Exception as e:
            print e

