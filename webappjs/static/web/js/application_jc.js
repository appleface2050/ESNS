/**
 * Date: 15/1/23
 * Time: 14:47
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

var jc_array = [];
var jc_save_fun = null;

function show_browse_jc() {
    /**
     * 显示列表浏览页面
     * by:范俊伟 at:2015-02-02
     */

    templateRender('web/mst/application_browse_jc.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        jc_array = [];
        getJcDataItems(current_app_group.flag);
    });
}


function getJcDataItems(flag) {
    /**
     * 获取列表数据,填充文件列表浏览界面
     * by:范俊伟 at:2015-02-02
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/query_enginecheck_by_group_old';
    var data = {
        flag: flag
    };
    if (jc_array.length > 0) {
        data['timeline'] = jc_array[jc_array.length - 1].timeline;
    }
    httpRequest(url, data).done(function (data) {
        if (data.result && data.result.length > 0) {
            jc_array = jc_array.concat(data.result);//数组合并
            console.log('getJcDataItems', data);
            appendJcData(data);

            setTimeout("getJcDataItems('" + flag + "')", 0);
        }
    });
}

var status_display = function () {
    /**
     * 模板所需函数,输出状态信息
     * by:范俊伟 at:2015-02-02
     */
    if (this.status) {
        return '<span class="glyphicon glyphicon-ok"></span><br>完成';
    }
    else {
        return '<div class="text-danger"> <span class="glyphicon glyphicon-wrench"></span><br>处理中</div>';
    }
};

function appendJcData(data) {
    /**
     * 追加列表数据
     * by:范俊伟 at:2015-02-02
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    data.status_display = status_display;
    templateRender('web/mst/application_jc_dataitem.mst', data, function (rendered) {
        $('#jc_content').append(rendered);
    });
}

function openJcItem(id) {
    /**
     * 检查项目点击处理函数
     * by:范俊伟 at:2015-02-02
     */
    for (var i = 0; i < jc_array.length; i++) {
        if (jc_array[i].id == id) {
            var data = jc_array[i];
            if (!data.status) {
                showDoJcItem(data);
            }
            else {
                showJcItem(data);
            }
        }
    }
}

function showDoJcItem(data) {
    /**
     * 显示检查处理界面
     * by:范俊伟 at:2015-02-02
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    templateRender('web/mst/application_do_jc.mst', data, function (rendered) {
        $('#app_content').html(rendered);
        jc_init_form();
    });
}
var jc_template_image = function () {
    /**
     * 模板所需函数,显示原图
     * by:范俊伟 at:2015-02-01
     * @type {template_image}
     */
    var file_id = this;
    getImageByFileid(file_id, false, '500px', '500px');
    return file_id;
};

function showJcItem(data) {
    /**
     * 显示检查结果界面
     * by:范俊伟 at:2015-02-02
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    data.template_image = jc_template_image;
    data.pre_pic_array = [data.pre_pic];
    data.chuli_pic_array = [data.chuli_pic];
    templateRender('web/mst/application_jc_open_item.mst', data, function (rendered) {
        $('#app_content').html(rendered);
    });
}

function jc_init_form() {
    /**
     * 初始化表单相关处理函数
     * by:范俊伟 at:2015-02-02
     */
    initForm();
    $('#upload').unbind('blur');

    var iframe = $('#bcs_upload')[0];
    if (iframe.attachEvent) {
        iframe.attachEvent("onload", function () {
            imagesForJcUploadIFrameCallback();
        });
    } else {
        iframe.onload = function () {
            imagesForJcUploadIFrameCallback();
        };
    }
}

function showCreateJc() {
    /**
     * 显示创建文件列表界面
     * by:范俊伟 at:2015-02-02
     * 逻辑修改
     by: 范俊伟 at:2015-02-13
     */
    last_get_upload_result = null;
    last_file_info = null;
    templateRender('web/mst/application_create_jc.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        jc_init_form();
    });
}

