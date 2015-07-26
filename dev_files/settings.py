# coding=utf-8
"""
Django settings for RealName project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
# 设置默认编码
# by: 范俊伟 at: 2015-02-08
reload(sys)
sys.setdefaultencoding('utf-8')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gzqhpc2jwowos7&k^k^y7iq^f*gqkpq9zet!4wyutl@%#4va1t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'
SHORT_DATETIME_FORMAT = 'y/m/d'


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'realphone',
    'weixin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = "realphone.LiYuUser"

ROOT_URLCONF = 'RealName.urls'

WSGI_APPLICATION = 'RealName.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'realname2',                      # Or path to database file if using sqlite3.
            'USER': 'huaxin',                      # Not used with sqlite3.
            'PASSWORD': '!@#huaxin$%^',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }


# $$$$$$$$$$$$$$$$$$$$$$$
# 必须使用文件缓存,由于apache会有多个进程调用django,为了保证各个进程数据的同步,不能使用内存缓存
# $$$$$$$$$$$$$$$$$$$$$$$
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'static','cache'),
        'TIMEOUT': 60 * 60 * 24,
        'KEY_PREFIX': 'real_name',
        'OPTIONS': {
            'MAX_ENTRIES': 2000,
            'CULL_FREQUENCY': 2,
        }
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_all')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

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
            'filename': os.path.join(BASE_DIR, 'static','log','error.log'),
            #'class': 'logging.StreamHandler',
            'formatter': 'verbose_sp',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error'],
            'level': 'INFO',
            'propagate': True
        },
    },
}
AFTER_INPUT_PHONE_NUMBER_MESSAGE = u'您好，请按照实名标准流程提供四张照片：第一张为身份证正面和本人的合照；第二张为身份证正面和卡号的合照；第三张是身份证的正面照，第四张是身份证的背面照，四张缺一不可。'
FIRST_MESSAGE = u'已经接入，客服正在紧锣密鼓的为您办理业务。'
COMPLETE_MESSAGE = u'感谢您的光临，如有问题请拨打客服电话：400-011-6060，祝您生意兴隆，再见！'
REAL_NAME_SUCCESS = u'恭喜，您的号码已经实名成功。/:v'
# 初始管理员信息
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'
ADMIN_NAME = u'管理员'

# 实名账户配置
# SHI_MING_API_USERNAME = "BJ040_01"
# SHI_MING_API_PASSWORD = "pass010203"

# 微信公众平台配置
SERVER_TOKEN = "74EA125737309EE31BA9356DE40463C8"
WEIXIN_APP_ID = 'wx876e2a3df20164eb'
WEIXIN_APPSECRET = '8e4b17c3ea9c1daf915d39942ecd7621'
# 通过执行python manage.py weixin_menu来设置菜单
# 格式参照wechat_sdk/basic/create_menu
WEIXIN_MENU_DATA = \
    {
        "button":
            [
                {
                    'type': u'click',
                    'name': u'一键实名',
                    'key': u'RN_REQ'
                },
                {"name": u"小六商城", "sub_button":
                    [
                        {
                            "url": u"http://mp.weixin.qq.com/bizmall/mallshelf?id=&t=mall/list&biz=MzA4NDA2MTUyNQ==&shelf_id=2&showwxpaytitle=1#wechat_redirect",
                            "type": u"view",
                            "name": u"旗舰商城",
                        },
                    ]
                },
                {"name": u"联系我们", "sub_button":
                    [
                        {
                            "url": u"https://mp.weixin.qq.com/payfb/payfeedbackindex?appid=wx876e2a3df20164eb#wechat_webview_type=1&wechat_redirect",
                            "type": u"view",
                            "name": u"维权"
                        }
                    ]
                }
            ]
    }

POMELO_PORT = 3052  # POMELO gate端口
POMELO_HOST = "sell3.liulv.net"  # POMELO gate ip地址
POMELO_HTTP_BASE_URL = "http://127.0.0.1:3001"  # POMELO 所提供的http api的host和端口,如果和Pomelo是同一台服务器,不需要修改

IDCARD_IDENTIFY_USERNAME = 'testbjllkj'
IDCARD_IDENTIFY_PASSWORD = 'sjsj34953sdkdsu5ssek234ksd234dswpoiu'

DEFAULT_PASSWORD = '123456'

# 输入手机号时间
INPUT_PHONE_NUMBER_TIMEOUT = 3 * 60

# 排队和开始时间
QUEUE_AND_START_TIMEOUT = 1 * 60 * 60
