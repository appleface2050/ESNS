# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
from django.db import transaction
from django.http import Http404

__author__ = u'王健'

import uuid
from django.shortcuts import get_object_or_404

from nsbcs.models import File, FILE_BUCKET, QN_FRIENDS_ICON_BUCKET, BaseFile, QN_FILE_BUCKET, QN_WEBIMAGE_ICON_BUCKET, \
    SysFile, QN_COMPANY_ICON_BUCKET, ComFile

from util.jsonresult import getResult

from util.loginrequired import client_login_project_required, client_login_required


def create_user_icon_fileobj(request, bucket=QN_FRIENDS_ICON_BUCKET):
    """
    创建用户头像
    by:王健 at:2015-1-29
    用户头像存储位置 标记为以用户id为文件夹目录的位置
    by:王健 at:2015-2-3
    :param request:
    :param bucket:
    :return:
    """
    fileobj = BaseFile()
    fileobj.user_id = request.user.pk
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype', 'file')
    fileobj.size = int(request.REQUEST.get('size', '0'))
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    uuidname = str(uuid.uuid4())
    object_name = str('/%s/%s.%s' % (fileobj.user_id, uuidname, fileobj.filetype))
    fileobj.fileurl = object_name
    # fileobj.shareurl = bcs.sign('GET', FILE_BUCKET, object_name)
    # posturl = bcs.sign('POST', FILE_BUCKET, object_name, T=int(time.time() + 3600), S=fileobj.size)
    fileobj.save()
    return fileobj


def create_fileobj(request, project_id, bucket=FILE_BUCKET):
    """
    创建项目文件
    by:王健 at:2015-1-29
    :param request:
    :param project_id:
    :param bucket:
    :return:
    """
    fileobj = File()
    fileobj.user_id = request.user.pk
    fileobj.bucket = bucket
    fileobj.project_id = project_id
    # fileobj.shareurl = '/share/%s' % str(uuid.uuid4())
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype', 'file')
    fileobj.size = int(request.REQUEST.get('size', '0'))
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    uuidname = str(uuid.uuid4())
    object_name = str('/%s/%s.%s' % (fileobj.project_id, uuidname, fileobj.filetype))
    fileobj.fileurl = object_name
    # fileobj.shareurl = bcs.sign('GET', FILE_BUCKET, object_name)
    # posturl = bcs.sign('POST', FILE_BUCKET, object_name, T=int(time.time() + 3600), S=fileobj.size)
    fileobj.save()
    return fileobj

def create_big_company_fileobj(request, bucket=QN_WEBIMAGE_ICON_BUCKET):
    """
    创建集团文件
    by：尚宗凯 at：2015-06-16
    """
    fileobj = SysFile()
    fileobj.user_id = request.user.pk
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype', 'file')
    fileobj.size = int(request.REQUEST.get('size', '0'))
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    filename = str(uuid.uuid4()) + '.' + fileobj.name.split('.')[-1]
    object_name = str('/%s/%s' % ('sys_bigcom', filename))
    fileobj.fileurl = object_name
    fileobj.save()
    return fileobj


def create_sys_banner_fileobj(request, bucket=QN_WEBIMAGE_ICON_BUCKET):
    """
    创建系统banner文件
    by：尚宗凯 at：2015-06-23
    """
    fileobj = SysFile()
    fileobj.user_id = request.user.pk
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype', 'file')
    fileobj.size = int(request.REQUEST.get('size', '0'))
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    filename = str(uuid.uuid4()) + '.' + fileobj.name.split('.')[-1]
    object_name = str('/%s/%s' % ('sys_banner', filename))
    fileobj.fileurl = object_name
    fileobj.save()
    return fileobj


def create_company_fileobj(request, company_id, bucket=QN_COMPANY_ICON_BUCKET):
    """
    创建公司文件
    by：尚宗凯 at：2015-06-17
	修改文件名称
	by：尚宗凯 at：2015-06-23
    """
    fileobj = ComFile()
    fileobj.company_id = company_id
    fileobj.user_id = request.user.pk
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype', 'file')
    fileobj.size = int(request.REQUEST.get('size', '0'))
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    filename =  str(uuid.uuid4()) + '.' + fileobj.name.split('.')[-1]
    object_name = str('/%s/%s' % ('company', filename))
    fileobj.fileurl = object_name
    fileobj.save()
    return fileobj


