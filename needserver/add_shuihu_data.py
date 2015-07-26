#coding=utf-8

import json
import urllib,urllib2
import codecs,os
import datetime

# os.environ['DJANGO_SETTINGS_MODULE'] = 'Need_Server.settings'
from django.utils import timezone
from needserver.models import Project,Person,NSUser,UserInfo,Group,SGlog,SGTQlog, FileGroup, FileRecord, EngineCheck, \
    SysMessage, ProjectMessage, ProjectRechargeRecord
from needserver.management import create_user_and_person
from Need_Server.settings import SHOW_PROJECT_ID

#SHOW_PROJECT_ID = 71

def add_shuihu_user():
    """
    初始化108将
    by：尚宗凯 at：2015-04-13
    去掉一行
    by：尚宗凯 at：2015-04-13
    修改水浒的项目id
    by：尚宗凯 at：2015-04-15
    增加水浒日志
    by：尚宗凯 at：2015-04-16
	修改气温
	by：尚宗凯 at：2015-04-16
	删除已有的100个日志
	by：尚宗凯 at：2015-04-16
	修改阿里云水浒文件路径
	by：尚宗凯 at：2015-04-16
	修改阿里云水浒文件路径
	by：尚宗凯 at：2015-04-16
	删除错误的天气log
	by：尚宗凯 at：2015-04-16
    """

    a = SGlog.objects.filter(project_id=SHOW_PROJECT_ID)
    a.delete()
    b = SGTQlog.objects.filter(project_id=SHOW_PROJECT_ID)
    b.delete()



    shuihu_project = Project.objects.get(pk=SHOW_PROJECT_ID)

    file_dir = u'/web/Need_Server/dev_files/108.txt'
    f = codecs.open(file_dir,'r',"utf-8-sig")
    # f = open(file_dir,'r')

    person_dict = {}

    for line in f.readlines():
    # for line in f.readlines():
        data = line.strip().split('\t')
        tel = data[0]
        nickname = data[1]
        name = data[2]
        title = data[3]
        group = data[4]
        group_type = data[5]
        sex = data[6]

        u = create_user_and_person(tel, name,nickname, sex, shuihu_project, title, group, group_type)
        person_dict[name] = u
    log_file_path = '/web/Need_Server/dev_files/shuihu_sglog.txt'
    f = codecs.open(log_file_path,'r',"utf-8-sig")
    for line in f.readlines():
        d = line.split(' ')
        s, created = SGTQlog.objects.get_or_create(project_id=SHOW_PROJECT_ID, file_group=FileGroup.objects.get(flag='gong_cheng_ri_zhi'), date=datetime.datetime.strptime(d[1], '%Y-%m-%d'), weather="晴朗", wind='3-4级', qiwen="10-20")
        sglog = SGlog()
        sglog.user = person_dict[d[0]]
        sglog.text = ' '.join(d[2:])
        sglog.project_id = SHOW_PROJECT_ID
        sglog.sg_tq_log = s
        s.last_create_user_id = person_dict[d[0]].pk
        s.num +=1
        s.save()
        sglog.save()

    #将宋江加入到管理员这个group
    # songjiang = get_user_model().objects.get(name='宋江')
    # grp = Group.objects.get(project_id=temp_project, type='sys_manage')
    # grp.say_members.add(songjiang)

