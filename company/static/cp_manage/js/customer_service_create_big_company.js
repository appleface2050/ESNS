/**
 * Created by EasyShare004 on 2015/6/16.
 */
/**
 * Created by EasyShare004 on 2015/6/16.
 */
 var last_get_upload_result = null;
 var last_file_info = null;
function init_view_customer_service_create_big_company() {
    /**
     * 增加jpeg图片格式的上传
     by: 刘奕辰 at:2015-06-25
     添加参数
     by: 王健 at:2015-06-27
     优化图片上传格式
     by: 刘奕辰 at:2015-06-27
     */
    showView();
    function showView() {
        show_breadcrumb([{name: '创建集团'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_create_big_company.ejs', {id:'', name:'', logo_url:''}).done(function (html) {
            $('#view_content').html(html);
            var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((  type == 'jpg' || type == 'png' || type == 'jpeg')) {
                    //if (checkForm(imagelist_from)) {
                    var deferred = $.Deferred();
                    showMask();
                    window.getUploadUrl(type, file_obj.size, file_name, function (result) {
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
                    messageBox.showMessage('温馨提示', '请选择图片格式文件(*.jpg,*.png,*.jpeg)');
                    return false;
                }

            },
            onComplete: function (file, response) {
                window.checkFileUpload(last_get_upload_result.fileid, function (success) {
                        hideMask();
                        if (success) {
//                            upload_fileids = [last_get_upload_result.fileid];
                            window.appendUploadImage(last_get_upload_result.fileid);
                            $("#logoimage").val(last_get_upload_result.fileid);
                            last_get_upload_result = null;
                            last_file_info = null;
                        }

                    }
                );
            }
        });
            window.viewDTD.resolve();
        });
    }

    window.checkFileUpload = function (fileid, cb) {
    /**
     * 检测文件是否上传成功
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/nf/check_bigcompany_file_upload_status';
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

    window.customer_service_create_big_company_callback = function (form) {
        /**
         修改密码
         by: 范俊伟 at:2015-06-12
		 修改url路径
         by：尚宗凯 at：2015-06-15
         防止重复提交
         by：王健 at：2015-06-27
         */
        var obj = form.serializeArray();
        httpRequest('/cp/create_bigcompany', obj).then(function (date) {
            $.simplyToast('执行成功', 'success');
            $('#bigcompany_id').val(data.result.id);
        }, function () {
        })
    }

    window.getFileInfo =function (fileid, cb, img_w, img_h) {
        /**
         * 下载文件
         * by:范俊伟 at:2015-01-26
         * 使用通用http请求函数
         by: 范俊伟 at:2015-03-16
         增加图片缩放参数
         by: 范俊伟 at:2015-04-08
         * @type {string}
         */
        var url = '/nf/get_bigcompany_url_by_file';
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
    window.appendUploadImage = function(fileid) {
         /**
         * 上传文件后附加已上传文件信息
         * by:范俊伟 at:2015-02-01
          * 修改附加已上传文件信息的方式
          * by:闫宇 at:2015-07-02
         * @type {string}
         */
        window.getFileInfo(fileid, function (result) {
            //var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
            //html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            //$('#upload_list').html(html);
            $('#column_image').attr("src", result.geturl);
            $('#column_image1').attr("src", result.geturl);
        });
    }

    window.getUploadUrl = function (filetype, size, filename, cb) {
        /**
         * 获取上传URL
         * by:范俊伟 at:2015-01-26
         * 使用通用http请求函数
         by: 范俊伟 at:2015-03-16
         * @type {string}
         */
//        var url = '/nf/'+ window.project_id +'/get_company_qn_upload_files_url';
//        var url = '/nf/big_company/get_company_qn_upload_files_url';
        var url = '/nf/get_bigcompany_qn_upload_files_url';
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


}