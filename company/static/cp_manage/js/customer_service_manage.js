
function init_view_customer_service_manage() {
var page_start = 0;
    /**
     * 客服管理
     by：尚宗凯 at;2015-06-15
	 默认展示数据
	 by：尚宗凯 at：2015-06-18
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         */
        show_breadcrumb([{name: '公司管理'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_manage.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_big_company;
           loadNextPage();



        });
    }

    window.query_big_company = function () {
        /**
         * 查询用户
         by: 范俊伟 at:2015-06-12
         增加查询方式
         by: 范俊伟 at:2015-06-12
		 修改url路径
         by：尚宗凯 at：2015-06-15
          优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         * @type {*|jQuery}
         */
             var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();

//        var user_type = $('#search_user_type').val();
        httpRequest('/cp/query_big_company', {keyword: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
             page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_manage_table_data.ejs', data);
        }).then(function (html) {
              $('tbody').append(html);
            dtd.resolve();
        });
         return dtd.promise();
    };

    window.orientation_query_big_company = function () {
        /**
		 查询按钮查询集团默认展示
         by：刘奕辰 at：2015-06-19

         * @type {*|jQuery}
         */
        page_start=0;
            $('#view_content tbody').empty();
    window.loadNextPageCallback = window.query_big_company;
            loadNextPage();

    };


    window.setBigCompanyDisplay = function (is_display) {
        /**
         * 设置是否展示
         * by：尚宗凯 at：2015-06-15
         *  *    * 优化设置刷新
         * by：刘奕辰 at：2015-07-01
         * @type {*|{name, value}|jQuery}
         */
        var message = "是否确认设置所选显示方式为：";
        if (is_display == false) {
            message += "不展示";
        }
        else if (is_display == true) {
            message += "展示";
        }

        bootbox.dialog({
            title: "提示",
            message: message,
            buttons: {
                "cancel": {
                    "label": "取消",
                    "className": "btn-sm"
                },
                "button": {
                    "label": "确定",
                    "className": "btn-sm",
                    "callback": function () {
//                        var obj = $('#user_list').serializeArray();
                        var obj = $('#big_company_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
                        obj.push({name: "is_display", value: is_display});

                        httpRequest('/cp/set_big_company_display', obj).done(function () {
                              $('#view_content tbody').empty();
                            orientation_query_big_company();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }
    /**
    修改集团
     by:王健 at:2015-06-27
     */
    window.update_bigcompany = function(bigcompany_id){
        httpRequest('/cp/create_bigcompany', {id: bigcompany_id}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.name}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_create_big_company.ejs', data.result);
        }).then(function (html) {
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

        });
    };

    window.checkFileUpload = function (fileid, cb) {
    /**
     * 检查文件
     * by:王健 at:2015-06-27
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
         * 修改集团信息
         by:王健 at:2015-06-27
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
         * 获取文件信息
         * by:王健 at:2015-06-27
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
         * by:王健 at:2015-06-27
         * @type {string}
         */
        window.getFileInfo(fileid, function (result) {
            var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
            html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            $('#upload_list').html(html);
        });
    }

    window.getUploadUrl = function (filetype, size, filename, cb) {
        /**
         * 获取上传的post url
         * by:王健 at:2015-06-27
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
    window.enterIn = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_query_big_company();
            }
     }
}