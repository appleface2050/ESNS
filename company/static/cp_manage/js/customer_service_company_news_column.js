/**
 * Created by EasyShare004 on 2015/6/17.
 */
function init_view_customer_service_company_news_column() {

    /**
     * 系统column
     by：尚宗凯 at;2015-06-16
     * 实现上传栏目图片
     by: 闫宇 at:2015-06-25
     */
    var company_columns=null;//本公司栏目集合
    var current_column=null;//默认栏目
    showView();
    function showView() {
        /**
         * 显示视图
         by: 尚宗凯 at:2015-06-16
          * 显示视图
         by: 闫宇 at:2015-06-25
         修改接口
         by:王健 at:2015-06-26
         */
        show_breadcrumb([{name: '新闻栏目'}]);
        //得到本公司栏目集合
        httpRequest('/cp/'+window.companyid+'/get_company_column', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            company_columns = data.result;
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_news_column.ejs', data.result);
        }).then(function (html) {
            //EJSTemplateRender('cp_manage/ejs/customer_service_company_news_column.ejs').done(function (html) {
            window.loadNextPageCallback = null;
            $('#view_content').html(html);
            window.set_update_column('GONGSIJIANJIE');
             var ajaxupload = new AjaxUpload($('#btn_select_file'), {
            name: 'file',
            data: {},
            onChange: function (file_name, type, file_obj) {
                if ((type == 'bmp' || type == 'jpg' || type == 'png' || type == 'gif')) {
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
                    messageBox.showMessage('温馨提示', '请选择图片格式文件(*.bmp,*.jpg,*.png,*.gif)');
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
    window.set_update_column = function(flag){
        /**
     * 通过flag得到默认栏目，在页面中显示默认图片
     by: 闫宇 at:2015-06-25
     */
        for(var i=0;i<company_columns.length;i++){
            if(company_columns[i]['flag']==flag){
                current_column = company_columns[i];
                if(current_column.flag=='GONGSIJIANJIE'){
                    $("#vidoShow").css("background",'url(http://7xjnpa.com2.z0.glb.qiniucdn.com//company/b0fb4172-f3d4-4df0-b0a9-fd032f7c2d76.jpg?attname=gongsi_banner.jpg) no-repeat');
                }
                if(current_column.flag=='QIYEWENHUA'){
                    $("#vidoShow").css("background",'url(http://7xjnpa.com2.z0.glb.qiniucdn.com//company/2e9f23cf-1f5d-4c9b-b87c-6bfc02e05b5d.jpg?attname=qiyewenhua.jpg) no-repeat');
                }
                if(current_column.flag=='GONGSIYEJI'){
                    $("#vidoShow").css("background",'url(http://7xjnpa.com2.z0.glb.qiniucdn.com//company/66b796e6-6605-4f70-89dd-c7626fd21b12.jpg?attname=gongsiyeji.jpg) no-repeat');
                }
                $('#column_image1').attr('src', current_column['image_url']);
                $('#column_image').attr('src', current_column['image_url']);
            }
        }
    };

    window.customer_service_update_company_callback1 = function (form) {
        /**
         *实现栏目图片上传功能
         by: 闫宇 at:2015-06-25
         修改接口
         by:王健 at:2015-06-26
         */
        var obj = form.serializeArray();
        obj.push({"name":"flag","value": current_column['flag']});
        httpRequest('/cp/'+window.companyid+'/update_company_column_image', obj).then(function (data) {
            $.simplyToast('图片上传成功', 'success');
            return  httpRequest('/cp/'+window.companyid+'/get_company_column', {})
        }, function () {
        }).done(function (data) {
            company_columns = data.result;
        });
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
            //var html = 'column_image';
            //html = html.replace('/url/', result.geturl).replace('/name/', result.name);
            $('#column_image').attr("src", result.geturl);
            $('#column_image1').attr("src", result.geturl);
        });
    };


    window.getUploadUrl = function (filetype, size, filename, cb) {
        /**
         * 获取上传URL
         * by:范俊伟 at:2015-01-26
         * 使用通用http请求函数
         by: 范俊伟 at:2015-03-16
         修改接口
         by:王健 at:2015-06-26
         * @type {string}
         */

        var url = '/nf/' + window.companyid + '/get_company_qn_upload_files_url';
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