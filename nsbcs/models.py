# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import urllib
from qiniu.services.storage import uploader
import requests
from Need_Server import settings
from Need_Server.settings import BCS_HOST, BAE_AK, BAE_SK, QN_AK, QN_SK, QN_FILE_BUCKET_DOMAIN, \
    QN_FRIENDS_ICON_BUCKET_DOMAIN, QN_PROJECT_ICON_BUCKET_DOMAIN, QN_WEBIMAGE_ICON_BUCKET_DOMAIN, \
    QN_COMPANY_ICON_BUCKET_DOMAIN, QN_COMPANY_PRI_ICON_BUCKET_DOMAIN
import qiniu
from util.basemodel import JSONBaseModel

__author__ = u'王健'
from django.db import models
import time
from django.utils import timezone

FILE_BUCKET = 'projectfiles'
FRIENDS_ICON_BUCKET = 'pubfriendsicon'
PROJECT_ICON_BUCKET = 'pubproject'

# 七牛存储
# by: 范俊伟 at:2015-04-08
#增加公司公共文件
# by:王健 at:2015-06-10
QN_FILE_BUCKET = 'qn-projectfiles'
QN_FRIENDS_ICON_BUCKET = 'qn-pubfriendsicon'
QN_PROJECT_ICON_BUCKET = 'qn-pubproject'
QN_WEBIMAGE_ICON_BUCKET = 'qn-webimage'
QN_COMPANY_ICON_BUCKET = 'qn-pubcompany'
QN_COMPANY_PRI_ICON_BUCKET = 'qn-pricompany'
qn_auth = qiniu.Auth(QN_AK, QN_SK)


