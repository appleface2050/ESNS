/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_admin_company_manage() {
     var page_start = 0;
    /**
     登陆后展示左右公司
     by：尚宗凯 at：2015-06-18
        优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
     * @type {*|jQuery}
     */
    var company_id=null;
    var manager="manager";
    var manager1="user";
    showView();
    function showView() {
        show_breadcrumb([
            {name: '公司管理'}
        ]);
        EJSTemplateRender('cp_manage/ejs/customer_service_admin_company_manage.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.get_all_company;
            loadNextPage();

        });
    }
       window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:刘奕辰 at:2015-06-19
         */
        showView();
    }

    get_all_company = function () {
        /**
		 查询系统新闻
         by：尚宗凯 at：2015-06-16

        优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         * @type {*|jQuery}
         */
              var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
//        var user_type = $('#search_user_type').val();
        httpRequest('/cp/get_all_company', {keyword: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
             page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_manage_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
         return dtd.promise();
    };
      window.orientation_get_all_company = function () {
        /**
		 查询按钮查询公司项目
         by：刘奕辰 at：2015-06-30
         * @type {*|jQuery}
         */
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.get_all_company;
            loadNextPage();

      };
     window.enterIn = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_get_all_company();
            }
     }


      window.create_company_user = function(c_id){
        /**
         * 添加成员页面
         * by:刘奕辰 at:2015-6-19
         */
         show_breadcrumb([{name: '添加成员设置'}]);
          company_id = c_id;
        EJSTemplateRender('cp_manage/ejs/customer_service_add_company_user.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.find_company_user;
            loadNextPage();
        });

    };
   window.find_company_user = function () {
        /**
		 查询成员
         * by:刘奕辰 at:2015-6-19
         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
//        var user_type = $('#search_user_type').val();

        httpRequest('/cp/query_user_name', {key: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            data['company_id'] = company_id;
            return EJSTemplateRender('cp_manage/ejs/customer_service_find_company_user.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };
window.orientation_find_company_user = function () {
        /**
		 查询按钮查询成员
         by：刘奕辰 at：2015-06-19

         * @type {*|jQuery}
         */
        page_start=0;
            $('#view_content tbody').empty();
    window.loadNextPageCallback = window.find_company_user;
            loadNextPage();
        // EJSTemplateRender('cp_manage/ejs/customer_service_add_company_user.ejs').done(function (html) {
        //    $('#view_content').html(html);
        //    window.viewDTD.resolve();
        //    page_start=0;
        //    $('#view_content tbody').empty();
        //    window.loadNextPageCallback = window.find_company_user;
        //    loadNextPage();
        //});
    };
  window.enterIn1 = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_find_company_user();
            }
     }
window.AddCompanyUser = function () {
        /**
         * 添加成员
         * by：刘奕辰 at：2015-06-19
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";

            message = "是否添加成员";


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
                        obj.push({name: "company_id", value: company_id});

                        httpRequest('/cp/add_user_to_company', obj).done(function () {
                            find_company_user();
                            $.simplyToast('添加成功', 'success');
                        })
                    }
                }
            }
        });

    }

     window.create_update_admin = function(c_id){
        /**
         * 修改管理员页面
         * by:刘奕辰 at:2015-6-19
         */
         show_breadcrumb([{name: '修改管理员设置'}]);
         company_id = c_id;
        EJSTemplateRender('cp_manage/ejs/customer_service_create_update_admin.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.find_our_company_user;
            loadNextPage();
        });

    };
      window.enterIn2 = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                find_our_company_user();
            }
     }

window.find_our_company_user = function () {
        /**
		 查询本公司员工
         * by:刘奕辰 at:2015-6-19
         *  修复查询按钮bug
         * by:刘奕辰 at:2015-6-26
         * @type {*|jQuery}
         */
            $('#view_content tbody').empty();
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
        window.loadNextPageCallback = null;
        httpRequest('/cp/'+company_id+'/get_user_by_company_id', {key: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {

                return "";
            }

            page_start+=data.result.length;
            data['company_id'] = company_id;
            return EJSTemplateRender('cp_manage/ejs/customer_service_find_our_company_user.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };
window.update_admin = function () {
        /**
         * 设置管理员
         * by：刘奕辰 at：2015-06-19
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";

            message = "是否设置管理员";

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
                        obj.push({name: "do", value: manager});

                        httpRequest('/cp/'+company_id+'/set_company_admin', obj).done(function () {
                            $('#view_content tbody').empty();
                            find_our_company_user();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }
    window.cancel_admin = function () {
        /**
         * 取消管理员
         * by：刘奕辰 at：2015-06-19
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";

            message = "是否取消管理员";

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
                        obj.push({name: "do", value: manager1});

                        httpRequest('/cp/'+company_id+'/set_company_admin', obj).done(function () {
                           $('#view_content tbody').empty();
                           find_our_company_user();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }

     window.update_company = function(c_id) {
         /**
          * 修改公司
          * by:王健 at:2015-6-17
          * 更新修改公司页面
          *  by:刘奕辰 at:2015-6-24
          *  * 增加jpeg图片格式的上传
             by: 刘奕辰 at:2015-06-25
           * 增加修改页面的集团选择
             by: 刘奕辰 at:2015-06-26
           * 优化图片上传格式
             by: 刘奕辰 at:2015-06-26
          */
         company_id = c_id;
         var tmp_bigcompany_id=null
         httpRequest('/cp/' + company_id + '/get_company_detail_by_id', {}).then(function (data) {
             if (!data.result) {
                 return "";
             }
             show_breadcrumb([{name: data.result.name}]);
             tmp_bigcompany_id = data.result.bigcompany;
             return EJSTemplateRender('cp_manage/ejs/customer_service_company_update.ejs', data.result);
         }).then(function (html) {
             window.loadNextPageCallback = null;
             $('#view_content').html(html);


             var ajaxupload = new AjaxUpload($('#btn_select_file'), {
                 name: 'file',
                 data: {},
                 onChange: function (file_name, type, file_obj) {
                     if (( type == 'jpg' || type == 'png' || type == 'jpeg')) {
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
             /**
              * 添加标题logo的上传功能
              * by:王健 at:2015-6-22
              *    * 增加jpeg图片格式的上传
                by: 刘奕辰 at:2015-06-25
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
             return httpRequest('/cp/get_all_big_company',{});
         }).then(function(data){
             if (!data.result) {
                 return "";
             }
             return EJSTemplateRender('cp_manage/ejs/customer_service_company_bigcompany_option.ejs', {id:'', bigcompany_id:tmp_bigcompany_id,  'bigcompany_list': data.result});
             window.viewDTD.resolve();
         }).then(function(html){
                  $('#bigcompany_option').html(html);
         });
     }
     window.customer_service_company_manage_callback = function (form) {
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

    window.customer_service_company_manage_callback2 = function (form) {
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

    window.customer_service_company_manage_callback3 = function (form) {
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
         * @type {string}
         */
        window.getFileInfo(fileid, function (result) {
            var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
            html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            $('#upload_list').html(html);
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
            var html = '<div class="col-md-3"><img src="/url/" style="max-width: 500px;"><p>/name/</p></div>';
            html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            $('#upload_list3').html(html);
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