
##你的need 客户端 api接口说明-企业版
**目录：**

------------------

* [1.获取我的企业](#1)
* [2.获取默认展示的集团](#2)
* [3.默认展示的行业资讯](#3)
* [4.查询所有集团](#4)
* [5.获取首页banner](#5)
* [6.设置收藏](#6)
* [7.取消收藏](#7)
* [8.获取我的收藏](#8)
* [9.获取公司banner](#9)
* [10.获取公司栏目(首页)](#10)
* [11.获取公司企业动态信息](#11)
* [12.获取公司的项目](#12)
* [13.创建公司(客服用)](#13)
* [14.设置关注企业](#14)
* [15.取消关注企业](#15)
* [16.客服创建集团](#16)
* [17.客服上传系统新闻](#17)
* [18.客服发布新闻](#18)
* [19.客服取消发布新闻](#19)
* [20.客服创建系统栏目](#20)
* [21.设置公司首页banner](#21)
* [22.创建公司新闻](#22)
* [23.设置公司管理员](#23)
* [24.修改公司栏目](#24)
* [25.设置系统首页banner](#25)
* [26.通过关键词搜索公司](#26)
* [27.通过集团id获取集团的公司](#27)
* [28.获取公司pv](#28)
* [29.获取公司pv](#29)
* [30.获得公司的新闻index页面](#30)
* [31.获得公司的4个圈页面](#31)
* [32.赞系统新闻](#32)
* [33.删除系统新闻](#33)
* [34.收藏系统新闻](#34)
* [35.取消收藏系统新闻](#35)
* [36.评论系统新闻](#36)
* [37.获取系统新闻的评论](#37)
* [38.获取系统新闻的评论数量](#38)
* [39.获取系统新闻的评论数量、是否收藏、是否点赞](#39)
* [40.赞公司新闻](#40)
* [41.删除公司新闻](#41)
* [42.收藏公司新闻](#42)
* [43.取消收藏公司新闻](#43)
* [44.评论公司新闻](#44)
* [45.获取公司新闻的评论](#45)
* [46.获取公司新闻的评论数量](#46)
* [47.获取公司新闻的评论数量、是否收藏、是否点赞](#47)
* [48.获取用户姓名前20个](#48)
* [49.修改公司栏目](#49)
* [50.根据用户id添加用户进入公司](#50)
* [51.获取联系我们html](#51)
* [52.根据公司id查询公司下用户](#52)
* [53.根据系统栏目id获取系统栏目](#53)
* [54.获取用户权限](#54)
* [55.获取公司企业资讯新闻](#55)
* [56.恢复项目(取消删除项目)](#56)
* [57.关闭项目](#57)
* [58.删除项目](#58)
* [59.查找公司下面所有的项目](#59)
* [60.通过手机号把人加到公司里面](#60)
* [61.删除系统栏目](#61)
* [62.删除综合管理子节点的新闻](#62)
* [63.通过公司id查询综合管理子节点的公司栏目id](#63)
* [64.公司企业信息](#64)
* [65.根据flag查询新闻](#65)
* [66.获取企业资讯下面的新闻](#66)
* [67.获取子节点column list](#67)
* [68.更新权限](#68)
* [69.获取当前用户作为管理员的公司的权限](#69)
* [70.删除公司成员](#70)
* [71.通过公司id获取公司信息](#71)
* [72.设置公司状态](#72)
* [73.企业员工管理,增加删除员工和权限管理](#73)
* [74.企业添加新员工](#74)


<br/>
**注意**：统一返回数据均包括这些：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>status_code</td>
      <td>状态码</td>
   </tr>
   <tr>
      <td>message</td>
      <td>返回信息</td>
   </tr>
   <tr>
      <td>dialog</td>
      <td>提示框样式</td>
   </tr>
   <tr>
      <td>success</td>
      <td>提交是否成功</td>
   </tr>
   <tr>
      <td>resulet</td>
      <td>不同接口返回数据不同</td>
   </tr>
   <tr>
      <td>jifen</td>
      <td>获取的积分值，如果不存在则 表示没有获取积分</td>
   </tr>
   <tr>
      <td>jifen_msg</td>
      <td>获取的积分，提示的信息，如果没获取积分则不存在</td>
   </tr>
</table>
##接口：
-----------------------
 <h3 id="1">1.获取我的企业</h3>
      /cp/my_company

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>bigcompany_id</td>
      <td>集团id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>公司名称</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>公司logo</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>expired_date</td>
      <td>过期时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>修改时间</td>
   </tr>
   <tr>
      <td>address</td>
      <td>地址</td>
   </tr>
   <tr>
      <td>phone</td>
      <td>联系电话</td>
   </tr>
   <tr>
      <td>logo_url</td>
      <td>logo的url</td>
   </tr>
   <tr>
      <td>top_logo_url</td>
      <td>top logo的url</td>
   </tr>
</table>

-----------------------
 <h3 id="2">2.获取默认展示的集团</h3>
      /cp/get_default_big_company

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>logo</td>
   </tr>
   <tr>
      <td>name</td>
      <td>集团名称</td>
   </tr>
   <tr>
      <td>id</td>
      <td>集团id</td>
   </tr>
</table>

-----------------------
 <h3 id="3">3.默认展示的行业资讯</h3>
      /cp/get_default_sys_news

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>sys_column</td>
      <td>所属的栏目</td>
   </tr>
   <tr>
      <td>company_id</td>
      <td>公司id</td>
   </tr>
   <tr>
      <td>title</td>
      <td>标题</td>
   </tr>
   <tr>
      <td>pre_content</td>
      <td>预览内容</td>
   </tr>
   <tr>
      <td>content</td>
      <td>新闻内容</td>
   </tr>
   <tr>
      <td>author</td>
      <td>作者</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否发布</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>publish_time</td>
      <td>发布时间</td>
   </tr>
   <tr>
      <td>replay_num</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan_num</td>
      <td>赞数量</td>
   </tr>
   <tr>
      <td>read_num</td>
      <td>阅读数量</td>
   </tr>
</table>

-----------------------
 <h3 id="4">4.查询所有集团</h3>
      /cp/get_all_big_company

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>name</td>
      <td>集团名称</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>logo</td>
   </tr>
</table>

-----------------------
 <h3 id="5">5.获取首页banner</h3>
      /cp/sys_banner

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>系统bannerid</td>
   </tr>
   <tr>
      <td>image</td>
      <td>图片id</td>
   </tr>
   <tr>
      <td>url</td>
      <td>图片url</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>可用否</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>

-----------------------
 <h3 id="6">6.设置收藏</h3>
      /cp/save_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>news_id</td>
	  <td>是</td>
	  <td>收藏新闻id</td>
   </tr>
   <tr>
	  <td>news_type</td>
	  <td>是</td>
	  <td>新闻类型</td>
   </tr>
</table>

####返回结果说明：
无

-----------------------
 <h3 id="7">7.取消收藏</h3>
      /cp/cancel_save_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>news_id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
   <tr>
	  <td>news_type</td>
	  <td>是</td>
	  <td>新闻类型</td>
   </tr>
</table>

####返回结果说明：
无

-----------------------
 <h3 id="8">8.获取我的收藏</h3>
      /cp/get_my_save_news

无
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>user_id</td>
      <td>用户</td>
   </tr>
   <tr>
      <td>news_id</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>


-----------------------
 <h3 id="9">9.获取公司banner</h3>
      /cp/company_banner
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>user_id</td>
      <td>用户</td>
   </tr>
   <tr>
      <td>news_id</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>

-----------------------
 <h3 id="10">10.获取公司栏目(首页)</h3>
      /cp/company_id/get_company_column

无参数
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>company</td>
      <td>公司id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>栏目</td>
   </tr>
   <tr>
      <td>columntype</td>
      <td>栏目类型 1为普通型，栏目下可以有很多新闻，0为特殊型，只可以有一个新闻。</td>
   </tr>
   <tr>
      <td>index_num</td>
      <td>排序字段</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>father</td>
      <td>父级栏目</td>
   </tr>
   <tr>
      <td>flag</td>
      <td>栏目标示</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>

-----------------------
 <h3 id="11">11.获取公司企业动态信息</h3>
      /cp/get_company_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>company_column</td>
      <td>所属的栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>隶属公司</td>
   </tr>
   <tr>
      <td>pre_title</td>
      <td>预览版 title </td>
   </tr>
   <tr>
      <td>title</td>
      <td>title</td>
   </tr>
   <tr>
      <td>pre_content</td>
      <td>新闻内容 预览版</td>
   </tr>
   <tr>
      <td>content</td>
      <td>新闻内容</td>
   </tr>
   <tr>
      <td>author</td>
      <td>作者</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否发布</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>publish_time</td>
      <td>发布时间</td>
   </tr>
   <tr>
      <td>replay_num</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan_num</td>
      <td>赞数量</td>
   </tr>
   <tr>
      <td>read_num</td>
      <td>阅读数量</td>
   </tr>
</table>

-----------------------
 <h3 id="12">12.获取公司的项目</h3>
      /cp/get_project_by_company

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
	  <td>参数</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>工程名称</td>
   </tr>
   <tr>
	  <td>total_name</td>
	  <td>工程全称</td>
   </tr>
   <tr>
	  <td>address</td>
	  <td>工程地点</td>
   </tr>
   <tr>
	  <td>jzmj</td>
	  <td>建筑面积</td>
   </tr>
   <tr>
	  <td>jglx</td>
	  <td>结构类型</td>
   </tr>
   <tr>
	  <td>jzcs</td>
	  <td>建筑层数</td>
   </tr>
   <tr>
	  <td>htzj</td>
	  <td>合同造价</td>
   </tr>
   <tr>
	  <td>kg_date</td>
	  <td>开工日期</td>
   </tr>
   <tr>
	  <td>days</td>
	  <td>总工期(天)</td>
   </tr>
   <tr>
	  <td>jsdw</td>
	  <td>建设单位</td>
   </tr>
   <tr>
	  <td>jsdw_fzr</td>
	  <td>建设单位负责人</td>
   </tr>
   <tr>
	  <td>jsdw_fzr_tel</td>
	  <td>建设单位负责人电话</td>
   </tr>
   <tr>
	  <td>kcdw</td>
	  <td>勘察单位</td>
   </tr>
   <tr>
	  <td>kcdw_fzr</td>
	  <td>建设单位负责人</td>
   </tr>
   <tr>
	  <td>kcdw_fzr_tel</td>
	  <td>勘察单位负责人电话</td>
   </tr>
   <tr>
	  <td>sgdw</td>
	  <td>施工单位</td>
   </tr>
   <tr>
	  <td>sgdw_fzr</td>
	  <td>施工单位</td>
   </tr>
   <tr>
	  <td>sgdw_fzr_tel</td>
	  <td>施工单位负责人电话</td>
   </tr>
   <tr>
	  <td>jldw</td>
	  <td>监理单位</td>
   </tr>
   <tr>
	  <td>jldw_fzr</td>
	  <td>监理单位负责人</td>
   </tr>
   <tr>
	  <td>jldw_fzr_tel</td>
	  <td>监理单位负责人电话</td>
   </tr>
   <tr>
	  <td>sjdw</td>
	  <td>设计单位</td>
   </tr>
   <tr>
	  <td>sjdw_fzr</td>
	  <td>设计单位负责人</td>
   </tr>
   <tr>
	  <td>sjdw_fzr_tel</td>
	  <td>设计单位负责人电话</td>
   </tr>
   <tr>
	  <td>model</td>
	  <td>模型</td>
   </tr>
   <tr>
	  <td>manager</td>
	  <td>管理员id</td>
   </tr>
   <tr>
	  <td>manager_name</td>
	  <td>管理员姓名</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>项目id</td>
   </tr>
   <tr>
	  <td>create_time</td>
	  <td>创建时间</td>
   </tr>
   <tr>
	  <td>is_activite</td>
	  <td>是否激活</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td></td>
   </tr>
   <tr>
	  <td>pk</td>
	  <td></td>
   </tr>
   <tr>
	  <td>icon_url</td>
	  <td>项目头像url</td>
   </tr>
   <tr>
	  <td>timeline</td>
	  <td>时间线</td>
   </tr>
   <tr>
	  <td>is_guanzhu</td>
	  <td>是否是关注项目</td>
   </tr>
   <tr>
	  <td>guanzhu_num</td>
	  <td>关注人数</td>
   </tr>
   <tr>
	  <td>chengyuan_num</td>
	  <td>成员人数</td>
   </tr>
   <tr>
	  <td>status</td>
	  <td>项目状态 0正常 1欠费 2关闭 3已删除 4删除公示期</td>
   </tr>
   <tr>
	  <td>person_num</td>
	  <td>项目成员数量</td>
   </tr>
   <tr>
	  <td>company</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>pay_type</td>
	  <td>付费类型 0试用项目 1自费项目 2企业付费项目</td>
   </tr>
   <tr>
	  <td>dose_user_in_project</td>
	  <td>用户是否在项目中</td>
   </tr>
</table>

-----------------------
 <h3 id="13">13.创建公司(客服用)</h3>
      /cp/create_company

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>bigcompany_id</td>
	  <td>是</td>
	  <td>集团id</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>是</td>
	  <td>公司名</td>
   </tr>
   <tr>
	  <td>logo</td>
	  <td>是</td>
	  <td>logo</td>
   </tr>
   <tr>
	  <td>expired_date</td>
	  <td>否</td>
	  <td>过期时间 默认为一周</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="14">14.设置关注企业</h3>
      /cp/set_follow_company

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="15">15.取消关注企业</h3>
      /cp/cancel_follow_company

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="16">16.客服创建集团</h3>
      /cp/create_bigcompany

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>logo</td>
	  <td>是</td>
	  <td>公司logo</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>是</td>
	  <td>公司名称</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="17">17.客服上传系统新闻</h3>
      /cp/create_sys_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>sys_column_id</td>
	  <td>是</td>
	  <td>栏目id</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>pre_title</td>
	  <td>是</td>
	  <td>预览标题</td>
   </tr>
   <tr>
	  <td>title</td>
	  <td>是</td>
	  <td>标题</td>
   </tr>
   <tr>
	  <td>pre_content</td>
	  <td>是</td>
	  <td>预览内容</td>
   </tr>
   <tr>
	  <td>content</td>
	  <td>是</td>
	  <td>内容</td>
   </tr>
   <tr>
	  <td>author_id</td>
	  <td>是</td>
	  <td>作者id</td>
   </tr>

</table>
####返回结果说明：
无


-----------------------
 <h3 id="18">18.客服发布新闻</h3>
      /cp/release_sys_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>sys_news_id</td>
	  <td>是</td>
	  <td>系统新闻id</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="19">19.客服取消发布新闻</h3>
      /cp/cancel_release_sys_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>sys_news_id</td>
	  <td>是</td>
	  <td>系统新闻id</td>
   </tr>
</table>
####返回结果说明：
无

-----------------------
 <h3 id="20">20.客服创建系统栏目</h3>
      /cp/create_sys_column

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>是</td>
	  <td>栏目名称</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>是</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>是</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>father_id</td>
	  <td>是</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>是</td>
	  <td>flag</td>
   </tr>
   <tr>
	  <td>timeline</td>
	  <td>是</td>
	  <td>flag</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="21">21.设置公司首页banner</h3>
      /cp/set_company_banner

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>image</td>
	  <td>是</td>
	  <td>图片</td>
   </tr>
   <tr>
	  <td>url</td>
	  <td>是</td>
	  <td>url</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>是</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>是</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>company_banner_id</td>
	  <td>是</td>
	  <td>公司banner id</td>
   </tr>

</table>
####返回结果说明：
无


-----------------------
 <h3 id="22">22.创建公司新闻</h3>
      /cp/create_company_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>com_column_id</td>
	  <td>是</td>
	  <td>column id</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司</td>
   </tr>
   <tr>
	  <td>pre_title</td>
	  <td>是</td>
	  <td>预览标题</td>
   </tr>
   <tr>
	  <td>title</td>
	  <td>是</td>
	  <td>标题</td>
   </tr>
   <tr>
	  <td>pre_content</td>
	  <td>是</td>
	  <td>预览内容</td>
   </tr>
   <tr>
	  <td>content</td>
	  <td>是</td>
	  <td>内容</td>
   </tr>
   <tr>
	  <td>author_id</td>
	  <td>是</td>
	  <td>作者id</td>
   </tr>

</table>
####返回结果说明：
无

-----------------------
 <h3 id="23">23.设置公司管理员</h3>
      /cp/company_id/set_company_admin

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>user_id</td>
	  <td>是</td>
	  <td>要设置的管理员的用户id</td>
   </tr>
   <tr>
	  <td>do</td>
	  <td>是</td>
	  <td>设置为管理员还是用户 可选(manager,user)</td>
   </tr>

</table>
####返回结果说明：
无

-----------------------
 <h3 id="24">24.修改公司栏目</h3>
      /cp/update_company_column

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>否</td>
	  <td>栏目名称</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>否</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>columntype</td>
	  <td>否</td>
	  <td>栏目类型</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>否</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>father_id</td>
	  <td>否</td>
	  <td>父节点id</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>否</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>company_column_id</td>
	  <td>是</td>
	  <td>公司栏目id</td>
   </tr>
</table>
####返回结果说明：
无


-----------------------
 <h3 id="25">25.设置系统首页banner</h3>
      /cp/set_sys_banner

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>image</td>
	  <td>否</td>
	  <td>图片id</td>
   </tr>
   <tr>
	  <td>url</td>
	  <td>否</td>
	  <td>url</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>否</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>sys_banner_id</td>
	  <td>是</td>
	  <td>系统banner id</td>
   </tr>
</table>
####返回结果说明：


-----------------------
 <h3 id="26">26.通过关键词搜索公司</h3>
      /cp/query_company_by_name

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>key</td>
	  <td>否</td>
	  <td>搜索关键词</td>
   </tr>
   <tr>
	  <td>start</td>
	  <td>否</td>
	  <td>分页开始值(每次返回20条数据)</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>bigcompany_id</td>
      <td>集团id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>公司名称</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>公司logo</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>expired_date</td>
      <td>过期时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>修改时间</td>
   </tr>
   <tr>
      <td>address</td>
      <td>地址</td>
   </tr>
   <tr>
      <td>phone</td>
      <td>联系电话</td>
   </tr>
</table>

-----------------------
 <h3 id="27">27.通过集团id获取集团的公司</h3>
      /cp/query_company_by_bigcompnay

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>bigcompany_id</td>
	  <td>否</td>
	  <td>集团id (为空则返回所有公司)</td>
   </tr>

</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>bigcompany_id</td>
      <td>集团id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>公司名称</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>公司logo</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>expired_date</td>
      <td>过期时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>修改时间</td>
   </tr>
   <tr>
      <td>address</td>
      <td>地址</td>
   </tr>
   <tr>
      <td>phone</td>
      <td>联系电话</td>
   </tr>
</table>

-----------------------
 <h3 id="28">28.获取公司pv</h3>
      /cp/company_id/query_company_pv

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>pv</td>
      <td>访问数量</td>
   </tr>
</table>

-----------------------
 <h3 id="29">29.获取公司pv</h3>
      /cp/company_id/get_company_news_index_by_flag

无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>pv</td>
      <td>访问数量</td>
   </tr>
</table>

-----------------------
 <h3 id="30">30.获得公司的新闻index页面</h3>
      /cp/company_id/get_company_news_index_by_flag

无
####返回结果说明：
html


-----------------------
 <h3 id="31">31.获得公司的4个圈页面</h3>
      /cp/company_id/flag/get_company_button_html_by_flag

无
####返回结果说明：
html


-----------------------
 <h3 id="32">32.赞系统新闻</h3>
      /cp/ding_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="33">33.删除系统新闻</h3>
      /cp/delete_ding_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>

-----------------------
 <h3 id="34">34.收藏系统新闻</h3>
      /cp/favorite_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="35">35.取消收藏系统新闻</h3>
      /cp/delete_favorite_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="36">36.评论系统新闻</h3>
      /cp/replay_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
   <tr>
	  <td>content</td>
	  <td>是</td>
	  <td>评论内容</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>

-----------------------
 <h3 id="37">37.获取系统新闻的评论</h3>
      /cp/query_replay_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="38">38.获取系统新闻的评论数量</h3>
      /cp/count_replay_by_news_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>count</td>
      <td>评论数量</td>
   </tr>
</table>


-----------------------
 <h3 id="39">39.获取系统新闻的评论数量、是否收藏、是否点赞</h3>
      /cp/query_news_favorite_zan

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>count</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan</td>
      <td>boolean 是否赞了</td>
   </tr>
   <tr>
      <td>favorite</td>
      <td>boolean是否收藏</td>
   </tr>
</table>


-----------------------
 <h3 id="40">40.赞公司新闻</h3>
      /cp/company_id/ding_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="41">41.删除公司新闻</h3>
      /cp/company_id/delete_ding_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>

-----------------------
 <h3 id="42">42.收藏公司新闻</h3>
      /cp/company_id/favorite_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="43">43.取消收藏公司新闻</h3>
      /cp/company_id/delete_favorite_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="44">44.评论公司新闻</h3>
      /cp/company_id/replay_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
   <tr>
	  <td>content</td>
	  <td>是</td>
	  <td>评论内容</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>

-----------------------
 <h3 id="45">45.获取公司新闻的评论</h3>
      /cp/company_id/query_replay_news_by_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>赞id</td>
   </tr>
   <tr>
      <td>author</td>
      <td>发出请求的用户id</td>
   </tr>
   <tr>
      <td>column</td>
      <td>所属栏目</td>
   </tr>
   <tr>
      <td>company</td>
      <td>所属公司，如果是系统新闻，则无值</td>
   </tr>
   <tr>
      <td>news</td>
      <td>新闻id</td>
   </tr>
   <tr>
      <td>is_sys</td>
      <td>是否系统新闻</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>时间戳</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
</table>


-----------------------
 <h3 id="46">46.获取公司新闻的评论数量</h3>
      /cp/company_id/count_replay_by_news_id

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>count</td>
      <td>评论数量</td>
   </tr>
</table>


-----------------------
 <h3 id="47">47.获取公司新闻的评论数量、是否收藏、是否点赞</h3>
      /cp/company_id/query_news_favorite_zan

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>count</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan</td>
      <td>boolean 是否赞了</td>
   </tr>
   <tr>
      <td>favorite</td>
      <td>boolean是否收藏</td>
   </tr>
</table>

-----------------------
 <h3 id="48">48.获取用户姓名前20个</h3>
      /cp/query_user_name

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>key</td>
	  <td>否</td>
	  <td>搜索关键词，可以模糊匹配姓名或手机号码</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>用户id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>用户名字</td>
   </tr>
</table>


-----------------------
 <h3 id="49">49.修改公司栏目</h3>
      /cp/update_sys_column

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>否</td>
	  <td>栏目名称</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>否</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>否</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>sys_column_id</td>
	  <td>是</td>
	  <td>系统栏目id</td>
   </tr>
</table>
####返回结果说明：
无
-----------------------
 <h3 id="50">50.根据用户id添加用户进入公司</h3>
      /cp/add_user_to_company
<table>
    <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>可为checkbox复数值</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>是</td>
	  <td>公司id</td>
   </tr>
</table>
####返回结果说明：
无结果

-----------------------
 <h3 id="51">51.获取联系我们html</h3>
    /cp/company_id/get_contact_us_html
无
####返回结果说明：
无结果

-----------------------
 <h3 id="52">52.根据公司id查询公司下用户</h3>
    /cp/company_id/get_user_by_company_id
无
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>用户id</td>
   </tr>
   <tr>
      <td>tel</td>
      <td>电话</td>
   </tr>
   <tr>
      <td>is_manager</td>
      <td>是否是管理员</td>
   </tr>
   <tr>
      <td>name</td>
      <td>姓名</td>
   </tr>
</table>

-----------------------
 <h3 id="53">53.根据系统栏目id获取系统栏目</h3>
    /cp/get_sys_column_by_column_id
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>sys_column_id</td>
	  <td>是</td>
	  <td>系统栏目id</td>
   </tr>
</table>
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>id</td>
      <td>系统栏目id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>系统栏目名称</td>
   </tr>
   <tr>
      <td>index_num</td>
      <td>排序</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>father_id</td>
      <td>父节点id</td>
   </tr>
   <tr>
      <td>flag</td>
      <td>节点flag</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>

-----------------------
 <h3 id="54">54.获取用户权限</h3>
    /cp/company_id/query_permission
无参数
####返回结果说明：
<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>zhgl</td>
      <td>综合管理栏目是否可以访问</td>
   </tr>
   <tr>
      <td>gcxmgl</td>
      <td>工程项目管理是否可以访问</td>
   </tr>
</table>


-----------------------
 <h3 id="56">56.恢复项目(取消删除项目)</h3>
    /cp/cancel_delete_project
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>project_id</td>
	  <td>是</td>
	  <td>项目id</td>
   </tr>
</table>
####返回结果说明：

无


-----------------------
 <h3 id="57">57.关闭项目</h3>
    /cp/close_project
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>project_id</td>
	  <td>是</td>
	  <td>项目id</td>
   </tr>
</table>
####返回结果说明：

无

-----------------------
 <h3 id="58">58.删除项目</h3>
    /cp/delete_project
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>project_id</td>
	  <td>是</td>
	  <td>项目id</td>
   </tr>
</table>
####返回结果说明：

无


-----------------------
 <h3 id="59">59.查找公司下面所有的项目</h3>
    /cp/company_id/query_company_project
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>key</td>
	  <td>否</td>
	  <td>搜索关键词</td>
   </tr>
   <tr>
	  <td>page_start</td>
	  <td>否</td>
	  <td>开始页</td>
   </tr>
</table>
####返回结果说明：

<table>
   <tr>
	  <td>参数</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>工程名称</td>
   </tr>
   <tr>
	  <td>total_name</td>
	  <td>工程全称</td>
   </tr>
   <tr>
	  <td>address</td>
	  <td>工程地点</td>
   </tr>
   <tr>
	  <td>jzmj</td>
	  <td>建筑面积</td>
   </tr>
   <tr>
	  <td>jglx</td>
	  <td>结构类型</td>
   </tr>
   <tr>
	  <td>jzcs</td>
	  <td>建筑层数</td>
   </tr>
   <tr>
	  <td>htzj</td>
	  <td>合同造价</td>
   </tr>
   <tr>
	  <td>kg_date</td>
	  <td>开工日期</td>
   </tr>
   <tr>
	  <td>days</td>
	  <td>总工期(天)</td>
   </tr>
   <tr>
	  <td>jsdw</td>
	  <td>建设单位</td>
   </tr>
   <tr>
	  <td>jsdw_fzr</td>
	  <td>建设单位负责人</td>
   </tr>
   <tr>
	  <td>jsdw_fzr_tel</td>
	  <td>建设单位负责人电话</td>
   </tr>
   <tr>
	  <td>kcdw</td>
	  <td>勘察单位</td>
   </tr>
   <tr>
	  <td>kcdw_fzr</td>
	  <td>建设单位负责人</td>
   </tr>
   <tr>
	  <td>kcdw_fzr_tel</td>
	  <td>勘察单位负责人电话</td>
   </tr>
   <tr>
	  <td>sgdw</td>
	  <td>施工单位</td>
   </tr>
   <tr>
	  <td>sgdw_fzr</td>
	  <td>施工单位</td>
   </tr>
   <tr>
	  <td>sgdw_fzr_tel</td>
	  <td>施工单位负责人电话</td>
   </tr>
   <tr>
	  <td>jldw</td>
	  <td>监理单位</td>
   </tr>
   <tr>
	  <td>jldw_fzr</td>
	  <td>监理单位负责人</td>
   </tr>
   <tr>
	  <td>jldw_fzr_tel</td>
	  <td>监理单位负责人电话</td>
   </tr>
   <tr>
	  <td>sjdw</td>
	  <td>设计单位</td>
   </tr>
   <tr>
	  <td>sjdw_fzr</td>
	  <td>设计单位负责人</td>
   </tr>
   <tr>
	  <td>sjdw_fzr_tel</td>
	  <td>设计单位负责人电话</td>
   </tr>
   <tr>
	  <td>model</td>
	  <td>模型</td>
   </tr>
   <tr>
	  <td>manager</td>
	  <td>管理员id</td>
   </tr>
   <tr>
	  <td>manager_name</td>
	  <td>管理员姓名</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>项目id</td>
   </tr>
   <tr>
	  <td>create_time</td>
	  <td>创建时间</td>
   </tr>
   <tr>
	  <td>is_activite</td>
	  <td>是否激活</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td></td>
   </tr>
   <tr>
	  <td>pk</td>
	  <td></td>
   </tr>
   <tr>
	  <td>icon_url</td>
	  <td>项目头像url</td>
   </tr>
   <tr>
	  <td>timeline</td>
	  <td>时间线</td>
   </tr>
   <tr>
	  <td>is_guanzhu</td>
	  <td>是否是关注项目</td>
   </tr>
   <tr>
	  <td>guanzhu_num</td>
	  <td>关注人数</td>
   </tr>
   <tr>
	  <td>chengyuan_num</td>
	  <td>成员人数</td>
   </tr>
   <tr>
	  <td>status</td>
	  <td>项目状态 0正常 1欠费 2关闭 3已删除 4删除公示期</td>
   </tr>
   <tr>
	  <td>pay_type</td>
	  <td>付费类型 0试用项目 1自费项目 2企业付费项目</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>隶属公司id</td>
   </tr>
</table>



-----------------------
 <h3 id="60">60.通过手机号把人加到公司里面</h3>
    /cp/company_id/company_add_user_by_tel
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>tel</td>
	  <td>是</td>
	  <td>电话号码</td>
   </tr>
</table>
####返回结果说明：

无


-----------------------
 <h3 id="61">61.删除系统栏目</h3>
    /cp/delete_sys_column
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>系统栏目id</td>
   </tr>
</table>
####返回结果说明：

无

-----------------------
 <h3 id="62">62.删除综合管理子节点的新闻</h3>
    /cp/delete_company_news
<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>id</td>
	  <td>是</td>
	  <td>新闻id</td>
   </tr>
</table>
####返回结果说明：

无


-----------------------
 <h3 id="63">63.通过公司id查询综合管理子节点的公司栏目id</h3>
    /cp/company_id/get_company_column_by_company
无

####返回结果说明：

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>name</td>
	  <td>否</td>
	  <td>栏目名称</td>
   </tr>
   <tr>
	  <td>company_id</td>
	  <td>否</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>columntype</td>
	  <td>否</td>
	  <td>栏目类型</td>
   </tr>
   <tr>
	  <td>index_num</td>
	  <td>否</td>
	  <td>排序</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否可用</td>
   </tr>
   <tr>
	  <td>father_id</td>
	  <td>否</td>
	  <td>父节点id</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>否</td>
	  <td>公司id</td>
   </tr>
   <tr>
	  <td>company_column_id</td>
	  <td>是</td>
	  <td>公司栏目id</td>
   </tr>
</table>


-----------------------
 <h3 id="64">64.公司企业信息</h3>
    /cp/company_id/company_info
无

####返回结果说明：


<table>
   <tr>
	  <td>参数</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>金豆</td>
	  <td>价格</td>
   </tr>
   <tr>
	  <td>person_num</td>
	  <td>用户数量</td>
   </tr>
   <tr>
	  <td>days</td>
	  <td>天数</td>
   </tr>
   <tr>
	  <td>project_num</td>
	  <td>项目数量</td>
   </tr>
</table>


-----------------------
 <h3 id="65">65.公司企业信息</h3>
    /cp/company_id/get_news_by_flag

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>key</td>
	  <td>否</td>
	  <td>搜索关键词</td>
   </tr>
   <tr>
	  <td>page_start</td>
	  <td>否</td>
	  <td>搜索开始页</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否生效</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>是</td>
	  <td>FLAG</td>
   </tr>
</table>

####返回结果说明：


<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>sys_column</td>
      <td>所属的栏目</td>
   </tr>
   <tr>
      <td>company_id</td>
      <td>公司id</td>
   </tr>
   <tr>
      <td>title</td>
      <td>标题</td>
   </tr>
   <tr>
      <td>pre_content</td>
      <td>预览内容</td>
   </tr>
   <tr>
      <td>content</td>
      <td>新闻内容</td>
   </tr>
   <tr>
      <td>author</td>
      <td>作者</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否发布</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>publish_time</td>
      <td>发布时间</td>
   </tr>
   <tr>
      <td>replay_num</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan_num</td>
      <td>赞数量</td>
   </tr>
   <tr>
      <td>read_num</td>
      <td>阅读数量</td>
   </tr>
</table>

-----------------------
 <h3 id="66">66.获取企业资讯下面的新闻</h3>
    /cp/company_id/get_qiyezixun_news

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>key</td>
	  <td>否</td>
	  <td>搜索关键词</td>
   </tr>
   <tr>
	  <td>page_start</td>
	  <td>否</td>
	  <td>搜索开始页</td>
   </tr>
   <tr>
	  <td>is_active</td>
	  <td>否</td>
	  <td>是否生效</td>
   </tr>
</table>

####返回结果说明：


<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>sys_column</td>
      <td>所属的栏目</td>
   </tr>
   <tr>
      <td>company_id</td>
      <td>公司id</td>
   </tr>
   <tr>
      <td>title</td>
      <td>标题</td>
   </tr>
   <tr>
      <td>pre_content</td>
      <td>预览内容</td>
   </tr>
   <tr>
      <td>content</td>
      <td>新闻内容</td>
   </tr>
   <tr>
      <td>author</td>
      <td>作者</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否发布</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>publish_time</td>
      <td>发布时间</td>
   </tr>
   <tr>
      <td>replay_num</td>
      <td>评论数量</td>
   </tr>
   <tr>
      <td>zan_num</td>
      <td>赞数量</td>
   </tr>
   <tr>
      <td>read_num</td>
      <td>阅读数量</td>
   </tr>
</table>

-----------------------
 <h3 id="67">67.获取子节点column list</h3>
    /cp/company_id/get_child_comapny_column_list

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>flag</td>
	  <td>是</td>
	  <td>FLAG</td>
   </tr>
</table>

####返回结果说明：


<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>company</td>
      <td>公司id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>栏目</td>
   </tr>
   <tr>
      <td>columntype</td>
      <td>栏目类型 1为普通型，栏目下可以有很多新闻，0为特殊型，只可以有一个新闻。</td>
   </tr>
   <tr>
      <td>index_num</td>
      <td>排序字段</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>father</td>
      <td>父级栏目</td>
   </tr>
   <tr>
      <td>flag</td>
      <td>栏目标示</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>timeline</td>
   </tr>
</table>


-----------------------
 <h3 id="68">68.更新权限 list</h3>
    /cp/company_id/update_permission

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>power</td>
	  <td>是</td>
	  <td>权限数据</td>
   </tr>
</table>

####返回结果说明：


权限数据


-----------------------
 <h3 id="69">69.获取当前用户作为管理员的公司的权限 list</h3>
    /cp/company_id/delete_company_user

无

####返回结果说明：


权限数据


-----------------------
 <h3 id="70">70.删除公司成员 list</h3>
    /cp/company_id/get_permission

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>user_id</td>
	  <td>是</td>
	  <td>用户id</td>
   </tr>
</table>

####返回结果说明：


无

-----------------------
 <h3 id="71">71.通过公司id获取公司信息 list</h3>
    /cp/company_id/get_company_detail_by_id

无

####返回结果说明：


<table>
   <tr>
      <td>参数</td>
      <td>含义</td>
   </tr>
   <tr>
      <td>bigcompany_id</td>
      <td>集团id</td>
   </tr>
   <tr>
      <td>name</td>
      <td>公司名称</td>
   </tr>
   <tr>
      <td>logo</td>
      <td>公司logo</td>
   </tr>
   <tr>
      <td>is_active</td>
      <td>是否可用</td>
   </tr>
   <tr>
      <td>create_time</td>
      <td>创建时间</td>
   </tr>
   <tr>
      <td>expired_date</td>
      <td>过期时间</td>
   </tr>
   <tr>
      <td>timeline</td>
      <td>修改时间</td>
   </tr>
   <tr>
      <td>address</td>
      <td>地址</td>
   </tr>
   <tr>
      <td>phone</td>
      <td>联系电话</td>
   </tr>
   <tr>
      <td>logo_url</td>
      <td>logo的url</td>
   </tr>
   <tr>
      <td>top_logo_url</td>
      <td>top logo的url</td>
   </tr>
</table>


-----------------------
 <h3 id="72">72.设置公司状态</h3>
    /cp/company_id/set_company_status

<table>
   <tr>
	  <td>参数</td>
	  <td>是否必须</td>
	  <td>含义</td>
   </tr>
   <tr>
	  <td>status</td>
	  <td>是</td>
	  <td>状态</td>
   </tr>
</table>

####返回结果说明：

无


-----------------------
 <h3 id="73">73.企业员工管理,增加删除员工和权限管理</h3>
    /cp/company_id/manage_com_user_html

无

####返回结果说明：

html页面


-----------------------
 <h3 id="74">74.企业添加新员工</h3>
    /cp/company_id/manage_com_user

无

####返回结果说明：

html页面