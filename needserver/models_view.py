# coding=utf-8

__author__ = u'尚宗凯'

from django.db import models
from util.basemodel import JSONBaseModel

class VNSUser(JSONBaseModel):
    '''
    用户视图
    by:尚宗凯 at:2015-3-6
    '''
    user_id = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text=u'手机号')
    name = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=30, blank=True, verbose_name=u'昵称', help_text=u'昵称')
    sex = models.NullBooleanField(blank=True, null=True, verbose_name=u'性别')
    icon_url_id = models.IntegerField(blank=True, null=True,verbose_name=u'默认头像')
    is_staff = models.BooleanField(blank=True)
    is_active = models.BooleanField(blank=True)
    create_time = models.DateTimeField(blank=True, null=True)
    hxpassword = models.CharField(max_length=50, verbose_name=u'环信密码')
    hx_reg = models.BooleanField(blank=True)

    USERNAME_FIELD = 'tel'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return unicode(self.name)

class VNSUseruUserInfoPersonBaseFile(JSONBaseModel):
    '''
    NSUseruUserInfoPersonBaseFile视图
    by:尚宗凯 at:2015-3-6
    修正字段重复bug
    by:尚宗凯 at:2015-3-7
    '''
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text=u'手机号')
    name = models.CharField(max_length=30, blank=True)
    nickname = models.CharField(max_length=30, blank=True, verbose_name=u'昵称', help_text=u'昵称')
    sex = models.NullBooleanField(blank=True, null=True, verbose_name=u'性别')
    is_staff = models.BooleanField(blank=True)
    nsuser_is_active = models.BooleanField(blank=True)
    hxpassword = models.CharField(max_length=50, verbose_name=u'环信密码')
    hx_reg = models.BooleanField(blank=True)
    nsuser_craete_time = models.DateTimeField(blank=True, null=True)

    basefile_name = models.CharField(max_length=50, verbose_name=u'附件名称', blank=True, null=True)
    fileurl = models.CharField(max_length=250, verbose_name=u'文件存储位置', blank=True, null=True)
    filetype = models.CharField(max_length=20, verbose_name=u'文件类型', blank=True, null=True)
    size = models.IntegerField(default=0, verbose_name=u'文件大小')
    file_status = models.BooleanField(default=False, verbose_name=u'状态', help_text=u'True 以保存,False 未保存')
    bucket = models.CharField(max_length=20, verbose_name=u'是否开放', blank=True, null=True)
    basefile_create_time = models.DateTimeField(blank=True, null=True)

    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    address = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'籍贯', help_text=u'3.2日决定改为籍贯')
    xueli = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'最高学历')
    zhicheng = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'职称')
    zhiyezigezheng = models.CharField(max_length=100, blank=True, null=True ,verbose_name=u'职业资格证')
    company = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'所在公司名称')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'职务', help_text=u'职务')
    department = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'部门', help_text=u'任职部门')
    email = models.EmailField(blank=True, null=True, verbose_name=u'电子邮件')
    qq = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'qq', help_text=u'qq号')

    project_id = models.IntegerField(blank=True, null=True,)
    person_is_active = models.BooleanField(default=True,verbose_name=u'是否在用')
    timeline = models.IntegerField(default=0, blank=True, null=True, verbose_name=u'修改版本，时间戳')
    person_create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_needserver_nsuser_userinfo_person_basefile'





