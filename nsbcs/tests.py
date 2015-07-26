# coding=utf-8
#Date:2015/1/10
#Email:wangjian2254@gmail.com
import json
import os
from django.conf import settings
from django.contrib.auth import get_user_model
import requests

from needserver.models import Project
from nsbcs.models import File
from util.jsonresult import getTestResult, MyEncoder


__author__ = u'王健'

from django.test import TestCase

username = '18622231518'
truename = u'测试用户1'


class RegUserTest(TestCase):
    """
    bcs 文件上传 接口单元测试
    by:王健 at:2015-1-10
    """

    def setUp(self):
        """
        所有单元测试前的 基础设置，注册用户、创建项目
        by:王健 at:2015-1-10
        增加了smsdebug 参数，方便测试
        by:王健 at:2015-1-15
        修改个人信息返回值
        by:王健 at:2015-1-20
        :return:
        """
        # 注册新用户
        newuserdata = {"password": '123456', 'tel': username,
                       'name': truename, 'smsdebug': 'sdf' }
        response = self.client.post('/ns/reg_user', newuserdata)

        self.assertEqual(200, response.status_code, u'注册新用户报错')
        user = get_user_model().objects.get(tel=username)
        self.assertJSONEqual(response.content, getTestResult(True, u'注册成功', user.get_user_map(True)), u'注册新用户，返回结果有变化，需要确认，或修改单元测试')

        # 创建项目
        newuserdata = {"name": u'测试项目1', 'total_name': u'单元测试创建的项目',  'jzmj': 300, 'jglx': u'钢结构',
                       'jzcs': 3, 'htzj': 340000, 'kg_date': '2015-12-01', 'days': 50, 'address': 1,
                       'jsdw': u'水水水水是建设六局',  'jsdw_fzr': u'小刘', 'jsdw_fzr_tel': '18632234548',
                       'kcdw': u'勘察第一分院', 'kcdw_fzr': u'喜洋洋', 'kcdw_fzr_tel': '321313',
                       'sjdw': u'设计第二院', 'sjdw_fzr': u'灰太狼', 'sjdw_fzr_tel': '5455',
                       'sgdw': u'施工第三局', 'sgdw_fzr': u'美羊羊', 'sgdw_fzr_tel': '741165',
                       'jldw': u'监理第二单位', 'jldw_fzr': u'村长', 'jldw_fzr_tel': '7881131',
        }
        response = self.client.post('/ns/reg_project', newuserdata)


        self.assertEqual(200, response.status_code, u'注册新用户报错')
        project = Project.objects.filter(manager=user)[0]
        self.assertJSONEqual(response.content, getTestResult(True, u'成功创建：%s' % project.total_name, MyEncoder.default(project)), u'创建项目，返回结果有变化，需要确认，或修改单元测试')


    def login(self, username, password):
        """
        登录 接口测试
        by:王健 at:2015-1-5
        username 改为tel字段
        by:王健 at:2015-1-8
        返回值 修改
        by:王健 at:2015-1-16
        修改个人信息返回值
        by:王健 at:2015-1-20
        """
        # 登录
        login_response = self.client.post('/ns/login', {'tel': username, 'password': password})
        self.assertEqual(200, login_response.status_code, u'用户登录报错')
        user = get_user_model().objects.get(tel=username)

        self.assertJSONEqual(login_response.content,
                             getTestResult(True, u'登录成功', user.get_user_map(True)),
                             u'用户登录，返回结果有变化，需要确认，或修改单元测试')

    def logout(self):
        """
        登出接口测试
        by:王健 at:2015-1-10
        :return:
        """
        # 登录
        login_response = self.client.post('/ns/logout')
        self.assertEqual(200, login_response.status_code, u'用户登录报错')

    def get_upload_files_url(self, project_id):
        """
        获取附件上传的url
        by:王健 at:2015-1-10
        获取上传文件的url，结果校验
        by:王健 at:2015-1-12
        优化了获取文件上传url签名的接口
        by:王健 at:2015-1-14
        :return:
        """
        # 登录组织
        login_response = self.client.post('/nf/%s/get_upload_files_url' % project_id, {'filename': u'沙发上地方的说法', 'size': 30*1024, 'filetype': 'image'})
        self.assertEqual(200, login_response.status_code, u'获取附件上传的url 错误')
        fileobj = File.objects.all()[0]
        self.assertJSONEqual(login_response.content, getTestResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_post_url(), 'puturl': fileobj.get_put_url()}),
                             u'获取附件上传的url，返回结果有变化，需要确认，或修改单元测试')

    def get_qn_upload_files_url(self, project_id):
        """
        七牛,获取附件上传的url
        by:范俊伟 at:2015-4-8
        :return:
        """
        response = self.client.post('/nf/%s/get_qn_upload_files_url' % project_id, {'filename': u'沙发上地方的说法', 'size': 30*1024, 'filetype': 'image'})
        self.assertEqual(200, response.status_code, u'获取附件上传的url 错误')
        fileobj = File.objects.all()[1]
        self.assertJSONEqual(response.content, getTestResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()}),
                             u'七牛,获取附件上传的url，返回结果有变化，需要确认，或修改单元测试')

    def confirm_upload_files(self, project_id, fileid):
        """
        设置文件为上传成功状态 测试
        by:王健 at:2015-1-10
        增加图片原始图片大小参数
        by: 范俊伟 at:2015-04-09
        :return:
        """
        # 我关注的项目列表
        login_response = self.client.post('/nf/%s/confirm_upload_files' % project_id, {'fileid': fileid})
        self.assertEqual(200, login_response.status_code, u'设置文件为上传成功状态 错误')
        fileobj = File.objects.get(pk=fileid)
        self.assertJSONEqual(login_response.content, getTestResult(True, u'上传文件成功', {'geturl': fileobj.get_url()}),
                             u'设置文件为上传成功状态，返回结果有变化，需要确认，或修改单元测试')

    def get_url_by_file(self, project_id, fileid):
        """
        获取文件下载url 测试
        by:王健 at:2015-1-12
        :return:
        """
        # 我关注的项目列表
        login_response = self.client.post('/nf/%s/get_url_by_file' % project_id, {'fileid': fileid})
        self.assertEqual(200, login_response.status_code, u'获取文件下载url 错误')
        fileobj = File.objects.get(pk=fileid)
        self.assertJSONEqual(login_response.content, getTestResult(True, u'', {'id': fileobj.id, 'geturl': fileobj.get_url(), 'name': fileobj.name, 'filetype': fileobj.filetype, 'size': fileobj.size, 'img_size':fileobj.img_size}),
                             u'获取文件下载url，返回结果有变化，需要确认，或修改单元测试')


    def check_file_upload_status(self, project_id, fileid):
        """
        根据fileid 检查文件是否已在bcs上
        by:王健 at:2015-1-12
        修改判断条件
        by:王健 at:2015-1-27
        :return:
        """
        # 我关注的项目列表
        login_response = self.client.post('/nf/%s/check_file_upload_status' % project_id, {'fileid': fileid})
        self.assertEqual(200, login_response.status_code, u'获取文件下载url 错误')
        self.assertJSONEqual(login_response.content, getTestResult(True, u'', False),
                             u'获取文件下载url，返回结果有变化，需要确认，或修改单元测试')

    def test_join_org(self):
        """
        按照登录、获取用户信息、登出的顺序测试
        获取文件上传url
        by:王健 at:2015-1-10
        使用本单例测试创建的项目作为查询参数
        by:王健 at:2015-1-21
        bcs上文件检查
        by:王健 at:2015-1-26
        :return:
        """
        # 加入组织

        self.login(username, '123456')
        project = Project.objects.filter(manager__tel=username)[0]
        self.get_upload_files_url(project.pk)
        self.get_qn_upload_files_url(project.pk)
        fileobj = File.objects.all()[0]
        self.confirm_upload_files(project.pk, fileobj.pk)
        self.get_url_by_file(project.pk, fileobj.pk)
        # self.check_file_upload_status(project.pk, fileobj.pk)
        self.logout()


    # def test_upload_download(self):
    #     '''
    #     文件上传,检测,下载综合测试
    #     by:范俊伟 at:2015-1-28
    #     :return:
    #     '''
    #     # 初始化操作
    #     self.login(username, '123456')
    #     test_content = 'test_sdfjlsdkjdskfkljd_xxxxxx'
    #     test_file_path = os.path.join(settings.STATIC_ROOT, 'test.txt')
    #     file = open(test_file_path, 'w')
    #     file.write(test_content)
    #     file.close()
    #     project = Project.objects.filter(manager__tel=username)[0]
    #
    #     # 获取上传地址
    #     response = self.client.post('/nf/%s/get_upload_files_url' % project.pk,
    #                                 {'filename': u'test.txt', 'filetype': 'txt'})
    #     self.assertEqual(200, response.status_code, u'获取文件下载url 错误--1')
    #     data = json.loads(response.content)
    #     self.assertTrue(data.get('success'), '获取文件下载url 错误--2')
    #     posturl = data.get('result').get('posturl')
    #     print posturl
    #     fileid = data.get('result').get('fileid')
    #     file = open(test_file_path, 'rb')
    #
    #     # 通过django为桥梁上传到bcs
    #     response = self.client.post('/nf/%s/upload_files' % project.pk,
    #                                 {'fileid': fileid, 'file': file})
    #     file.close()
    #     self.assertEqual(200, response.status_code, u'上传文件错误--1')
    #     data = json.loads(response.content)
    #     self.assertTrue(data.get('success'), '上传文件错误--2')
    #     self.assertTrue(data.get('result'), '上传文件错误--3')
    #
    #     # 检测上传是否成功
    #     response = self.client.post('/nf/%s/check_file_upload_status' % project.pk,
    #                                 {'fileid': fileid})
    #     self.assertEqual(200, response.status_code, u'文件检测错误--1')
    #     data = json.loads(response.content)
    #     self.assertTrue(data.get('success'), '文件检测错误--2')
    #     self.assertTrue(data.get('result'), '文件检测错误--3')
    #
    #     # 获取下载url
    #     response = self.client.post('/nf/%s/get_url_by_file' % project.pk,
    #                                 {'fileid': fileid})
    #     self.assertEqual(200, response.status_code, u'获取下载url错误--1')
    #     data = json.loads(response.content)
    #     self.assertTrue(data.get('success'), '获取下载url错误--2')
    #     geturl = data.get('result').get('geturl')
    #     print geturl
    #
    #     # 下载文件
    #     response = requests.get(geturl)
    #     self.assertEqual(200, response.status_code, u'下载文件错误--1')
    #     download_content = response.content
    #     self.assertEqual(download_content, test_content, u'下载文件错误--2')
    #
    #     #删除测试文件
    #     os.remove(test_file_path)
