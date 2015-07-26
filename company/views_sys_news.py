#coding=utf-8
from django.template import RequestContext
import time
from company.models import SysNews, SysColumn, CompanyNews, CompanyColumn

__author__ = 'wangjian'
from django.shortcuts import render_to_response, get_object_or_404


def show_sys_news(request, column_id, news_id):
    """
    显示新闻，手机端系统新闻
    by:王健 at:2015-06-17
    :param request:
    :param column_id:
    :param news_id:
    :return:
    """
    news = get_object_or_404(SysNews, pk=news_id, sys_column_id=column_id)
    if news:
        news.add_pv()
    return render_to_response('cp_manage/phone/news.html', RequestContext(request, {'news': news.toJSON()}))


def show_sys_news_look(request, column_id, news_id):
    """
    系统新闻预览
    by:王健 at:2015-06-27
    :param request:
    :param column_id:
    :param news_id:
    :return:
    """
    news = get_object_or_404(SysNews, pk=news_id, sys_column_id=column_id)
    news = news.toJSON()
    if not news['is_active']:
        news['title'] = news['pre_title']
        news['content'] = news['pre_content']
    return render_to_response('cp_manage/phone/news.html', RequestContext(request, {'news': news, 'is_debug': True, 't': int(time.time())}))


def show_news(request, column_id, news_id, company_id=None):
    """
    公司新闻
    by:王健 at:2015-06-19
    增加pv +1
    by：尚宗凯 at：2015-06-22
    :param request:
    :param column_id:
    :param news_id:
    :return:
    """
    news = get_object_or_404(CompanyNews, pk=news_id, company_id=company_id, company_column_id=column_id)
    if news:
        news.add_pv()
    return render_to_response('cp_manage/phone/company_news.html', RequestContext(request, {'news': news.toJSON()}))


def show_news_noreplay(request, column_id, news_id, company_id=None):
    """
    公司无评论的新闻界面
    by:王健 at:2015-06-27
    :param request:
    :param column_id:
    :param news_id:
    :return:
    """
    news = get_object_or_404(CompanyNews, pk=news_id, company_id=company_id, company_column_id=column_id)
    if news:
        news.add_pv()
    return render_to_response('cp_manage/phone/company_news_noreplay.html', RequestContext(request, {'news': news.toJSON()}))


def show_news_look(request, column_id, news_id, company_id=None):
    """
    公司新闻预览
    by:王健 at:2015-06-27
    :param request:
    :param column_id:
    :param news_id:
    :return:
    """
    news = get_object_or_404(CompanyNews, pk=news_id, company_id=company_id, company_column_id=column_id)
    news = news.toJSON()
    if not news['is_active']:
        news['title'] = news['pre_title']
        news['content'] = news['pre_content']
    return render_to_response('cp_manage/phone/company_news.html', RequestContext(request, {'news': news, 'is_debug': True, 'is_debug': True, 't': int(time.time())}))


def get_company_button_html_by_flag(request, company_id=None, flag=None):
    """
    返回html页面
    by：尚宗凯 at：2015-06-17
    改了一下
    by：尚宗凯 at：2015-06-17
    公司首页按钮的html
    by:王健 at:2015-06-19
    迁移位置
    by:王健 at:2015-06-19
    改用RequestContext
    by:王健 at:2015-06-19
    设置企业综合管理的界面
    by:王健 at:2015-06-22
    优化综合管理的显示
    by:王健 at:2015-06-23
    修改栏目排序
    by:王健 at:2015-06-27
    增加html的title字段
    by：尚宗凯 at：2015-06-27
    去掉title
    by：尚宗凯 at：2015-06-27
    未发布的新闻不显示
    by:王健 at:2015-06-30
    对企业咨询优化
    by:王健 at:2015-07-01
    企业咨询优化显示
    by:王健 at:2015-07-02
    """
    # flag = request.REQUEST.get("flag","")

    company_column = CompanyColumn.objects.get(company_id=company_id, flag=flag).toJSON()
    current_column = company_column
    if company_column['father']:
        father_column = CompanyColumn.objects.get(pk=current_column.get('father')).toJSON()
        columns = [x.toJSON() for x in CompanyColumn.objects.filter(company_id=company_id, father_id=company_column['father']).order_by('index_num')]
    else:
        father_column = current_column
        columns = [x.toJSON() for x in CompanyColumn.objects.filter(company_id=company_id, father__flag=flag).order_by('index_num')]
        if len(columns) > 0:
            current_column = columns[0]

    if flag == 'ZONGHEGUANLI':
        return render_to_response('cp_manage/phone/company_xzgl.html', RequestContext(request, {"columnslist": columns, "column": father_column, 'company_id': company_id}))
    if current_column.get("columntype") == 0:
        news = [x.toJSON() for x in CompanyNews.objects.filter(company_id=company_id, company_column_id=current_column.get('id'), is_active=True)[:1]]
        if len(news) > 0:
            news = news[0]
        else:
            news = {}
        return render_to_response('cp_manage/phone/company_column_news.html', RequestContext(request, {"columnslist": columns, "news": news, "column": current_column, 'father_column': father_column}))
    news = [x.toJSON() for x in CompanyNews.objects.filter(company_id=company_id, company_column_id=current_column.get('id'), is_active=True)[:20]]
    if flag == 'QIYEZIXUN':
        return render_to_response('cp_manage/phone/company_news_list.html', RequestContext(request, {"columnslist": columns, "newslist": news, "column": current_column, 'father_column': father_column}))
    return render_to_response('cp_manage/phone/company_column_index.html', RequestContext(request, {"columnslist": columns, "newslist": news, "column": current_column, 'father_column': father_column}))


def show_index_news(request, column_id=None, company_id=None):
    """
    显示新闻栏目列表,有无栏目兼容
    by:王健 at:2015-06-18
    修改新闻列表页
    by:王健 at:2015-06-19
    优化显示综合管理的界面
    by:王健 at:2015-06-27
    :param request:
    :return:
    """
    current_column = CompanyColumn.objects.get(company_id=company_id, id=column_id).toJSON()

    news = [x.toJSON() for x in CompanyNews.objects.filter(company_id=company_id, company_column_id=current_column.get('id'))[:20]]

    return render_to_response('cp_manage/phone/zongheguanli_news_list.html', RequestContext(request, {"newslist": news, "column": current_column}))


def show_sys_index_news(request, column_id=None, company_id=None):
    """
    显示新闻栏目列表,有无栏目兼容
    by:王健 at:2015-06-18
    优化排序
    by:王健 at:2015-07-02
    :param request:
    :return:
    """
    sys_columns = [x.toJSON() for x in SysColumn.objects.filter(is_active=True).order_by('index_num')]
    newslist = []
    if len(sys_columns) > 0:
        if column_id:
            column = SysColumn.objects.get(pk=column_id).toJSON()
            newslist = [x.toJSON() for x in SysNews.objects.filter(is_active=True, sys_column_id=column.get('id')).order_by('-publish_time')[:20]]
        else:
            column = sys_columns[0]
            newslist = [x.toJSON() for x in SysNews.objects.filter(is_active=True, sys_column_id=column.get('id')).order_by('-publish_time')[:20]]

    return render_to_response('cp_manage/phone/sys_news_list.html', RequestContext(request, {'newslist': newslist, 'columnslist': sys_columns, 'column': column}))