function uploadImageForJcSubmit() {
    /**
     * 文件上传
     * by:范俊伟 at:2015-02-02
     * @type {*|jQuery|HTMLElement}
     */
    var form = $('#upload_form');
    var files = $('#upload')[0].files;
    if (files.length == 1) {
        var file = files[0];
        var ldot = file.name.lastIndexOf(".");
        var type = file.name.substring(ldot + 1);
        console.log(file.lastModifiedDate, file.name, file.size, type);
        getUploadUrl(type, file.size, file.name, function (result) {
            form.attr('action', result.posturl);
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

function imageForJcUploadCheck() {
    /**
     * 检查是否选择了文件
     * by:范俊伟 at:2015-02-02
     */
    console.log('imageForJcUploadCheck');
    var form = $('#upload_form');
    var files = $('#upload')[0].files;
    if (files.length == 1) {
        var file = files[0];
        var ldot = file.name.lastIndexOf(".");
        var type = file.name.substring(ldot + 1);
        if (type == 'bmp' || type == 'jpg' || type == 'png' || type == 'gif')
            return null;
        else
            return "请选择图片格式文件(*.bmp,*.jpg,*.png,*.gif)";
    }
    else if (files.length > 1) {
        return '请选择一个文件';
    }
    else if (files.length == 0) {
        return '未选择文件';
    }
}

function createJcFormCallback(data) {
    /**
     * jc form回调函数
     * by:范俊伟 at:2015-02-02
     */
    if (data.success) {
        $('#fileid').val('');
        last_get_upload_result = null;
        confirmBox.showConfirm('完成', '保存成功', '确定', '', function () {
            show_browse_jc();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }
}

function imagesForJcUploadIFrameCallback() {
    /**
     * jc 上传iframe载入后回调函数
     * by:范俊伟 at:2015-02-02
     */
    if (last_get_upload_result) {
        checkFileUpload(last_get_upload_result.fileid, function () {
                jc_save_fun(last_get_upload_result.fileid);
                last_get_upload_result = null;
                last_file_info = null;
            }
        );
    }
}


function uploadImageForJc() {
    /**
     * 文件上传
     * by:范俊伟 at:2015-02-02
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
            var url = result.posturl;
            form.attr('action', result.posturl);
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
function checkAndUploadImageForJc() {
    /**
     * 检查并上传
     * by:范俊伟 at:2015-02-02
     */
    if (last_file_info) {
        $.simplyToast('正在上传,请稍后...', 'danger');
    }
    else {
        var upload_form = $('#upload_form');
        if (checkForm(upload_form)) {
            uploadImageForJc();
        }
    }

}
function createJc(fileid) {
    /**
     * 创建检查函数
     * by:范俊伟 at:2015-02-02
     * @type {*|jQuery|HTMLElement}
     */
    var jc_from = $('#jc_from');
    $('#fileid').val(fileid);
    $('#flag').val(current_app_group.flag);
    var url = '/ns/' + window.project_id + '/create_enginecheck_by_group';
    jc_from.attr('action', url);
    jc_from.submit();
}
function doJc(fileid) {
    /**
     * 处理检查函数
     * by:范俊伟 at:2015-02-02
     * 检测处理需要flag
     by: 范俊伟 at:2015-03-11
     * @type {*|jQuery|HTMLElement}
     */
    var jc_from = $('#jc_from');
    $('#fileid').val(fileid);
    $('#flag').val(current_app_group.flag);
    var url = '/ns/' + window.project_id + '/update_enginecheck_by_group';
    jc_from.attr('action', url);
    jc_from.submit();
}
function saveJcButtonClick() {
    /**
     * jc 创建按钮点击事件
     * by:范俊伟 at:2015-02-02
     */
    jc_save_fun = createJc;
    var upload_form = $('#upload_form');
    var jc_from = $('#jc_from');
    if (checkForm(jc_from) && checkForm(upload_form)) {
        checkAndUploadImageForJc();
    }

}

function doJcButtonClick() {
    /**
     * jc 创建按钮点击事件
     * by:范俊伟 at:2015-02-02
     */
    jc_save_fun = doJc;
    var upload_form = $('#upload_form');
    var jc_from = $('#jc_from');
    if (checkForm(jc_from) && checkForm(upload_form)) {
        checkAndUploadImageForJc();
    }

}