# coding=utf-8
# Date:2015/1/10
# Email:wangjian2254@gmail.com
__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('nsbcs',
                        #url添加$结束符
                        #by:王健 at:2015-1-21
                       url(r'^(?P<project_id>\d+)/get_upload_files_url$', 'views_bcsfile.get_upload_files_url'),

                        #上传集团文件接口
                        #by：尚宗凯 at：2015-06-16
                       # url(r'^(?P<big_company_id>\d+)/get_company_qn_upload_files_url', 'views_bcsfile.get_company_qn_upload_files_url'),
                       url(r'^get_bigcompany_qn_upload_files_url$', 'views_bcsfile.get_bigcompany_qn_upload_files_url'),
                        #集团文件检查
                        #by：尚宗凯 at：2015-06-16
                       url(r'^check_bigcompany_file_upload_status$', 'views_bcsfile.check_bigcompany_file_upload_status'),
                        #获取集团附件url
                        #by：尚宗凯 at：2015-06-16
                       url(r'^get_bigcompany_url_by_file$', 'views_bcsfile.get_bigcompany_url_by_file'),
                        #上传公司文件接口
                        #by：尚宗凯 at：2015-06-16
                       url(r'^(?P<company_id>\d+)/get_company_qn_upload_files_url$', 'views_bcsfile.get_company_qn_upload_files_url'),
                        #公司文件检查
                        #by：尚宗凯 at：2015-06-16
                       url(r'^check_company_file_upload_status$', 'views_bcsfile.check_company_file_upload_status'),
                        #获取公司附件url
                        #by：尚宗凯 at：2015-06-16
                       url(r'^get_company_url_by_file$', 'views_bcsfile.get_company_url_by_file'),


                        # 七牛云存储获取上传地址
                        # by: 范俊伟 at:2015-04-08
                       url(r'^(?P<project_id>\d+)/get_qn_upload_files_url$', 'views_bcsfile.get_qn_upload_files_url'),

                       url(r'^(?P<project_id>\d+)/confirm_upload_files$', 'views_bcsfile.confirm_upload_files'),
                       url(r'^(?P<project_id>\d+)/get_url_by_file$', 'views_bcsfile.get_url_by_file'),
                        #检查文件是否在bcs中
                        #by:王健 at:2015-1-26
                       url(r'^(?P<project_id>\d+)/check_file_upload_status$', 'views_bcsfile.check_file_upload_status'),
                        #文件上传接口
                        #by:王健 at:2015-1-68
                        # 服务器post和put中转到七牛接口
                        # by: 范俊伟 at:2015-04-14
                       url(r'^(?P<file_id>\d+)/upload_files$', 'views_bcsfile.upload_files'),
                       url(r'^(?P<file_id>\d+)/put_file$', 'views_bcsfile.put_file'),
                        #上传系统banner接口
                        #by：尚宗凯 at：2015-06-23
                        url(r'^get_sys_banner_qn_upload_files_url$', 'views_bcsfile.get_sys_banner_qn_upload_files_url'),
                        #系统banner文件检查
                        #by：尚宗凯 at：2015-06-16
                       url(r'^check_sys_banner_file_upload_status$', 'views_bcsfile.check_bigcompany_file_upload_status'),
                        #获取集团附件url
                        #by：尚宗凯 at：2015-06-16
                       url(r'^get_sys_banner_url_by_file$', 'views_bcsfile.get_bigcompany_url_by_file'),


)