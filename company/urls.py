# coding=utf-8
__author__ = 'EasyShare004'

from django.conf.urls import patterns, url
from company import views
from company.base import views as base_views

urlpatterns = patterns('company',
                       # 后台管理
                       # by：尚宗凯 at：2015-06-14
                       url(r'^manage$', views.AppView.as_view(), name='cp_manage'),

                       url(r'^login$', base_views.LoginView.as_view(), name='login'),
                       url(r'^logout$', views.logout, name='logout'),
                       url(r'^query_user$', views.query_user),
                       url(r'^set_user_type$', views.set_user_type),
                       url(r'^change_password$', views.change_password),
                       url(r'^query_big_company$', views.query_big_company),
                       # 设置集团展示
                       # by：尚宗凯 at：2015-06-15
                       url(r'^set_big_company_display$', views.set_big_company_display),
                       #查询系统新闻
                       #by:尚宗凯 at：2015-06-16
                       url(r'^query_sys_news$', views.query_sys_news),
                       #批量设置系统新闻发布状态
                       #by：尚宗凯 at：2015-06-16
                       url(r'^set_sys_news_is_active$', views.set_sys_news_is_active),
                       #批量设置公司新闻发布状态
                       #by：尚宗凯 at：2015-06-19
                       url(r'^set_company_news_is_active$', views.set_company_news_is_active),
                       #设置系统column状态
                       #by：尚宗凯 at：2015-06-17
                       url(r'^set_sys_column_is_active$', views.set_sys_column_is_active),
                       #获取所有公司
                       #by：尚宗凯 at：2015-06-16
                       url(r'^get_all_company$', views.get_all_company),
                       #设置系统banner状态
                       #by：尚宗凯 at：2015-06-16
                       url(r'^set_sys_banner_is_active$', views.set_sys_banner_is_active),
                       #设置公司banner状态
                       #by：尚宗凯 at：2015-06-23
                       url(r'^(?P<company_id>\d+)/set_company_banner_is_active$', views.set_company_banner_is_active),

                       #删除系统banner
                       #by：尚宗凯 at：2015-06-16
                       url(r'^delete_sys_banner$', views.delete_sys_banner),
                       #删除公司banner
                       #by：尚宗凯 at：2015-06-23
                       url(r'^(?P<company_id>\d+)/delete_company_banner$', views.delete_company_banner),

                       #创建系统banner
                       #by：尚宗凯 at：2015-06-16
                       url(r'^create_sys_banner$', views.create_sys_banner),

                       #创建公司banner
                       #by：尚宗凯 at:2015-06-23
                       url(r'^(?P<company_id>\d+)/create_company_banner$', views.create_company_banner),


                       #根据公司id查询公司下用户
                       #by: 尚宗凯 at：2015-06-19
                       url(r'^(?P<company_id>\d+)/get_user_by_company_id$', views.get_user_by_company_id),

                       #根据关键词获取用户名称
                       #by: 尚宗凯 at：2015-06-19
                       url(r'^query_user_name$', views.query_user_name),

                       #获取我的企业
                       #by：尚宗凯 at：2015-06-10
                       url(r'^my_company$', 'views.my_company'),
                       #获取默认展示的集团
                       #by：尚宗凯 at：2015-06-11
                       url(r'^get_default_big_company', 'views.get_default_big_company'),
                       #默认展示的行业资讯
                       #by：尚宗凯 at：2015-06-11
                       url(r'^get_default_sys_news$', 'views.get_default_sys_news'),
                       #查询所有集团
                       #by：尚宗凯 at：2015-06-11
                       url(r'^get_all_big_company$', 'views.get_all_big_company'),
                       #设置收藏
                       #by：尚宗凯 at：2015-06-11
                       # url(r'^save_news$', 'views.save_news'),
                       #取消收藏
                       #by：尚宗凯 at：2015-06-11
                       # url(r'^cancel_save_news$', 'views.cancel_save_news'),
                       #获取我的收藏
                       #by：尚宗凯 at：2015-06-11
                       # url(r'^get_my_save_news$', 'views.get_my_save_news'),
                       #获取我的收藏html
                       #by：尚宗凯 at：2015-06-17
                       url(r'^get_my_save_html$', 'views.get_my_save_html'),

                       #获取公司banner
                       #by：尚宗凯 at：2015-06-11
                       url(r'^(?P<company_id>\d+)/company_banner$', 'views.company_banner'),
                       #获取首页banner
                       #by：尚宗凯 at：2015-06-12
                       url(r'^sys_banner$', 'views.sys_banner'),
                       #获取所有首页banner
                       #by：尚宗凯 at：2015-06-12
                       url(r'^all_sys_banner$', 'views.all_sys_banner'),
                       #获取所有系统column
                       #by：尚宗凯 at：2015-06-17
                       url(r'^all_sys_column$', 'views.all_sys_column'),
                       #根据公司id 获取公司栏目列表
                       #by：尚宗凯 at：2015-06-19
                       url(r'^(?P<company_id>\d+)/get_company_column$', 'views.get_company_column'),
                       #获取公司企业动态信息
                       #by：尚宗凯 at：2015-06-11
                       url(r'^get_company_news$', 'views.get_company_news'),
                       #获取公司企业资讯新闻
                       #by:尚宗凯 at：2015-06-27
                       url(r'^(?P<company_id>\d+)/get_qyzx_company_news$', 'views.get_qyzx_company_news'),
                       #获取公司的项目
                       #by：尚宗凯 at：2015-06-11
                       url(r'^get_project_by_company$', 'views.get_project_by_company'),
                       #创建公司(客服非客服通用）
                       #by：尚宗凯 at：2015-06-11
                       url(r'^create_company$', 'views.create_company'),
                       #设置关注企业
                       #by：尚宗凯 at：2015-06-11
                       url(r'^set_follow_company$', 'views.set_follow_company'),
                       #取消关注企业
                       #by：尚宗凯 at：2015-06-11
                       url(r'^cancel_follow_company$', 'views.cancel_follow_company'),

                       #客服创建企业
                       #by：尚宗凯 at：2015-06-11
                       url(r'^create_bigcompany$', 'views.create_bigcompany'),
                       #客服上传系统新闻
                       #by：尚宗凯 at：2015-06-11
                       #修改函数名称
                       #by：尚宗凯 at：2015-06-16
                       url(r'^create_sys_news$', 'views.create_sys_news'),
                       # 根据id获取新闻信息，方便修改
                       # by:王健 at:2015-06-17
                       url(r'^get_sys_news_by_id$', 'views.get_sys_news_by_id'),
                       # 根据id获取公司新闻信息，方便修改
                       # by:尚宗凯 at:2015-06-23
                       url(r'^get_company_news_by_id$', 'views.get_company_news_by_id'),
                       # 根据id获取公司新闻信息，column_list内容为这个新闻的父节点下面的所有子节点
                       # by:尚宗凯 at:2015-06-27
                       url(r'^get_company_news_by_id2$', 'views.get_company_news_by_id2'),
                       # 根据id获取公司
                       # by：尚宗凯 at：2015-06-18
                       url(r'^get_company_by_id$', 'views.get_company_by_id'),
                       #客服发布新闻
                       #by：尚宗凯 at：2015-06-11
                       url(r'^release_sys_news$', 'views.release_sys_news'),
                       #客服取消发布新闻
                       #by：尚宗凯 at：2015-06-11
                       url(r'^cancel_release_sys_news$', 'views.cancel_release_sys_news'),
                       #客服创建系统栏目
                       #by：尚宗凯 at：2015-06-11
                       url(r'^create_sys_column$', 'views.create_sys_column'),
                       #设置系统首页banner
                       #by：尚宗凯 at：2015-06-11
                       url(r'^set_sys_banner$', 'views.set_sys_banner'),
                       #设置公司首页banner
                       #by：尚宗凯 at：2015-06-11
                       url(r'^set_company_banner$', 'views.set_company_banner'),
                       #创建公司新闻
                       #by：尚宗凯 at：2015-06-11
                       #优化一下代码
                       #by：尚宗凯 at：2015-06-22
                       url(r'^(?P<company_id>\d+)/create_company_news$', 'views.create_company_news'),
                       #创建综合管理新闻
                       #by：尚宗凯 at：2015-06-27
                       url(r'^(?P<company_id>\d+)/create_zhgl_company_news$', 'views.create_zhgl_company_news'),
                       #设置公司管理员
                       #by：尚宗凯 at：2015-06-11
                       #修改设置公司管理员接口
                       #by：尚宗凯 at：2015-06-19
                       url(r'^(?P<company_id>\d+)/set_company_admin$', 'views.set_company_admin'),
                       #修改公司栏目
                       #by：尚宗凯 at：2015-06-11
                       url(r'^update_company_column$', 'views.update_company_column'),
                       #修改系统栏目
                       #by：尚宗凯 at：2015-06-11
                       url(r'^update_sys_column$', 'views.update_sys_column'),
                       #修改公司借款
                       #by：尚宗凯 at:2015-06-18
                       url(r'^update_company$', 'views.update_company'),
                       # 修改栏目图片
                       #by：尚宗凯 at：2015-06-25
                       url(r'^(?P<company_id>\d+)/update_company_column_image$', 'views.update_company_column_image'),


                       #获得公司的新闻index页面
                       #by:尚宗凯 at：2015-06-17
                       #优化接口
                       #by：尚宗凯 at：2015-06-17
                       url(r'^(?P<company_id>\d+)/get_company_news_index_by_flag$',
                           'views.get_company_news_index_by_flag'),

                       #获取公司四个圈
                       #by：尚宗凯 at：2015-06-17
                       #改用正则匹配
                       #by：尚宗凯 at：2015-06-17
                       url(r'^(?P<company_id>\d+)/(?P<flag>[a-zA-Z0-9_]+)/get_company_button_html_by_flag$',
                           'views_sys_news.get_company_button_html_by_flag'),

                       #通过关键词搜索公司名称
                       #by:尚宗凯 at：2015-06-17
                       url(r'^query_company_by_name$', 'views.query_company_by_name'),
                       #通过集团id获取集团的公司
                       #by：尚宗凯 at：2015-06-17
                       url(r'^query_company_by_bigcompnay$', 'views.query_company_by_bigcompnay'),
                       #返回公司页面访问次数
                       #by：尚宗凯 at：2015-06-17
                       #修改一个bug
                       #by：尚宗凯 at：2015-06-18
                       url(r'^(?P<company_id>\d+)/query_company_pv$', 'views.query_company_pv'),
                       # url(r'^(?P<project_id>\d+)/leave_project$', 'views_project.leave_project'),

                       # 行业资讯列表展示手机端
                       # by:王健 at:2015-06-18
                       url(r'^show_sys_phone_index_news$', 'views_sys_news.show_sys_index_news'),
                       # 行业资讯列表展示手机端, 根据栏目显示
                       # by:王健 at:2015-06-18
                       url(r'^show_sys_phone_index_news/(?P<column_id>\d+)$', 'views_sys_news.show_sys_index_news'),
                       # 新闻展示手机端
                       # by:王健 at:2015-06-17
                       url(r'^show_sys_phone_news/(?P<column_id>\d+)/(?P<news_id>\d+)', 'views_sys_news.show_sys_news'),
                       # 预览接口
                       # by:王健 at:2015-06-27
                       url(r'^show_sys_phone_news_look/(?P<column_id>\d+)/(?P<news_id>\d+)',
                           'views_sys_news.show_sys_news_look'),
                       url(r'^show_sys_news/(?P<column_id>\d+)/(?P<news_id>\d+)', 'views_sys_news.show_sys_news'),

                       # 企业资讯列表展示手机端, 根据栏目显示
                       # by:王健 at:2015-06-18
                       url(r'^show_phone_index_news/(?P<company_id>\d+)/(?P<column_id>\d+)$',
                           'views_sys_news.show_index_news'),
                       # 企业新闻展示手机端
                       # by:王健 at:2015-06-17
                       url(r'^show_phone_news/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)',
                           'views_sys_news.show_news'),
                       # 无需评论的新闻界面
                       # by:王健 at:2015-06-27
                       url(r'^show_qiye_news/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)',
                           'views_sys_news.show_news_noreplay'),
                       # 预览接口
                       # by:王健 at:2015-06-27
                       url(r'^show_phone_news_look/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)',
                           'views_sys_news.show_news_look'),
                       url(r'^show_news/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)',
                           'views_sys_news.show_news'),

                       # 评论相关接口
                       # by:王健 at:2015-06-18
                       # 修改评论相关接口，兼容系统和公司
                       # by:王健 at:2015-06-22
                       url(r'^(?P<company_id>\d*)/ding_news_by_id', 'views_replay.ding_news_by_id'),
                       url(r'^(?P<company_id>\d*)/delete_ding_news_by_id', 'views_replay.delete_ding_news_by_id'),
                       # 收藏新闻接口
                       # by:王健 at:2015-06-22
                       url(r'^(?P<company_id>\d*)/favorite_news_by_id', 'views_replay.ding_favorite_by_id'),
                       url(r'^(?P<company_id>\d*)/delete_favorite_news_by_id',
                           'views_replay.delete_favorite_news_by_id'),
                       url(r'^(?P<company_id>\d*)/replay_news_by_id', 'views_replay.replay_news_by_id'),
                       url(r'^(?P<company_id>\d*)/query_replay_news_by_id', 'views_replay.query_replay_news_by_id'),
                       # 修改接口，之前写错了
                       # by:王健 at:2015-06-22
                       url(r'^(?P<company_id>\d*)/query_news_favorite_zan',
                           'views_replay.query_favorite_zan_count_news_by_id'),
                       url(r'^(?P<company_id>\d*)/count_replay_by_news_id', 'views_replay.count_replay_by_news_id'),

                       url(r'^ding_news_by_id', 'views_replay.ding_news_by_id'),
                       url(r'^delete_ding_news_by_id', 'views_replay.delete_ding_news_by_id'),
                       url(r'^favorite_news_by_id', 'views_replay.ding_favorite_by_id'),
                       url(r'^delete_favorite_news_by_id', 'views_replay.delete_favorite_news_by_id'),
                       url(r'^replay_news_by_id', 'views_replay.replay_news_by_id'),
                       url(r'^query_replay_news_by_id', 'views_replay.query_replay_news_by_id'),
                       url(r'^query_news_favorite_zan', 'views_replay.query_favorite_zan_count_news_by_id'),
                       url(r'^count_replay_by_news_id', 'views_replay.count_replay_by_news_id'),

                       # 向公司中添加用户
                       # by:王健 at:2015-06-19
                       url(r'^add_user_to_company$', 'views_manage_com_user.add_user_to_company'),
                       # 通过手机号向公司中添加用户
                       # by:范俊伟 at:2015-06-25
                       url(r'^(?P<company_id>\d+)/add_user_by_tel_to_company$',
                           'views_manage_com_user.add_user_by_tel_to_company'),
                       # 检查用户是否注册
                       # by:范俊伟 at:2015-06-25
                       url(r'^check_user_registered$', 'views_manage_com_user.check_user_registered'),
                       #联系我们
                       # by：尚宗凯 at：2015-06-19
                       url(r'^(?P<company_id>\d+)/get_contact_us_html$', 'views.get_contact_us_html'),
                       # 根据系统栏目id获取系统栏目
                       # by：尚宗凯 at：2015-06-22
                       url(r'^get_sys_column_by_column_id$', 'views.get_sys_column_by_column_id'),

                       # 企业添加新员工
                       # by:王健 at:2015-06-22
                       url(r'^^(?P<company_id>\d*)/user_manage', 'views_manage_com_user.manage_com_user'),
                       # 企业员工管理,增加删除员工和权限管理
                       # by:王健 at:2015-06-22
                       url(r'^^(?P<company_id>\d*)/manage_com_user_html$',
                           'views_manage_com_user.manage_com_user_html'),
                       # 设置公司状态
                       # by：尚宗凯 at：2015-06-23
                       url(r'^(?P<company_id>\d*)/set_company_status', 'views.set_company_status'),
                       # 通过公司id获取公司信息
                       # by：尚宗凯 at：2015-06-23
                       url(r'^(?P<company_id>\d+)/get_company_detail_by_id', 'views.get_company_detail_by_id'),
                       # 删除公司成员
                       # by：尚宗凯 at：2015-06-24
                       url(r'^(?P<company_id>\d+)/delete_company_user', 'views.delete_company_user'),

                       # 根据登陆的人是哪个公司的管理员返回公司栏目
                       # by：尚宗凯 at：2015-06-25
                       # 修改接口名称
                       # by：尚宗凯 at：2015-06-26

                       # 获取当前用户作为管理员的公司的权限
                       # by：尚宗凯 at：2015-06-25
                       url(r'^(?P<company_id>\d+)/get_permission$', 'views.get_permission'),
                       # 更新权限
                       # by：尚宗凯 at：2015-06-25
                       url(r'^(?P<company_id>\d+)/update_permission$', 'views.update_permission'),

                       # 获取用户权限
                       # by：尚宗凯 at：2015-06-25
                       url(r'^(?P<company_id>\d+)/query_permission$', 'views.query_permission'),

                       # 获取所有父节点
                       # by:尚宗凯 at：2015-06-26
                       # url(r'^(?P<company_id>\d+)/get_father_company_column_list$', 'views.get_father_company_column_list'),
                       # 获取子节点column list
                       # by：尚宗凯 at：2015-06-26
                       url(r'^(?P<company_id>\d+)/get_child_comapny_column_list$',
                           'views.get_child_comapny_column_list'),
                       # 获取企业资讯下面的新闻
                       # by：尚宗凯 at：2015-06-26
                       url(r'^(?P<company_id>\d+)/get_qiyezixun_news$', 'views.get_qiyezixun_news'),
                       # 根据flag查询新闻
                       # by：尚宗凯 at：2015-06-26
                       url(r'^(?P<company_id>\d+)/get_news_by_flag$', 'views.get_news_by_flag'),

                       # 公司企业信息
                       # by：王健 at：2015-06-25
                       url(r'^(?P<company_id>\d+)/company_info$', 'views.company_info'),

                       # 通过flag查询栏目id
                       # by：尚宗凯 at：2015-06-27
                       url(r'^(?P<company_id>\d+)/get_company_column_by_flag$', 'views.get_company_column_by_flag'),
                       # 通过公司id查询综合管理子节点的公司栏目id
                       # by:尚宗凯 at：2015-06-27
                       url(r'^(?P<company_id>\d+)/get_company_column_by_company$',
                           'views.get_company_column_by_company'),
                       # 删除综合管理子节点的新闻
                       # by:尚宗凯 at：2015-06-27
                       url(r'^delete_company_news$', 'views.delete_company_news'),
                       # 删除系统栏目
                       # by：尚宗凯 at：2015-06-29
                       url(r'^delete_sys_column$', 'views.delete_sys_column'),
                       # 查找公司下面所有的项目
                       # by：尚宗凯 at：2015-06-30
                       url(r'^(?P<company_id>\d+)/query_company_project$', 'views.query_company_project'),
                       # 通过手机号把人加到公司里面
                       # by：尚宗凯 at;2015-06-30
                       url(r'^(?P<company_id>\d+)/company_add_user_by_tel$', 'views.company_add_user_by_tel'),
                       #关闭项目
                       # by:尚宗凯 at：2015-06-30
                       url(r'^close_project$', 'views.close_project'),
                       #删除项目
                       # by：尚宗凯 at：2015-06-30
                       url(r'^delete_project$', 'views.delete_project'),
                       #恢复项目
                       # by：尚宗凯 at：2015-06-30
                       url(r'^cancel_delete_project$', 'views.cancel_delete_project'),
                       # 综合管理功能开发
                       # by:王健 at:2015-07-01
                       url(r'^zhgl/(?P<company_id>\d+)/(?P<column_id>\d+)/show_html$',
                           'views_zhgl.show_zhgl_list_html'),
                       url(r'^zhgl/(?P<company_id>\d+)/(?P<column_id>\d+)$', 'views_zhgl.show_zhgl_list'),
                       url(r'^zhgl/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)/show_html$',
                           'views_zhgl.show_zhgl_news_html'),
                       url(r'^zhgl/(?P<company_id>\d+)/(?P<column_id>\d+)/(?P<news_id>\d+)$',
                           'views_zhgl.show_zhgl_news'),

                       # 创建公司项目
                       # by:王健 at:2015-07-02
                       url(r'^(?P<company_id>\d+)/create_project_html$', 'views_zhgl.create_project_html'),

)


