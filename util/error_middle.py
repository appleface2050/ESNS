# coding=utf-8
# Date:2014/7/10
#Email:wangjian2254@gmail.com
import logging
import sys
import traceback

from django.conf import settings

from util.jsonresult import getResult


__author__ = u'王健'


class ExceptionMiddleware(object):
    """
    错误异常捕获的中间件
    by:王健 at:2015-1-3
    """

    def process_exception(self, request, e):
        """
        程序遇到未捕获的异常，会在此处整理出错误信息，和代码行数
        by:王健 at:2015-1-3
        修改日志 配置
        by:王健 at:2015-3-10
        修改获取用户手机号
        by:王健 at:2015-3-15
        优化 日志输入
        by:王健 at:2015-3-17
        修改错误堆栈信息 获取方式
        by:王健 at:2015-4-7
        修改错误输出格式
        by: 范俊伟 at:2015-04-19
        修改log输出函数
        by: 范俊伟 at:2015-05-05
        :param request:
        :param e:
        :return:
        """
        import time

        errorid = time.time()
        log = logging.getLogger('django')
        s = [u'错误码:%s' % errorid, u'%s:%s' % (request.method, request.path)]
        user = getattr(request, 'user', None)
        if hasattr(user, "tel"):
            s.append(u'用户：%s' % user.tel)
        else:
            s.append(u'未登录用户')
        s.append(u'出现以下错误：')
        #s.append(traceback.format_exc())
        etype, value, tb = sys.exc_info()
        s.append(repr(value.message))
        s.append(u'错误代码位置如下：')
        while tb is not None:
            f = tb.tb_frame
            lineno = tb.tb_lineno
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            s.append(u'File "%s", line %d, in %s' % (filename, lineno, name))
            tb = tb.tb_next
        if not settings.DEBUG:
            log.exception('\n    '.join(s))
            return getResult(False, u'服务器端错误,请联系管理员,错误标记码：%s' % errorid, dialog=2)
        else:
            m = '\n    '.join(s)
            log.exception(m)
            return getResult(False, u'服务器端错误,错误如下：\n%s' % (m), dialog=2)