class BaseFile(JSONBaseModel):
    """
    附件基础类
    by:王健 at:2015-1-28
    添加七牛存储的 bucket
    by:王健 at:2015-3-24
    增加img_size字段
    by: 范俊伟 at:2015-04-09
    编码中文文件名
    by: 范俊伟 at:2015-04-13
    """
    BUCKET = (
    ('projectfiles', u'隐私文件'), ('pubfriendsicon', u'用户头像'), ('pubproject', u'公开文件'), (QN_FILE_BUCKET, u'隐私文件'))
    name = models.CharField(max_length=50, verbose_name=u'附件名称')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    # shareurl = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name=u'文件共享url')
    fileurl = models.CharField(max_length=250, unique=True, verbose_name=u'文件存储位置')
    filetype = models.CharField(max_length=20, verbose_name=u'文件类型')
    size = models.IntegerField(default=0, verbose_name=u'文件大小')
    file_status = models.BooleanField(default=False, verbose_name=u'状态', help_text=u'True 以保存,False 未保存')
    bucket = models.CharField(default=QN_FILE_BUCKET, max_length=20, choices=BUCKET, verbose_name=u'是否开放')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'作者', help_text=u'上传人')
    img_size = models.CharField(max_length=20, null=True, verbose_name=u'图片大小', help_text=u'格式:80x80')

    def get_url(self, fop=None):
        """
        T 取个整数，方便单元测试
        by:王健 at:2015-1-30
        修改 本机头像的 url
        by:王健 at:2015-3-6
        增加七牛云存储
        by: 范俊伟 at:2015-04-08
        七牛云存储增加处理数据功能
        by: 范俊伟 at:2015-04-08
        :return:
        """
        if self.fileurl.find('/static/headicon') == 0:
            return 'http://%s%s' % ('www.tjeasyshare.com', self.fileurl)
        elif self.bucket.startswith('qn-'):
            if self.bucket == QN_FILE_BUCKET:
                url = QN_FILE_BUCKET_DOMAIN + self.fileurl
            elif self.bucket == QN_FRIENDS_ICON_BUCKET:
                url = QN_FRIENDS_ICON_BUCKET_DOMAIN + self.fileurl
            elif self.bucket == QN_PROJECT_ICON_BUCKET:
                url = QN_PROJECT_ICON_BUCKET_DOMAIN + self.fileurl
            elif self.bucket == QN_WEBIMAGE_ICON_BUCKET:
                url = QN_WEBIMAGE_ICON_BUCKET_DOMAIN + self.fileurl
            elif self.bucket == QN_COMPANY_ICON_BUCKET:
                url = QN_COMPANY_ICON_BUCKET_DOMAIN + self.fileurl
            elif self.bucket == QN_COMPANY_PRI_ICON_BUCKET:
                url = QN_COMPANY_PRI_ICON_BUCKET_DOMAIN + self.fileurl
            else:
                raise Exception(self.bucket + ':未知的bucket')
            params = []
            if fop:
                params.append(fop)

            params.append("attname=" + urllib.quote(self.name.encode('utf-8')))
            url = url + '?' + '&'.join(params)
            if self.bucket == QN_FILE_BUCKET:
                url = qn_auth.private_download_url(url, expires=3600)
            return url

        else:
            if self.bucket == FILE_BUCKET:
                # return bcs.sign('GET', self.bucket, self.fileurl, T=int(int((time.time()) / 1000) * 1000 + 3600))
                pass
            else:
                return '%s/%s%s' % (BCS_HOST, self.bucket, self.fileurl)

    def get_post_url(self):
        """
        T 取个整数，方便单元测试
        by:王健 at:2015-1-30
        通过服务器转到七牛云存储
        by: 范俊伟 at:2015-04-14
        修改 获取url的函数，无需参数
        by: 王健 at:2015-04-14
        :return:
        """
        # host = request.META.get('HTTP_HOST', '')
        url = u"http://%s/nf/%s/upload_files" % (settings.HOST_URL, self.id)
        return url

    def get_qn_post_url(self):
        """
        获取七牛post url
        by: 范俊伟 at:2015-04-08
        :return:
        """
        return 'http://upload.qiniu.com/'

    def get_qn_params(self):
        """
        获取七牛post 参数
        by: 范俊伟 at:2015-04-08
        :return:
        """
        token = qn_auth.upload_token(self.bucket, expires=3600 * 24)
        params = {'token': token, 'key': self.fileurl}
        return params

    def get_put_url(self):
        """
        T 取个整数，方便单元测试
        by:王健 at:2015-1-30
        通过服务器转到七牛云存储
        by: 范俊伟 at:2015-04-14
        修改 获取url的函数，无需参数
        by: 王健 at:2015-04-14
        :return:
        """
        # host = request.META.get('HTTP_HOST', '')
        url = u"http://%s/nf/%s/put_file" % (settings.HOST_URL, self.id)
        return url

    def delete(self, using=None):
        # try:
        #     bucket = bcs.bucket(self.bucket)
        #     o1 = bucket.object(self.fileurl)
        #     result = o1.delete()
        # except:
        #     pass
        #todo:改为使用七牛删
        super(BaseFile, self).delete(using)

    def putdata(self, data):
        """
        把文件推送到bcs
        by:王健 at:2015-1-28
        把文件推送到七牛
        by: 范俊伟 at:2015-04-14
        :param data:
        :return:
        """
        key = self.fileurl
        token = qn_auth.upload_token(self.bucket, expires=3600 * 24)
        ret, info = uploader.put_data(token, key, data, check_crc=True)
        return ret['key'] == key


    def check_file(self):
        """
        检查文件是否在bcs上
        by:王健 at:2015-1-26
        修改dic读取错误
        by:范俊伟 at:2015-01-26
        :return:
        """
        # try:
        #     bucket = bcs.bucket(self.bucket)
        #     o1 = bucket.object(self.fileurl)
        #     # o1 = bucket.object('/1/a74d49a7-e050-400c-8ad3-fb6c7a4aef64.bmp')
        #     result = o1.head()
        #     if result.get('status') == 200:
        #         return True
        #     return False
        # except:
        #     return False
        #todo:改为使用七牛
        return True

    def save(self, *args, **kwargs):
        """
        重载save函数,获取图片分辨率
        by: 范俊伟 at:2015-04-09
        """
        from util.tools import common_except_log
        if self.file_status and self.img_size == None and self.bucket.startswith('qn-'):
            try:
                url = self.get_url('imageInfo')
                response = requests.get(url)
                data = response.json()
                error=data.get('error')
                if error and error.find('unsupported format')!=-1:
                    self.img_size='0x0'
                else:
                    width = data.get('width')
                    height = data.get('height')
                    if width and height:
                        self.img_size = '%dx%d' % (width, height)
            except:
                common_except_log()

        return super(BaseFile, self).save(*args, **kwargs)


class File(BaseFile):
    """
    附件
    by:王健 at:2015-1-10
    避免嵌套import问题，在class中再import
    by:王健 at:2015-1-11
    增加put上传接口
    by:王健 at:2015-1-14
    post 去掉 size的签名
    by:王健 at:2015-1-26
    """
    project = models.ForeignKey('needserver.Project', verbose_name=u'隶属项目', help_text=u'隶属项目')


class ComFile(BaseFile):
    """
    公司相关的附件
    by:王健 at:2015-06-09
    """
    company = models.ForeignKey('company.Company', verbose_name=u'隶属公司', help_text=u'隶属公司')


class SysFile(BaseFile):
    """
    系统相关的附件，新闻图片等……
    by:王健 at:2015-06-14
    """
    is_sys = models.BooleanField(default=True, verbose_name=u'是否系统图片')