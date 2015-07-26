/**
 * Date: 15/02/03
 * Time: 14:04
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

function updateUserInfoClick() {
    /**
     * 用户信息修改按钮事件
     * by:范俊伟 at:2015-02-03
     */
    $('#update_user_info_from').submit();
}
function showProjectInfoView() {
    /**
     * 显示项目信息
     * by:范俊伟 at:2015-02-03
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * 改用checkManage
     by: 范俊伟 at:2015-03-01
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     显示账号余额
     by: 范俊伟 at:2015-03-15
     错误处理
     by: 范俊伟 at:2015-03-15
     */
    checkManage(function (manager) {
        var is_manage = manager.on && manager.say;
        getProjectInfo(function (data) {
            data.is_manage = is_manage;
            templateRender('web/mst/project_info_panel.mst', data, function (rendered) {
                $('#view_content').html(rendered);

                if (is_manage) {
                    var url = '/ns/' + window.project_id + '/get_project_balance';
                    httpRequest(url, {}).then(function (data) {
                        window.viewDTD.resolve();
                        console.log('get_project_balance', data);
                        var result = data.result;
                        $('#person_nums').text(result.person_nums);
                        $('#days').text(result.days + '天');
                        $('#balance').text((result.total - result.price) + '金豆');
                    }, function () {
                        window.viewDTD.resolve();
                    });
                }
                else {
                    window.viewDTD.resolve();
                }
            });
        });

    });

}
function showUpdateProjectInfo() {
    /**
     * 显示修改项目界面
     * by:范俊伟 at:2015-02-03
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    getProjectInfo(function (data) {
        console.log('showUpdateProjectInfo', data);
        templateRender('web/mst/project_save.mst', data, function (rendered) {
            $('#view_content').html(rendered);
            initForm();
            initDateTimePicker();
            initCity();
        });
    });

}
function formCallback(data) {
    /**
     * 表单ajax提交回调函数
     * by:范俊伟 at:2015-02-03
     */
    if (data.success) {
        try {
            window.projectInfo = undefined;
        } catch (e) {

        }

        $('#form_error').text('');
        $('#project_from')[0].reset();
        initPage();
        showProjectInfoView();
        $.simplyToast('保存成功', 'success');
    }
    else {
        onFormCheckError();
        $('#form_error').text(data.message);
    }
}
function upateProjectButtonClick() {
    /**
     * 保存工程按钮事件
     * by:范俊伟 at:2015-02-03
     */
    var form = $('#project_from');
    var url = '/ns/' + window.project_id + '/update_project';
    form.attr('action', url);
    form.submit();
}

function showUpdateProjectIcon() {
    /**
     * 显示修改项目头像界面
     * by:范俊伟 at:2015-02-09
     * 逻辑修改
     by: 范俊伟 at:2015-02-13
     */
    last_get_upload_result = null;
    last_file_info = null;
    templateRender('web/mst/update_project_icon.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        initForm();
        $('#upload').unbind('blur');

        var iframe = $('#bcs_upload')[0];
        if (iframe.attachEvent) {
            iframe.attachEvent("onload", function () {
                updateProjectIconUploadIFrameCallback();
            });
        } else {
            iframe.onload = function () {
                updateProjectIconUploadIFrameCallback();
            };
        }
    });
}

function updateProjectIconUploadIFrameCallback() {
    /**
     * 头像上传iframe载入后回调函数
     * by:范俊伟 at:2015-02-09
     */
    if (last_get_upload_result) {
        //checkFileUpload(last_get_upload_result.fileid, function () {
        updateProjectIcon(last_get_upload_result.fileid);
        last_get_upload_result = null;
        last_file_info = null;
        //});

    }
}
function updateProjectIcon(fileid) {
    /**
     * 更新项目头像
     * by:范俊伟 at:2015-02-09
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {*|jQuery|HTMLElement}
     */
    var url = '/ns/' + window.project_id + '/update_project_icon_url';
    httpRequest(url, {fileid: fileid}).done(function (data) {
        initPage();
        showProjectInfoView();
    });
}
function imageForProjectIconUploadCheck() {
    /**
     * 检查是否选择了图片文件
     * by:范俊伟 at:2015-02-09
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
function getUploadProjectIconUrl(filetype, size, filename, cb) {
    /**
     * 获取上传头像的URL
     * by:范俊伟 at:2015-02-09
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/get_qn_upload_project_icon_url';
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
function uploadImageForProjectIcon() {
    /**
     * 图片上传
     * by:范俊伟 at:2015-02-09
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
        getUploadProjectIconUrl(type, file.size, file.name, function (result) {
            last_file_info = {
                name: file.name,
                type: type
            };
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

function saveProjectIcon() {
    /**
     * 保存头像按钮事件
     * by:范俊伟 at:2015-02-09
     */
    if (last_file_info) {
        $.simplyToast('正在上传,请稍后...', 'danger');
    }
    else {
        var upload_form = $('#upload_form');
        if (checkForm(upload_form)) {
            uploadImageForProjectIcon();
        }
    }

}
function confirmLeaveProjectInfo() {
    /**
     * 退出项目
     * by: 范俊伟 at: 2015-02-09
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    confirmBox.showConfirm('退出项目', '是否确认要退出此项目', '确定', '取消', function () {
        var url = '/ns/' + window.project_id + '/leave_project';
        httpRequest(url).done(function (data) {
            window.project_id = undefined;
            openView('home');
        });
    }, null)
}
function init_view_project_info() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     */
    showProjectInfoView();
    saveProjectButtonClick = upateProjectButtonClick;
}