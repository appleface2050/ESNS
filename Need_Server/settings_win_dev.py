# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com

# 部署环境设置非调试状态
#by:王健 at:2015-3-18
import sys
import os
DEBUG = True
TEMPLATE_DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


#设置mongodb配置
#by：尚宗凯 at：2015-05-18
# NEED_MONGODB_CONFIG = {
#     "host": "192.168.1.106",
#     "port": 27017,
#     "name": "need",
#     "username": None,
#     "password": None,
# }
# NEED_MONGODB_CONFIG = {
#     "host": "192.168.10.251",
#     "port": 27017,
#     "name": "need",
#     "username": None,
#     "password": None,
# }

#修改为本地内存缓存
#by：尚宗凯 at：2015-05-21
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        # 'BACKEND': 'redis_cache.RedisCache',
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cache1',
        'OPTIONS': {
            'MAX_ENTRIES': 20000
        },
    },
}

#去掉多数据库配置
# by:尚宗凯 at:2015-4-30
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'mydatabase1',
#         # 'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         # 'NAME': 'needserver',  # Or path to database file if using sqlite3.
#         # 'USER': 'root',  # Not used with sqlite3.
#         # 'PASSWORD': 'root',  # Not used with sqlite3.
#         # 'HOST': '192.168.231.130',  # Set to empty string for localhost. Not used with sqlite3.
#         # 'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
#         # 'ATOMIC_REQUEST': True,
#     },
#     'master': {
#         'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'szk_need_server',  # Or path to database file if using sqlite3.
#         'USER': 'admin',  # Not used with sqlite3.
#         'PASSWORD': 'admin',  # Not used with sqlite3.
#         'HOST': '192.168.10.251',  # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
#         'ATOMIC_REQUEST': True,
#     },
#     'slave': {
#         'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'slave_szk_need_server',  # Or path to database file if using sqlite3.
#         'USER': 'admin',  # Not used with sqlite3.
#         'PASSWORD': 'admin',  # Not used with sqlite3.
#         'HOST': '192.168.10.251',  # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
#         'ATOMIC_REQUEST': True,
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'szk_need_server',  # Or path to database file if using sqlite3.
#         'USER': 'admin',  # Not used with sqlite3.
#         'PASSWORD': 'admin',  # Not used with sqlite3.
#         'HOST': '192.168.10.251',  # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
#         'ATOMIC_REQUEST': True,
#     },
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# #mysql主库从库配置
#by：尚宗凯 at：2015-04-28
# DATABASE_ROUTERS = ['util.multi_db_router.MasterSlaveRouter']


#添加使用mysql测试的配置
#by:尚宗凯 at:2015-3-10
#变更mysql配置
# by:尚宗凯 at:2015-3-25
#测试不发推送
#by：尚宗凯 at：2015-05-31
if 'test' in sys.argv:
    PUSH_ON = False
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'szk_need_server',  # Or path to database file if using sqlite3.
        # 'USER': 'admin',  # Not used with sqlite3.
        # 'PASSWORD': 'admin',  # Not used with sqlite3.
        # 'HOST': '192.168.10.251',  # Set to empty string for localhost. Not used with sqlite3.
        # 'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        # 'ATOMIC_REQUEST': True,
    }

#环信配置
#by:王健 at:2015-1-19
if 'test' in sys.argv:
    HUANXIN_APP = 'yourneedtest2'
    HUANXIN_USERNAME = 'YXA6znEFgMCOEeSQJ0HuBSVFbg'
    HUANXIN_PASSWORD = 'YXA6L3f4RLtnlcw0XNBkQOP0hNtcSWY'
else:
    HUANXIN_APP = 'yourneedtest'
    HUANXIN_USERNAME = 'YXA60ju5MMB6EeS23Z3QPGkYjg'
    HUANXIN_PASSWORD = 'YXA6ohTdjhBjXr3Oo__oMpdtCQ_3ZYQ'

# 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
#修改回调地址
#by: 范俊伟 at:2015-03-07
ALIPAY_RETURN_URL = 'http://192.168.10.247:8080/zhifubao_pay_complete'

# PC付完款后跳转的页面（同步通知
ALIPAY_PC_RETURN_URL = 'http://192.168.10.247:8080/zhifubao_pay_pc_complete'
# 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
#修改回调地址
#by: 范俊伟 at:2015-03-07
ALIPAY_NOTIFY_URL = 'http://192.168.10.247:8080/zhifubao_pay_callback'

# PC交易过程中服务器异步通知的页面
ALIPAY_PC_NOTIFY_URL = 'http://192.168.10.247:8080/zhifubao_pay_pc_callback'

# 去掉sql日志
# by:尚宗凯 by：2015-05-27
# LOGGING = {
#         'version': 1,
#         'disable_existing_loggers': False,
#         'handlers': {
#             'console':{
#                 'level':'DEBUG',
#                 'class':'logging.StreamHandler',
#             },
#         },
#         'loggers': {
#             'django.db.backends': {
#                 'handlers': ['console'],
#                 'propagate': True,
#                 'level':'DEBUG',
#             },
#         }
#     }

# 客服系统地址
# by: 范俊伟 at:2015-05-07
NEED_KF_BASE_URL = 'http://needkftest.duapp.com'

#API cloud 应用的参数
#by:王健 at:2015-05-28
#修改一下配置
#by：尚宗凯 at:2015-06-22
APICLOUD_REPLAY_APP = 'A6987223828457'
APICLOUD_REPLAY_AK = 'D82A7903-2A0E-21E3-72D0-C6802D21F940'

API_HOST_URL = 'https://d.apicloud.com'


#删除项目公示期天数
#by：尚宗凯 at：2015-06-01
DELETE_PROJECT_PUBLICITY_PERIOD = 7

#阿里云搜索URL
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH = 'http://baetest.tjeasyshare.com'

#阿里云搜索是否启用
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH_ON = True