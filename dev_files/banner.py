# coding=utf-8
# Date: 15/4/3'
# Email: wangjian2254@icloud.com
import json
from django.conf import settings

__author__ = u'王健'

#生成 banner 的url列表文件
# 增加bae测试banner
# by:尚宗凯 at：2015-4-6

f = file('../static/client_banner/banner.json', 'w')
l = []
for i in range(5):
    l.append('http://baetest.tjeasyshare.com/static/client_banner/home_banner%s.jpg' % i)
f.write(json.dumps(l))
f.close()