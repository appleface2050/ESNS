# coding=utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Need_Server.settings'
import time
from django.shortcuts import get_object_or_404
from needserver.models import EngineCheck, FileRecord
import qiniu
import urllib2
from qiniu.services.storage import uploader

from qiniu import BucketManager
from nsbcs.models import BaseFile,File

QN_AK = '_Jsy--Hfm1ldj070dRJth1a4Gx-6TkcpySMcZm3V'
QN_SK = 'Xa1r9yMQwwiGZb2GZTOV13BzDrJiY6JAXSVZ9AkJ'

QN_FILE_BUCKET_DOMAIN = 'http://7xihic.com2.z0.glb.qiniucdn.com/'
QN_FRIENDS_ICON_BUCKET_DOMAIN = 'http://7xihie.com2.z0.glb.qiniucdn.com/'
QN_PROJECT_ICON_BUCKET_DOMAIN = 'http://7xihif.com2.z0.glb.qiniucdn.com/'

mime_type = "text/plain"

def bcs_pic_to_qiniu():
    """
    把bcs图片弄到七牛上面
    by：尚宗凯 at：2015-06-03
    修改为数据流上传
    by：尚宗凯 at：2015-06-03
    优化bucket
    by：尚宗凯 at：2015-06-03
    """
    bf = BaseFile.objects.all()
    for i in bf:
        if i.bucket in ("projectfiles","pubfriendsicon","pubproject"):
        # if i.bucket in ("qn-projectfiles"):
            url = i.get_url()
            if url.startswith("http://bcs.duapp.com/"):
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
                        pass
                    else:
                        assert ret['key'] == key
                        i.bucket = bucket
                        i.save()
                        # 验证文件是否能打开
                        if bucket == 'qn-projectfiles':
                            base_url = QN_FILE_BUCKET_DOMAIN + key
                        elif bucket == 'pubfriendsicon':
                            base_url = QN_FRIENDS_ICON_BUCKET_DOMAIN + key
                        elif i.bucket == 'pubproject':
                            base_url = QN_PROJECT_ICON_BUCKET_DOMAIN + key
                        private_url = qn_auth.private_download_url(base_url, expires=3600)
                        print "private_url:",private_url
                except Exception as e:
                    print e


                # ret, info = uploader.put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
                # if os.path.exists(localfile):
                #     os.remove(localfile)
                # if info.status_code == 614:
                #     pass
                # else:
                #     assert ret['key'] == key
                #     i.bucket = "qn-projectfiles"
                #     i.save()


def delete_qiniu_pic_where_file_status_is_false():
    """
    把七牛上面图片失效的删掉，数据库的删掉
    by：尚宗凯 at：2015-06-03
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

def cal_scale():
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


if __name__ == '__main__':
    delete_qiniu_pic_where_file_status_is_false()
    bcs_pic_to_qiniu()
    cal_scale()
