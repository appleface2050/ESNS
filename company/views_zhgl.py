#coding=utf-8
import json
from django.template import RequestContext
import time
from company.models import SysNews, SysColumn, CompanyNews, CompanyColumn
from nsbcs.models import ComFile
from util.jsonresult import getResult
from django.conf import settings

__author__ = 'wangjian'
from django.shortcuts import render_to_response, get_object_or_404


def show_zhgl_list_html(request, column_id=None, company_id=None):
    """
    综合管理列表显示
    by:王健 at:2015-07-01
    显示列名
    by:王健 at:2015-07-03
    :param request: 
    :param column_id: 
    :param company_id: 
    :return:
    """
    column = CompanyColumn.objects.get(company_id=company_id, pk=column_id)

    return render_to_response('cp_manage/phone/company_gonggaotongzhi.html', RequestContext(request, {"company_id": company_id, "column_id": column_id, 'column': column}))


def show_zhgl_list(request, column_id=None, company_id=None):
    """
    综合管理列表显示
    by:王健 at:2015-07-01
    :param request:
    :param column_id:
    :param company_id:
    :return:
    """
    page_start = int(request.REQUEST.get('page_start', '0'))
    newsquery = CompanyNews.objects.filter(company_id=company_id, company_column_id=column_id, is_active=True).order_by('-publish_time')
    l = []
    for n in newsquery[page_start:page_start+20]:
        d = n.toJSON2()
        if d['files'] and d['type_flag'] == 'files' and len(d['files']) == 1:
            try:
                f = ComFile.objects.get(pk=d['files'][0])
                d['files_url'] = f.get_url()
                d['files_image_url'] = '%scp_manage/phone/images/%s.png' % (settings.STATIC_URL, f.filetype)
            except:
                pass
        l.append(d)
    return getResult(True, u'', l)


def show_zhgl_news(request, column_id=None, company_id=None):
    """
    综合管理列表显示
    by:王健 at:2015-07-01
    :param request:
    :param column_id:
    :param company_id:
    :return:
    """
    page_start = int(request.REQUEST.get('page_start', '0'))
    newsquery = CompanyNews.objects.filter(company_id=company_id, company_column_id=column_id, is_active=True).order_by('-publish_time')
    l = []
    for n in newsquery[page_start:page_start+20]:
        l.append(n.toJSON2())
    return getResult(True, u'', l)


def show_zhgl_news_html(request, column_id=None, company_id=None, news_id=None):
    """
    综合管理列表显示
    by:王健 at:2015-07-01
    :param request:
    :param column_id:
    :param company_id:
    :return:
    """
    news = CompanyNews.objects.get(pk=news_id, company_id=company_id, company_column_id=column_id)

    if news.type_flag == 'news':
        news = news.toJSON()
        return render_to_response('cp_manage/phone/company_news_noreplay.html', RequestContext(request, {'news': news}))
    elif news.type_flag == 'files':
        pks = []
        if news.files:
            pks = json.loads(news.files)
        fileslist = []
        for f in ComFile.objects.filter(pk__in=pks):
            fileslist.append({'url': f.get_url(), 'name': f.name, 'type': f.filetype})
        news = news.toJSON()
        news['fileslist'] = fileslist
        return render_to_response('cp_manage/phone/company_news_files_noreplay.html', RequestContext(request, {'news': news}))
    else:
        return render_to_response('cp_manage/phone/company_news_noreplay.html', RequestContext(request, {'news': news}))


def create_project_html(request, company_id=None):
    """
    创建企业界面
    by:王健 at:2015-07-02
    :param request:
    :param company_id:
    :return:
    """
    return render_to_response('cp_manage/phone/company_create_project.html', RequestContext(request, {'company_id': company_id}))
