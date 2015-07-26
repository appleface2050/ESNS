#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'

#缓存key
#by:王健 at:2015-3-9

PROJECT_POWER_TIMELINE = '%s_project_power_timeline'

PROJECT_INFO = '%s_projectinfo'

USERINFO_INFO = '%s_userinfo'

PROJECT_GROUP_LIST = '%s_project_group'

PROJECT_PERSON_LIST = '%s_project_person'

PROJECT_QUERY_LIST = '%s_project_query'

MY_PROJECT_QUERY_LIST = '%s_my_project_query_no_guanzhu'

PERSON_TIMELINE = '%s_%s_person_timeline'

PROJECT_IS_ACTIVE = '%s_%s_project_is_active'

#工程id flag对应的alias
#by：尚宗凯 at：2015-05-09
#修改key名称
#by：王健 at：2015-05-07
PROJECT_ID_FLAG_OR_FILEGROUP_ID_ALIAS = "%s_%s_project_id_flag_alias"


#获取未读数量的缓存
#by：尚宗凯 at：2015-05-06
# UNREAD_NUM_BY_PROJECT_ID = "%s_%s_get_unread_num_by_project_id"
# UNREAD_NUM_BY_FLAG = "%s_%s_%s_get_unread_num_by_flag"


#小红点数据用户最后读取时间
#by：尚宗凯 at：2015-05-19
RED_DOT_USER_LAST_READ_TIMELINE = "red_dot_user_last_read_timeline_%s_%s_%s"
#项目应用节点最新数据时间
#by：尚宗凯 at：2015-05-19
RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE = "red_dot_project_file_group_last_new_data_timeline_%s_%s"

#项目应用节点最新数据时间——合并节点（FileRecord）
#by：王健 at：2015-05-21
RED_DOT_PROJECT_FILE_GROUP_LAST_NEW_DATA_TIMELINE_FILERECORD = "red_dot_project_file_group_last_new_data_timeline_filerecord_%s"

#项目应用节点最新数据时间
#by：尚宗凯 at：2015-05-19
RED_DOT_PROJECT_LAST_NEW_DATA_TIMELINE = "red_dot_project_last_new_data_timeline_%s"

#项目应用节点缓存
#by：尚宗凯 at：2015-05-19
PROJECT_FILEGROUP = "project_filegroup_%s"

PROJECT_FILEGROUP_NORMAL = "project_filegroup"

#项目用户真实权限
#by：尚宗凯 at：2015-05-20
PROJECT_USER_REALPOWERS = "project_user_realpowers_%s_%s"

#用户项目应用节点未读数量
#by：尚宗凯 at：2015-05-20
RED_DOT_UNREAD_NUMBER = "red_dot_unread_number_%s_%s_%s"        #flag, user_id, project_id

#系统消息项目公告用户最后阅读时间
#by：尚宗凯 at:2015-05-21
RED_DOT_PROJECT_SYS_MESSAGE_LAST_READ_TIMELINE = "red_dot_project_sys_message_last_read_timeline_%s_%s_%s_%s"     #type, user_id, project_id, group_id

#系统消息项目公告未读数量
#by：尚宗凯 at:2015-05-21
RED_DOT_PROJECT_SYS_MESSAGE_UNREAD_NUMBER = "red_dot_project_sys_message_unread_number_%s_%s_%s_%s"                #type, user_id, project_id, group_id

#系统消息项目公告最新数据时间
#by：尚宗凯 at:2015-05-21
RED_DOT_PROJECT_SYS_MESSAGE_LAST_NEW_DATA_TIMELINE = "red_dot_project_sys_message_last_new_data_timeline_%s_%s_%s"        #type, project_id, group_id


#项目中所有用户的缓存
#by：尚宗凯 at:2015-05-21
PROJECT_GROUP_USER = "project_group_user_%s"    #project_id

#用户活跃度缓存
USER_ACTIVITY = "user_activity_%s_%s_%s"  #user_id, project_id, date

