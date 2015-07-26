# coding=utf-8
# Date: 15/2/5'
# Email: wangjian2254@icloud.com
from django.test import TestCase
import json

__author__ = u'王健'


class BaseTestCase(TestCase):
    """
    自定义单元测试，解决积分返回值
    by:王健 at:2015-2-5
    """
    def assertJSONEqual(self, raw, expected_data, msg=None):
        """
        把返回值的积分 去除
        by:王健 at:2015-2-5
        :param raw:
        :param expected_data:
        :param msg:
        :return:
        """
        try:
            data = json.loads(raw)
            if data.has_key('jifen'):
                del data['jifen']
            if data.has_key('jifen_msg'):
                del data['jifen_msg']
            super(BaseTestCase, self).assertJSONEqual(json.dumps(data), expected_data, msg)
        except ValueError:
            self.fail("First argument is not valid JSON: %r" % raw)