@client_login_project_required
@transaction.atomic()
def get_upload_files_url(request, project_id, bucket=QN_FILE_BUCKET):
    """
    上传附件, 客户端提供 文件的类型、大小
    服务器返回，bcs的POST url，当天有效，客户成功后，告诉服务器，服务器修改文件的保存状态。
    优势：上传下载、不走服务器流量，不占用服务器带宽，
    by:王健 at:2015-1-10
    参数兼容 get 和 post， 增加put上传接口
    by:王健 at:2015-1-14
    文件长度，超过50，则只取后50个字
    by:王健 at:2015-1-27
    抽象出创建 file的函数，方便别的模块调用
    by:王健 at:2015-1-28
    上传到七牛
    by: 范俊伟 at:2015-04-14
    修改 获取url的函数，无需参数
    by: 王健 at:2015-04-14
    :param request:
    :return:
    """
    fileobj = create_fileobj(request, project_id, bucket)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_post_url(), 'puturl': fileobj.get_put_url()})


def get_bigcompany_qn_upload_files_url(request, bucket=QN_WEBIMAGE_ICON_BUCKET):
    """
    集团logo上传
    by：尚宗凯 at：2015-06-16
    """
    fileobj = create_big_company_fileobj(request, bucket)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


def get_sys_banner_qn_upload_files_url(request, bucket=QN_WEBIMAGE_ICON_BUCKET):
    """
    系统banner上传
    by：尚宗凯 at：2015-06-23
    """
    fileobj = create_sys_banner_fileobj(request, bucket)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


def get_company_qn_upload_files_url(request, company_id, bucket=QN_COMPANY_ICON_BUCKET):
    """
    公司logo上传
    by：尚宗凯 at：2015-06-16
    """
    fileobj = create_company_fileobj(request, company_id, bucket)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


