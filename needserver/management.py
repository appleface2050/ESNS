#coding=utf-8
#Date: 15-1-12
#Time: 上午11:48
import datetime
from django.contrib.auth import models as django_user, get_user_model
from django.utils import timezone

from needserver.models import FileGroup, Project, Group, Person, ProjectApply, SGTQlog, SGlog, UserInfo
import datetime, sys, codecs, random, os
reload(sys)
sys.setdefaultencoding('utf8')
from nsbcs.models import BaseFile
from django.db import connection
from django.conf import settings
from Need_Server.settings import DATABASES

__author__ = u'王健'

from django.db.models import signals
from app_json_file import appitem

def fix_tel(tel):
    '''
    将tel补全3位数字
    by:尚宗凯 at:2015-3-4
    :param tel:
    :return tel:
    '''
    if int(tel)<10:
        return "00"+tel
    elif int(tel)<100:
        return "0"+tel
    else:
        return tel

def create_user_by_tel_name(tel, name, nickname, sex):
    """
    根据电话号用户名生成用户
    y:尚宗凯 at:2015-3-4
    :param tel , name:
    :return:
    """
    user = get_user_model()()
    user.tel = tel
    user.set_password('123456')
    user.name = str(name)
    user.nickname = str(nickname)
    user.save()

    bf = BaseFile()
    tel = tel[1:]
    # bf.fileurl = '/static/headicon/001宋江.jpg'
    bf.name = tel
    bf.fileurl = '/static/headicon/'+bf.name+'.jpg'
    bf.filetype = 'jpg'
    bf.file_status = True
    bf.bucket = 'pubfriendsicon'
    bf.user = user
    bf.save()
    user.icon_url = bf

    assert sex in ('male','female')
    if sex == 'male':
        user.sex = True
    else:
        user.sex = False
    user.save()
    return user

def add_app_by_children(appchildren, filegroup):
    """
    保存应用子节点
    by:王健 at:2015-1-12
    修改Model名字，去除下划线，index改为sorted
    by:王健 at:2015-1-13
    应用节点icon_url 字段
    by:王健 at:2015-1-28
    :param appchildren:
    :param filegroup:
    :return:
    """
    index = 1
    for app in appchildren:
        if not FileGroup.objects.filter(flag=app.get('flag')).exists():
            fgroup = FileGroup()
        else:
            fgroup = FileGroup.objects.get(flag=app.get('flag'))
        fgroup.flag = app.get('flag')
        fgroup.name = app.get('name')
        fgroup.icon = app.get('icon')
        # fgroup.icon_url = '/static/icon/%s' % app.get('icon')
        fgroup.typeflag = app.get('typeflag')
        fgroup.sorted = index
        index += 1
        fgroup.father = filegroup
        fgroup.status = 'sys'
        fgroup.save()
        if app.has_key('children'):
            add_app_by_children(app['children'], fgroup)

def add_default_app(**kwargs):
    """
    保存应用节点，初始化项目使用
    by:王健 at:2015-1-12
    修改Model名字，去除下划线，index改为sorted
    by:王健 at:2015-1-13
    初始化时，添加测试数据
    by:王健 at:2015-1-20
    应用节点icon_url 字段
    by:王健 at:2015-1-28
    初始化 第一个用户 id 自10000起， 失败，直接修改数据库
    by:王健 at:2015-3-6
    数据初始化只在第一次运行
    by: 范俊伟 at:2015-06-29
    :param kwargs:
    :return:
    """
    if FileGroup.objects.all().count() == 0:
        index = 1
        for app in appitem['children']:
            if not FileGroup.objects.filter(flag=app.get('flag')).exists():
                fgroup = FileGroup()
            else:
                fgroup = FileGroup.objects.get(flag=app.get('flag'))
            fgroup.flag = app.get('flag')
            fgroup.name = app.get('name')
            fgroup.icon = app.get('icon')
            # fgroup.icon_url = '/static/icon/%s' % app.get('icon')
            fgroup.typeflag = app.get('typeflag')
            fgroup.sorted = index
            index += 1
            fgroup.status = 'sys'
            fgroup.save()
            if app.has_key('children'):
                add_app_by_children(app['children'], fgroup)

    if Project.objects.all().count() == 0:
        test_data_insert()


