# coding=utf-8
# Date: 15/2/4'
# Email: wangjian2254@icloud.com
import datetime
from django.utils import timezone
from django.conf import settings
from util.jsonresult import is_success_mongodb_result
from django.db.models import Sum

#mysql
from models import NSJiFen

__author__ = u'王健'
#
# s = db.schedule.find_one({'_id': pk})
# result = db.schedule.update({"_id": pk}, {"$set": ups})
# q = db.schedule.find({"org": get_current_org().get('oid'),
#                                       "$or": [
#                                           {"enddate": {"$lt": outoftime_str}, 'status': {"$lt": 4},
#                                            "project": {"$in": projectids}},
#                                           {"enddate": {"$lt": outoftime_str}, 'status': {"$lt": 4},
#                                            "department": departid},
#                                             {"date": {"$lt": outoftime_str}, 'status': {"$lt": 4},
#                                            "project": {"$in": projectids}},
#                                           {"date": {"$lt": outoftime_str}, 'status': {"$lt": 4},
#                                            "department": departid},
#                                       ]
#                 })

LOGIN_JIFEN = '%s_%s_login'
LEIJI_JIFEN = '%s_%s_%s_leiji'
LEIJILIST_KEY = 'leijilist'
LOGINLIST_KEY = 'loginlist'

def login_jifen2(request, date=None):
    """
    连续登陆 产生积分
    by:王健 at:2015-2-4
    优化登录送积分，兼容测试
    by:王健 at:2015-2-5
    屏蔽mongodb
    by:王健 at:2015-3-8
    优化 settings 的配置
    by:王健 at:2015-3-9
    :return:
    """
    from mango import database as db
    uid = request.user.pk
    if date == None:
        date = timezone.now()
    jifen_id = LOGIN_JIFEN % (uid, date.strftime('%Y%m%d'))
    if not hasattr(request.session, jifen_id):
        if not hasattr(request.session, LOGINLIST_KEY):
            request.session[LOGINLIST_KEY] = []
        if jifen_id not in request.session[LOGINLIST_KEY]:
            request.session[LOGINLIST_KEY].append(jifen_id)
        login_data = db.jifen.find_one({'_id': jifen_id})
        if not login_data:
            pre_date = date + datetime.timedelta(days=-1)
            pre_jifen_id = LOGIN_JIFEN % (uid, pre_date.strftime('%Y%m%d'))
            pre_login_data = db.jifen.find_one({'_id': pre_jifen_id})
            if not pre_login_data:
                days = 1
                fen = settings.LOGIN_MAX_DAYS_FEN
            else:
                days = pre_login_data.get('days', 0) + 1
                if days > settings.LOGIN_MAX_DAYS:
                    fen = settings.LOGIN_MAX_DAYS * settings.LOGIN_MAX_DAYS_FEN
                else:
                    fen = days * settings.LOGIN_MAX_DAYS_FEN
            login_data = {'_id': jifen_id, 'days': days, 'type': 'login', 'fen': fen}
            result = db.jifen.insert(login_data)
            if is_success_mongodb_result(result):
                request.session[jifen_id] = jifen_id
                return True, fen, u'连续登录%s天，奖励%s积分' % (days, fen)
        else:
            request.session[jifen_id] = jifen_id
    else:
        if hasattr(request.session, LOGINLIST_KEY) and len(request.session[LOGINLIST_KEY]) > 1:
            for jid in request.session[LOGINLIST_KEY]:
                if jifen_id != jid:
                    del request.session[jid]
            request.session[LOGINLIST_KEY] = [jifen_id]
    return False, 0, u''

