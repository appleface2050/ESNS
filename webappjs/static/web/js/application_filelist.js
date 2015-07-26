/**
 * Date: 15/1/23
 * Time: 14:47
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */


var filelist_array = [];
var last_get_upload_result;
var upload_fileids = [];
var last_file_info = null;

function getUploadUrl(filetype, size, filename, cb) {
    /**
     * 获取上传URL
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/nf/' + window.project_id + '/get_qn_upload_files_url';
    var data = {
        filetype: filetype,
        size: size,
        filename: filename
    };
    httpRequest(url, data).done(function (data) {
        if (data.result) {
            console.log(data.result);
            last_get_upload_result = data.result;
            cb(data.result);
        }
    });
}

function checkFileUpload(fileid, cb) {
    /**
     * 检测文件是否上传成功
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/nf/' + window.project_id + '/check_file_upload_status';
    var data = {
        fileid: fileid
    };
    httpRequest(url, data).then(function (data) {
        console.log(data);
        cb(true);

    }, function () {
        cb(false);
        $.simplyToast('上传失败', 'danger');
    });
}

function getFileInfo(fileid, cb, img_w, img_h) {
    /**
     * 下载文件
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     增加图片缩放参数
     by: 范俊伟 at:2015-04-08
     * @type {string}
     */
    var url = '/nf/' + window.project_id + '/get_url_by_file';
    var data = {
        fileid: fileid
    };
    if (img_w && img_h) {
        data['img_w'] = img_w;
        data['img_h'] = img_h;
    }
    httpRequest(url, data).done(function (data) {
        console.log(data);
        cb(data.result);
    });
}

function show_browse_filelist() {
    /**
     * 显示文件列表浏览页面
     * by:范俊伟 at:2015-01-26
     */
    templateRender('web/mst/application_browse_filelist.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        filelist_array = [];
        getFileList(current_app_group.flag);
    });
}

function getFileList(flag) {
    /**
     * 获取文件列表数据,填充文件列表浏览界面
     * by:范俊伟 at:2015-01-26
     * 参数修改
     by: 范俊伟 at:2015-02-13
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/query_file_by_group_old';
    var data = {
        flag: flag
    };
    if (filelist_array.length > 0) {
        data['timeline'] = filelist_array[filelist_array.length - 1].timeline;
    }
    httpRequest(url, data).then(function (data) {
        if (data.result && data.result.length > 0) {
            console.log(data);
            filelist_array = filelist_array.concat(data.result);//数组合并
            appendFilelistData(data);
            setTimeout(function () {
                getFileList(flag)
            }, 0)
        }
    });
}


var getFileTypeIcon = function (type) {
    /**
     * 根据文件扩展名获取图标
     * by:范俊伟 at:2015-02-07
     * @type {string[]}
     */
    var known_type = ['doc', 'docx', 'jpg', 'pdf', 'png', 'ppt', 'pptx', 'xls', 'xlsx'];
    var is_known_type = false;
    for (var i = 0; i < known_type.length; i++) {
        if (type == known_type[i]) {
            is_known_type = true;
        }
    }
    if (is_known_type)
        return staticUrl + 'web/img/file_type/' + type + '@3x.png';
    else
        return staticUrl + 'web/img/file@3x.png';
};

var template_fileinfo = function () {
    return function (text, render) {
        /**
         * 模板所需函数,获得文件信息
         * by:范俊伟 at:2015-02-01
         * 增加文件类型图标
         * by:范俊伟 at:2015-02-07
         * @type {string}
         */
        var fileid = $.trim(render(text));
        getFileInfo(fileid, function (result) {
            var html_a = $('<a>');
            html_a.attr('href', result.geturl);
            var html_a_div = $('<div>');
            html_a_div.attr('class', 'row');
            html_a.append(html_a_div);
            var html_a_div_div1 = $('<div>');
            html_a_div_div1.attr('class', 'col-md-12 text-center');
            var html_a_div_div1_img = $('<img>');
            html_a_div_div1_img.attr('class', 'file_type_icon');
            console.log(result);
            html_a_div_div1_img.attr('src', getFileTypeIcon(result.filetype));
            html_a_div_div1.append(html_a_div_div1_img);


            var html_a_div_div2 = $('<div>');
            html_a_div_div2.attr('class', 'col-md-12 text-center filelist_file_name');
            html_a_div_div2.text(result.name);

            html_a_div.append(html_a_div_div1);
            html_a_div.append(html_a_div_div2);

            $('div[file_display=' + fileid + ']').html(html_a);
        });
        return '<div class="col-md-3" file_display="' + fileid + '"></div>';
        //<div class="col-md-3" id="file_{{ . }}">{{ fileinfo }}</div>
    };
};

function appendFilelistData(data) {
    /**
     * 追加文件列表数据
     * by:范俊伟 at:2015-01-26
     */
    data.fileinfo = template_fileinfo;
    templateRender('web/mst/application_filelist_dataitem.mst', data, function (rendered) {

        $('#filelist_content').append(rendered);
    });
}

