# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
__author__ = u'王健'

from django.conf.urls import patterns, url

#url添加$结束符
#by:王健 at:2015-1-21
urlpatterns = patterns('needserver',
                       url(r'^login$', 'views_user.login'),
                       url(r'^logout$', 'views_user.logout'),
                       #发送手机校验码
                       #by:王健 at:2015-01-14
                       url(r'^send_sms_code$', 'views_user.send_sms_code'),
                       url(r'^reg_user$', 'views_user.reg_user'),
                       url(r'^submit_user_tel$', 'views_user.submit_user_tel'),
                       url(r'^change_password$', 'views_user.change_password'),
                       #重置密码
                       #by:尚宗凯 at:2015-05-05
                       url(r'^forget_password$', 'views_user.forget_password'),
                       #强制重置密码
                       #by:尚宗凯 at:2015-05-14
                       url(r'^enforce_reset_password', 'views_user.enforce_reset_password'),
                       url(r'^update_userinfo$', 'views_user.update_userinfo'),
                       url(r'^(?P<project_id>\d+)/get_userinfo$', 'views_user.get_userinfo'),
                       url(r'^current_user$', 'views_user.current_user'),

                       #获取用户头像上传接口，和 更新用户头像接口
                       url(r'^get_upload_user_icon_url$', 'views_user.get_upload_user_icon_url'),
                       url(r'^update_user_icon_url$', 'views_user.update_user_icon_url'),

                       # 七牛云存储,获取用户头像上传接口
                       # by: 范俊伟 at:2015-04-08
                       url(r'^get_qn_upload_user_icon_url$', 'views_user.get_qn_upload_user_icon_url'),
                       # 公司创建项目
                       # by:尚宗凯 at：2015-06-29
                       url(r'^reg_project_by_company$', 'views_project.reg_project_by_company'),
                       url(r'^reg_project$', 'views_project.reg_project'),
                       #修改项目
                       #by:王健 at:2015-2-3
                       url(r'^(?P<project_id>\d+)/update_project$', 'views_project.update_project'),
                       #关注项目
                       #by:王健 at:2015-1-30
                       url(r'^guanzhu_project$', 'views_user.guanzhu_project'),
                       #获取上传项目图标的url
                       #by:王健 at:2015-1-28
                       url(r'^(?P<project_id>\d+)/get_upload_project_icon_url$', 'views_project.get_upload_project_icon_url'),
                       # 七牛云存储,获取上传项目图标的url
                       # by: 范俊伟 at:2015-04-08
                       url(r'^(?P<project_id>\d+)/get_qn_upload_project_icon_url$', 'views_project.get_qn_upload_project_icon_url'),
                        #更新项目图标
                       #by:王健 at:2015-1-29
                       url(r'^(?P<project_id>\d+)/update_project_icon_url$', 'views_project.update_project_icon_url'),
                       url(r'^(?P<project_id>\d+)/get_all_applyproject$', 'views_project.get_all_applyproject'),
                       url(r'^(?P<project_id>\d+)/change_applyproject$', 'views_project.change_applyproject'),
                       #增加获取用户详细信息接口
                       #by：尚宗凯 at：2015-05-11
                       url(r'^(?P<project_id>\d+)/get_applyproject_user_infomation', 'views_project.get_applyproject_user_infomation'),
                       #离开项目，和删除成员接口
                       #by:王健 at:2015-1-30
                       url(r'^(?P<project_id>\d+)/leave_project$', 'views_project.leave_project'),
                       url(r'^(?P<project_id>\d+)/remove_person$', 'views_project.remove_person'),
                       #修改人员隶属的群组
                       #by:王健 at:2015-2-6
                       url(r'^(?P<project_id>\d+)/change_user_group$', 'views_user.change_user_group'),
                       #增加一个my_project2
                       #by:尚宗凯 at：2015-05-07
                       url(r'^my_project$', 'views_project.my_project'),
                       url(r'^my_project2$', 'views_project.my_project2'),
                       url(r'^query_project$', 'views_project.query_project'),

                       #增加查询相似项目名接口
                       #by:王健 at:2015-03-4
                       url(r'^query_project_name$', 'views_project.query_project_name'),
                        #增加get_project接口,通过project_id获取项目详情
                        #by:范俊伟 at:2015-01-22
                       url(r'^get_project$', 'views_project.get_project'),

                        #增加示例项目获取接口
                       #by:王健 at:2015-3-25
                       url(r'^get_show_project$', 'views_project.get_show_project'),
                       # url(r'^query_project_by_key$', 'views_project.query_project_by_key'),

                       #申请加入工程
                       url(r'^(?P<project_id>\d+)/apply_project$', 'views_project.apply_project'),
                       #根据手机端上传的手机号，加入项目成员
                       #by:王健 at:2015-2-25
                       #使用新版通过手机号加人
                       #by:王健 at:2015-3-10
                       url(r'^(?P<project_id>\d+)/add_person_by_tel$', 'views_project.add_person_by_tel3'),
                       #注掉这一行
                       #by:尚宗凯 at:2015-4-3
                       # url(r'^guest_app_url$', 'views_project.guest_app_url'),
                       #获取所有成员、群组
                       #by:王健 at:2015-1-16
                       url(r'^(?P<project_id>\d+)/query_person$', 'views_user.query_person'),
                       url(r'^(?P<project_id>\d+)/query_group$', 'views_user.query_group'),

                       #工程日志

                       url(r'^(?P<project_id>\d+)/query_log_date_list$', 'views_sglog.query_log_date_list'),
                       #添加查询旧数据
                       #by:王健 at:2015-01-08
                       url(r'^(?P<project_id>\d+)/query_log_date_list_old$', 'views_sglog.query_log_date_list_old'),
                       url(r'^(?P<project_id>\d+)/query_log_list_by_date$', 'views_sglog.query_log_list_by_date'),
                       url(r'^(?P<project_id>\d+)/update_log_by_date$', 'views_sglog.update_log_by_date'),
                       #删除日志
                       #by:王健 at:2015-2-10
                       url(r'^(?P<project_id>\d+)/del_log_by_id$', 'views_sglog.del_log_by_id'),
                       #工程检查
                       #by:王健 at:2015-01-13
                       url(r'^(?P<project_id>\d+)/query_enginecheck_by_group$', 'views_gcjc.query_enginecheck_by_group'),
                       url(r'^(?P<project_id>\d+)/query_enginecheck_by_group_old$', 'views_gcjc.query_enginecheck_by_group_old'),
                       url(r'^(?P<project_id>\d+)/create_enginecheck_by_group$', 'views_gcjc.create_enginecheck_by_group'),
                       url(r'^(?P<project_id>\d+)/update_enginecheck_by_group$', 'views_gcjc.update_enginecheck_by_group'),
                       # 删除工程检查
                       #by:尚宗凯 at:2015-03-30
                       url(r'^(?P<project_id>\d+)/delete_enginecheck_by_enginecheck_id$', 'views_gcjc.delete_enginecheck_by_enginecheck_id'),

                       #物资管理
                       #by:王健 at:2015-01-14
                       url(r'^(?P<project_id>\d+)/query_gysaddress_by_group$', 'views_wzgl.query_gysaddress_by_group'),
                       url(r'^(?P<project_id>\d+)/query_gysaddress_by_group_old$', 'views_wzgl.query_gysaddress_by_group_old'),
                       url(r'^(?P<project_id>\d+)/create_gysaddress_by_group$', 'views_wzgl.create_gysaddress_by_group'),

                       url(r'^(?P<project_id>\d+)/query_wuzirecord_by_group$', 'views_wzgl.query_wuzirecord_by_group'),
                       # url(r'^(?P<project_id>\d+)/query_wuzirecord_by_group_old$', 'views_wzgl.query_wuzirecord_by_group_old'),
                       url(r'^(?P<project_id>\d+)/create_wuzirecord_by_group$', 'views_wzgl.create_wuzirecord_by_group'),
                       #删除物资记录
                       #by:王健 at:2015-2-10
                       url(r'^(?P<project_id>\d+)/del_wuzirecord_by_id$', 'views_wzgl.del_wuzirecord_by_id'),
                       #删除供应商地址
                       #by:尚宗凯 at:2015-3-26
                       #加$
                       #by:尚宗凯 at:2015-3-27
                       url(r'^(?P<project_id>\d+)/del_gysaddress_by_id$', 'views_wzgl.del_gysaddress_by_id'),

                        #查询记录日期的新数据和旧数据的接口
                       #by:王健 at:2015-01-14
                       url(r'^(?P<project_id>\d+)/query_record_date_by_group$', 'views_wzgl.query_record_date_by_group'),
                       url(r'^(?P<project_id>\d+)/query_record_date_by_group_old$', 'views_wzgl.query_record_date_by_group_old'),


                       #应用模块
                       #by:王健 at:2015-01-12
                       url(r'^(?P<project_id>\d+)/query_app_list$', 'views_app.query_app_list'),
                       url(r'^(?P<project_id>\d+)/create_file_by_group$', 'views_app.create_file_by_group'),
                       #追加新照片或新文档
                       #by:王健 at:2015-1-31
                       url(r'^(?P<project_id>\d+)/append_file_by_group$', 'views_app.create_file_by_group'),
                       url(r'^(?P<project_id>\d+)/query_file_by_group$', 'views_app.query_file_by_group'),
                       url(r'^(?P<project_id>\d+)/query_file_by_group_old$', 'views_app.query_file_by_group_old'),
                       #删除上传的文件信息
                       #by:尚宗凯 at:2015-3-27
                       url(r'^(?P<project_id>\d+)/delete_file_by_filerecord_id$', 'views_app.delete_file_by_filerecord_id'),

                       #社会化登陆，分web端和手机端
                       #by:王健 at:2015-01-12
                       # 社会化登陆，绑定账号
                       #by:王健 at:2015-01-16
                       url(r'^get_user_social_list$', 'views_social.get_user_social_list'),
                       url(r'^client_social_callback$', 'views_social.client_social_callback'),
                       #社会化登陆，结果页，方便手机端跳转
                       #by:王健 at:2015-01-25
                       url(r'^client_social_result$', 'views_social.client_social_result'),
                       url(r'^client_add_social_callback$', 'views_social.client_add_social_callback'),
                       url(r'^web_social_callback$', 'views_social.web_social_callback'),
                       url(r'^web_add_social_callback$', 'views_social.web_add_social_callback'),

                       #成功发送分享，调用此接口，可以获得积分
                       #by:王健 at:2015-2-5
                       url(r'^send_social_success$', 'views_social.send_social_success'),

                       #查询我的积分
                       #by:王健 at:2015-2-6
                       url(r'^query_my_jifen$', 'views_user.query_my_jifen'),

                       #根据城市id获取天气
                       #by:王健 at:2015-2-6
                       url(r'^get_today_weather$', 'views_weather.get_today_weather'),

                       #顶、评论
                       #by:王健 at:2015-2-25
                       #评论新接口
                       # by:王健 at:2015-05-28
                       url(r'^(?P<project_id>\d+)/ding_filerecord_by_id$', 'views_replay.ding_filerecord_by_id'),
                       url(r'^(?P<project_id>\d+)/delete_ding_filerecord_by_id$', 'views_replay.delete_ding_filerecord_by_id'),
                       url(r'^(?P<project_id>\d+)/replay_filerecord_by_id$', 'views_replay.replay_filerecord_by_id'),
                       url(r'^(?P<project_id>\d+)/query_replay_filerecord_by_id$', 'views_replay.query_replay_filerecord_by_id'),
                       url(r'^(?P<project_id>\d+)/query_replay_filerecord_by_timeline$', 'views_replay.query_replay_filerecord_by_timeline'),
                       url(r'^(?P<project_id>\d+)/count_replay_filerecord_by_timeline$', 'views_replay.count_replay_filerecord_by_timeline'),

                        #系统消息、项目组公告
                       #by:王健 at:2015-2-26
                       url(r'create_sysmessage$', 'views_message.create_sysmessage'),
                       url(r'^(?P<project_id>\d+)/query_sysmessage$', 'views_message.query_sysmessage'),
                       url(r'^(?P<project_id>\d+)/query_sysmessage_old$', 'views_message.query_sysmessage_old'),
                       url(r'^(?P<project_id>\d+)/create_project_message$', 'views_message.create_project_message'),
                       url(r'^(?P<project_id>\d+)/query_project_message$', 'views_message.query_project_message'),
                       url(r'^(?P<project_id>\d+)/query_project_message_old$', 'views_message.query_project_message_old'),

                        #用户消息
                        #by:尚宗凯 at：2015-03-31
                        #修改函数名
                        #by:尚宗凯 at：2015-04-01
                        #增加用户need消息读取时间
                       url(r'create_needmessage$', 'views_message.create_needmessage'),
                       url(r'query_need_message$', 'views_message.query_need_message'),
                       url(r'^read_needmessage$', 'views_message.read_needmessage'),

                       #获取项目的余额信息
                       #by:王健 at:2015-3-2
                       url(r'^(?P<project_id>\d+)/get_project_balance$', 'views_project.get_project_balance'),

                       #自动扣款接口
                       #by:王健 at:2015-3-10
                       #弃用
                       #by:王健 at:2015-3-15
                       # url(r'auto_price$', 'views_price.auto_price'),
                       #报停功能
                        #by:王健 at:2015-3-15
                       url(r'^(?P<project_id>\d+)/set_project_baoting$', 'views_project.set_project_baoting'),
                       #删除项目
                       #by:尚宗凯 at:2015-3-18
                       # url(r'^(?P<project_id>\d+)/delete_project$', 'views_project.delete_project'),

                       #初始化密码
                       #by:王健 at:2015-3-20
                       url(r'^admin_init_password$', 'views_admin.admin_init_password'),

                        #修改新的权限接口
                       #by:王健 at:2015-5-7
                       url(r'^(?P<project_id>\d+)/change_power_by_group$', 'views_project.change_power_by_group2'),
                       url(r'^(?P<project_id>\d+)/change_power_by_person$', 'views_project.change_power_by_person2'),
                       #初始化powers
                       #by:尚宗凯 at:2015-4-13                       
                       # 示例项目初始化接口关闭掉
                       # by：尚宗凯 at：2015-04-16
                       # url(r'^init_group_power$', 'view.init_group_power'),
                       #初始化水浒测试项目数据
                       #by: 尚宗凯 at：2015-04-15
                       # 示例项目初始化接口关闭掉
                       # by：尚宗凯 at：2015-04-16
                       # url(r'^add_shuihu_user$', 'view.add_shuihu_user'),
                       # 修改水浒内容
                       # by：尚宗凯 at：2015-04-16
                       url(r'^update_shuihu_data$', 'view.update_shuihu_data'),
                        #显示错误日志页面
                        #by: 范俊伟 at:2015-04-15
                       url(r'^logging$', 'views_logging.logging'),
                       url(r'^logging_count$', 'views_logging.logging_count'),

                       url(r'^logging$', 'views_logging.logging'),


                       #根据project_id,flag获取用户的新消息数量
                       #by:尚宗凯 at：2015-05-06
                       url(r'^(?P<project_id>\d+)/get_unread_num_by_flag', 'views_project.get_unread_num_by_flag'),
                       #根据project_id,获取用户所有flag的新消息数量
                       #by:尚宗凯 at：2015-05-06
                       # url(r'^get_unread_num_by_project_id', 'views_project.get_unread_num_by_project_id'),
                       # url(r'create_sysmessage$', 'views_message.create_sysmessage'),
                       #刷新project最后阅读时间
                       #by:尚宗凯 at：2015-05-07
                       url(r'^(?P<project_id>\d+)/flush_project_last_read_timeline$', 'views_project.flush_project_last_read_timeline'),
                       #获取未读项目公告数量
                       #by:尚宗凯 at：2015-05-07
                       # url(r'^(?P<project_id>\d+)/get_project_message_unread_number$', 'views_project.get_project_message_unread_number'),
                       #获取未读系统消息数量
                       #by:尚宗凯 at：2015-05-07
                       # url(r'^(?P<project_id>\d+)/get_sysmessage_unread_number', 'views_project.get_sysmessage_unread_number'),
                       #获取未读系统消息和未读项目公告数量的和
                       #by:尚宗凯 at：2015-05-07
                       url(r'^(?P<project_id>\d+)/get_projectmessage_sysmessage_unread_number', 'views_project.get_projectmessage_sysmessage_unread_number'),
                       #获取NEED消息未读数
                       #by:尚宗凯 at：2015-05-28
                       url(r'^get_needmessage_unread_number$', 'views_project.get_needmessage_unread_number'),
                       #测试充值
                       #by:王健 at:2015-05-08
                       url(r'^add_price_2_project$', 'view.add_price_2_project'),
                       #阿里云搜索接口
                       #by：尚宗凯 at：2015-05-15
                       url(r'^search', 'view.search'),

                       #关闭项目（项目状态设为关闭） 删除项目
                       #by：尚宗凯 at：2015-05-15
					   #增加设置项目状态接口
                       #by：尚宗凯 at：2015-06-04
                       url(r'^(?P<project_id>\d+)/close_project', 'views_project.close_project'),
                       url(r'^(?P<project_id>\d+)/delete_project', 'views_project.delete_project'),
                       url(r'^(?P<project_id>\d+)/cancel_delete_project', 'views_project.cancel_delete_project'),
                       url(r'^(?P<project_id>\d+)/set_project_status', 'views_project.set_project_status'),

                       #管理接口，统计数据
                       url(r'^show_tongji_page$', 'view.show_tongji_page'),
                       url(r'^commit_user_total$', 'view.commit_user_total'),
                       url(r'^commit_user_count_by_date$', 'view.commit_user_count_by_date'),
                       url(r'^commit_user_jifen_by_date$', 'view.commit_user_jifen_by_date'),
                       url(r'^commit_project_by_date$', 'view.commit_project_by_date'),
                       url(r'^commit_jifen_paiming_by_jifen$', 'view.commit_jifen_paiming_by_jifen'),
                       url(r'^export_excel_jifen$', 'view.export_excel_jifen'),

                       # 倒图片用临时接口
                       # by：尚宗凯 at：2015-06-03
                       url(r'^tmp_bae_to_qiniu$', 'view.tmp_bae_to_qiniu'),
                       url(r'^delete_qiniu_pic_where_file_status_is_false$', 'view.delete_qiniu_pic_where_file_status_is_false'),
                       url(r'^bcs_pic_to_qiniu$', 'view.bcs_pic_to_qiniu'),
                       url(r'^cal_scale$', 'view.cal_scale'),

                       # 用户活跃度
                       # by：尚宗凯 at：2015-06-04
                       url(r'^(?P<project_id>\d+)/user_activity', 'view.user_activity'),
                       # # 客服设置项目过期时间
                       # # by：尚宗凯 at：2015-06-08
                       # url(r'^set_project_expired_date', 'views_project.set_project_expired_date'),


)