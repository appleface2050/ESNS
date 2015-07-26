/**
 * Created by EasyShare004 on 2015/6/16.

 */
function init_view_customer_service_company_manage() {
    /**
     *  更新公司管理功能
 * by：刘奕辰 at：2015-06-24
     * *  * 增加jpeg图片格式的上传
             by: 刘奕辰 at:2015-06-25
     */
    var company_id=window.companyid;
    var last_get_upload_result=null;
    showView();


    function showView() {
        show_breadcrumb([
            {name: '公司管理'}
        ]);
        
        httpRequest('/cp/'+company_id+'/get_company_detail_by_id', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.name}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_update_company.ejs', data.result);
        }).then(function (html) {
            window.loadNextPageCallback = null;
            $('#view_content').html(html);



             var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((type == 'bmp' || type == 'jpg' || type == 'png' || type == 'gif'|| type == 'jpeg')) {
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
                    messageBox.showMessage('温馨提示', '请选择图片格式文件(*.bmp,*.jpg,*.png,*.gif,*.jpeg)');
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
            /**
             * 添加标题logo的上传功能
             * by:王健 at:2015-6-22
             * @type {Window.AjaxUpload}
             */
            var ajaxupload_top_logo = new AjaxUpload($('#btn_select_file_top_image'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((type == 'bmp' || type == 'jpg' || type == 'png' || type == 'gif'|| type == 'jpeg')) {
                    //if (checkForm(imagelist_from)) {
                    var deferred = $.Deferred();
                    showMask();
                    window.getUploadUrl(type, file_obj.size, file_name, function (result) {
                        last_file_info = {
                            name: file_name,
                            type: type
                        };
                        ajaxupload_top_logo._settings.action = result.posturl;
                        var parm = {};
                        _(result.params).each(function (value, key) {
                            parm[key] = value;
                        });
                        ajaxupload_top_logo._settings.data = parm;
                        console.log(ajaxupload_top_logo._settings.data);
                        deferred.resolve();
                    });
                    return deferred.promise();
                    //}
                    //else {
                    //    return false;
                    //}

                }
                else {
                    messageBox.showMessage('温馨提示', '请选择图片格式文件(*.bmp,*.jpg,*.png,*.gif,*.jpeg)');
                    return false;
                }

            },
            onComplete: function (file, response) {
                window.checkFileUpload(last_get_upload_result.fileid, function (success) {
                        hideMask();
                        if (success) {
//                            upload_fileids = [last_get_upload_result.fileid];
                            window.appendUploadImage3(last_get_upload_result.fileid);
                            $("#logoimage3").val(last_get_upload_result.fileid);
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


    window.customer_service_update_company_callback = function (form) {
        /**
         回调函数
         by：尚宗凯 at：2015-06-16
         创建公司后，公司id保留本地
         by：王健 at：2015-06-16
         规范格式
         by:王健 at:2015-6-22
         */
        var obj = form.serializeArray();
        obj.push({"name":"company_id","value": company_id});
        httpRequest('/cp/create_company', obj).then(function (data) {

            $.simplyToast('执行成功', 'success');
        }, function () {
        })
    };

    window.customer_service_update_company_callback2 = function (form) {
        /**
         回调函数，上传企业logo
         by：王健 at：2015-06-22
         图片id使用 logoimage 的
         by：王健 at：2015-06-22
         规范格式
         by:王健 at:2015-6-22
         */
        var obj = form.serializeArray();
        obj.push({"name":"id","value": company_id});

        httpRequest('/cp/update_company', obj).then(function (data) {
            $.simplyToast('图片上传成功', 'success');
        }, function () {
        })
    };

    window.customer_service_update_company_callback3 = function (form) {
        /**
         回调函数，上传企业标题logo
         by：王健 at：2015-06-22
         图片id使用 logoimage 的
         by：王健 at：2015-06-22
         */
        var obj = form.serializeArray();
        obj.push({"name":"id","value": company_id});

        httpRequest('/cp/update_company', obj).then(function (data) {
            $.simplyToast('图片上传成功', 'success');
        }, function () {
        })
    };

    window.checkFileUpload = function (fileid, cb) {
    /**
     * 检测文件是否上传成功
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/nf/check_company_file_upload_status';
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
        var url = '/nf/get_company_url_by_file';
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
          * by:闫宇 at:2015-07-01
         * @type {string}
         */
        window.getFileInfo(fileid, function (result) {
            //var html = '<img src="/url/" style="max-width: 500px;">';
            //html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            //$('#upload_list').html(html);
            $('#column_image').attr("src", result.geturl);
            $('#column_image2').attr("src", result.geturl);
        });
    };

    window.appendUploadImage3 = function(fileid) {
         /**
         * 上传文件后附加已上传文件信息
         * by:范俊伟 at:2015-02-01
          * 显示标题logo
         * by:范俊伟 at:2015-06-22
         * @type {string}
         */
        window.getFileInfo(fileid, function (result) {
            //var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
            //html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            //$('#upload_list3').html(html);
            $('#column_image1').attr("src", result.geturl);
            $('#column_image3').attr("src", result.geturl);
        });
    };

    window.getUploadUrl = function (filetype, size, filename, cb) {
        /**
         * 获取上传URL
         * by:范俊伟 at:2015-01-26
         * 使用通用http请求函数
         by: 范俊伟 at:2015-03-16
         * @type {string}
         */
            if(!company_id){
                $.simplyToast('请先创建公司。', 'danger');
                hideMask();
                return;
            }
        var url = '/nf/' + company_id + '/get_company_qn_upload_files_url';
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