def login_jifen(request, date=None):
    """
    连续登陆 产生积分 mysql
    by:尚宗凯 at:2015-3-7
    优化 settings 的配置
    by:王健 at:2015-3-9
    积分暂停开发
    by:王健 at:2015-06-29
    :param request:
    :param date:
    :return:
    """
    return False, 0, u''
    uid = request.user.pk
    if not date:
        date = timezone.now()
    jifen_id = LOGIN_JIFEN % (uid, date.strftime('%Y%m%d'))
    if not hasattr(request.session, jifen_id):
        if not hasattr(request.session, LOGINLIST_KEY):
            request.session[LOGINLIST_KEY] = []
        if jifen_id not in request.session[LOGINLIST_KEY]:
            request.session[LOGINLIST_KEY].append(jifen_id)
        try:
            login_data = NSJiFen.objects.get(id=jifen_id)
            if login_data:
                request.session[jifen_id] = jifen_id
        except NSJiFen.DoesNotExist:
            pre_date = date + datetime.timedelta(days=-1)
            pre_jifen_id = LOGIN_JIFEN % (uid, pre_date.strftime('%Y%m%d'))
            try:
                pre_login_data = NSJiFen.objects.get(id=pre_jifen_id)
                days = pre_login_data.toJSON().get('days', 0) + 1
                if days > settings.LOGIN_MAX_DAYS:
                    fen = settings.LOGIN_MAX_DAYS * settings.LOGIN_MAX_DAYS_FEN
                else:
                    fen = days * settings.LOGIN_MAX_DAYS_FEN
            except NSJiFen.DoesNotExist:
                days = 1
                fen = settings.LOGIN_MAX_DAYS_FEN

            jf = NSJiFen()
            jf.id = jifen_id
            jf.days = days
            jf.type = 'login'
            jf.fen = fen
            jf.save()
            request.session[jifen_id] = jifen_id
            return True, fen, u'连续登录%s天，奖励%s积分' % (days, fen)

    else:
        if hasattr(request.session, LOGINLIST_KEY) and len(request.session[LOGINLIST_KEY]) > 1:
            for jid in request.session[LOGINLIST_KEY]:
                if jifen_id != jid:
                    del request.session[jid]
            request.session[LOGINLIST_KEY] = [jifen_id]
    return False, 0, u''

def create_data_jifen2(request, jifentype, date=None):
    """
    因为创建了数据而获得积分
    by:王健 at:2015-2-4
    优化累计积分，兼容测试
    by:王健 at:2015-2-5
    屏蔽mongodb
    by:王健 at:2015-3-8
    优化 settings 的配置
    by:王健 at:2015-3-9
    :param request:
    :param jifentype: 发送数据的来的积分还是分享的来的积分
    :return:
    """
    from mango import database as db
    uid = request.user.pk
    if date == None:
        date = timezone.now()
    jifen_id = LEIJI_JIFEN % (uid, date.strftime('%Y%m%d'), jifentype)

    value = settings.LEIJI_MAX.get(jifentype)[0]
    maxvalue = settings.LEIJI_MAX.get(jifentype)[1]
    message = settings.LEIJI_MAX.get(jifentype)[2]
    if not hasattr(request.session, jifen_id) or str(request.session[jifen_id]) < maxvalue:
        if not hasattr(request.session, LEIJILIST_KEY):
            request.session[LEIJILIST_KEY] = []
        if jifen_id not in request.session[LEIJILIST_KEY]:
            request.session[LEIJILIST_KEY].append(jifen_id)
        login_data = db.jifen.find_one({'_id': jifen_id})
        if not login_data:
            login_data = {'_id': jifen_id, 'type': jifentype, 'fen': value}
            result = db.jifen.insert(login_data)
            if is_success_mongodb_result(result):
                request.session[jifen_id] = value
                #todo: 提示文字需要优化
                return True, value, message % value
        else:
            if login_data.get('fen', 0) < maxvalue:
                login_data['fen'] = login_data.get('fen', 0) + value
                result = db.jifen.update({"_id": jifen_id}, {"$set": {'fen': login_data.get('fen', 0)}})
                if is_success_mongodb_result(result):
                    request.session[jifen_id] = login_data['fen']
                    #todo: 提示文字需要优化
                    return True, value, message % value
            else:
                request.session[jifen_id] = maxvalue
    else:
        if hasattr(request.session, LEIJILIST_KEY) and len(request.session[LEIJILIST_KEY]) > 1:
            for jid in request.session[LEIJILIST_KEY]:
                if jifen_id != jid:
                    del request.session[jid]
            request.session[LEIJILIST_KEY] = [jifen_id]
    return False, 0, u''

def create_data_jifen(request, jifentype, date=None):
    """
    因为创建了数据而获得积分 mysql
    by:尚宗凯 at:2015-3-7
    优化 settings 的配置
    by:王健 at:2015-3-9
    暂停积分
    by:王健 at:2015-06-26
    :param request:
    :param jifentype:
    :param date:
    :return:
    """
    return False, 0, u''
    uid = request.user.pk
    if date == None:
        date = timezone.now()
    jifen_id = LEIJI_JIFEN % (uid, date.strftime('%Y%m%d'), jifentype)

    value = settings.LEIJI_MAX.get(jifentype)[0]
    maxvalue = settings.LEIJI_MAX.get(jifentype)[1]
    message = settings.LEIJI_MAX.get(jifentype)[2]

    if not hasattr(request.session, jifen_id) or request.session[jifen_id] < maxvalue:
        if not hasattr(request.session, LEIJILIST_KEY):
            request.session[LEIJILIST_KEY] = []
        if jifen_id not in request.session[LEIJILIST_KEY]:
            request.session[LEIJILIST_KEY].append(jifen_id)
        try:
            login_data = NSJiFen.objects.get(id=jifen_id)
            if login_data.fen < maxvalue:
                login_data.fen += value
                login_data.save()
                return True, value, message % value
            else:
                request.session[jifen_id] = maxvalue
        except NSJiFen.DoesNotExist:
            jf = NSJiFen()
            jf.id = jifen_id
            jf.type = 'login'
            jf.fen = value
            jf.save()
            request.session[jifen_id] = value
            return True, value, message % value
    else:
        if hasattr(request.session, LEIJILIST_KEY) and len(request.session[LEIJILIST_KEY]) > 1:
            for jid in request.session[LEIJILIST_KEY]:
                if jifen_id != jid:
                    del request.session[jid]
            request.session[LEIJILIST_KEY] = [jifen_id]
    return False, 0, u''

