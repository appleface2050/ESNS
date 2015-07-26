# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com

# 部署环境设置非调试状态
#by:王健 at:2015-3-18
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = True

NEED_MONGODB_CONFIG = {
    "host": "192.168.10.251",
    "port": 27017,
    "name": "need",
    "username": None,
    "password": None,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'szk_need_server',  # Or path to database file if using sqlite3.
        'USER': 'admin',  # Not used with sqlite3.
        'PASSWORD': 'admin',  # Not used with sqlite3.
        'HOST': '192.168.10.251',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUEST': True,
    },
}


#添加使用mysql测试的配置
#by:尚宗凯 at:2015-3-10
# 激光推送，单元测试时关闭
# by:王健 at:2015-05-28
if 'test' in sys.argv:
    PUSH_ON = False
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'szk_need_server',  # Or path to database file if using sqlite3.
        # 'USER': 'admin',  # Not used with sqlite3.
        # 'PASSWORD': 'admin',  # Not used with sqlite3.
        # 'HOST': '192.168.2.254',  # Set to empty string for localhost. Not used with sqlite3.
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
ALIPAY_RETURN_URL = 'http://www.tjeasyshare.com/zhifubao_pay_complete'

# PC付完款后跳转的页面（同步通知
ALIPAY_PC_RETURN_URL = 'http://www.tjeasyshare.com/zhifubao_pay_pc_complete'
# 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
#修改回调地址
#by: 范俊伟 at:2015-03-07
ALIPAY_NOTIFY_URL = 'http://www.tjeasyshare.com/zhifubao_pay_callback'

# PC交易过程中服务器异步通知的页面
ALIPAY_PC_NOTIFY_URL = 'http://www.tjeasyshare.com/zhifubao_pay_pc_callback'

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
            'filename': os.path.join(BASE_DIR, 'static_all', 'error.log'),  # 'class': 'logging.StreamHandler',
            'formatter': 'verbose_sp',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'static_all', 'debug.log'),  # 'class': 'logging.StreamHandler',
            'formatter': 'verbose_sp',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'ERROR',
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
APICLOUD_REPLAY_APP = 'A6987223828457'
APICLOUD_REPLAY_AK = 'D82A7903-2A0E-21E3-72D0-C6802D21F940'

API_HOST_URL = 'https://d.apicloud.com'

#删除项目公示期天数
#by：尚宗凯 at：2015-06-01
DELETE_PROJECT_PUBLICITY_PERIOD = 7

#阿里云搜索URL
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH = 'http://baetest.tjeasyshare.com'

HOST_URL = '192.168.9.208:8000'