signals.post_syncdb.connect(add_default_app,sender=django_user,dispatch_uid='needserver.create_defaultapp')


def create_user(tel):
    """
    根据用户名生成用户
    :param tel:
    :return:
    """
    user = get_user_model()()
    user.tel = tel
    user.set_password('123456')
    user.name = u'测试%s' % tel
    user.save()
    return user

def create_user_no_ceshi(tel):
    """
    根据用户名生成用户
    by:尚宗凯 at:2015-3-17
    :param tel:
    :return:
    """
    user = get_user_model()()
    user.tel = tel
    user.set_password('123456')
    user.name = u'%s' % tel
    user.save()
    return user

def create_project(user, name, totalname):
    """
    创建项目
    by:王健 at:2015-1-21
    恢复total_name 字段
    by:王健 at:2015-2-2
    分组排序字段修改
    by:王健 at:2015-2-3
    创建项目 基础信息,增加社会大众通道
    by:王健 at:2015-2-16
    增加环信群组的属性
    by:王健 at:2015-2-27
    修改负责人长度
    by:王健 at:2015-3-5
    添加默认 地址
    by:王健 at:2015-3-9
    指定超级管理员
    by:王健 at:2015-3-16
    优化初始创建群聊
    by:王健 at:2015-3-20
    取消社会大众 分组
    by:王健 at:2015-4-9
    :param user:
    :return:
    """
    project = Project()
    project.name = name
    project.total_name = totalname
    project.address = 101030100
    project.jzmj = 50000
    project.jglx = u'钢筋'
    project.jzcs = 3
    project.htzj = 455732183
    project.kg_date = '2015-01-10'
    project.days = 433
    project.jsdw = u'建设单位%s' % user.tel
    project.jsdw_fzr = u'负责人%s' % user.tel[-1:]
    project.kcdw = u'勘察单位%s' % user.tel[-1:]
    project.kcdw_fzr = u'勘察%s' % user.tel[-1:]
    project.sjdw = u'设计单位%s' % user.tel[-1:]
    project.sjdw_fzr = u'设计%s' % user.tel[-1:]
    project.sgdw = u'施工单位%s' % user.tel[-1:]
    project.sgdw_fzr = u'施工%s' % user.tel[-1:]
    project.jldw = u'监理单位%s' % user.tel[-1:]
    project.jldw_fzr = u'监理%s' % user.tel[-1:]
    project.manager = user
    project.save()

    person = Person()
    person.user = user


    project.manager = user
    project.save()
    rootgroup = Group()
    rootgroup.user = user
    rootgroup.name = project.total_name
    rootgroup.type = 'root'
    rootgroup.project = project
    rootgroup.save()
    person.project = project
    person.save()

    rootgroup.say_members.add(person.user)

    group = Group()
    group.name = u'管理员'
    group.type = 'sys_manage'
    group.project = project
    group.sorted = 0
    group.save()
    group.say_members.add(person.user)

    group = Group()
    group.name = u'行政主管'
    group.type = 'sys_xzzg'
    group.project = project
    group.sorted = 1
    group.save()

    group = Group()
    group.name = u'建设单位'
    group.type = 'sys_jsdw'
    group.project = project
    group.sorted = 2
    group.save()

    group = Group()
    group.name = u'设计单位'
    group.type = 'sys_sjdw'
    group.project = project
    group.sorted = 3
    group.save()

    group = Group()
    group.name = u'勘察单位'
    group.type = 'sys_kcdw'
    group.project = project
    group.sorted = 4
    group.save()

    group = Group()
    group.name = u'监理单位'
    group.type = 'sys_jldw'
    group.project = project
    group.sorted = 5
    group.save()

    group = Group()
    group.name = u'施工单位'
    group.type = 'sys_sgdw'
    group.project = project
    group.sorted = 6
    group.save()

    group = Group()
    group.name = u'项目经理部'
    group.type = 'sys_xmjl'
    group.project = project
    group.sorted = 7
    group.is_needhx = True
    group.save()
    group.say_members.add(person.user)
    group.save()

    group = Group()
    group.name = u'劳务分包单位'
    group.type = 'sys_lwfbdw'
    group.project = project
    group.sorted = 8
    group.save()

    group = Group()
    group.name = u'专业分包单位'
    group.type = 'sys_zyfbdw'
    group.project = project
    group.sorted = 9
    group.save()

    # group = Group()
    # group.name = u'社会大众通道'
    # group.type = 'sys_shdztd'
    # group.project = project
    # group.sorted = 1000
    # group.save()

    return project

