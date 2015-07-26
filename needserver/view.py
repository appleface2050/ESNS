# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import datetime
import urllib2
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from needserver.init_group_prower import init_prower_by_group
from needserver.models import Group, ProjectRechargeRecord, Project, NSUser, NSJiFen, FileRecord, EngineCheck
from needserver.add_shuihu_data import add_shuihu_user as add_shuihu_user_fun
from needserver.add_shuihu_data import update_shuihu_data as update_shuihu_data_fun
from nsbcs.models import BaseFile, File
import qiniu
from qiniu.services.storage import uploader
from qiniu import BucketManager
from util.aliyun_search import AliyunSearch
from util.jsonresult import getResult
from util.loginrequired import client_admin_login_required
from Need_Server.settings import QN_AK, QN_SK, QN_FILE_BUCKET_DOMAIN, QN_FRIENDS_ICON_BUCKET_DOMAIN, QN_PROJECT_ICON_BUCKET_DOMAIN
from util.cache_handle import get_project_user_group_use_cache, get_user_activity

__author__ = u'王健'

def init_group_power(request):
    gs = Group.objects.all()
    for g in gs:
        init_prower_by_group(g)
        g.save()
    return HttpResponse('')

#增加水浒测试项目初始化内容
#by：尚宗凯 at：2015-04-15
def add_shuihu_user(request):
    add_shuihu_user_fun()
    return HttpResponse('success')

def add_shuihu_sglog(request):
    return HttpResponse('success')

#修改水浒内容
#by：尚宗凯 at：2015-04-16
def update_shuihu_data(request):
    update_shuihu_data_fun()
    return HttpResponse("success")

@transaction.atomic()
def add_price_2_project(request):
    """
    测试充值
    by:王健 at:2015-05-08
    :param request:
    :return:
    """
    if settings.ENVIRONMENT != 'aliyun':
        pr = ProjectRechargeRecord()
        pr.project = Project.objects.get(pk=49)
        pr.date = timezone.now()
        pr.order_id = None
        pr.price0 = 10
        pr.price_type = 1
        pr.save(sysmessage=1)
    return HttpResponse("success")


def search(request):
    """
    阿里开放搜索
    by：尚宗凯 at：2015-05-15
    """
    search_flag = request.REQUEST.get('search_flag')
    query = request.REQUEST.get('query')
    if not search_flag:
        return getResult(False, u'search_flag参数未填')
    result = AliyunSearch.query(index_name=search_flag, table_name=search_flag, query=query)
    return getResult(True, u'搜索成功', result)


@client_admin_login_required
def export_excel_jifen(request):
    """
    积分导出
    by:王健 at:2015-05-21
    只统计可用用户
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    import xlwt
    userlist = NSUser.objects.filter(is_active=True)
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'导出结果')

    # ri = 0
    # ci = 0
    # for c in VRealNameHistory.export_list_name:
    #     ws.write(0, ci, c)
    #     ci += 1
    # ri = 1
    # for r in query_set:
    #     ci = 0
    #     for c in r.export_data_to_list():
    #         ws.write(ri, ci, c)
    #         ci += 1
    #     ri += 1


    ws.write(0, 0, u'手机号')
    ws.write(0, 1, u'昵称')
    ws.write(0, 2, u'积分')
    for i, user in enumerate(userlist):
        fen_dict = NSJiFen.objects.filter(id__startswith='%s_' % user.id).aggregate(Sum('fen'))
        ws.write(i+1, 0, user.tel)
        ws.write(i+1, 1, user.name)
        ws.write(i+1, 2, fen_dict['fen__sum'])
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = u'Need客户积分.xls'
    response['Content-Disposition'] = (u'attachment; filename=%s' % (filename)).encode('utf-8')
    wb.save(response)
    return response


# @client_admin_login_required
def show_tongji_page(request):
    return render_to_response('needserver/tongji.html', RequestContext(request, {'date': datetime.datetime.now()}))


def get_date_by_request(request, date_key='date'):
    date = request.REQUEST.get(date_key, datetime.datetime.now())
    if isinstance(date, (str, unicode)):
        date = datetime.datetime.strptime(date, '%Y%m%d')
    return date


@client_admin_login_required
def commit_user_total(request):
    """
    获取用户总数，基于某一天
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    date = get_date_by_request(request)
    count = NSUser.objects.filter(create_time__lt=date + datetime.timedelta(days=1), is_active=True).count()

    return getResult(True, u'', count)


