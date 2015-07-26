# coding=utf-8
"""
Django settings for Need_Server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
# 解决 字符编码问题
# by:王健 at:2015-3-10
reload(sys)
sys.setdefaultencoding('utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 创建日志目录
# by: 范俊伟 at:2015-06-23
if not os.path.exists(os.path.join(BASE_DIR, 'static_all', 'log')):
    os.makedirs(os.path.join(BASE_DIR, 'static_all', 'log'))

# 环境变量：aliyun、 baidu、mac_dev、win_dev
ENVIRONMENT = 'win_dev'
if 'SERVER_SOFTWARE' in os.environ:
    ENVIRONMENT = 'baidu'

if 'mac_dev' in os.environ:
    ENVIRONMENT = 'mac_dev'

if 'win_dev' in os.environ:
    ENVIRONMENT = 'win_dev'

# 增加配置
# by: 范俊伟 at:2015-06-01
if 'fjw_dev' in os.environ:
    ENVIRONMENT = 'fjw_dev'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2b61+xn+wabbt0^uo-^hs%o-(dy=7_c1p@5u&7u33^(q_oki@i'


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']
# 修改默认时间日期格式
# by: 范俊伟 at:2015-02-14
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'
SHORT_DATETIME_FORMAT = 'y/m/d'
# 设置百度的ak 和sk
# by:王健 at:2015-1-10
BCS_HOST = 'http://bcs.duapp.com'
BAE_AK = 'yT9Lxqc0U56Bv0oB7bvotqGg'
BAE_SK = 'dflAmd61oxFnw9pm1qFt0jXHK1cMZaC4'

# 七牛云存储ak,sk
# by: 范俊伟 at:2015-04-08
# 增加企业版对应的url
# by：尚宗凯 at：2015-06-16
QN_AK = '_Jsy--Hfm1ldj070dRJth1a4Gx-6TkcpySMcZm3V'
QN_SK = 'Xa1r9yMQwwiGZb2GZTOV13BzDrJiY6JAXSVZ9AkJ'
QN_FILE_BUCKET_DOMAIN = 'http://7xihic.com2.z0.glb.qiniucdn.com/'
QN_FRIENDS_ICON_BUCKET_DOMAIN = 'http://7xihie.com2.z0.glb.qiniucdn.com/'
QN_PROJECT_ICON_BUCKET_DOMAIN = 'http://7xihif.com2.z0.glb.qiniucdn.com/'
QN_WEBIMAGE_ICON_BUCKET_DOMAIN = 'http://7xj20h.com2.z0.glb.qiniucdn.com/'
QN_COMPANY_ICON_BUCKET_DOMAIN = 'http://7xjnpa.com2.z0.glb.qiniucdn.com/'
QN_COMPANY_PRI_ICON_BUCKET_DOMAIN = 'http://7xjnpf.com2.z0.glb.qiniucdn.com/'


# 本机网址
#by:尚宗凯 at：2015-04-15
HOST_URL = 'www.tjeasyshare.com'
#示例项目 id
#by:王健 at:2015-3-25
#修改示例项目id
#by:尚宗凯 at:2015-4-14
#修改示例项目id
#by:尚宗凯 at:2015-4-14
#根据环境配置不同
#by:王健 at:2015-4-15
SHOW_PROJECT_ID = 71

#示例用户 id
#by:王健 at:2015-3-25
#改示例用户id
#by:尚宗凯 at:2015-4-14
#改示例用户id
#by:尚宗凯 at:2015-4-14
#根据环境配置不同
#by:王健 at:2015-4-15
SHOW_USER_ID = 10009

#缓存时间
#by:王健 at:2015-3-9
CACHES_TIMEOUT = 3600 * 24
#极光推送alias缓存时间
#by:王健 at:2015-3-9
CACHES_JPUSH_ALIAS_TIME_OUT = 3600

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easemob',
    'needserver',
    'nsbcs',
    #增加统计模块
    #by:王健 at:2015-4-3
    'tongji',

    # add webjs app by:范俊伟 at:2015-01-19
    # 改用webappjs模块,实现完全无刷新
    # by:范俊伟 at:2015-02-06
    'webappjs',
    # add webhtml app by:王健 at:2015-01-26
    'webhtml',
    # 所见即所得的在线编辑
    # by:王健 at:2015-04-19
    'ueditor',
    # 增加公司模块
    # by:尚宗凯 at:2015-06-10
    'company',
    # 后台管理模块
    # by: 范俊伟 at:2015-06-10
    'ns_manage',
)
# 注释掉csrf中间件
# by:王健 at:2015-01-08
# 增加UserAgent中间件
# by: 范俊伟 at:2015-03-04
MIDDLEWARE_CLASSES = (
    # add for redis
    # 'django.middleware.cache.UpdateCacheMiddleware',	# This must be first on the list

    'util.middleware.UserAgentMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'util.error_middle.ExceptionMiddleware'

    # add for redis
    # 'django.middleware.cache.FetchFromCacheMiddleware',   # This must be last
)

ROOT_URLCONF = 'Need_Server.urls'

WSGI_APPLICATION = 'Need_Server.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

#修改时区
#by:王健 at:2015-01-12
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

#不使用时区了
#by:王健 at:2015-01-08
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#by:范俊伟 at:2015-01-19 static配置
STATIC_ROOT = os.path.join(BASE_DIR, 'static_all')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

AUTH_USER_MODEL = "needserver.NSUser"

#环信配置
#by:王健 at:2015-1-19
#配置发布环境和测试环境
#by:王健 at:2015-3-2
#环信 org
#修改环境
#管理员账户名
#by:王健 at:2015-3-16
HUANXIN_ORG = 'easyshare'
HUANXIN_ADMIN = 'easyshare'



#发送短信邀请加入时，使用的url
#by:王健 at:2015-1-25
#优化统计模块，对apk的下载
#by:王健 at:2015-4-3
#修改短信里的 短连接
#by:王健 at:2015-4-8
MESSAGE_URL = 'http://dwz.cn/GPv3r'

APK_DOWNLOAD_URL = 'http://zhushou.360.cn/detail/index/soft_id/2756289?recrefer=SE_D_%E4%BD%A0%E7%9A%84Need'

APK_DOWNLOAD_CHANNEL_URL = 'http://bcs.duapp.com/easysharepf/apk/YourNeed%s.apk'

IOS_DOWNLOAD_URL = 'https://itunes.apple.com/cn/app/ni-deneed/id956441505'

WECHAT_DOWNLOAD_URL = 'http://a.app.qq.com/o/simple.jsp?pkgname=com.yzx.youneed'


# SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'

#登陆连续最大天数
#by:王健 at:2015-2-4
LOGIN_MAX_DAYS = 8
#登陆连续天数积分倍增数
#by:王健 at:2015-2-4
LOGIN_MAX_DAYS_FEN = 5

#累计积分设置
#by:王健 at:2015-2-4

CREATE_DATA = 'create_data'
FENXIANG = 'fenxiang'
LEIJI_MAX = {CREATE_DATA: (2, 20, u'奖励%s积分'), FENXIANG: (5, 20, u'分享成功，奖励%s积分')}


# 支付宝相关参数
# by: 范俊伟 at:2015-03-06

# 安全检验码，以数字和字母组成的32位字符
ALIPAY_KEY = 'oe2zbsbpp0dxksi63bx3po2pmz1fg597'
ALIPAY_INPUT_CHARSET = 'utf-8'
# 合作身份者ID，以2088开头的16位纯数字
ALIPAY_PARTNER = '2088811259449883'
# 授权接口所使用的请求号
ALIPAY_AUTH_REQ_ID = '35391036483262936512'
# 签约支付宝账号或卖家支付宝帐户
ALIPAY_SELLER_EMAIL = 'tjeasyshare@163.com'
#加密方式,目前只支持MD5
ALIPAY_SIGN_TYPE = 'MD5'

# 访问模式
ALIPAY_TRANSPORT = 'http'
# 交易自动关闭时间,单位为分钟。
PAY_EXPIRE = '30'


# 接口请求阈值配置
# by: 范俊伟 at:2015-04-16
# 修改阈值次数
# by：尚宗凯 at：2015-05-18
# 修改阈值分组
# by：尚宗凯 at：2015-05-22
API_WARNING_DANGER_COUNTER_PER_DAY = {
    "class1" : [10, 15],
    "class2" : [100, 200],
    "class3" : [200, 400],
}



# logger = logging.getLogger('django')
# logger.setLevel(logging.ERROR)
# logger.addHandler(handler)

# 用于更快速创建测试用户
# by:尚宗凯 at:2015-3-10
# PASSWORD_HASHERS = (
#     'django.contrib.auth.hashers.MD5PasswordHasher',
# )

#去掉开头的空行
#by:尚宗凯 at:2015-04-16
CREATE_PROJECT_SYSMESSAGE = u'【依子轩软件科技】欢迎您使用“你的Need”。您已成功创建“%s”项目，系统自动在项目账号中充入600个消费金豆（按项目成员20人计，预计可使用30天）。\n    现在您可以在联系人中添加成员。祝您使用愉快！谢谢！'

#NEED消息类型和状态
#by：尚宗凯 at：2015-04-01
NEED_MESSAGE_TYPE = [1, 2, 3]  #1：系统消息   2：用户消息   3：客服消息
NEED_MESSAGE_STATUS = [1, 2]  #1:未读 2：已读


# 极光推送配置
#by：尚宗凯 at：2015-04-02
# 极光推送配置修改
#by：尚宗凯 at：2015-04-02
JPUSH_APP_KEY = u'8f4a9f535730627d506a09a8'
JPUSH_MASTER_SECRET = u'f466d3d7dce269654ee0ad86'
# import jpush as jpush
from util import jpush

_jpush = jpush.JPush(JPUSH_APP_KEY, JPUSH_MASTER_SECRET)
# 极光推送文本
#by：尚宗凯 at：2015-04-08
JPUSH_MESSAGE = "有了新进展"

# 极光推送开关
#by：尚宗凯 at：2015-04-09
PUSH_ON = False


# 系统发出的消息文本
#by：尚宗凯 at：2015-04-10
# 添加推送话术
# by:王健 at:2015-05-12
# 修改一下文字
#by：尚宗凯 at：2015-05-14
#  优化need系统消息提示语句
#  by：尚宗凯 at：2015-05-15
# 增加欠费，关闭，删除消息
# by：尚宗凯 at：2015-07-01
SYS_MESSAGE = {
    "reg_user": "您已注册成功，请完善您的个人信息，谢谢！",
    "reg_project": "您已成功创建 %s 项目，点击“我的项目”进入您刚创建的项目，可以添加其他成员加入。祝您使用愉快！谢谢！",
    # "change_user_group":"所属分组改变",
    "change_applyproject": " %s 项目管理员已审核通过您的申请，现在您已是该项目的成员，可以进入项目上传或获取项目信息。祝您使用愉快！谢谢！",
    "reject_applyproject": " %s 项目管理员已审核拒绝您的申请，您可以在申请信息中详细描述您的身份信息方便管理员核实您的身份。祝您使用愉快！谢谢！",
    "apply_project_manager": "%s 已提交加入 %s 项目的申请，请管理员进入该项目联系人列表中的申请消息栏进行审核，谢谢！",
    "apply_project": "您已成功提交加入 %s 项目的申请，请耐心等待项目管理员的审核，谢谢。",
    "remove_person": "您已被 %s 项目管理员移出该项目。",
    "add_person_by_tel": "您已被 %s 项目管理员加入该项目。",
    "leave_project": "您已成功退出 %s 项目",
    "appley_project_reject_group_person": "%s 项目管理员 %s 拒绝了 %s 的加入申请。",
    "appley_project_approval_group_person": "%s 项目管理员 %s 审核通过了 %s 的加入申请",
    "add_person_by_tel_project_member": "%s 项目管理员 %s 已将 %s 拉入此项目中",

    "project_arrears":"%s 项目已欠费，请充值",
    "project_close":"%s 项目已关闭",
    "project_delete":"%s 项目进入公示期，%s日以后删除项目",
}

# 客服发出的消息文本
#by:尚宗凯 at:2015-04-13
CUSTOMER_SERVICE_MESSAGE = {
    "auto_reply": "您好！客服001小依为您服务。若您有疑问，可留言，我会尽快为您解答，谢谢！"
}

#项目中心系统消息文本
#by:尚宗凯 at:2015-04-13
#去掉开头的空行
#by:尚宗凯 at:2015-04-16
SYSTEM_MESSAGE = {
    "add_person_by_tel3": "【依子轩软件科技】%s 已加入项目",
}

EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'lyteam2014@163.com'
EMAIL_HOST_PASSWORD = 'fanjunwei003,./'
SEND_WARNING_EMAIL_TO = 'wj@tjeasyshare.com'



#删除项目公示期天数
#by：尚宗凯 at：2015-06-01
DELETE_PROJECT_PUBLICITY_PERIOD = 7

#阿里云搜索URL
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH = 'http://www.tjeasyshare.com'

#阿里云搜索是否启用
#by：尚宗凯 at：2015-06-01
ALI_OPEN_SEARCH_ON = True

#默认的公司栏目
#by：尚宗凯 at：2015-06-19
DEFAULT_COMPANY_COLUMN = ["QIYEJIESHAO","GONGSIJIESHAO","QIYERONGYU","HEXINCENGJIESHAO","LINGDAOGUANHUAI","ZUZHIJIAGOU","QIYEWENHUA","WENHUAJIANJIE","GONGSIHUODONG","YUANGONGFENGCAI","QIYEYEJI","GONGCHENGYEJI","CHUANGYOUYEJI","ZAISHIGONGCHENGJIESHAO","ZONGHEGUANLI","GONGGAOTONGZHI","WENJIANCHUANDA","XINXIFABU","JISHUZHIDAO","SHANGBAOZILIAO","XUANCHUANTOUGAO","QIYEZIXUN"]

# 添加通用模版变量
# by: 范俊伟 at:2015-06-24
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'util.context_processors.base',

)

# 项目每天的使用价格，50金豆
# by:王健 at:2015-06-24
DEFAULT_PRICE_EVERYDAY = 50
#**********************************************************
#**               注意将所有配置添加到此行之前               **
#**********************************************************
# 执行子配置
# by: 范俊伟 at:2015-06-01
if ENVIRONMENT:
    settings_path = os.path.join(BASE_DIR, 'Need_Server', 'settings_%s.py' % ENVIRONMENT)
    if os.path.exists(settings_path):
        file = open(settings_path, 'r')
        text = file.read()
        file.close()
        try:
            exec(text)
        except Exception,e:
            print e

