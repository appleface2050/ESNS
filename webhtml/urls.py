# coding=utf-8
# Date:2015/1/10
# Email:wangjian2254@gmail.com
from webhtml.base.views import LoginView, login
from webhtml.view_address import get_provinces, get_cities, get_counties, get_address_by_id
from webhtml.views import HomeView, ReginsterView, logout, DownloadView, UserCenterView, HtmlCommonView, ListView, \
    PhoneReginsterView, ForgetPassword, NeedHelper, HelpQuestion, HelpDetail, HelpManager, HelpSearch, HelpIndex, \
    HelpVersion, help_delete, HelpMenuDetailView, HelpSecondMenuView, HelpThridMenuView,HelpMenuManager, \
    help_menu_delete, HelpIndexAppleChecker
from webhtml.views_forum import forum_login
from webhtml.views_pay import zhifubao_pay, PayView, zhifubao_pay_callback, \
    ZhifubaoPayCompleteView, JiFenView, zhifubao_pay_pc, zhifubao_pay_pc_callback, ZhifubaoPayPCCompleteView, \
    PayOrderView, cancel_order, PayViewV2, PayProductChooseView, PayReceiptView, ZhifubaoPayCompleteViewV2, \
    ZhiFuXieYiView, JiFenDetailView, ProjectPayDetail, ProjectPayDetailAppleCheck
from webhtml.views_web import BuyCarView, CreateOrderView, ProductView


__author__ = u'王健'

from django.conf.urls import patterns, url

# web端接口
# by:王健 at:2015-1-15

