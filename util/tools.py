# coding=utf-8
# Date: 15/3/8
# Time: 14:58
# Email:fanjunwei003@163.com
import logging
import traceback
# import datetime

__author__ = u'范俊伟'
log = logging.getLogger('django')


def common_except_log():
    """
    通用错误输出
    by: 范俊伟 at:2015-03-08
    :return:
    """
    log.error('\n**common_except_log**\n' + traceback.format_exc())

def find_file_type(filename):
    """
    根据文件名找到文件类型
    by: 尚宗凯 at:2015-03-30
    改为根据最后一个确定扩展名
    by: 尚宗凯 at:2015-03-30
    :return:
    """
    if filename:
        a = filename.strip().split(".")
        if len(a) > 1:
            return a[-1]
    return ""

# def init_expired_date():
#     """
#     初始化project 的 expired_date
#     by: 尚宗凯 at：2015-06-08
#     """
#     return datetime.datetime.now()+datetime.timedelta(days=7)