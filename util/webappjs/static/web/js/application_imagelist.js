/**
 * Date: 15/1/23
 * Time: 14:47
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

var imagelist_array = [];
var is_bg_state;//是否为曝光警告,bgimages

function show_browse_imagelist() {
    /**
     * 显示文件列表浏览页面
     * by:范俊伟 at:2015-01-29
     */
    if (current_app_group.typeflag == 'bgimages') {
        is_bg_state = true;
    }
    else {
        is_bg_state = false;
    }

    templateRender('web/mst/application_browse_imagelist.mst', {is_bg_state: is_bg_state}, function (rendered) {
        $('#app_content').html(rendered);
        imagelist_array = [];
        getImagelistDataItems(current_app_group.flag);
    });
}

function openImagelistItem(id) {
    /**
     * 打开项目
     * by:范俊伟 at:2015-02-01
     * 显示评论
     by: 范俊伟 at:2015-02-26
     */
    for (var i = 0; i < imagelist_array.length; i++) {
        if (imagelist_array[i].id == id) {
            var data = imagelist_array[i];
            data.template_image = template_image;
            data.is_bg_state = is_bg_state;
            templateRender('web/mst/application_imagelist_open_item.mst', data, function (rendered) {
                $('#app_content').html(rendered);
                getImagesReplay(id);
            });
        }

    }

}
function getImagesReplay(id) {
    /**
     * 获取评论
     by: 范俊伟 at:2015-02-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_replay_filerecord_by_id';
    var data = {
        id: id,
        flag: current_app_group.flag
    };
    httpRequest(url, data).done(function (data) {
        console.log(data);
        var tmp_data = {
            list: data.result.pinglun,
            images_id: id
        };
        templateRender('web/mst/application_imagelist_open_item_replay.mst', tmp_data, function (rendered) {
            $('#replay_list').html(rendered);
        });
    });
}

function getImagelistDataItems(flag) {
    /**
     * 获取文件列表数据,填充文件列表浏览界面
     * by:范俊伟 at:2015-01-29
     * 参数修改
     by: 范俊伟 at:2015-02-13
     修改错误
     by: 范俊伟 at:2015-02-13
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/query_file_by_group_old';
    var data = {
        flag: flag
    };
    if (imagelist_array.length > 0) {
        data['timeline'] = imagelist_array[imagelist_array.length - 1].timeline;
    }
    httpRequest(url, data).done(function (data) {
        if (data.result && data.result.length > 0) {
            imagelist_array = imagelist_array.concat(data.result);//数组合并

            appendImagelistData(data);
            setTimeout("getImagelistDataItems('" + flag + "')", 0);
        }
    });
}

var template_first_image = function () {
    /**
     * 模板所需函数,显示第一个图片缩略图
     * by:范俊伟 at:2015-02-01
     * @type {FileList}
     */
    var files = this.files;
    var file_id = files[0];
    getImageByFileid(file_id, true);
    return file_id;
};

var template_image = function () {
    /**
     * 模板所需函数,显示原图
     * by:范俊伟 at:2015-02-01
     * @type {template_image}
     */
    var file_id = this;
    getImageByFileid(file_id, false);
    return file_id;
};

function appendImagelistData(data) {
    /**
     * 追加文件列表数据
     * by:范俊伟 at:2015-01-29
     */
    data.template_first_image = template_first_image;
    data.is_bg_state = is_bg_state;
    templateRender('web/mst/application_imagelist_dataitem.mst', data, function (rendered) {
        $('#imagelist_content').append(rendered);
    });
}


function getImageByFileid(fileid, thumbnail, max_width, max_height) {
    /**
     * 获取图片
     * by:范俊伟 at:2015-01-29
     * 增加图片缩放参数
     by: 范俊伟 at:2015-04-08
     * @type {string}
     */
    if (thumbnail) {
        max_width = 100;
        max_height = 100;
    }
    getFileInfo(fileid, function (result) {
        var img = $('<img>');
        img.attr('src', result.geturl);
        if (max_width) {
            img.css('max-width', max_width);
        }
        if (max_height) {
            img.css('max-height', max_height);
        }
        $('#image_file_id_' + fileid).html(img);
    }, max_width, max_height);


}