def create_project_detail(user, p_detail):
    """
    创建项目 完全版
    by:尚宗凯 at:2015-3-17
    :param user:
    :param kwargs:
    :return:
    """
    project = Project()
    project.name = p_detail['name']
    project.total_name = p_detail['total_name']
    project.address = p_detail['address']
    project.jzmj = p_detail['jzmj']
    project.jglx = p_detail['jglx']
    project.jzcs = p_detail['jzcs']
    project.htzj = p_detail['htzj']
    project.kg_date = p_detail['kg_date']
    project.days = p_detail['days']

    # project.jsdw = u'建设单位%s' % user.tel
    # project.jsdw_fzr = u'负责人%s' % user.tel[-1:]
    # project.kcdw = u'勘察单位%s' % user.tel[-1:]
    # project.kcdw_fzr = u'勘察%s' % user.tel[-1:]
    # project.sjdw = u'设计单位%s' % user.tel[-1:]
    # project.sjdw_fzr = u'设计%s' % user.tel[-1:]
    # project.sgdw = u'施工单位%s' % user.tel[-1:]
    # project.sgdw_fzr = u'施工%s' % user.tel[-1:]
    # project.jldw = u'监理单位%s' % user.tel[-1:]
    # project.jldw_fzr = u'监理%s' % user.tel[-1:]
    project.jsdw = p_detail['jsdw']
    project.jsdw_fzr = p_detail['jsdw_fzr']
    project.kcdw = p_detail['kcdw']
    project.kcdw_fzr = p_detail['kcdw_fzr']
    project.sjdw = p_detail['sjdw']
    project.sjdw_fzr = p_detail['sjdw_fzr']
    project.sgdw = p_detail['sgdw']
    project.sgdw_fzr = p_detail['sgdw_fzr']
    project.jldw = p_detail['jldw']
    project.jldw_fzr = p_detail['jldw_fzr']
    project.manager = user
    project.save()

    person = Person()
    person.user = user


    project.manager = user
    project.save()
    rootgroup = Group()
    rootgroup.user = user
    rootgroup.name = project.total_name
    rootgroup.type = 'root'
    rootgroup.project = project
    rootgroup.save()
    person.project = project
    person.save()

    rootgroup.say_members.add(person.user)

    group = Group()
    group.name = u'管理员'
    group.type = 'sys_manage'
    group.project = project
    group.sorted = 0
    group.save()
    group.say_members.add(person.user)

    group = Group()
    group.name = u'行政主管'
    group.type = 'sys_xzzg'
    group.project = project
    group.sorted = 1
    group.save()

    group = Group()
    group.name = u'建设单位'
    group.type = 'sys_jsdw'
    group.project = project
    group.sorted = 2
    group.save()

    group = Group()
    group.name = u'设计单位'
    group.type = 'sys_sjdw'
    group.project = project
    group.sorted = 3
    group.save()

    group = Group()
    group.name = u'勘察单位'
    group.type = 'sys_kcdw'
    group.project = project
    group.sorted = 4
    group.save()

    group = Group()
    group.name = u'监理单位'
    group.type = 'sys_jldw'
    group.project = project
    group.sorted = 5
    group.save()

    group = Group()
    group.name = u'施工单位'
    group.type = 'sys_sgdw'
    group.project = project
    group.sorted = 6
    group.save()

    group = Group()
    group.name = u'项目经理部'
    group.type = 'sys_xmjl'
    group.project = project
    group.sorted = 7
    group.is_needhx = True
    group.save()
    group.say_members.add(person.user)

    group = Group()
    group.name = u'劳务分包单位'
    group.type = 'sys_lwfbdw'
    group.project = project
    group.sorted = 8
    group.save()

    group = Group()
    group.name = u'专业分包单位'
    group.type = 'sys_zyfbdw'
    group.project = project
    group.sorted = 9
    group.save()

    group = Group()
    group.name = u'社会大众通道'
    group.type = 'sys_shdztd'
    group.project = project
    group.sorted = 1000
    group.save()

    return project

