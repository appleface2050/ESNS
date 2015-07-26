#-*- coding:utf-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'Need_Server.settings'

path = os.path.dirname(os.path.abspath(__file__)) + '/Need_Server'
if path not in sys.path:
    sys.path.insert(1, path)

from django.core.handlers.wsgi import WSGIHandler
from bae.core.wsgi import WSGIApplication

from django.core.management import execute_from_command_line
# 自动执行collectstatic
# by: 范俊伟 at:2015-06-23
try:
    execute_from_command_line(['manage.py', 'collectstatic','--noinput'])
except Exception, e:
    print str(e)

application = WSGIApplication(WSGIHandler(),stderr='log')