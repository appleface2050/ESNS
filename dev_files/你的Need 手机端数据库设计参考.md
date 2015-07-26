##你的Need 手机端数据库设计参考
###数据库表
* [1.手机端用户表（UserInfo）](#1)
* [2.项目成员（Person）](#2)
* [3.项目表（Project）](#3)
* [4.分组表（Group）](#4)
* [5.分组和用户关联表（Group-person）](#5)
* [6.项目申请表（ProjectApply）](#6)
* [7.施工日志天气表（SG_TQ_Log）](#7)
* [8.施工日志表（SG_Log）](#8)
* [9.应用节点表（File_Group）](#9)
* [10.应用内容表（AppItem_file）](#10)
* [11.文件表（File)](#11)
* [12.工程检查（EngineCheck）](#12)
* [13.供应商名录](#13)
* [14.物资记录](#14)


<h3 id="1">1.手机端用户表（UserInfo）</h3>
用来记录手机端登录过的用户
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>_id</td> <td>数字自增</td>  <td>客户端主键</td>  </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器端id</td>  </tr>
   <tr> <td>tel</td> <td>数字，手机号</td>  <td>用户名</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>真实姓名</td>  </tr>	  
   <tr> <td>password</td> <td>字符</td>  <td>密码</td>  </tr>
   <tr> <td>icon</td> <td>字符</td>  <td>头像</td>  </tr>
   <tr> <td>idnumber</td> <td>字符</td>  <td>身份证id</td>  </tr>	     
</table>
-------------------
<h3 id="2">2.项目成员（Person）</h3>
用来记录项目内各组成员的
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器端id</td>  </tr>
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>
   <tr> <td>tel</td> <td>数字</td>  <td>电话</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>真实姓名</td>  </tr>	  
   <tr> <td>icon</td> <td>字符</td>  <td>头像</td>  </tr>
   <tr> <td>idnumber</td> <td>字符</td>  <td>身份证号</td>  </tr>	 
   <tr> <td>title</td> <td>字符</td>  <td>岗位</td>  </tr>
   <tr> <td>is_active</td> <td>布尔</td>  <td>是否可用</td>  </tr>
   <tr> <td>create_time</td> <td>字符</td>  <td>加入日期</td>  </tr>	  
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳（最后修改）</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	      
</table>
------------------		
<h3 id="3">3.项目表（Project）</h3>
用来记录登录用户关注的项目
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器端id</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>项目简称</td>  </tr>
   <tr> <td>total_name</td> <td>字符</td>  <td>项目全称</td>  </tr>
   <tr> <td>icon</td> <td>字符</td>  <td>头像url</td>  </tr>	  
   <tr> <td>address</td> <td>数字</td>  <td>地址</td>  </tr>
   <tr> <td>jzmj</td> <td>数字</td>  <td>建筑面积</td>  </tr>	 
   <tr> <td>jglx</td> <td>字符</td>  <td>结构类型</td>  </tr>
   <tr> <td>jzcs</td> <td>数字</td>  <td>建筑层数</td>  </tr>
   <tr> <td>htzj</td> <td>数字</td>  <td>合同造价</td>  </tr>	  
   <tr> <td>kg_date</td> <td>字符</td>  <td>开工日期</td>  </tr>
   <tr> <td>days</td> <td>字符</td>  <td>总工期</td>  </tr>	
   <tr> <td>jsdw</td> <td>字符</td>  <td>建设单位</td>  </tr>
   <tr> <td>jsdw_fzr</td> <td>字符</td>  <td>建设单位负责人</td>  </tr>
   <tr> <td>jsdw_fzr_tel</td> <td>字符</td>  <td>建设单位负责人电话</td>  </tr>
   <tr> <td>kcdw</td> <td>字符</td>  <td>勘察单位</td>  </tr>	  
   <tr> <td>kcdw_fzr</td> <td>字符</td>  <td>勘察单位负责人</td>  </tr>
   <tr> <td>kcdw_fzr_tel</td> <td>字符</td>  <td>勘察单位负责人电话</td>  </tr>	 
   <tr> <td>sjdw</td> <td>字符</td>  <td>设计单位</td>  </tr>
   <tr> <td>sjdw_fzr</td> <td>字符</td>  <td>设计单位负责人</td>  </tr>
   <tr> <td>sjdw_fzr_tel</td> <td>字符</td>  <td>设计单位负责人电话</td>  </tr>	  
   <tr> <td>sgdw</td> <td>字符</td>  <td>施工单位</td>  </tr>
   <tr> <td>sgdw_fzr</td> <td>字符</td>  <td>施工单位负责人</td>  </tr>	
   <tr> <td>sgdw_fzr_tel</td> <td>字符</td>  <td>施工单位负责人电话</td>  </tr>     
   <tr> <td>jldw</td> <td>字符</td>  <td>监理单位</td>  </tr>
   <tr> <td>jldw_fzr</td> <td>字符</td>  <td>监理单位负责人</td>  </tr>
   <tr> <td>jldw_fzr_tel</td> <td>字符</td>  <td>监理单位负责人电话</td>  </tr>	  
   <tr> <td>manager</td> <td>数字</td>  <td>超级管理员</td>  </tr>
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳（最后修改）</td>  </tr>	
   <tr> <td>userinfo_id</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>  
</table>
---------------		
<h3 id="4">4.分组表（Group）</h3>
联系人分组
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器端id</td>  </tr>
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>分组名称</td>  </tr>	  
   <tr> <td>icon</td> <td>字符</td>  <td>头像</td>  </tr>
   <tr> <td>type</td> <td>字符</td>  <td>类型标记</td>  </tr>	 
   <tr> <td>sorted</td> <td>数字</td>  <td>排序</td>  </tr>
   <tr> <td>is_active</td> <td>布尔</td>  <td>是否可用</td>  </tr>
   <tr> <td>pser</td> <td>数字</td>  <td>Person表id</td>  </tr>	  
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳（最后修改）</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	      
</table>
--------------------	
<h3 id="5">5.分组和用户关联表（Group-person）</h3>
分组内用户和用户的权限
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>_id</td> <td>数字</td>  <td>分组id</td>  </tr>
   <tr> <td>group</td> <td>数字</td>  <td>分组id</td>  </tr>
   <tr> <td>user</td> <td>数字</td>  <td>Person表id</td>  </tr>	  
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>
   <tr> <td>type</td> <td>字符0/1</td>  <td>能否发言</td>  </tr>	 
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	      
</table>
------------------
<h3 id="6">6.项目申请表（ProjectApply）</h3>
项目之外的人申请加入项目（管理员用户才会去获取）
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>user_name</td> <td>数字</td>  <td>申请人姓名</td>  </tr>
   <tr> <td>icon</td> <td>字符</td>  <td>申请人头像</td>  </tr>	  
   <tr> <td>text</td> <td>字符</td>  <td>申请人的申请信息</td>  </tr>
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>	 
   <tr> <td>status	</td> <td>数字</td>  <td>处理状态</td>  </tr>	     
   <tr> <td>checker</td> <td>数字</td>  <td>Person表id，处理人</td>  </tr>
   <tr> <td>create_time</td> <td>字符</td>  <td>发出项目申请的日期</td>  </tr>	  
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳（最后修改）</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
   <tr> <td>ss_read	</td> <td>数字	0/1</td>  <td>手机端用户 是否读过</td>  </tr>	  
</table>
------------------
<h3 id="7">7.施工日志天气表（SG_TQ_Log）</h3>
施工天气表，该表无需手机端插入数据，仅作显示使用
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>	 
   <tr> <td>date	</td> <td>字符</td>  <td>日期</td>  </tr>	     
   <tr> <td>weather</td> <td>字符</td>  <td>天气情况</td>  </tr>
   <tr> <td>wind</td> <td>字符</td>  <td>风力</td>  </tr>	  
   <tr> <td>qiwen</td> <td>字符</td>  <td>气温</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>
---------
<h3 id="8">8.施工日志表（SG_Log）</h3>
施工日志内容表
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>sg_tq_log</td> <td>数字</td>  <td>施工日志天气id</td>  </tr>	 
   <tr> <td>text	</td> <td>字符</td>  <td>施工日志内容</td>  </tr>	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目</td>  </tr>
   <tr> <td>user</td> <td>数字</td>  <td>Person表id，书写人</td>  </tr>	  
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳（最后修改）</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
  <tr> <td>is_read</td> <td>数字	0/1</td>  <td>手机端用户 是否读过</td>  </tr>	  
   <tr> <td>is_upload</td> <td>数字	0/1</td>  <td>手机端断网下写的日志是否上传</td>  </tr>
</table>
-----------------
<h3 id="9">9.应用节点表（File_Group）</h3>
应用模块的节点表，某些应用还有下级节点
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>flag</td> <td>字符</td>  <td>功能标记，唯一</td>  </tr>	 
   <tr> <td>name	</td> <td>字符</td>  <td>名称</td>  </tr>	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目，可能是空的，系统默认的应用节点，project就是空的</td>  </tr>
   <tr> <td>icon</td> <td>字符</td>  <td>图标名字</td>  </tr>	  
   <tr> <td>typeflag</td> <td>字符</td>  <td>展示类型</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
  <tr> <td>father</td> <td>数字	0/1</td>  <td>父级节点，为空时，为一级节点</td>  </tr>	  
   <tr> <td>sorted</td> <td>数字	0/1</td>  <td>排序</td>  </tr>
  <tr> <td>status</td> <td>数字</td>  <td>应用类型，sys：系统创建，c：用户自建</td>  </tr>	  
   <tr> <td>timeline</td> <td>数字</td>  <td>时间戳</td>  </tr>
</table>
--------------
<h3 id="10">10.应用内容表（AppItem_file）</h3>
应用项的文件数据
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>title</td> <td>字符</td>  <td>文件名称</td>  </tr>	 	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目，可能是空的，系统默认的应用节点，project就是空的</td>  </tr>
   <tr> <td>file_group</td> <td>字符</td>  <td>AppItem 表s_id </td>  </tr>	  
   <tr> <td>create_time</td> <td>字符</td>  <td>创建时间</td>  </tr>
   <tr> <td>text	</td> <td>字符</td>  <td>文字补充</td>  </tr>	   
   <tr> <td>sorted</td> <td>数字	0/1</td>  <td>排序</td>  </tr>
  <tr> <td>user</td> <td>数字</td>  <td>Person表的id</td>  </tr>	  
   <tr> <td>file</td> <td>数字</td>  <td>File 表的id</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>
---------------------
<h3 id="11">11.文件表（File)</h3>
客户端或web端上传的文件，在本地是否下载过，的记录，防止重复下载
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr> 
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>文件名称</td>  </tr>	 	     
   <tr> <td>url</td> <td>字符</td>  <td>文件的路径名</td>  </tr>
   <tr> <td>filetype</td> <td>字符</td>  <td>文件类型 </td>  </tr>	  
   <tr> <td>size</td> <td>数字</td>  <td>文件大小</td>  </tr>
   <tr> <td>localpath	</td> <td>字符</td>  <td>本地路径</td>  </tr>	   
   <tr> <td>is_download</td> <td>数字</td>  <td>是否下载过了</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>
------------------------------
<h3 id="12">12.工程检查（EngineCheck）</h3>
工程检查类的数据
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>title</td> <td>字符</td>  <td>文件名称</td>  </tr>	 	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目，可能是空的，系统默认的应用节点，project就是空的</td>  </tr>
   <tr> <td>file_group</td> <td>字符</td>  <td>AppItem 表s_id  </td>  </tr>	  
   <tr> <td>create_time</td> <td>字符</td>  <td>创建时间</td>  </tr>
   <tr> <td>path	</td> <td>字符</td>  <td>问题部位</td>  </tr>	   
   <tr> <td>pre_pic</td> <td>数字</td>  <td>File表的id</td>  </tr>
   <tr> <td>user</td> <td>数字</td>  <td>Person表的id</td>  </tr>
   <tr> <td>desc	</td> <td>字符</td>  <td>问题描述</td>  </tr>	   
   <tr> <td>chuli</td> <td>字符</td>  <td>处理意见</td>  </tr>
   <tr> <td>chuli_pic</td> <td>数字</td>  <td>File表id</td>  </tr>
   <tr> <td>fucha</td> <td>数字</td>  <td>复查意见</td>  </tr>
   <tr> <td>status	</td> <td>字符</td>  <td>状态</td>  </tr>	   
   <tr> <td>timeline</td> <td>数字</td>  <td>修改时间戳</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>
------------
<h3 id="13">13.供应商名录</h3>	
物资管理中的供应商名录
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>文件名称</td>  </tr>	 	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目，可能是空的，系统默认的应用节点，project就是空的</td>  </tr>
   <tr> <td>file_group</td> <td>字符</td>  <td>AppItem 表s_id  </td>  </tr>	  
   <tr> <td>create_time</td> <td>字符</td>  <td>创建时间</td>  </tr>
   <tr> <td>ghs	</td> <td>字符</td>  <td>供应商</td>  </tr>	   
   <tr> <td>ghs_fzr</td> <td>字符</td>  <td>供应商负责人</td>  </tr>
   <tr> <td>ghs_fzr_tel</td> <td>字符</td>  <td>供应商负责人电话</td>  </tr>
   <tr> <td>is_hetong	</td> <td>数字</td>  <td>是否签订了合同</td>  </tr>	   
   <tr> <td>pay_type</td> <td>字符</td>  <td>付款方式</td>  </tr>
   <tr> <td>shr</td> <td>字符</td>  <td>送货人</td>  </tr>
   <tr> <td>shr_tel</td> <td>字符</td>  <td>送货人电话</td>  </tr>
   <tr> <td>bz	</td> <td>字符</td>  <td>备注</td>  </tr>	   
   <tr> <td>user</td> <td>数字</td>  <td>Person id 记录人</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>
---------------------
<h3 id="14">14.物资记录</h3>	
物资记录数据
<table>
   <tr>
	  <td>字段名（不区分大小写）</td>
	  <td>类型</td>
	  <td>解释</td>
   </tr>
   <tr> <td>s_id</td> <td>数字</td>  <td>服务器id</td>  </tr>
   <tr> <td>name</td> <td>字符</td>  <td>文件名称</td>  </tr>	 	     
   <tr> <td>project</td> <td>数字</td>  <td>所属项目，可能是空的，系统默认的应用节点，project就是空的</td>  </tr>
   <tr> <td>file_group</td> <td>字符</td>  <td>AppItem 表s_id  </td>  </tr>	  
   <tr> <td>create_time</td> <td>字符</td>  <td>创建时间</td>  </tr>
   <tr> <td>gg	</td> <td>字符</td>  <td>规格</td>  </tr>	   
   <tr> <td>num</td> <td>数字</td>  <td>数量</td>  </tr>
   <tr> <td>status</td> <td>字符</td>  <td>状态：bug购买记录：come 入库记录；out 出库记录</td>  </tr>
   <tr> <td>company	</td> <td>字符</td>  <td>领料单位</td>  </tr>	   
   <tr> <td>lingliaoren</td> <td>字符</td>  <td>领料人</td>  </tr>
   <tr> <td>count</td> <td>数字</td>  <td>库存量</td>  </tr>   
   <tr> <td>user</td> <td>数字</td>  <td>Person id 记录人</td>  </tr>
   <tr> <td>userInfo_id	</td> <td>数字</td>  <td>用来区分，这条数据，属于手机端哪个用户的</td>  </tr>	 
</table>

