# -*- coding: utf-8 -*-
'''
Created on 2011-4-21
支付宝接口
@author: Yefe
'''
import logging
import types
from urllib import urlencode, urlopen
import urllib
from xml.dom import minidom
import re
from django.conf import settings
import requests
from hashcompat import md5_constructor as md5
from util.tools import common_except_log

need_log = logging.getLogger('need')


def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                                           errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

# 网关地址
_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm?'
_PC_GATEWAY = 'https://mapi.alipay.com/gateway.do?'


# 对数组排序并除去数组中的空值和签名参数
# 返回数组和链接串
def params_filter(params, keys=None):
    """
    修改过滤参数
    by: 范俊伟 at:2015-03-06
    1.过滤掉sign_type2.添加固定key顺序校验
    by: 范俊伟 at:2015-03-08
    :param params:
    :return:
    """
    if keys == None:
        ks = params.keys()
        ks.sort()
    else:
        ks = keys
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if not k in ['sign', 'sign_type'] and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key, sign_type='MD5'):
    if sign_type == 'MD5':
        return md5(prestr + key).hexdigest()
    return ''


def build_xml_parm(root, xml_parm):
    '''
    生成xml格式req_data
    增加跟节点设置参数
    by: 范俊伟 at:2015-03-07
    :param xml_parm:
    :type xml_parm dict
    :return:
    '''
    res = '<%s>' % root
    for (k, v) in xml_parm.items():
        if (type(k) == unicode):
            k = k.encode('utf-8')
        if (type(v) == unicode):
            v = v.encode('utf-8')
        res += '<%s>%s</%s>' % (k, v, k)
    res += '</%s>' % root
    return res


def parseXml(xml):
    """
    解码支付宝返回的xml格式的参数
    by: 范俊伟 at:2015-03-06
    :param xml:
    :return:
    """
    if not xml:
        return None
    result = {}
    xml = re.sub(r'<\?.*\?>', '', xml)
    doc = minidom.parseString(xml)

    params = [ele for ele in doc.childNodes[0].childNodes
              if isinstance(ele, minidom.Element)]
    for param in params:
        if param.childNodes:
            text = param.childNodes[0]
            result[param.tagName] = text.data
    return result


def get_auth(subject, out_trade_no, total_fee):
    """
    手机支付授权接口
    by: 范俊伟 at:2015-03-06
    xml根节点设置
    by: 范俊伟 at:2015-03-07
    修改参数
    by: 范俊伟 at:2015-03-07
    :param subject:商品名称
    :param out_trade_no:商户网站唯一订单号
    :param total_fee:交易金额
    :return:request_token 请求token
    """
    params = {}
    params['service'] = 'alipay.wap.trade.create.direct'
    params['format'] = 'xml'
    params['v'] = '2.0'

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['req_id'] = settings.ALIPAY_AUTH_REQ_ID

    xml_parm = {}
    xml_parm['subject'] = subject
    xml_parm['out_trade_no'] = out_trade_no
    xml_parm['total_fee'] = total_fee
    params['sec_id'] = settings.ALIPAY_SIGN_TYPE
    xml_parm['seller_account_name'] = settings.ALIPAY_SELLER_EMAIL
    xml_parm['call_back_url'] = settings.ALIPAY_RETURN_URL
    xml_parm['notify_url'] = settings.ALIPAY_NOTIFY_URL
    xml_parm['pay_expire'] = settings.PAY_EXPIRE

    params['req_data'] = build_xml_parm('direct_trade_create_req', xml_parm)

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)

    url = _GATEWAY + urlencode(params)
    res = requests.get(url)
    if res.ok:
        res_parms_itmes = res.text.encode('utf-8').split('&')
        res_parms = {}
        for i in res_parms_itmes:
            parm = i.split('=')
            if len(parm) == 2:
                res_parms[parm[0]] = urllib.unquote(parm[1])
        res_error = parseXml(res_parms.get('res_error'))
        res_data = parseXml(res_parms.get('res_data'))

        if res_error:
            messge = ''
            for (k, v) in res_error.items():
                messge += u'%s:%s,' % (k, v)
            raise Exception(messge)
        if res_data:
            return res_data.get('request_token')

    print None


def create_direct_phone_pay(request_token):
    """
    授权后,生成支付url
    by: 范俊伟 at:2015-03-06
    xml根节点设置
    by: 范俊伟 at:2015-03-07
    :param request_token: 授权请求token
    :return:
    """
    params = {}
    params['service'] = 'alipay.wap.auth.authAndExecute'
    params['format'] = 'xml'
    params['v'] = '2.0'

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['sec_id'] = settings.ALIPAY_SIGN_TYPE

    xml_parm = {}
    xml_parm['request_token'] = request_token

    params['req_data'] = build_xml_parm('auth_and_execute_req', xml_parm)

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)

    return _GATEWAY + urlencode(params)