urlpatterns = patterns('',
                       # web 界面 接口
                       # by:王健 at:2015-01-26
                       # web界面视图
                       # by:范俊伟 at:2015-02-11
                       # 通用模板
                       # by: 范俊伟 at:2015-02-14
                       # 修改支付url,根据浏览器UserAgent跳转到不同支付界面
                       # by: 范俊伟 at:2015-03-04
                       # 修改手机和PC支付界面接口
                       # by: 范俊伟 at:2015-03-11
                       # 登录界面通过userAgent跳转
                       # by: 范俊伟 at:2015-03-17
                       # 删除重复的register url
                       # by: 范俊伟 at:2015-03-17
                       # 添加手机注册接口
                       # by: 尚宗凯 at:2015-03-19
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^(?P<html_name>.*?).html$', HtmlCommonView.as_view(), name='common_html'),
                       url(r'^login$', login, name='login'),
                       url(r'^download$', DownloadView.as_view(), name='download'),
                       url(r'^register$', ReginsterView.as_view(), name='register'),
                       url(r'^phone_register$', PhoneReginsterView.as_view(), name='phone_register'),
                       url(r'^logout$', logout, name='logout'),
                       url(r'^product$', ProductView.as_view(), name='product'),
                       url(r'^add_buycar$', BuyCarView.as_view(), name='add_buycar'),
                       url(r'^create_order$', CreateOrderView.as_view(), name='create_order'),
                       url(r'^pay$', PayView.as_view(), name='pay'),
                       url(r'^user_center', UserCenterView.as_view(), name='user_center'),
                       url(r'^zhifubao_pay$', zhifubao_pay, name='zhifubao_pay'),

                       # 积分介绍界面
                       # by:王健 at:2015-3-6
                       # 修改name错误
                       # by: 范俊伟 at:2015-03-06
                       # 修改积分界面
                       # by: 王健 at:2015-03-10
                       # 增加积分详情页面
                       # by: 尚宗凯 at:2015-04-27
                       url(r'^jifen_role$', JiFenView.as_view(), name='jifen_role'),
                       url(r'^jifen_detail$', JiFenDetailView.as_view(), name='jifen_detail'),

                       # 重新添加手机支付url
                       # by: 范俊伟 at:2015-03-06
                       # url(r'^phone_pay', PayView.as_view(), name='phone_pay', kwargs={"isPhone": True}),
                       
                       # 手机支付url
                       # by: 尚宗凯 at:2015-04-21
                       url(r'^phone_pay$', PayViewV2.as_view(), name='phone_pay', kwargs={"isPhone": True}),
                       url(r'^phone_pay_product_choose$', PayProductChooseView.as_view(), name='phone_pay_product_choose', kwargs={"isPhone": True}),
                       url(r'^phone_pay_receipt$', PayReceiptView.as_view(), name='phone_pay_receipt', kwargs={"isPhone": True}),

                       # 手机支付协议页面
                       # by：尚宗凯 at：2015-04-21
                       url(r'^zhi_fu_xie_yi$', ZhiFuXieYiView.as_view(), name='zhi_fu_xie_yi', kwargs={"isPhone": True}),
                       # 支付宝回调url
                       # by: 范俊伟 at:2015-03-06
                       # 支付宝回调url
                       # by: 尚宗凯 at:2015-04-22
                       url(r'^zhifubao_pay_complete$', ZhifubaoPayCompleteViewV2.as_view(), name='zhifubao_pay_complete'),
                       url(r'^zhifubao_pay_callback$', zhifubao_pay_callback, name='zhifubao_pay_callback'),
                       # list布局示例页面
                       url(r'^list$', ListView.as_view(), name='list'),

                       # pc支付相关接口
                       url(r'^zhifubao_pay_pc$', zhifubao_pay_pc, name='zhifubao_pay_pc'),
                       url(r'^zhifubao_pay_pc_complete$', ZhifubaoPayPCCompleteView.as_view(),
                           name='zhifubao_pay_pc_complete'),
                       url(r'^zhifubao_pay_pc_callback$', zhifubao_pay_pc_callback, name='zhifubao_pay_pc_callback'),

                       # 地址数据相关接口
                       # by: 范俊伟 at:2015-03-20
                       url(r'^get_provinces', get_provinces, name='get_provinces'),
                       url(r'^get_cities', get_cities, name='get_cities'),
                       url(r'^get_counties', get_counties, name='get_counties'),
                       url(r'^get_address_by_id', get_address_by_id, name='get_address_by_id'),

                       # 未完成订单处理
                       # by: 范俊伟 at:2015-03-20
                       url(r'^pay_order', PayOrderView.as_view(), name='pay_order'),
                       url(r'^cancel_order', cancel_order, name='cancel_order'),

                       # 找回密码
                       # by： 尚宗凯 at 2015-03-27
                       url(r'^forget_password', ForgetPassword.as_view(), name='get_password'),

                       # 修改密码
                       # by： 王健 at 2015-03-27
                       url(r'^change_password', ForgetPassword.as_view(), name='get_password'),


                       #小助手
                       #by：尚宗凯 at：2015-04-03
                       url(r'^need_helper', NeedHelper.as_view(), name='need_helper'),

                       #手机帮助页
                       #by:尚宗凯 at：2015-04-09
                       #手机帮助页详情页
                       #by:尚宗凯 at：2015-04-19
                       #手机帮助页修改
                       #by:尚宗凯 at：2015-04-19
                       #手机帮助页删除接口
                       #by:尚宗凯 at：2015-04-19
                       #增加使用手册以及一级目录
                       #by:尚宗凯 at：2015-05-05
                       #又增加了一级目录
                       #by:尚宗凯 at：2015-05-12
                       # 添加应付苹果审核的url
                       # by:王健 at:2015-05-29
                       url(r'^help_apple_checker2$', HelpIndexAppleChecker.as_view(), name='help_apple_checker$'),
                       url(r'^help_apple_checker$', HelpIndexAppleChecker.as_view(), name='help_apple_checker$'),
                       url(r'^help$', HelpIndex.as_view(), name='help$'),
                       url(r'^help_question$', HelpQuestion.as_view(), name='help_question$'),
                       url(r'^help_version$', HelpVersion.as_view(), name='help_version$'),
                       url(r'^helpupdate$', HelpManager.as_view(), name='helpupdate$'),
                       # 添加菜单修改接口
                       # by:王健 at:2015-05-12
                       url(r'^help_menu_update$', HelpMenuManager.as_view(), name='help_menu_update$'),
                       url(r'^help_detail', HelpDetail.as_view(), name='help_detail$'),
                       url(r'^help_search', HelpSearch.as_view(), name='help_search$'),
                       # 添加菜单删除接口
                       # by:王健 at:2015-05-12
                       url(r'^help_menu_delete', help_menu_delete, name='help_menu_delete$'),
                       url(r'^help_delete', help_delete, name='help_delete$'),
                       # url(r'^help_menu$', HelpMenuView.as_view(), name='help_menu'),
                       url(r'^help_menu_detail', HelpMenuDetailView.as_view(), name='help_menu_detail'),
                       url(r'^help_menu_parent', HelpSecondMenuView.as_view(), name='help_menu_parent'),
                       url(r'^help_thrid_menu_parent', HelpThridMenuView.as_view(), name='help_thrid_menu_parent'),

                       # help 使用帮助
                       #by:尚宗凯 at：2015-05-05
                       # url(r'^help_usage$', HelpUsageView.as_view(), name='help_usage'),
                       # url(r'^help_usage_detail', HelpUsageDetail.as_view(), name='help_usage_detail'),
                       # url(r'^help_usage_search', HelpUsageSearch.as_view(), name='help_usage_search'),
                       # url(r'^help_usage_delete', help_usage_delete, name='help_usage_delete'),
                       # url(r'^help_usage_update$', HelpUsageManager.as_view(), name='help_usage_update'),
                       #验证码图片
                       #by:尚宗凯 at：2015-04-27
                       # url(r'^verification_code$', verification_code, name='verification_code$'),
                       # url(r'^check_verification_code', check_verification_code, name='check_verification_code$'),

                        #项目账户信息
                        #by:王健 at:2015-05-12
                       # 修改为正确的内容，为apple检查切换成 审核版
                       # by:王健 at:2015-05-14
                       # 付费界面
                       # by:王健 at:2015-06-05
                       url(r'^project_detail$', ProjectPayDetail.as_view(), name='project_pay_detail_apple_check'),

                        # 设置论坛的接口，方便未来开发论坛和needserver单点登录
                        # by:王健 at:2015-06-24
                       url(r'^forum_login$', forum_login, name='forum_login'),
                       )