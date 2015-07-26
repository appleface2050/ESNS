# coding=utf-8
"""
WSGI config for Need_Server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Need_Server.settings")

from django.core.wsgi import get_wsgi_application

from django.core.management import execute_from_command_line
# 自动执行collectstatic
# by: 范俊伟 at:2015-06-23
try:
    execute_from_command_line(['manage.py', 'collectstatic','--noinput'])
except Exception, e:
    print str(e)

application = get_wsgi_application()
