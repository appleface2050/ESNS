/**
 * Date: 15/1/21
 * Time: 14:04
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
function show_update_user_info() {
    /**
     * 显示用户信息修改
     * by:范俊伟 at:2015-02-02
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    getUserInfo(function (userInfo) {
        templateRender('web/mst/update_user_info.mst', userInfo, function (rendered) {
            $('#user_info').html(rendered);
            initForm();
            initDateTimePicker();
            initCity();
        });
    });
}
function updateUserInfoClick() {
    /**
     * 用户信息修改按钮事件
     * by:范俊伟 at:2015-02-02
     */
    $('#update_user_info_from').submit();
}
function updateUserInfoFormCallback(data) {
    /**
     * 用户信息修改表单回调函数
     * by:范俊伟 at:2015-02-02
     * 修改用户信息后,重新初始化页面
     * by:范俊伟 at:2015-02-03
     */
    if (data.success) {
        window.userInfo = undefined;
        initPage();
        showUserInfo();
    }
    else {
        onFormCheckError();
        $('#form_error').text(data.message);
    }
}
function showUserInfo() {
    /**
     * 显示用户信息
     * by:范俊伟 at:2015-02-02
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     错误处理
     by: 范俊伟 at:2015-03-15
     */
    $.when(
        getUserInfo(),
        getUserJifen()
    ).then(function (userinfo, jifen) {
            console.log('jifen', jifen);
            window.viewDTD.resolve();
            userinfo.jifen = jifen;
            templateRender('web/mst/user_info.mst', userinfo, function (rendered) {
                $('#user_info').html(rendered);
            });
        }, function () {
            window.viewDTD.resolve();
        });
}
function showUpdateUserIcon() {
    /**
     * 显示修改用户头像界面
     * by:范俊伟 at:2015-02-09
     * 逻辑修改
     by: 范俊伟 at:2015-02-13
     */
    last_get_upload_result = null;
    last_file_info = null;
    templateRender('web/mst/update_user_icon.mst', {}, function (rendered) {
        $('#user_info').html(rendered);
        initForm();
        $('#upload').unbind('blur');

        var iframe = $('#bcs_upload')[0];
        if (iframe.attachEvent) {
            iframe.attachEvent("onload", function () {
                updateUserIconUploadIFrameCallback();
            });
        } else {
            iframe.onload = function () {
                updateUserIconUploadIFrameCallback();
            };
        }
    });
}

function updateUserIconUploadIFrameCallback() {
    /**
     * 头像上传iframe载入后回调函数
     * by:范俊伟 at:2015-02-09
     */
    if (last_get_upload_result) {
        //checkFileUpload(last_get_upload_result.fileid, function () {
        updateUserIcon(last_get_upload_result.fileid);
        last_get_upload_result = null;
        last_file_info = null;
        //});

    }
}
function updateUserIcon(fileid) {
    /**
     * 更新用户头像
     * by:范俊伟 at:2015-02-09
     * 修改头像后清空用户信息变量
     by: 范俊伟 at:2015-03-11
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {*|jQuery|HTMLElement}
     */
    httpRequest('/ns/update_user_icon_url', {fileid: fileid}).done(function (data) {
        window.userInfo = undefined;
        showUserInfo();
    });
}
function imageForUserIconUploadCheck() {
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
function getUploadUserIconUrl(filetype, size, filename, cb) {
    /**
     * 获取上传头像的URL
     * by:范俊伟 at:2015-02-09
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var data = {
        filetype: filetype,
        size: size,
        filename: filename
    };
    httpRequest('/ns/get_qn_upload_user_icon_url', data).done(function (data) {
        if (data.result) {
            console.log(data.result);
            last_get_upload_result = data.result;
            cb(data.result);
        }
    });
}
function uploadImageForUserIcon() {
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
        getUploadUserIconUrl(type, file.size, file.name, function (result) {
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

function saveUserIcon() {
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
            uploadImageForUserIcon();
        }
    }

}

function init_view_user_info() {
    /**
     * 初始化用户信息视图
     * by:范俊伟 at:2015-02-06
     */
    var html = '<div id="user_info"></div>';
    $('#view_content').html(html);
    showUserInfo();
}