def update_shuihu_data():
    pass
    #解决log换行问题
    #by：尚宗凯 at：2015-04-16
    # logquery = SGlog.objects.filter(project_id=SHOW_PROJECT_ID)
    # # print log.count()
    # for i in logquery:
    #     tmp_text = i.text
    #     i.text = tmp_text.strip()
    #     sg_log_id = i.sg_tq_log_id
    #     i.create_time = datetime.datetime.strptime(str(SGTQlog.objects.get(pk=sg_log_id).date),'%Y-%m-%d')
    #     i.save()
    #
    # #删除宣传报道
    # #by：尚宗凯 at：2015-04-16
    # file_group_id = FileGroup.objects.get(flag="xuan_chuan_bao_dao").pk
    # frs = FileRecord.objects.filter(project_id=SHOW_PROJECT_ID, file_group_id=file_group_id)
    # frs.delete()
    #
    # #现场安全文明检查
    # #by：尚宗凯 at：2015-04-16
    # ecs = EngineCheck.objects.filter(project_id=SHOW_PROJECT_ID)
    # for i in ecs:
    #     i.fucha = "整改合格"
    #     i.save()
    #
    #
    # #违章曝光去掉问题描述
    # #by：尚宗凯 at：2015-04-17
    # file_group_id = FileGroup.objects.get(flag="bao_guang_jing_gao").pk
    # frs = FileRecord.objects.filter(project_id=SHOW_PROJECT_ID, file_group_id=file_group_id)
    # for fr in frs:
    #     if fr.title.startswith("问题描述："):
    #         fr.title = fr.title.encode('utf-8')
    #         fr.title = fr.title[15:]
    #         fr.save(flag=None)
    #
    # #新增3个项目公告
    # #by：尚宗凯 at：2015-04-17
    # project_message_group = Group.objects.get(project_id=SHOW_PROJECT_ID, type="sys_xmjl")
    # pm = ProjectMessage()
    # pm.title = "开会通知"
    # pm.text = "明天晚上七点，在项目部会议室召开4月份施工管理例会，要求所有管理人员及各班组长必须参加，不得请假。请大家相互转告并准时参加。"
    # pm.user_id = NSUser.objects.get(tel=1108).pk #段景住
    # pm.project_id = SHOW_PROJECT_ID
    # pm.to_group_id = project_message_group.pk
    # pm.save()
    #
    # pm2 = ProjectMessage()
    # pm2.title = "迎检通知"
    # pm2.text = "刚接到上级通知，本周五下午，市质量总队到我项目进行季度大检查，请各位管理人员做好各项工作，准备迎检。"
    # pm2.user_id = NSUser.objects.get(tel=1108).pk #段景住
    # pm2.project_id = SHOW_PROJECT_ID
    # pm2.to_group_id = project_message_group.pk
    # pm2.save()
    #
    # pm3 = ProjectMessage()
    # pm3.title = "放假 通知"
    # pm3.text = "根据项目现场实际施工情况，五月一日放假一天，项目部将组织所有员工进行户外活动。具体活动，另通知。"
    # pm3.user_id = NSUser.objects.get(tel=1108).pk #段景住
    # pm3.project_id = SHOW_PROJECT_ID
    # pm3.to_group_id = project_message_group.pk
    # pm3.save()
    #
    # #3个系统消息
    # #by：尚宗凯 at：2015-04-17
    # sm = SysMessage()
    # sm.title = "创建项目成功，赠送金豆"
    # sm.text = "【依子轩软件科技】友情提示：您已成功创建“英国宫一期”项目,系统将自动在该项目帐户上充值600个消费金豆，预计可正常使用30天（按项目成员20人计算）。现在您可以在联系人中添加项目新成员。祝您使用愉快！如有疑问，可拨打免费客服电话：400-001-5552进行咨询，谢谢。"
    # sm.project_id = SHOW_PROJECT_ID
    # sm.save()
    #
    # sm2 = SysMessage()
    # sm2.title = "账户余额信息"
    # sm2.text = "【依子轩软件科技】友情提示：您所在的“英国宫一期”项目帐户余额还剩下236个消费金豆，预计还能使用2天。帐户余额不足时，系统将自动封存该项目帐户。为了不影响项目帐户的正常使用，请项目管理员尽快办理续费充值业务。如有疑问，可拨打免费客服电话：400-001-5552进行咨询，谢谢。"
    # sm2.project_id = SHOW_PROJECT_ID
    # sm2.save()
    #
    # sm3 = SysMessage()
    # sm3.title = "账户余额信息"
    # sm3.text = "【依子轩软件科技】友情提示：您所在的“英国宫一期”项目帐户余额不足，已被系统自动封存，停止使用。若重新开通此帐户，请项目管理员办理续费充值。如有疑问，可拨打免费客服电话：400-001-5552进行咨询，谢谢。"
    # sm3.project_id = SHOW_PROJECT_ID
    # sm3.save()
    #
    # sm4 = SysMessage()
    # sm4.title = "充值信息"
    # sm4.text = "【依子轩软件科技】友情提示：您所在的“英国宫一期”项目帐户已办理续费充值15000个金豆，当前帐户余额15010个金豆，预计可使用138天，祝您使用愉快。如有疑问，可拨打免费客服电话：400-001-5552进行咨询，谢谢。"
    # sm4.project_id = SHOW_PROJECT_ID
    # sm4.save()
    #

    #违章曝光新文本
    #by：尚宗凯 at：2015-04-19
    #违章曝光新文本
    #by：尚宗凯 at：2015-04-19
    #修改错误
    #by：尚宗凯 at：2015-04-19
    # file_group_id = FileGroup.objects.get(flag="bao_guang_jing_gao").pk
    # frs = FileRecord.objects.filter(project_id=SHOW_PROJECT_ID, file_group_id=file_group_id)[:]
    # n = len(frs)
    # if n==10:
    #     frs[0].title = "防水施工队工人进行喷枪明火作业时，未在周围设置灭火器。"
    #     frs[0].text = "1）责令班组按要求设置灭火器材。2）对工人进行安全教育。"
    #     frs[0].save(flag=None)
    #     frs[1].title = "截桩班组工人违章指挥挖机司机挖断桩身。"
    #     frs[1].text = "1）对挖机司机批评教育，挖机严禁触碰桩身。2）记录此桩号，重点观察该桩小应变检测结果。3）对工人处以100元罚款。"
    #     frs[1].save(flag=None)
    #     frs[2].title = "木工班操作工人在楼层作业时未戴安全帽。"
    #     frs[2].text = "1）对其安全教育，责令其正确配戴安全帽。2）对个人处以50元罚款。"
    #     frs[2].save(flag=None)
    #     frs[3].title = "9号楼十一层剪力墙，木工模板加固不到位，造成砼浇筑时涨模跑模，砼清理不到位。"
    #     frs[3].text = "1）砼浇筑前质量员做好对模板的检查验收。2）对班组处以500元罚款。"
    #     frs[3].save(flag=None)
    #     frs[4].title = "5号楼12层剪力墙木工班拆模过早，造成砼面表脱皮，影响外观质量。"
    #     frs[4].text = "1）墙柱模板拆模严格按照规范要求进行。2）模板表面涂刷脱模剂。3）对木工班组处以200元罚款。"
    #     frs[4].save(flag=None)
    #     frs[5].title = "裙塔作业时，两台塔吊垂直高度不在安全范围，存在很大的安全隐患。"
    #     frs[5].text = "1）立即暂停使用两台塔吊。2）通知塔吊安装公司进行塔吊升节，确保安全距离。"
    #     frs[5].save(flag=None)
    #     frs[6].title = "木工班工人私拉乱接电线。"
    #     frs[6].text = "1）立即拆除私拉的电线，按规范接电。2）对工人进行安全教育。"
    #     frs[6].save(flag=None)
    #     frs[7].title = "烟道安装班工人在楼板随意剔凿开洞，造成安装预埋线管断裂。"
    #     frs[7].text = "1）未经项目部允许，不得在结构任何部位剔凿开洞。2）对班组处以200元罚款。"
    #     frs[7].save(flag=None)
    #     frs[8].title = "砌筑班工人落手清工作不到位，落地灰未进行有效利用，造成材料浪费。"
    #     frs[8].text = "1）加强巡查，对工人做好技术交底。2）对班组处以200元罚款。"
    #     frs[8].save(flag=None)
    #     frs[9].title = "安装班操作工人进行线盒安装时，随意开槽，造成砌块严重破损。"
    #     frs[9].text = "1）安装前做好技术交底，砌块破损处采用细石砼封堵。2）对安装班组处以100元罚款。"
    #     frs[9].save(flag=None)
    #
    #充值
    #by：尚宗凯 at：2015-04-20
    # pr = ProjectRechargeRecord()
    # pr.project_id = SHOW_PROJECT_ID
    # pr.date = timezone.now()
    # pr.order_id = None
    # pr.price0 = 15000
    # pr.price_type = 1
    # pr.save(sysmessage=SysMessage())
    #
    # #文件通知，会议纪要删除,段景住加入项目经理部
    # #by：尚宗凯 at：2015-04-20
    # file_group_id = FileGroup.objects.get(flag="wen_jian_tong_zhi").pk
    # frs = FileRecord.objects.filter(project_id=SHOW_PROJECT_ID, file_group_id=file_group_id)
    # frs.delete()
    #
    # file_group_id = FileGroup.objects.get(flag="hui_yi_ji_yao").pk
    # frs = FileRecord.objects.filter(project_id=SHOW_PROJECT_ID, file_group_id=file_group_id)
    # frs.delete()
    #
    # djz = NSUser.objects.get(tel=1108)
    # xm_group = Group.objects.get(project_id=SHOW_PROJECT_ID, type='sys_xmjl')
    # xm_group.say_members.add(djz)
    # xm_group.save()