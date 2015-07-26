# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com


# 部署环境设置非调试状态
#by:王健 at:2015-3-18
DEBUG = False
TEMPLATE_DEBUG = False

#阿里云设置 示例项目 和游客账号
#by:王健 at:2015-4-15
SHOW_PROJECT_ID = 103
SHOW_USER_ID = 10212

# mongodb数据配置
# by: 范俊伟 at:2015-04-16
NEED_MONGODB_CONFIG = {
    "host": "10.172.2.142",
    "port": 27017,
    "name": "need_api",
    "username": None,
    "password": None,
}

# 修改阿里云测试服务器host
# by：尚宗凯 at：2015-05-25
# 改为正式mysql服务器
# by：尚宗凯 at：2015-05-25

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'needserver',  # Or path to database file if using sqlite3.
        'USER': 'needserver',  # Not used with sqlite3.
        'PASSWORD': 'needserver',  # Not used with sqlite3.
        'HOST': 'rdsmizy48ivz81cwa9uvt.mysql.rds.aliyuncs.com',
        # 'HOST': 'tmp1432525065374-rdsmizy48ivz81cwa9uvt.mysql.rds.aliyuncs.com',
        # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUEST': True,
    }
}


#使用redis
#by:尚宗凯 at:2015-3-8
#修改为 bae配置
#by:王健 at:2015-3-8
CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': '2ab5a15b02c64b3d.m.cnbjalicm12pub001.ocs.aliyuncs.com:11211',
        'OPTIONS': {
            'username': '2ab5a15b02c64b3d',
            'password': 'yizixuan001WJ'
        }
    }
}
#session 交由 redis 管理
#by:尚宗凯 at:2015-3-8
SESSION_ENGINE = 'mango.session'
SESSION_ENGINE = 'redis_sessions.session'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 31
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

SESSION_REDIS_HOST = '52918a1ef52f11e4.m.cnbja.kvstore.aliyuncs.com'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = "52918a1ef52f11e4:EasyShare20141118"
SESSION_REDIS_PREFIX = 'need_server_session'

#环信配置
#by:王健 at:2015-1-19
HUANXIN_APP = 'yourneed'
HUANXIN_USERNAME = 'YXA67S1Y4J_VEeSw2McUpVhftQ'
HUANXIN_PASSWORD = 'YXA6dE7EwcPGhYq5kGpx1TwEQoTmMn4'

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


# MongoDB日志配置示例
# by: 范俊伟 at:2015-04-15
LOGGING_MONGODB_CONFIG = {
    "host": "10.172.2.142",
    "port": 27017,
    "name": "logging",
    "username": None,
    "password": None,
}
# 开启mongodb日志记录
# by: 范俊伟 at:2015-04-19
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'util.mongodbLogging.MongoHandler',
            'host': LOGGING_MONGODB_CONFIG.get('host'),
            'port': LOGGING_MONGODB_CONFIG.get('port'),
            'database_name': LOGGING_MONGODB_CONFIG.get('name'),
            'username': LOGGING_MONGODB_CONFIG.get('username'),
            'password': LOGGING_MONGODB_CONFIG.get('password'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    },
}

# 客服系统地址
# by: 范俊伟 at:2015-05-07
NEED_KF_BASE_URL = 'http://needkf.tjeasyshare.com'

#API cloud 应用的参数
#by:王健 at:2015-05-28
APICLOUD_REPLAY_APP = 'A6987164678811'
APICLOUD_REPLAY_AK = 'F978FF6E-8390-9B77-FC17-E853F243F517'

API_HOST_URL = 'https://d.apicloud.com'

#删除项目公示期天数
#by：尚宗凯 at：2015-06-01
DELETE_PROJECT_PUBLICITY_PERIOD = 7

#阿里云搜索URL
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH = 'http://www.tjeasyshare.com'

#阿里云搜索是否启用
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH_ON = True