function show_create_filelist() {
    /**
     * 显示创建文件列表界面
     * by:范俊伟 at:2015-01-26
     */
    upload_fileids = [];
    last_get_upload_result = null;
    last_file_info = null;
    templateRender('web/mst/application_create_filelist.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        initForm();
        var create_filelist = $('#create_filelist');

        var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                //if (checkForm(create_filelist)) {
                var deferred = $.Deferred();
                showMask();
                getUploadUrl(type, file_obj.size, file_name, function (result) {
                    last_file_info = {
                        name: file_name,
                        type: type
                    };
                    ajaxupload._settings.action = result.posturl;
                    var parm = {};
                    _(result.params).each(function (value, key) {
                        parm[key] = value;
                    });
                    ajaxupload._settings.data = parm;
                    console.log(ajaxupload._settings.data);
                    deferred.resolve();
                });
                return deferred.promise();
                //}
                //else {
                //    return false;
                //}


            },
            onComplete: function (file, response) {
                checkFileUpload(last_get_upload_result.fileid, function (success) {
                        hideMask();
                        if (success) {
                            upload_fileids = [last_get_upload_result.fileid];
                            appendUploadFile(last_file_info);
                            last_get_upload_result = null;
                            last_file_info = null;

                        }

                    }
                );
            }
        });
    });
}

function uploadFile() {
    /**
     * 文件上传
     * by:范俊伟 at:2015-01-26
     * 修改上传接口
     * by:范俊伟 at:2015-01-29
     * 解决火狐浏览器上传某些文件格式会自动下载的bug
     by: 范俊伟 at:2015-03-18
     * @type {*|jQuery|HTMLElement}
     */
    console.log('uploadFile');
    var form = $('#upload_form');
    var files = $('#upload')[0].files;
    if (files.length == 1) {
        var file = files[0];
        var ldot = file.name.lastIndexOf(".");
        var type = file.name.substring(ldot + 1);
        console.log(file.lastModifiedDate, file.name, file.size, type);
        getUploadUrl(type, file.size, file.name, function (result) {
            last_file_info = {
                name: file.name,
                type: type
            };
            //var url = '/nf/' + window.project_id + '/upload_files?fileid=' + result.fileid;
            var url = result.posturl;
            form.attr('action', url);
            form.find('input[type=hidden]').remove();
            _(result.params).each(function (value, key) {
                var input = $('<input>');
                input.attr('type', 'hidden');
                input.attr('name', key);
                input.attr('value', value);
                form.append(input);
            });
            form.submit();
        });
    }
}

function filelistUploadCheck() {
    /**
     * input检测回调函数,检查是否选择了文件
     * by:范俊伟 at:2015-01-27
     */
    console.log('uploadFile');
    var form = $('#upload_form');
    var files = $('#upload')[0].files;
    if (files.length == 1) {
        return null;
    }
    else if (files.length > 1) {
        return '请选择一个文件';
    }
    else if (files.length == 0) {
        return '未选择文件';
    }
}

function filelistSaveFormCallback(data) {
    /**
     * filelist form回调函数
     * by:范俊伟 at:2015-01-26
     */
    if (data.success) {
        $('#fileid').val('');
        last_get_upload_result = null;
        confirmBox.showConfirm('完成', '保存成功', '确定', '', function () {
            show_browse_filelist();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }
}

function filesUploadIFrameCallback() {
    /**
     * filelist 上传iframe载入后回调函数
     * by:范俊伟 at:2015-01-26
     */
    if (last_get_upload_result) {
        checkFileUpload(last_get_upload_result.fileid, function () {
                console.log(last_get_upload_result.fileid);
                upload_fileids.push(last_get_upload_result.fileid)
                last_get_upload_result = null;
                appendUploadFile(last_file_info);
                last_file_info = null;
                $('#upload_form')[0].reset();
                $.simplyToast('上传成功!', 'success');
            }
        );
    }
}

function appendUploadFile(fileInfo) {
    /**
     * 上传文件后附加已上传文件信息
     * by:范俊伟 at:2015-02-01
     * 增加文件类型图标
     * by:范俊伟 at:2015-02-07
     * @type {string}
     */
    var html_root = $('<div class="col-md-3" ></div>');


    var html_a_div = $('<div>');
    html_a_div.attr('class', 'row');

    var html_a_div_div1 = $('<div>');
    html_a_div_div1.attr('class', 'col-md-12 text-center');
    var html_a_div_div1_img = $('<img>');
    html_a_div_div1_img.attr('class', 'file_type_icon');
    html_a_div_div1_img.attr('src', getFileTypeIcon(fileInfo.type));
    html_a_div_div1.append(html_a_div_div1_img);


    var html_a_div_div2 = $('<div>');
    html_a_div_div2.attr('class', 'col-md-12 text-center filelist_file_name');
    html_a_div_div2.text(fileInfo.name);

    html_a_div.append(html_a_div_div1);
    html_a_div.append(html_a_div_div2);

    html_root.html(html_a_div);

    $('#upload_list').html(html_root);
}

function uploadFileButtonClick() {
    /**
     * 上传按钮事件
     * by:范俊伟 at:2015-02-01
     */
    if (last_file_info) {
        $.simplyToast('正在上传,请稍后...', 'danger');
    }
    else {
        var upload_form = $('#upload_form');
        if (checkForm(upload_form)) {
            uploadFile();
        }
    }
}

function createFileListButtonClick() {
    /**
     * filelist 创建按钮点击事件
     * by:范俊伟 at:2015-01-26
     */
    if (upload_fileids.length == 0) {
        messageBox.showMessage('温馨提示', '还未选择文件');
    }
    else {
        var create_filelist = $('#create_filelist');
        $('#fileid').val(upload_fileids.join(','));
        $('#flag').val(current_app_group.flag);
        var url = '/ns/' + window.project_id + '/create_file_by_group';
        create_filelist.attr('action', url);
        create_filelist.submit();
    }

}