function showCreateImagelist() {
    /**
     * 显示创建文件列表界面
     * by:范俊伟 at:2015-01-29
     * 逻辑修改
     by: 范俊伟 at:2015-02-13
     初始化清空参数
     by: 范俊伟 at:2015-02-13
     处理方式改为自由输入
     by: 范俊伟 at:2015-03-11
     */
    last_get_upload_result = null;
    last_file_info = null;
    upload_fileids = [];
    templateRender('web/mst/application_create_imagelist.mst', {is_bg_state: is_bg_state}, function (rendered) {
        $('#app_content').html(rendered);
        initForm();
        $('#upload').unbind('blur');

        //if (is_bg_state) {
        //    $("#for_bg_je").unbind('blur').blur(function () {
        //        checkField($(this));
        //    });
        //    $("#for_bg").change(function () {
        //        var select_value = $(this).children('option:selected').val();
        //        if (select_value == '2') {
        //            $('#for_bg_je_group').show();
        //            $('#for_bg_je').attr('input-check', 'required,number');
        //        }
        //        else {
        //            $('#for_bg_je_group').hide();
        //            $('#for_bg_je').attr('input-check', '');
        //        }
        //    });
        //}
        var imagelist_from = $('#imagelist_from');

        var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((type == 'bmp' || type == 'jpg' || type == 'png' || type == 'gif')) {
                    //if (checkForm(imagelist_from)) {
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

                }
                else {
                    messageBox.showMessage('温馨提示', '请选择图片格式文件(*.bmp,*.jpg,*.png,*.gif)');
                    return false;
                }

            },
            onComplete: function (file, response) {
                checkFileUpload(last_get_upload_result.fileid, function (success) {
                        hideMask();
                        if (success) {
                            upload_fileids = [last_get_upload_result.fileid];
                            appendUploadImage(last_get_upload_result.fileid);
                            last_get_upload_result = null;
                            last_file_info = null;
                        }

                    }
                );
            }
        });

    });
}


function createImagelistFormCallback(data) {
    /**
     * imagelist form回调函数
     * by:范俊伟 at:2015-01-29
     */
    if (data.success) {
        $('#fileid').val('');
        last_get_upload_result = null;
        confirmBox.showConfirm('完成', '保存成功', '确定', '', function () {
            show_browse_imagelist();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }
}


function appendUploadImage(fileid) {
    /**
     * 上传文件后附加已上传文件信息
     * by:范俊伟 at:2015-02-01
     * @type {string}
     */
    getFileInfo(fileid, function (result) {
        var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
        html = html.replace('/url/', result.geturl).replace('/name/', result.name);
        $('#upload_list').html(html);
    });

}


function imagesDing(id) {
    /**
     * 顶操作
     by: 范俊伟 at:2015-02-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/ding_filerecord_by_id';
    var data = {
        id: id,
        flag: current_app_group.flag
    };
    httpRequest(url, data).done(function (data) {
        $.simplyToast('操作成功', 'success');
    });
}

function imagesReplay(id, to_user) {
    /**
     * 评论操作
     by: 范俊伟 at:2015-02-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    confirmBox.showConfirm('评论', '<textarea style="width:100%" id="apply_text" rows="3"></textarea>', '确定', '取消', function () {
        /**
         * 评论执行回调
         * @type {*|jQuery}
         */
        var content = $('#apply_text').val();
        var url = '/ns/' + window.project_id + '/replay_filerecord_by_id';
        var data = {
            id: id,
            to_user: to_user,
            content: content,
            flag: current_app_group.flag
        };
        httpRequest(url, data).done(function (data) {
            $.simplyToast('评论成功', 'success');
            getImagesReplay(id);
        });
    }, null);

}


function createImageListButtonClick() {
    /**
     * filelist 创建按钮点击事件
     * by:范俊伟 at:2015-01-26
     */
    if (upload_fileids.length == 0) {
        messageBox.showMessage('温馨提示', '还未选择文件');
    }
    else {
        var form = $('#imagelist_from');
        $('#fileid').val(upload_fileids.join(','));
        $('#flag').val(current_app_group.flag);
        var url = '/ns/' + window.project_id + '/create_file_by_group';
        form.attr('action', url);
        form.submit();
    }

}