# from bson.code import Code
# MAPPER = Code("""
#     function () {
#         emit(1, this.fen);
#     }
# """)
#
# SUB_FEN_FUN = Code("""
# function (key, values) {
#       var x = 0;
#     values.forEach(function(v) { x += v });
#     return x;
#     }
# """)

def query_fen_by_uid2(request, date=None, test=False):
    """
    根据用户查询积分值
    by:王健 at:2015-2-5
    屏蔽mongodb
    by:王健 at:2015-3-8
    :param request:
    :return:
    """
    from mango import database as db
    uid = request.user.pk
    if date == None:
        date = timezone.now()
    max_key = '%s_%s_' % (uid, date.strftime('%Y%m%d'))
    jifen_data = db.jifenresult.find_one({'_id': uid})
    if jifen_data:
        pre_key = jifen_data.get('key')
        pre_date_str = pre_key.split('_')[1]
        pre_date = datetime.datetime(int(pre_date_str[:4]), int(pre_date_str[4:6]), int(pre_date_str[6:8]))
        pre_key = '%s_%s_' % (uid, (pre_date).strftime('%Y%m%d'))
        query = {'_id': {'$lt': max_key, '$gt': pre_key}}
    else:
        pre_key = None
        jifen_data = {}
        query = {'_id': {'$lt': max_key, '$gt': '%s_%s_' % (uid, 0)}}
    if pre_key != max_key:
        if test:
            print '-------'
            print query
            for doc in db.jifen.find(query):
                print doc
        result = db.jifen.map_reduce(MAPPER, SUB_FEN_FUN, 'resultjifen', query=query)
        result_jifen_data = result.find_one()
        if not result_jifen_data:
            result_jifen_data = {}
        if jifen_data and result_jifen_data:
            r = db.jifenresult.update({"_id": uid}, {"$set": {'fen': result_jifen_data.get('value', 0) + jifen_data.get('fen', 0), 'key': max_key}})
        if not jifen_data and result_jifen_data:
            r = db.jifenresult.insert({"_id": uid, 'fen': result_jifen_data.get('value', 0), 'key': max_key})
    else:
        result_jifen_data = {}
    todayresult = db.jifen.map_reduce(MAPPER, SUB_FEN_FUN, 'resultjifen', query={'_id': {'$gt': max_key, '$lt': '%s_%s_' % (uid, 3)}})
    todayresult_data = todayresult.find_one()
    if not todayresult_data:
        todayresult_data = {}
    if test:
        print max_key, ':', '%s_%s_%s' % (jifen_data.get('fen', 0), result_jifen_data.get('value', 0), todayresult_data.get('value', 0))
    return jifen_data.get('fen', 0) + result_jifen_data.get('value', 0) + todayresult_data.get('value', 0)

def query_fen_by_uid(request, date=None, test=False):
    """
    根据用户查询积分值 mysql
    by:尚宗凯 at:2015-3-7
    :param request:
    :return:
    """
    uid = request.user.pk
    if not date:
        date = timezone.now()

    all_jifen_data = NSJiFen.objects.filter(id__gt="%s_1" % str(uid), id__lt="%s_3" % str(uid)).aggregate(Sum('fen'))
    fen = all_jifen_data['fen__sum']
    if fen:
        return fen
    else:
        return 0

def remove_fen():
    """
    删除积分，单元测试专用
    by:王健 at:2015-2-5
    测试后清理mongodb的数据库
    by:王健 at:2015-2-25
    屏蔽mongodb
    by:王健 at:2015-3-8
    :return:
    """
    from mango import database as db
    db.jifen.remove()
    db.jifenresult.remove()
    db.filereplay.remove()