# 即时到账交易接口
def create_direct_pay_by_user(out_trade_no, subject, total_fee):
    """
    即时到账接口修改
    by: 范俊伟 at:2015-03-12
    :param tn:
    :param subject:
    :param body:
    :param total_fee:
    :return:
    """
    params = {}
    params['service'] = 'create_direct_pay_by_user'
    params['payment_type'] = '1'

    # 获取配置文件
    params['partner'] = settings.ALIPAY_PARTNER
    params['seller_id'] = settings.ALIPAY_PARTNER
    params['seller_email'] = settings.ALIPAY_SELLER_EMAIL
    params['return_url'] = settings.ALIPAY_PC_RETURN_URL
    params['notify_url'] = settings.ALIPAY_PC_NOTIFY_URL
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET

    # 从订单数据中动态获取到的必填参数
    params['out_trade_no'] = out_trade_no  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    # params['body'] = body  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee'] = total_fee  # 订单总金额，显示在支付宝收银台里的“应付总额”里

    # 扩展功能参数——网银提前
    # params['paymethod'] = 'directPay'  # 默认支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)
    # params['defaultbank'] = ''  # 默认网银代号，代号列表见http://club.alipay.com/read.php?tid=8681379

    # 扩展功能参数——防钓鱼
    # params['anti_phishing_key'] = ''
    # params['exter_invoke_ip'] = ''

    # 扩展功能参数——自定义参数
    # params['buyer_email'] = ''
    # params['extra_common_param'] = ''

    # 扩展功能参数——分润
    # params['royalty_type'] = ''
    # params['royalty_parameters'] = ''

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _PC_GATEWAY + urlencode(params)


# 纯担保交易接口
def create_partner_trade_by_buyer(tn, subject, body, price):
    params = {}
    # 基本参数
    params['service'] = 'create_partner_trade_by_buyer'
    params['partner'] = settings.ALIPAY_PARTNER
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET
    params['notify_url'] = settings.ALIPAY_NOTIFY_URL
    params['return_url'] = settings.ALIPAY_RETURN_URL

    # 业务参数
    params['out_trade_no'] = tn  # 请与贵网站订单系统中的唯一订单号匹配
    params['subject'] = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['payment_type'] = '1'
    params['logistics_type'] = 'POST'  # 第一组物流类型
    params['logistics_fee'] = '0.00'
    params['logistics_payment'] = 'BUYER_PAY'
    params['price'] = price  # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['quantity'] = 1  # 商品的数量
    params['seller_email'] = settings.ALIPAY_SELLER_EMAIL
    params['body'] = body  # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['show_url'] = settings.ALIPAY_SHOW_URL

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


# 确认发货接口
def send_goods_confirm_by_platform(tn):
    params = {}

    # 基本参数
    params['service'] = 'send_goods_confirm_by_platform'
    params['partner'] = settings.ALIPAY_PARTNER
    params['_input_charset'] = settings.ALIPAY_INPUT_CHARSET

    # 业务参数
    params['trade_no'] = tn
    params['logistics_name'] = u'银河列车'  # 物流公司名称
    params['transport_type'] = u'POST'

    params, prestr = params_filter(params)

    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    return _GATEWAY + urlencode(params)


def notify_verify(post, keys=None, very_from_server=False):
    """
    签名验证
    by: 范俊伟 at:2015-03-07
    校验逻辑修改
    by: 范俊伟 at:2015-03-08
    :param post:
    :return:
    """
    _, prestr = params_filter(post, keys)
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    if mysign != post.get('sign'):
        return False

    if very_from_server:
        veryfy_result = 'true'
        try:
            notify_data = parseXml(post.get('notify_data').encode('utf-8'))
            notify_id = notify_data.get('notify_id')
            params = {}
            params['partner'] = settings.ALIPAY_PARTNER
            params['notify_id'] = notify_id
            params['service'] = 'notify_verify'
            gateway = 'https://mapi.alipay.com/gateway.do'
            veryfy_result = urllib.urlopen(gateway, urllib.urlencode(params)).read()
            need_log.debug('veryfy_result:' + veryfy_result)
        except:
            common_except_log()
        if veryfy_result != 'true':
            return False
        else:
            return True
    else:
        return True


def notify_pc_verify(post):
    """
    签名验证
    by: 范俊伟 at:2015-03-07
    校验逻辑修改
    by: 范俊伟 at:2015-03-08
    :param post:
    :return:
    """
    _, prestr = params_filter(post)
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)
    if mysign != post.get('sign'):
        return False

    veryfy_result = 'true'
    try:

        notify_id = post.get('notify_id')
        params = {}
        params['partner'] = settings.ALIPAY_PARTNER
        params['notify_id'] = notify_id
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
        veryfy_result = urllib.urlopen(gateway, urllib.urlencode(params)).read()
        need_log.debug('veryfy_result:' + veryfy_result)
    except:
        common_except_log()
    if veryfy_result != 'true':
        return False
    else:
        return True


