/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_company_project_manage() {

    var page_start = 0;
    /**
     * 项目管理
     by：刘奕辰 at;2015-06-30
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 刘奕辰 at:2015-06-30
         */
        show_breadcrumb([{name: '项目管理'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_company_project_manage.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.get_all_project;
            loadNextPage();

        });

    }


    window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:王健 at:2015-06-17
         */
        showView();
    }
     window.enterIn = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_get_all_project();
            }
     }


    window.get_all_project = function () {
        /**
		 查询公司项目
         by：刘奕辰 at：2015-06-30


         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var company_id=window.companyid;
         var keyword = $('#search_keyword').val();


        httpRequest('/cp/'+company_id+'/query_company_project',{key: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_project_manage_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };

     window.orientation_get_all_project = function () {
        /**
		 查询按钮查询公司项目
         by：刘奕辰 at：2015-06-30
         * @type {*|jQuery}
         */
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.get_all_project;
            loadNextPage();

    };

    window.update_company_project = function(id){
        /**
         * 修改项目
         * by:刘奕辰 at:2015-6-30
         *添加了initDateTimePicker()和initCity()
          * by:闫宇 at:2015-07-01
         */
           var _id=id;
            var obj = null;
            var projectlist = null;
         var company_id=window.companyid;
        httpRequest('/cp/'+company_id+'/query_company_project', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.name}]);
            projectlist=data.result;
             for(var k=0;k<projectlist.length;k++){
                 if(_id==projectlist[k].id){
                     obj=projectlist[k];
                 }
             }
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_update_project.ejs',obj);
        }).then(function (html) {
            $('#view_content').html(html);
            initDateTimePicker();
            initCity();
        });
    };



 window.customer_service_company_create_project = function(){
        /**
         * 新增项目页面
         by: 刘奕辰 at:2015-06-30
         初始化日期和地址控件
         by: 范俊伟 at:2015-07-01
         */
       show_breadcrumb([{name: '新增项目'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_company_create_project.ejs',{id:null}).done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            initDateTimePicker();
            initCity();
        });
    }
     window.customer_service_company_create_project_callback = function (form) {
        /**
           创建项目 提交
         by: 刘奕辰 at:2015-06-30
         */
        var obj = form.serializeArray();

         var company_id=window.companyid;

        obj.push({name: "company_id", value: company_id});

        httpRequest('/ns/reg_project_by_company', obj).then(function (data) {
            $.simplyToast('修改成功', 'success');
            $('#news_id').val(data.result.id);
        }, function () {
        })
    }

   window.customer_service_company_close_project = function(){
        /**
         * 关闭项目
         * by：刘奕辰 at：2015-06-30

         */

        message = "是否真的要关闭项目";
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
                        var obj = $('#sys_news_list').serializeArray();
                        httpRequest('/cp/close_project', obj).done(function () {
                            $('#view_content tbody').empty();

                           orientation_get_all_project();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }

     window.customer_service_company_delete_project = function(){
        /**
         * 删除项目
         * by：刘奕辰 at：2015-06-30

         */

        message = "是否真的要删除项目";
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

                        httpRequest('/cp/delete_project', obj).done(function () {
                            $('#view_content tbody').empty();

                           orientation_get_all_project();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }

}