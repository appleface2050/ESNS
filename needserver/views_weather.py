# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import json
import requests
from util.jsonresult import getResult, MyEncoder, getErrorFormResult
from util.loginrequired import client_login_required, login_project_manager_required, client_login_project_required


__author__ = u'王健'

WEATHER ="http://apistore.baidu.com/microservice/weather?cityid=%s"
@client_login_required
def get_today_weather(request):
    """
    web端获取天气接口
    by:王健 at:2015-1-3
    修改天气数据解析
    by:范俊伟 at:2015-02-07
    处理连接超时
    by:范俊伟 at:2015-02-10
    更换成 百度的接口
    by:王健 at:2015-02-25
    """
    address = request.REQUEST.get('address', '101010100')
    try:
        jsonhtml = requests.get(WEATHER % address, timeout=5)
        result = jsonhtml.json().get('retData', {})
        # result.update(jsonhtml2.json().get('weatherinfo', {}))
        return getResult(True, u'获取天气信息', result)
    except:
        return getResult(False, u'获取天气信息错误', None)



