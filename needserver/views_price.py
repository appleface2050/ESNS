# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import datetime
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from needserver.models import Project, ProjectRechargeRecord
from util.jsonresult import getResult
from django.conf import settings


__author__ = u'王健'

#
# def auto_price(request):
#     """
#     自动扣款记录,添加事务管理
#     by:王健 at:2015-03-10
#     """
#     nowdate = timezone.now() - datetime.timedelta(days=1)
#     nowdate2 = timezone.now()
#     if settings.DEBUG:
#         days = int(request.REQUEST.get('days', '0'))
#         nowdate = nowdate + datetime.timedelta(days=days)
#         nowdate2 = nowdate2 + datetime.timedelta(days=days)
#
#     project_num = 0
#     pay_num = 0
#     project_close_num = 0
#     for project in Project.objects.filter(is_active=True).exclude(projectpayment__date__gt=nowdate):
#         record_list = ProjectRechargeRecord.objects.filter(project_id=project.pk, date__lt=nowdate2).order_by('-date')[:1]
#         if len(record_list) > 0:
#             pre = record_list[0]
#             price_sum = ProjectPayment.objects.filter(project_id=project.pk, date__gt=pre.date).aggregate(Sum('price'))
#             members = project.person_set.filter(is_active=True).count()
#             price = price_sum['price__sum']
#             if not price:
#                 price = 0
#             try:
#                 with transaction.atomic():
#                     if pre.price2 <= price:
#                         project.is_active = False
#                         project.save()
#                         project_close_num += 1
#                     else:
#                         payment = ProjectPayment()
#                         payment.project = project
#                         payment.date = nowdate2
#                         payment.members = members
#                         payment.price = payment.members
#                         payment.pay_cause = 0
#                         payment.save()
#                         pay_num += 1
#             except:
#                 pass
#         else:
#             try:
#                 with transaction.atomic():
#                     project.is_active = False
#                     project.save()
#                     project_close_num += 1
#             except:
#                 pass
#         project_num += 1
#
#     return getResult(True, u'获取天气信息', u'project_num:%s, pay_num:%s, project_close_num:%s' % (project_num, pay_num, project_close_num))