@client_login_project_required
@transaction.atomic()
def get_qn_upload_files_url(request, project_id, bucket=QN_FILE_BUCKET):
    """
    上传附件, 客户端提供 文件的类型、大小
    服务器返回，bcs的POST url，当天有效，客户成功后，告诉服务器，服务器修改文件的保存状态。
    优势：上传下载、不走服务器流量，不占用服务器带宽，
    by:王健 at:2015-1-10
    参数兼容 get 和 post， 增加put上传接口
    by:王健 at:2015-1-14
    文件长度，超过50，则只取后50个字
    by:王健 at:2015-1-27
    抽象出创建 file的函数，方便别的模块调用
    by:王健 at:2015-1-28
    七牛云接口
    by: 范俊伟 at:2015-04-08
    :param request:
    :return:
    """
    fileobj = create_fileobj(request, project_id, bucket)
    return getResult(True, u'', {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


@client_login_required
def upload_files(request,file_id):
    """
    上传附件
    by:王健 at:2015-1-28
    上传到七牛
    by: 范俊伟 at:2015-04-14
    :param request:
    :return:
    """
    fileobj = get_object_or_404(BaseFile, pk=file_id)

    if not request.FILES.has_key('file'):
        return getResult(False, u'没有提交文件', None)
    else:
        f = request.FILES['file']
        data = ''
        for chunk in f.chunks():
            data += chunk
        return getResult(True, u'',  fileobj.putdata(data))

def put_file(request,file_id):
    """
    上传到七牛
    by: 范俊伟 at:2015-04-14
    根据七牛的返回结果，判断对错
    by: 王健 at:2015-04-15
    put方法没有cookie
    by: 范俊伟 at:2015-04-15
    :param request:
    :return:
    """
    fileobj = get_object_or_404(BaseFile, pk=file_id)
    data = request.read()
    res = fileobj.putdata(data)
    if res:
        return getResult(True, u'', res)
    else:
        raise Http404()

@client_login_project_required
def check_file_upload_status(request, project_id):
    """
    判断文件上传是否成功
    by:王健 at:2015-1-26
    :param request:
    :param project_id:
    :return:
    """
    fileurl = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(File, pk=fileurl, project_id=project_id)
    #todo:获取bcs端 文件是否存在
    return getResult(True, u'', fileobj.check_file())


def check_bigcompany_file_upload_status(request):
    """
    判断文件上传是否成功
    by:尚宗凯 at:2015-6-16
    :param request:
    :param project_id:
    :return:
    """
    fileurl = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(SysFile, pk=fileurl )
    #todo:获取bcs端 文件是否存在
    return getResult(True, u'', fileobj.check_file())


def check_company_file_upload_status(request):
    """
    判断文件上传是否成功
    by:尚宗凯 at:2015-6-16
    """
    fileurl = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(ComFile, pk=fileurl)
    #todo:获取bcs端 文件是否存在
    return getResult(True, u'', fileobj.check_file())


@client_login_project_required
@transaction.atomic()
def confirm_upload_files(request, project_id):
    """
    根据文件的路径，设置文件上传成功，并返回文件的geturl
    by:王健 at:2015-1-10
    :param request:
    :param project_id:
    :return:
    """
    fileurl = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(File, pk=fileurl, project_id=project_id)
    fileobj.file_status = True
    fileobj.save()
    return getResult(True, u'上传文件成功', {'geturl': fileobj.get_url()})

def get_qn_fop(request):
    """
    将请求参数转换为七牛云存储数据处理
    by: 范俊伟 at:2015-04-08
    :param request:
    :return:
    """
    img_w = request.REQUEST.get('img_w')
    img_h = request.REQUEST.get('img_h')
    fop_args= []
    if img_w and img_h:
        fop_args.append('imageView2/5/w/%s/h/%s' % (img_w, img_h))
    fop = '|'.join(fop_args)
    return fop

@client_login_project_required
def get_url_by_file(request, project_id):
    """
    根据文件的路径，设置文件上传成功，并返回文件的geturl
    by:王健 at:2015-1-12
    返回文件的名字、类型、大小
    by:王健 at:2015-1-13
    根据文件ids 查询文件信息列表, 防止fileid为None
    by:王健 at:2015-2-2
    支持图片缩放
    by: 范俊伟 at:2015-04-08
    输出图片分辨率字段
    by: 范俊伟 at:2015-04-09
    检测fileid参数格式
    by: 范俊伟 at:2015-05-04
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    :param request:
    :param project_id:
    :return:
    """
    fileurls = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    try:
        for i in fileurls:
            int(i)
    except:
        return getResult(False, 'fileid格式错误')

    fileobjs = File.objects.filter(pk__in=fileurls, project_id=project_id)
    l = []
    for fileobj in fileobjs:
        l.append({'id': fileobj.id, 'geturl': fileobj.get_url(get_qn_fop(request)), 'name': fileobj.name, 'filetype': fileobj.filetype, 'size': fileobj.size, 'img_size':fileobj.img_size})
    if len(fileurls) > 1:
        return getResult(True, u'', l)
    elif len(fileurls) == 1:
        if l:
            return getResult(True, u'', l[0])
    return Http404()


def get_bigcompany_url_by_file(request):
    """
    根据文件的路径，设置文件上传成功，并返回文件的geturl
    by:王健 at:2015-1-12
    返回文件的名字、类型、大小
    by:王健 at:2015-1-13
    根据文件ids 查询文件信息列表, 防止fileid为None
    by:王健 at:2015-2-2
    支持图片缩放
    by: 范俊伟 at:2015-04-08
    输出图片分辨率字段
    by: 范俊伟 at:2015-04-09
    检测fileid参数格式
    by: 范俊伟 at:2015-05-04
    优化兼容逗号分隔的列表
    by:王健 at:2015-05-19
    :param request:
    :param project_id:
    :return:
    """
    fileurls = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    try:
        for i in fileurls:
            int(i)
    except:
        return getResult(False, 'fileid格式错误')

    fileobjs = SysFile.objects.filter(pk__in=fileurls)
    l = []
    for fileobj in fileobjs:
        l.append({'id': fileobj.id, 'geturl': fileobj.get_url(get_qn_fop(request)), 'name': fileobj.name, 'filetype': fileobj.filetype, 'size': fileobj.size, 'img_size':fileobj.img_size})
    if len(fileurls) > 1:
        return getResult(True, u'', l)
    elif len(fileurls) == 1:
        if l:
            return getResult(True, u'', l[0])
    return Http404()


def get_company_url_by_file(request):
    """
    获取附件url
    by：尚宗凯 at：2015-06-17
    """
    fileurls = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    try:
        for i in fileurls:
            int(i)
    except:
        return getResult(False, 'fileid格式错误')

    fileobjs = ComFile.objects.filter(pk__in=fileurls)
    l = []
    for fileobj in fileobjs:
        l.append({'id': fileobj.id, 'geturl': fileobj.get_url(get_qn_fop(request)), 'name': fileobj.name, 'filetype': fileobj.filetype, 'size': fileobj.size, 'img_size':fileobj.img_size})
    if len(fileurls) > 1:
        return getResult(True, u'', l)
    elif len(fileurls) == 1:
        if l:
            return getResult(True, u'', l[0])
    return Http404()
