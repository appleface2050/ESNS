# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com

# 部署环境设置非调试状态
#by:王健 at:2015-3-18
import os
# 增加百度云环境配置
# by：尚宗凯 at：2015-05-29
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = True


#修改测试环境HOST_URL
#by：尚宗凯 at：2015-04-15
HOST_URL = 'baetest.tjeasyshare.com'
SHOW_PROJECT_ID = 71
SHOW_USER_ID = 10009

# 设置百度的ak 和sk
# by:王健 at:2015-1-10
BCS_HOST = 'http://bcs.duapp.com'
BAE_AK = 'yT9Lxqc0U56Bv0oB7bvotqGg'
BAE_SK = 'dflAmd61oxFnw9pm1qFt0jXHK1cMZaC4'


# mongodb数据配置
# by: 范俊伟 at:2015-04-16
NEED_MONGODB_CONFIG = {
    "host": "mongo.duapp.com",
    "port": 8908,
    "name": "oRQHvprTgmiHUtJCkWEb",
    "username": BAE_AK,
    "password": BAE_SK,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'svridke2dn5o074',  # Or path to database file if using sqlite3.
        'USER': 'bae',  # Not used with sqlite3.
        'PASSWORD': BAE_SK,  # Not used with sqlite3.
        'HOST': 'svridke2dn5o074.mysql.duapp.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '10296',  # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUEST': True,
    }
}


#使用redis
#by:尚宗凯 at:2015-3-8
#修改为 bae配置
#by:王健 at:2015-3-8
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        # 'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'cache1',
        'OPTIONS': {
            'MAX_ENTRIES': 20000
        },
    },
}

#session 交由 redis 管理
#by:尚宗凯 at:2015-3-8
SESSION_COOKIE_AGE = 60 * 60 * 24 * 31
SESSION_EXPIRE_AT_BROWSER_CLOSE = False



#环信配置
#by:王健 at:2015-1-19
HUANXIN_APP = 'yourneedweb'
HUANXIN_USERNAME = 'YXA6EOnGoKxDEeSKY61oHXhN4A'
HUANXIN_PASSWORD = 'YXA6Pn2cpdruqy1PmUTRH9iifcr6dzw'

# 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
#修改回调地址
#by: 范俊伟 at:2015-03-07
ALIPAY_RETURN_URL = 'http://baetest.tjeasyshare.com/zhifubao_pay_complete'

# PC付完款后跳转的页面（同步通知
ALIPAY_PC_RETURN_URL = 'http://baetest.tjeasyshare.com/zhifubao_pay_pc_complete'
# 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
#修改回调地址
#by: 范俊伟 at:2015-03-07
ALIPAY_NOTIFY_URL = 'http://baetest.tjeasyshare.com/zhifubao_pay_callback'

# PC交易过程中服务器异步通知的页面
ALIPAY_PC_NOTIFY_URL = 'http://baetest.tjeasyshare.com/zhifubao_pay_pc_callback'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose_sp': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s \n============================================================================\n'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'static_all', 'error.log'),
            # 'class': 'logging.StreamHandler',
            'formatter': 'verbose_sp',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'static_all', 'debug.log'),
            # 'class': 'logging.StreamHandler',
            'formatter': 'verbose_sp',
        },
        'bae': {
            # 'level': 'DEUBG',
            'class': 'bae_log.handlers.BaeLogHandler',
            'ak': BAE_AK,
            'sk': BAE_SK,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['bae'],
            # 'level': 'DEUBG',
            'propagate': True
        },
        'need': {
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

# 客服系统地址
# by: 范俊伟 at:2015-05-07
NEED_KF_BASE_URL = 'http://needkftest.duapp.com'



#API cloud 应用的参数
#by:王健 at:2015-05-27
#临时修改为测试参数
#by：尚宗凯 at：2015-06-22
# APICLOUD_REPLAY_APP = 'A6987223070696'
# APICLOUD_REPLAY_AK = '74E480D2-97FE-F676-7410-6A410B9A315B'
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
ALI_OPEN_SEARCH_ON = False