@client_admin_login_required
def commit_user_count_by_date(request):
    """
    获取某一天的注册用户数量
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    date = get_date_by_request(request)
    count = NSUser.objects.filter(create_time__gt=date, create_time__lt=date + datetime.timedelta(days=1), is_active=True).count()
    return getResult(True, u'', count)


@client_admin_login_required
def commit_user_jifen_by_date(request):
    """
    查询某日到某日的注册人员的积分详情
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    start_date = get_date_by_request(request, 'start_date')
    end_date = get_date_by_request(request, 'end_date')

    userlist = NSUser.objects.filter(create_time__gt=start_date, create_time__lt=end_date + datetime.timedelta(days=1), is_active=True)
    l = []
    for user in userlist:
        fen_dict = NSJiFen.objects.filter(id__startswith='%s_' % user.id).aggregate(Sum('fen'))
        l.append({'tel': user.tel, 'name': user.name, 'jifen': fen_dict['fen__sum']})
    return getResult(True, u'', l)


@client_admin_login_required
def commit_project_by_date(request):
    """
    查询某日到某日的新建项目列表
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    start_date = get_date_by_request(request, 'start_date')
    end_date = get_date_by_request(request, 'end_date')

    projectlist = Project.objects.filter(create_time__gt=start_date, create_time__lt=end_date + datetime.timedelta(days=1), is_active=True)

    l = []
    for p in projectlist:
        l.append({'date': p.create_time.strftime('%Y-%m-%d'), 'name': p.total_name, 'manager': p.manager.name, 'tel': p.manager.tel, 'num': p.person_set.filter(is_active=True).count()})

    return getResult(True, u'', l)


@client_admin_login_required
def commit_jifen_paiming_by_jifen(request):
    """
    查询某积分以上的人员有多少，占总人数百分比
    by:王健 at:2015-05-26
    :param request:
    :return:
    """
    fen = int(request.REQUEST.get('fen', '0'))
    userlist = NSUser.objects.filter(is_active=True)
    num1 = 0
    num2 = userlist.count()
    for i, user in enumerate(userlist):
        fen_dict = NSJiFen.objects.filter(id__startswith='%s_' % user.id).aggregate(Sum('fen'))
        if fen_dict['fen__sum'] >= fen:
            num1 += 1
    return getResult(True, u'', {'num1': num1, 'total': num2, 'per': '%.2f' % ((num1*1.0/num2)*100), 'per_str': '%.2f%%' % ((num1*1.0/num2)*100)})


def tmp_bae_to_qiniu(request):
    """
    增加用于倒图片的临时接口
    by：尚宗凯 at：2015-06-03
    """
    delete_qiniu_pic_where_file_status_is_false()
    bcs_pic_to_qiniu()
    cal_scale()
    return getResult(True, "success")


def bcs_pic_to_qiniu(request):
    """
    把bcs图片弄到七牛上面
    by：尚宗凯 at：2015-06-03
    修改为数据流上传
    by：尚宗凯 at：2015-06-03
    优化bucket
    by：尚宗凯 at：2015-06-03
    修改文件存在下的逻辑
    by：尚宗凯 at：2015-06-03
    """
    bf = BaseFile.objects.all()
    for i in bf:
        if i.bucket in ("projectfiles","pubfriendsicon","pubproject"):
        # if i.bucket in ("qn-projectfiles"):
            url = i.get_url()
            if not url.startswith("http://bcs.duapp.com/"):
                if i.bucket == 'projectfiles':
                    bucket = 'qn-projectfiles'
                elif i.bucket == 'pubfriendsicon':
                    bucket = 'qn-pubfriendsicon'
                elif i.bucket == 'pubproject':
                    bucket = 'qn-pubproject'
                i.bucket = bucket
                i.save()
            else:
                #下载
                # print url
                try:
                    conn = urllib2.urlopen(url)
                    # localfile = ""
                    # tmp = i.fileurl.strip().split("/")
                    # if len(tmp) == 3:
                    #     project_id = tmp[1]
                    #     pic_name = tmp[2]
                        # localfile = save_path+project_id+"_"+pic_name
                        # localfile = project_id+"_"+pic_name

                        # conn.read()
                        # f = open(localfile,'wb')
                        # f.write(conn.read())
                        # f.close()

                    #上传
                    # data = conn.read()
                    qn_auth = qiniu.Auth(QN_AK, QN_SK)
                    if i.bucket == 'projectfiles':
                        bucket = 'qn-projectfiles'
                    elif i.bucket == 'pubfriendsicon':
                        bucket = 'qn-pubfriendsicon'
                    elif i.bucket == 'pubproject':
                        bucket = 'qn-pubproject'
                    token = qn_auth.upload_token(bucket, expires=3600 * 24)
                    key = i.fileurl
                    ret, info = uploader.put_data(token, key, conn.read(), mime_type="application/octet-stream", check_crc=True)
                    if info.status_code == 614:
                        i.bucket = bucket
                        i.save()
                    else:
                        # assert ret['key'] == key
                        i.bucket = bucket
                        i.save()
                        # 验证文件是否能打开
                        # if bucket == 'qn-projectfiles':
                        #     base_url = QN_FILE_BUCKET_DOMAIN + key
                        # elif bucket == 'pubfriendsicon':
                        #     base_url = QN_FRIENDS_ICON_BUCKET_DOMAIN + key
                        # elif i.bucket == 'pubproject':
                        #     base_url = QN_PROJECT_ICON_BUCKET_DOMAIN + key
                        # private_url = qn_auth.private_download_url(base_url, expires=3600)
                        # print "private_url:",private_url
                except Exception as e:
                    print e
    return getResult(True, "success")

                # ret, info = uploader.put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
                # if os.path.exists(localfile):
                #     os.remove(localfile)
                # if info.status_code == 614:
                #     pass
                # else:
                #     assert ret['key'] == key
                #     i.bucket = "qn-projectfiles"
                #     i.save()


def delete_qiniu_pic_where_file_status_is_false(request):
    """
    把七牛上面图片失效的删掉，数据库的删掉
    by：尚宗凯 at：2015-06-03
    修改用于只删除七牛的数据
    by：尚宗凯 at：2015-06-04
    """
    bf = BaseFile.objects.filter(file_status=0)
    for f in bf:
        #删除
        if f.bucket in ("qn-projectfiles","qn-pubfriendsicon","qn-pubproject"):
            key = f.fileurl
            q = qiniu.Auth(QN_AK, QN_SK)
            bucket = BucketManager(q)
            # ret, info = bucket.stat(, key)
            ret, info = bucket.delete(f.bucket, key)
            # print(info)
            # assert ret is None
            # assert info.status_code == 612
            f.delete()
    return getResult(True, "success")

    # bf = BaseFile.objects.filter(file_status=0)
    # for f in bf:
    #     key = f.fileurl
    #     q = qiniu.Auth(QN_AK, QN_SK)
    #     bucket = BucketManager(q)
    #     ret, info = bucket.delete(f.bucket, key)
    # return getResult(True, "success")

def cal_scale(request):
    """
    计算比值
    by:尚宗凯 at：2015-06-03
    """
    enginechecks = EngineCheck.objects.all()
    for ec in enginechecks:
        if ec.pre_pic_scale is None:
            if File.objects.filter(pk=ec.pre_pic_id).exists():
                fileobj = File.objects.get(pk=ec.pre_pic_id)
                try:
                    tmp = fileobj.img_size.strip().split("x")
                    x = float(tmp[0])
                    y = float(tmp[1])
                    ec.pre_pic_scale = "%.02f" % (x/y)
                except Exception as e:
                    print e
        if ec.chuli_pic_scale is None:
            if File.objects.filter(pk=ec.chuli_pic_id).exists():
                fileobj = File.objects.get(pk=ec.chuli_pic_id)
                try:
                    tmp = fileobj.img_size.strip().split("x")
                    x = float(tmp[0])
                    y = float(tmp[1])
                    ec.chuli_pic_scale = "%.02f" % (x/y)
                except Exception as e:
                    print e
        ec.save()

    for i in FileRecord.objects.all():
        if not i.files_scale or i.files_scale == u"[]":
            files_scale = []
            if i.files:
                file_id_list = i.files.strip("[").strip("]").split(",")
                for file_id in file_id_list:
                    if File.objects.filter(pk=file_id).exists():
                        fileobj = File.objects.get(pk=file_id)
                        try:
                            tmp = fileobj.img_size.strip().split("x")
                            x = float(tmp[0])
                            y = float(tmp[1])
                            files_scale.append(float("%.02f" % (x/y)))

                        except Exception as e:
                            print e

                i.files_scale = str(files_scale)
                i.save()
    return getResult(True, "success")


def user_activity(request, project_id):
    """
    获取用户活跃度
    by：尚宗凯 at：2016-06-04
    """
    # now_date = request.REQUEST.get('date', '')
    # days = int(request.REQUEST.get('days', '7'))
    # if not now_date:
    #     now_date = timezone.now()
    # else:
    #     now_date = datetime.datetime.strptime(now_date, "%Y-%m-%d")
    # start_date = now_date - datetime.timedelta(days=days)
    #
    # tody = get_date(1) + datetime.timedelta(days=1)
    # yest = tody - datetime.timedelta(days=1)

    start_date = request.REQUEST.get('start_date', '')
    end_date = request.REQUEST.get('end_date', '')
    tody = time_start(datetime.datetime.now(),'day')

    if end_date:
        end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    else:
        end_date = tody
    if start_date:
        start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    else:
        start_date = end_date - datetime.timedelta(days=7)
    if start_date and end_date and start_date>end_date:
        return getResult(False, u"开始时间不能小于结束时间")

    project_user_group = get_project_user_group_use_cache(project_id)
    user_id_list = []
    for user_list in project_user_group.values():
        user_id_list.extend(user_list)
    user_id_list = list(set(user_id_list))
    # result = {}
    result = []
    for user_id in user_id_list:
        # result[user_id] = get_user_activity(user_id, project_id, start_date, end_date)
        result.append({str(user_id) : get_user_activity(user_id, project_id, start_date, end_date)})
    return getResult(True, u'获取用户活跃度成功', result)


def get_date(self, delta=0):
    date = self.get_argument('date','')
    if date:
        tody = datetime.datetime.strptime(date,'%Y-%m-%d')
    else:
        tody = time_start(datetime.datetime.now()-datetime.timedelta(days=delta),'day')
    return tody

def time_start(d, typ):
    if typ == "hour":
        d -= datetime.timedelta(minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "day":
        d -= datetime.timedelta(hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "week":
        d -= datetime.timedelta(days=d.weekday(),hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    elif typ == "month":
        d -= datetime.timedelta(days=d.day-1,hours=d.hour,minutes=d.minute,seconds=d.second,microseconds=d.microsecond)
    else:
        raise Exception("wrong type %s" % (typ,))
    return d