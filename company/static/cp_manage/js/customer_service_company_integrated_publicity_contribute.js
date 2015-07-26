var last_get_upload_result = null;
 var last_file_info = null;
function init_view_customer_service_company_integrated_publicity_contribute() {
    /**
     * 宣传报道
     * by 刘奕辰 2015-6-25
     */


    showView();
    function showView() {
   /**
       * * 宣传报道视图显示
     * by 闫宇 2015-6-27
     */
        show_breadcrumb([{name: '宣传报道'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_company_news;
            loadNextPage();
        });
    }
    window.orientation_query_company_news = function () {
        /**
		 查询按钮查询公司新闻
         by：刘奕辰 at：2015-06-22
         * @type {*|jQuery}
         */
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_company_news;
            loadNextPage();

    };
    window.query_company_news = function () {
  /**
     * 按key查询宣传报道,is_active为True
     * by 闫宇 2015-6-29
     */
        var dtd = $.Deferred();
        var company_id=window.companyid;
        var key = $('#search_keyword').val();
        //var obj = $('#query_sys_news_list').serializeArray();
        //obj.push({name: "company_column_id", value: company_column_id});

        var flag = 'XUANCHUANBAODAO';
        httpRequest('/cp/'+window.companyid+'/get_news_by_flag', {page_start:page_start,key:key,flag:flag,is_active:'True'}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };
    window.integrated_all = function () {
  /**
     * 宣传报道
     * by 刘奕辰 2015-6-26
     */

        EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated_all.ejs').done(function (html) {
            $('#view_content').html(html);
            //window.viewDTD.resolve();
            window.integrated_image_text();
        });
    };

         window.integrated_image_text = function (){
               /**
     * 宣传报道 图文
     * by 刘奕辰 2015-6-26
     */
        EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated_image_text.ejs',{id:null}).done(function (html) {
            $('#all').html(html);
        });
    };
            window.integrated_accessory = function (){
                  /**
     * 宣传报道 附件
     * by 刘奕辰 2015-6-29
     */
        EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated_accessory.ejs',{id:null}).done(function (html) {
            $('#all').html(html);

            var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((  type == 'jpg' || type == 'png' || type == 'jpeg'|| type == 'doc'|| type == 'docx'|| type == 'exl'|| type == 'exlx'|| type == 'ppt'|| type == 'pptx'|| type == 'pdf'|| type == 'txt')) {
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
                    messageBox.showMessage('温馨提示', '请选择以下格式的文件(*.jpg,*.png,*.jpeg,*.doc,*.docx,*.exl,*.exlx,*.ppt,*.pptx,*.pdf,*.txt)');
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
    };
  window.checkFileUpload = function (fileid, cb) {
    /**
     * 检测文件是否上传成功
     * by:范俊伟 at:2015-01-26
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
         修改接口
     by: 刘奕辰 at:2015-07-02
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
      window.customer_service_create_company_integrated_accessory_callback = function (form) {
        /**宣传报道
        创建附件
         by:刘奕辰 at:2015-06-29
         */
        var obj = form.serializeArray();
          var type_flag="files";
        var flag="XUANCHUANBAODAO";
        obj.push({name: "type_flag", value: type_flag});
        obj.push({name: "flag", value: flag});
        httpRequest('/cp/'+window.companyid+'/create_zhgl_company_news', obj).then(function () {
            $.simplyToast('执行成功', 'success');
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
             修改接口
     by: 刘奕辰 at:2015-07-02
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
         * 获取上传URL
         * by:范俊伟 at:2015-01-26
         * 使用通用http请求函数
         by: 范俊伟 at:2015-03-16
             修改接口
     by: 刘奕辰 at:2015-07-02
         * @type {string}
         */
//        var url = '/nf/'+ window.project_id +'/get_company_qn_upload_files_url';
//        var url = '/nf/big_company/get_company_qn_upload_files_url';
        var url = '/nf/'+window.companyid+'/get_company_qn_upload_files_url';
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



          window.integrated_slide = function (){
                /**
     * 宣传报道 幻灯片
     * by 刘奕辰 2015-6-29
     */
            EJSTemplateRender('cp_manage/ejs/customer_service_company_integrated_slide.ejs',{id:null}).done(function (html) {
            $('#all').html(html);

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
                    messageBox.showMessage('温馨提示', '请选择以下格式的文件(*.jpg,*.png,*.jpeg)');
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

    };
   window.customer_service_create_company_integrated_slide_callback = function (form) {
        /**宣传报道
        创建幻灯片
         by:刘奕辰 at:2015-06-29
         */
        var obj = form.serializeArray();
          var type_flag="images";
        var flag="XUANCHUANBAODAO";
        obj.push({name: "type_flag", value: type_flag});
        obj.push({name: "flag", value: flag});
        httpRequest('/cp/'+window.companyid+'/create_zhgl_company_news', obj).then(function () {
            $.simplyToast('执行成功', 'success');
             $('#news_id').val(data.result.id);
        }, function () {
        })
    }


    window.DeleteSysColumn = function(){
          /**
     * 删除新闻
     * by 闫宇 2015-6-29
     */

        message = "是否真的要删除";
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
                        var obj = $('#sys_news_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
//                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/delete_company_news', obj).done(function () {
                             $('#view_content tbody').empty();

                           orientation_query_company_news();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }

    window.customer_service_create_company_integrated_image_text_callback = function (form) {
        /**
          宣传报道 创建图文
         by: 刘奕辰 at:2015-06-27
         */
        var obj = form.serializeArray();
        var type_flag="news";
        var flag="XUANCHUANBAODAO";
        obj.push({name: "type_flag", value: type_flag});
        obj.push({name: "flag", value: flag});

        httpRequest('/cp/'+window.companyid+'/create_zhgl_company_news', obj).then(function (data) {
            $.simplyToast('修改成功', 'success');
            $('#news_id').val(data.result.id);
        }, function () {
        })
    }

  window.enterIn = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_query_company_news();
            }
     }
  window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:刘奕辰 at:2015-06-19
         */
        showView();
    }

}