def create_apply(project, user):
    """
    创建申请
    by:王健 at:2015-1-21
    :param project:
    :param user:
    :return:
    """
    apply = ProjectApply()
    apply.project = project
    apply.user = user
    apply.content = u'我是 %s ,请让我加入' % user.name
    apply.save()

def create_SGlog(project, user, date, text, sgtqlog):
    """
    创建施工日志详细数据
    by:王健 at:2015-1-21
    :param project:
    :param user:
    :param date:
    :param text:
    :param sgtqlog:
    :return:
    """
    l = SGlog()
    l.project = project
    l.sg_tq_log = sgtqlog
    l.user = user
    l.text = text
    l.create_time = date
    l.save()

def create_SGTQlog(project, user, date, text):
    """
    创建施工日志
    by:王健 at:2015-1-21
    修改初始化数据不正确的地方
    by:王健 at:2015-1-29
    :param project:
    :param user:
    :param date:
    :param text:
    :return:
    """
    tqlog, create = SGTQlog.objects.get_or_create(project=project, date=date, file_group=FileGroup.objects.get(flag='gong_cheng_ri_zhi'))
    if create:
        tqlog.project = project
        tqlog.date = date
        tqlog.weather = u'晴朗'
        tqlog.wind = u'威风'
        tqlog.qiwen = u'33度'
    else:
        tqlog.create_time = timezone.now()
    tqlog.num +=15
    tqlog.save()
    for i in range(15):
        create_SGlog(project, user, date + datetime.timedelta(hours=i), u'施工日志 %s %s' % (text, i), tqlog)

def generate_email(qq):
    '''
    根据中文得到拼音
    by:尚宗凯 at:2015-3-3
    修改生成email
    by：尚宗凯 at：2015-06-25
    '''
    # p = Pinyin().get_pinyin(name, '')
    return str(qq)+'@qq.com'

def generate_xueli(title):
    '''
    根据职务生成学历
    by:尚宗凯 at:2015-3-3
    title中含有 经理 总监 为 大本7 其他为大专6
    :param title:
    :return: xueli
    '''
    xueli = ""
    if title.find('经理') == -1 and title.find('总监') == -1:
        xueli = 6
    else:
        xueli = 7
    return xueli

def generate_qq():
    '''
    随机生成qq号
    by:尚宗凯 at:2015-3-3
    :return: qq
    '''
    return str(random.randint(100000,9999999999))

def generate_birthday(title):
    '''
    根据职位生成出生时间
    by:尚宗凯 at:2015-3-3
    总经理：60 副总经理：70 处长 70 经理 70 其他80 90随机
    :param title:
    :return: birthday
    '''
    birthday = ''
    if title == '总经理':
        birthday = datetime.date( random.randint(1960,1969) ,
                              random.randint(1,12) ,
                              random.randint(1,28))
    elif title.find('副总') !=-1 or title.find('处长') !=-1 or title.find('经理') !=-1:
        birthday = datetime.date( random.randint(1970,1979) ,
                              random.randint(1,12) ,
                              random.randint(1,28))
    else:
        birthday = datetime.date( random.randint(1980,1992) ,
                              random.randint(1,12) ,
                              random.randint(1,28))
    return birthday

