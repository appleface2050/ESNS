# coding=utf-8
__author__ = '尚宗凯'
import os
import copy
os.environ['DJANGO_SETTINGS_MODULE'] = 'Need_Server.settings'

from needserver.jifenutil import login_jifen, create_data_jifen, query_fen_by_uid, remove_fen, login_jifen2, create_data_jifen2, query_fen_by_uid2

from needserver.models import Project, SGlog, SGTQlog, ProjectApply, FileRecord, Person, FileGroupJSON, EngineCheck, \
    GYSAddress, WuZiRecord, Group, RecordDate, SysMessage, ProjectMessage, ProjectRechargeRecord, NSUser, UserInfo
from needserver.views_user import person_2_dict, group_2_dict
from nsbcs.models import File
from util.basetest import BaseTestCase
from nsbcs.models import BaseFile
from django.db import connection

class  ImportShuiHuData(object):
    """
    #用于单元测试数据准备
    #by:尚宗凯 at:2015-3-11
    """
    def login(self):
        """
        #login test dataa
        #by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        users = NSUser.objects.all()
        for i in users:
            # print i.tel
            data = {"tel":i.tel,
                "password":123456,
                "model":"login"
                }
            result.append(copy.deepcopy(data))
        return result

    def submit_user_tel(self):
        """
        #submit_user_tel test dataa
        #by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        users = NSUser.objects.all()
        for i in users:
            data = {"tel":i.tel,
                "password":123456,
                "model":"submit_user_tel"
                }
            result.append(copy.deepcopy(data))
        return result

    def update_userinfo(self):
        """
        update_userinfo test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        userinfos = UserInfo.objects.all()
        for i in userinfos:
            data = {"tel":i.user_id,
                "birthday":i.birthday,
                'address': i.address,
                'xueli': i.xueli,
                'zhicheng': i.zhicheng,
                'zhiyezigezheng':i.zhiyezigezheng,
                'company':i.company,
                'title': i.title,
                'department': i.department,
                'email': i.email,
                'qq': i.qq,
                "model":"update_userinfo"
                }
            result.append(copy.deepcopy(data))
        return result

    def update_project(self):
        """
        update_project test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        p = Project.objects.all()
        for i in p:
            data = {"project_id":i.pk,
                "name":i.name,
                "total_name":i.total_name,
                "address":i.address,
                "jzmj":i.jzmj,
                "jglx":i.jglx,
                "jzcs":i.jzcs,
                "htzj":i.htzj,
                "days":i.days,
                "jsdw":i.jsdw,
                "jsdw_fzr":i.jsdw_fzr,
                "kcdw": i.kcdw,
                "kcdw_fzr": i.kcdw_fzr,
                "sjdw": i.sjdw,
                "sjdw_fzr": i.sjdw_fzr,
                "sgdw": i.sgdw,
                "sgdw_fzr": i.sgdw_fzr,
                "jldw": i.jldw,
                "jldw_fzr": i.jldw_fzr,
                "model":"update_project"
                }
            result.append(copy.deepcopy(data))
        return result

    def get_upload_files_url(self):
        """
        get_upload_files_url test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        bf = File.objects.values("name","filetype","project_id","size")
        for i in bf:
            data = {
               "project_id": int(i['project_id']),
               "filename": i['name'],
               "filetype": i['filetype'],
               "size": int(i['size']),
               "model": "get_upload_files_url"
            }
            result.append(copy.deepcopy(data))
        return result

    def get_userinfo(self):
        """
        get_userinfo test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        p = Person.objects.all()
        for i in p:
            data = {"project_id": i.project_id,
                "user_id": i.user_id,
                "model":"get_userinfo"
                }
            result.append(copy.deepcopy(data))
        return result

    def my_project(self):
        """
        get_userinfo test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        pass

    def query_project(self):
        """
        query_project test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        p = Project.objects.all()
        for i in p:
            data = {  "start": '0',
                       "address": i.address,
                        "model":"query_project"
                }
            result.append(copy.deepcopy(data))
        return result

    def update_log_by_date(self):
        """
        update_log_by_date test data
        by:尚宗凯 at:2015-3-11
        :return:
        """
        result = []
        # SELECT a.project_id,a.text,b.weather,b.wind,b.qiwen  FROM needserver_sglog a JOIN needserver_sgtqlog b ON a.sg_tq_log_id = b.recorddate_ptr_id
        cursor = connection.cursor()
        # res = SGlog.objects.raw("SELECT a.project_id,a.text,b.weather,b.wind,b.qiwen  FROM needserver_sglog a JOIN needserver_sgtqlog b ON a.sg_tq_log_id = b.recorddate_ptr_id")
        logs = SGlog.objects.filter(project_id=11)
        for log in logs:
            # print log.sg_tq_log_id
            tg = SGTQlog.objects.get(recorddate_ptr_id = log.sg_tq_log_id)
            # print tg.weather, tg.wind, tg.qiwen
            data = { "project_id": log.project_id,
                   "text": log.text,
                    "sg_tq_id": log.sg_tq_log_id,
                    "weather": tg.weather,
                    "wind": tg.wind,
                    "qiwen":tg.qiwen,
                    "model":"update_log_by_date"
            }
            result.append(copy.deepcopy(data))
        return result

    def del_log_by_id(self):
        """
        del_log_by_id test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        logs = SGlog.objects.filter(project_id=11)
        for log in logs:
            # print log.sg_tq_log_id,log.project_id
            data = {"project_id": int(log.project_id) , 'sg_tq_log_id': int(log.sg_tq_log_id) ,"model": "del_log_by_id"}
            result.append(copy.deepcopy(data))
        return result

    def query_log_date_list(self):
        """
        query_log_date_list test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        tg = SGlog.objects.all()
        for i in tg:
            data = {'project_id': int(i.project_id), 'start':0, 'model': 'query_log_date_list' }
            result.append(copy.deepcopy(data))
        return result

    def query_log_date_list_old(self):
        """
        query_log_date_list_old test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        tg = SGlog.objects.all()
        for i in tg:
            data = {'project_id': int(i.project_id), 'start':0, 'model': 'query_log_date_list_old' }
            result.append(copy.deepcopy(data))
        return result

    def query_log_list_by_date(self):
        """
        query_log_list_by_date test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        tg = SGlog.objects.all()
        for i in tg:
            data = {'project_id': int(i.project_id),  'model': 'query_log_list_by_date' }
            result.append(copy.deepcopy(data))
        return result

    def query_log_list_by_date_2(self):
        """
        query_log_list_by_date_2 test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        tg = SGlog.objects.all()
        for i in tg:
            data = {'project_id': int(i.project_id),  'model': 'query_log_list_by_date_2' }
            result.append(copy.deepcopy(data))
        return result

    def apply_project(self):
        """
        apply_project test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        # result = []
        # persons = Person.objects.all()
        # for p in persons:
        #     tel = NSUser.objects.get(pk=p.user_id)
        #     data = {
        #         "project_id":p.project_id,
        #         "text": u"让我进去",
        #         "authorname":tel.tel,
        #         "model": "apply_project"
        #     }
        #     result.append(copy.deepcopy(data))
        # return result
        result = []
        applyproject = ProjectApply.objects.all()
        for i in applyproject:
            tel = NSUser.objects.get(pk=i.user_id)
            data = {
                "project_id":int(i.project_id),
                "text": i.content,
                "authorname":tel.tel,
                "model": "apply_project"
            }
            result.append(copy.deepcopy(data))
        return result

    def get_all_applyproject(self):
        """
        get_all_applyproject test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id":int(i.id),
                "model": "get_all_applyproject"
            }
            result.append(copy.deepcopy(data))
        return result

    def change_applyproject_add(self):
        pass

    def change_applyproject_remove(self):
        """
        change_applyproject_remove test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        applyproject = ProjectApply.objects.all()
        for i in applyproject:
            data = {
                "project_id": int(i.project_id),
                "apply_id": int(i.pk),
                "model": "change_applyproject_remove"
            }
            result.append(copy.deepcopy(data))
        return result

    def change_user_group_delete(self):
        """
        change_user_group delete  test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        a = Group.objects.filter(project_id=11)
        for i in a:
            for j in i.look_members.values('id'):
                # print  i.project_id,i.id,j['id']
                data = {
                    "model": "change_user_group_delete",
                    "project_id": int(i.project_id),
                    "group_id": int(i.id),
                    "user_id": int(j['id']),
                    "do": "delete"
                }
                result.append(copy.deepcopy(data))
        return result

    def change_user_group_join(self):
        """
        change_user_group join test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        a = Group.objects.filter(project_id=11)
        for i in a:
            for j in i.look_members.values('id'):
                # print  i.project_id,i.id,j['id']
                data = {
                    "model": "change_user_group_join",
                    "project_id": int(i.project_id),
                    "group_id": int(i.id),
                    "user_id": int(j['id']),
                    "do": "join"
                }
                result.append(copy.deepcopy(data))
        return result

    def query_person(self):
        """
        query_person test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "timeline": 0,
                "model": "query_person"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_group(self):
        """
        query_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "timeline": 0,
                "model": "query_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def check_file_upload_status(self):
        """
        check_file_upload_status test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        files = File.objects.all()
        for i in files:
            data = {
                "project_id": int(i.project_id),
                "fileid": int(i.pk),
                "model": "check_file_upload_status"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_app_list(self):
        """
        query_app_list test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "model": "query_app_list"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_app_list2(self):
        """
        query_app_list2 test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "timeline": 0,
                "model": "query_app_list2"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_app_list3(self):
        """
        query_app_list3 test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "model": "query_app_list3"
            }
            result.append(copy.deepcopy(data))
        return result

    def create_file_by_group(self):
        """
        create_file_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        bf = File.objects.values("name","id","project_id")
        for i in bf:
            data = {
               "project_id": int(i['project_id']),
               "fileid": int(i['id']),
               "title": i['name'],
               "text": "test",
               "model": "create_file_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_file_by_group_1(self):
        """
        query_file_by_group_1 test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "model": "query_file_by_group_1"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_file_by_group_2(self):
        """
        query_file_by_group_2 test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "model": "query_file_by_group_2"
            }
            result.append(copy.deepcopy(data))
        return result

    def create_enginecheck_by_group(self):
        """
        create_enginecheck_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        ec = EngineCheck.objects.all()
        for i in ec:
            data = {
                "project_id": int(i.project_id),
                "fileid": int(i.file_group_id),
                "flag": "bao_guang_jing_gao",
                "desc": i.desc,
                "model": "create_enginecheck_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def update_enginecheck_by_group(self):
        """
        update_enginecheck_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        ec = EngineCheck.objects.all()
        for i in ec:
            data = {
                "id": int(i.pk),
                "project_id": int(i.project_id),
                "fileid": int(i.file_group_id),
                "flag": "bao_guang_jing_gao",
                # "chuli": i.chuli,
                # "fucha": i.fucha,
                "model": "update_enginecheck_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_enginecheck_by_group(self):
        """
        query_enginecheck_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "flag": "bao_guang_jing_gao",
                "timeline": 0,
                "model": "query_enginecheck_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_enginecheck_by_group_old(self):
        """
        query_enginecheck_by_group_old test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "flag": "bao_guang_jing_gao",
                "timeline": 0,
                "model": "query_enginecheck_by_group_old"
            }
            result.append(copy.deepcopy(data))
        return result

    def create_gysaddress_by_group(self):
        """
        create_gysaddress_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        gy = GYSAddress.objects.all()
        for i in gy:
            data = {
                "project_id": int(i.project_id),
                "id": "",
                "flag": "",
                "name": i.name,
                "ghs": i.ghs,
                "ghs_fzr": i.ghs_fzr,
                "ghs_fzr_tel": i.ghs_fzr_tel,
                "is_hetong": '',
                "pay_type": "",
                "shr": i.shr,
                "shr_tel": i.shr_tel,
                "bz": i.bz,
                "model": "create_gysaddress_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_gysaddress_by_group(self):
        """
        query_gysaddress_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "flag": "gong_ying_shang_ming_lu",
                "timeline": 0,
                "model": "query_gysaddress_by_group"

            }
            result.append(copy.deepcopy(data))
        return result

    def query_gysaddress_by_group_old(self):
        """
        query_gysaddress_by_group_old test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        project = Project.objects.all()
        for i in project:
            data = {
                "project_id": int(i.pk),
                "flag": "wu_zi_ru_ku_ji_lu",
                "timeline": 0,
                "model": "query_gysaddress_by_group_old"
            }
            result.append(copy.deepcopy(data))
        return result

    def create_wuzirecord_by_group(self):
        """
        create_wuzirecord_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        wuzi = WuZiRecord.objects.all()
        for i in wuzi:
            data = {
                "project_id": i.project_id,
                "id": '',
                "flag": 'wu_zi_ru_ku_ji_lu',
                "name": i.name,
                "gg": i.gg,
                "num": i.count,
                "company": i.company,
                "lingliaoren": i.lingliaoren,
                "count" : i.count,
                "status": "",
                "model": "create_wuzirecord_by_group"
            }
            result.append(copy.deepcopy(data))
        return result

    def del_wuzirecord_by_id(self):
        """
        del_wuzirecord_by_id test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        wuzi = WuZiRecord.objects.all()
        for i in wuzi:
            data = {
                "project_id": i.project_id,
                "logid": i.pk,
                "model": "del_wuzirecord_by_id"
            }
            result.append(copy.deepcopy(data))
        return result

    def query_wuzirecord_by_group(self):
        """
        query_wuzirecord_by_group test data
        by:尚宗凯 at:2015-3-12
        :return:
        """
        result = []
        wuzi = WuZiRecord.objects.all()
        for i in wuzi:
            data = {
                "project_id": 11,
                "flag": "wu_zi_ru_ku_ji_lu",
                "timeline": 0,
                "record_date_id": int(i.record_date_id),
                "model": "query_wuzirecord_by_group"
            }
            result.append(copy.deepcopy(data))
        return result


if __name__ == '__main__':
    a = ImportShuiHuData()
    result = a.get_upload_files_url()
    for i in result:
        print i