def create_user_and_person(tel, name,nickname, sex, project, title, group, group_type):
    """
    根据电话号用户名生成nsuser和person
    by:尚宗凯 at:2015-3-3
    修改project id
    by:尚宗凯 at:2015-4-14
    修改生成email的方式
    by：尚宗凯 at：2015-06-25
    """
    if tel:
        tel = int(tel)
        tel += 1000
        tel = str(tel)
    user = create_user_by_tel_name(tel, name, nickname, sex)
    person = Person()
    person.user = user
    person.project = project
    person.save()

    userinfo = UserInfo()
    userinfo.user = user
    userinfo.title = title
    userinfo.address = 101120101
    userinfo.xueli = generate_xueli(title)
    #userinfo.company = u'依子轩软件科技有限公司'
    userinfo.qq = generate_qq()
    userinfo.email = generate_email(userinfo.qq)

    userinfo.birthday = generate_birthday(title)
    userinfo.save()

    grp = Group.objects.get(project_id=project.pk,name=group)
    assert group_type in ('1','0')
    if group_type == '1':
        print user
        grp.say_members.add(user)
    else:
        print user
        grp.look_members.add(user)

    return user

def test_data_insert():
    """
    插入测试数据
    by:王健 at:2015-1-13
    插入初始化测试数据
    by:王健 at:2015-1-21
    增加初始化项目信息
    by:王健 at:2015-2-16
    增加水浒测试数据
    by:尚宗凯 at:2015-3-6
    增加初始化数据库视图创建
    by:尚宗凯 at:2015-3-6
    增加mysql 数据库NSUser数据库id自增设定
    by:尚宗凯 at:2015-3-7
    修正查询条件错误
    by:尚宗凯 at:2015-3-8
    增加40个项目创建, 去除其他测试数据
    by:尚宗凯 at:2015-3-17
    恢复单元测试代码
    by:尚宗凯 at:2015-3-23
    使用sqlite时候不增加10000开始
    by:尚宗凯 at:2015-3-27
    """
    #NSUser id从10000开始自增
    if 'SERVER_SOFTWARE' in os.environ or settings.ENVIRONMENT=="win_dev":
        if "django.db.backends.sqlite3" not in DATABASES['default'].values():
            connection.cursor().execute("AlTER TABLE needserver_nsuser AUTO_INCREMENT=10000;")

    project_list = [(u"杭州江枫苑", u"杭州江枫苑住宅工程"), (u"天津凤凰商贸广场", u"天津凤凰商贸广场A区、B区、C区塔标工程"),\
                    (u"双春新家园二期", u"双春新家园二期10#二标段工程"), (u"盛和家园", u"天津南江路盛和家园经济适用房工程"),\
                    (u"玉环县党校", u"台州玉环县委党校迁建工程"), (u"创意中心大楼工程", u"舟山广电传媒创意中心大楼工程"), \
                    (u"对外经济贸易大学", u"北京对外经济贸易大学教学楼工程"), (u"人民医院", u"海南省人民医院门诊楼及外科楼工程"), \
                    (u"尚龙名苑", u"长沙尚龙名苑住宅小区工程"), (u"蒙城红星时代广场", u"蒙城红星美凯龙时代广场工程"), \
                    (u"依子轩办公大楼", u"天津依子轩科技软件公司办公大楼"), ]
    user1 = create_user(u'123')
    user2 = create_user(u'1234')
    user3 = create_user(u'12345')
    user4 = create_user(u'123456')
    user5 = create_user(u'1234567')


    project1 = create_project(user1, project_list[0][0],  project_list[0][1])
    project2 = create_project(user2, project_list[1][0],  project_list[1][1])
    project3 = create_project(user3, project_list[2][0],  project_list[2][1])

    create_apply(project1, user2)
    create_apply(project1, user3)
    create_apply(project1, user4)
    create_apply(project1, user5)

    create_apply(project2, user3)
    create_apply(project2, user4)
    create_apply(project2, user5)

    create_apply(project3, user1)
    create_apply(project3, user4)
    create_apply(project3, user5)

    temp_project = None
    for name, totalname in project_list[3:]:
        temp_project = create_project(user1, name, totalname)



    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 13), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 14), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 15), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 16), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 17), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 18), u'水水水水收拾收拾生生世世三十岁')
    create_SGTQlog(project1, user1, datetime.datetime(2015, 1, 19), u'水水水水收拾收拾生生世世三十岁')

    file_dir = u'dev_files/108.txt'
    f = codecs.open(file_dir,'r',"utf-8-sig")
    #单元测试 先改为 4个人
    #by:王健 at:2015-3-15
    # 改宋江
    # by：尚宗凯 at：2015-04-13
    for line in f.readlines()[:3]:
    # for line in f.readlines():
        data = line.strip().split('\t')
        tel = data[0]
        nickname = data[1]
        name = data[2]
        title = data[3]
        group = data[4]
        group_type = data[5]
        sex = data[6]
        create_user_and_person(tel, name,nickname, sex, temp_project, title, group, group_type)

    #将宋江加入到管理员这个group
    songjiang = get_user_model().objects.get(name='宋江')
    grp = Group.objects.get(project_id=temp_project, type='sys_manage')
    grp.say_members.add(songjiang)



    # # 创建40个项目
    # user1 = create_user_no_ceshi(u'13207608539')
    # user2 = create_user_no_ceshi(u'18622231518')
    # user3 = create_user_no_ceshi(u'15122506840')
    # user4 = create_user_no_ceshi(u'13602177158')
    # user5 = create_user_no_ceshi(u'15822135546')
    # users = [user1,user2,user3,user4,user5]
    # p_detail = {}
    # file_dir = u'dev_files/40project.txt'
    # f = codecs.open(file_dir,'r',"utf-8-sig")
    # i = 0
    # for line in f.readlines():
    #     # print line,
    #     temp = line.strip().split("：")
    #     if temp[0] == "项目全称":
    #         p_detail['total_name'] = temp[1].strip()
    #     elif temp[0] == "项目简称":
    #         p_detail['name'] = temp[1].strip()
    #     elif temp[0] == "address":
    #         p_detail["address"] = int(temp[1].strip())
    #     elif temp[0] == "建筑面积":
    #         jzmj = temp[1].strip().strip("m2")
    #         if jzmj.find("万") != -1:
    #             jzmj = int(float(jzmj.strip("万")) * 10000)
    #         else:
    #             jzmj = int(float(jzmj))
    #         p_detail['jzmj'] = jzmj
    #     elif temp[0] == "结构类型":
    #         p_detail['jglx'] = temp[1].strip()
    #     elif temp[0] == "建筑层数":
    #         p_detail['jzcs'] = temp[1].strip()
    #         # p_detail['jzcs'] = int(temp[1].strip().strip("层"))
    #     elif temp[0] == "合同造价":
    #         htzj = temp[1].strip()
    #         if htzj.find("亿") != -1:
    #             htzj = int(float(htzj.strip("亿")) * 100000000)
    #         else:
    #             # print htzj
    #             # print htzj[:-2]
    #             # htzj = int(float(htzj[:-2]) * 10000)
    #             htzj = int(float(htzj.strip("万")) * 10000)
    #
    #         p_detail['htzj'] = htzj
    #     elif temp[0] == "开工日期":
    #         p_detail['kg_date'] = datetime.datetime.strptime(temp[1].strip(),"%Y-%m-%d")
    #     elif temp[0] == "总工期":
    #         p_detail['days'] = int(temp[1].strip())
    #     elif temp[0] == "建设单位":
    #         p_detail['jsdw'] = temp[1].strip()
    #     elif temp[0] == "建设单位负责人":
    #         p_detail['jsdw_fzr'] = temp[1].strip()
    #     elif temp[0] == "勘察单位":
    #         p_detail['kcdw'] = temp[1].strip()
    #     elif temp[0] == "勘察单位负责人":
    #         p_detail['kcdw_fzr'] = temp[1].strip()
    #     elif temp[0] == "施工单位":
    #         p_detail['sgdw'] = temp[1].strip()
    #     elif temp[0] == "施工单位负责人":
    #         p_detail['sgdw_fzr'] = temp[1].strip()
    #     elif temp[0] == "监理单位":
    #         p_detail['jldw'] = temp[1].strip()
    #     elif temp[0] == "监理单位负责人":
    #         p_detail['jldw_fzr'] = temp[1].strip()
    #     elif temp[0] == "设计单位":
    #         p_detail['sjdw'] = temp[1].strip()
    #     elif temp[0] == "设计单位负责人":
    #         p_detail['sjdw_fzr'] = temp[1].strip()
    #         i += 1
    #         print i%5,p_detail
    #         p1 = create_project_detail(users[i%5],p_detail)
