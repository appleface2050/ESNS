/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_news_company_performance() {

    var page_start = 0;
    /**
     * 新闻管理
     by：闫宇 at;2015-06-27
     */

    showView();
    function showView() {
        /**
         * 显示公司业绩视图
         by: 闫宇 at:2015-06-26
         *优化查询
         by: 闫宇 at:2015-06-27
         */
        show_breadcrumb([{name: '公司业绩'}]);

         httpRequest('/cp/'+window.companyid+'/get_child_comapny_column_list', {flag:'GONGSIYEJI'}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('cp_manage/ejs/customer_service_news_company_news.ejs', { company_column_id:0, 'column_list': data.result});
        }, function () {
        }).done(function (html) {
        $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_company_news;
            loadNextPage();
        })

        //EJSTemplateRender('cp_manage/ejs/customer_service_company_news.ejs').done(function (html) {
        //    $('#view_content').html(html);
        //    window.viewDTD.resolve();
        //
        //      page_start=0;
        //    $('#view_content tbody').empty();
        //    window.loadNextPageCallback = window.query_company_news;
        //    loadNextPage();
        //
        //});
    }


    window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:王健 at:2015-06-17
         */
        showView();
    }

    window.query_company_news = function () {
        /**
		  按是否已发布，栏目flag，关键词查询公司业绩
         by：闫宇 at：2015-06-26
         优化查询，使栏目选择时，只显示该父节点栏目下的子节点
         by：闫宇 at：2015-06-27
         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var company_id=window.companyid;
        var key = $('#search_keyword').val();
        var company_column_id = '33';
        var is_active = $('#form-field-is_active').val();
        //var obj = $('#query_sys_news_list').serializeArray();
        //obj.push({name: "company_column_id", value: company_column_id});
         var flag = $('#form-field-company_column_id').val();

//        var user_type = $('#search_user_type').val();
        if(flag==''){
            flag="GONGSIYEJI";
        }
        httpRequest('/cp/'+window.companyid+'/get_news_by_flag', {page_start:page_start,key:key,flag:flag,is_active:is_active}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_news_company_news_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };

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

    window.update_company_news = function(news_id){
        /**
           * 修改公司业绩
         * by:闫宇 at:2015-6-27
         */
        httpRequest('/cp/get_company_news_by_id2', {id: news_id}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.title}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_news_create_and_update_news.ejs', data.result);
        }).then(function (html) {
            $('#view_content').html(html);
        });
    };

    window.SetCompanyNewsIsActive = function (is_active) {
        /**
         * 设置是否发布
         * by：尚宗凯 at：2015-06-16
         * 优化
         * by：刘奕辰 at：2015-06-22
         * 是实现功能 实现优化后刷新
         * by：刘奕辰 at：2015-06-23
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";
        if (is_active == false) {
            message = "是否取消发布新闻";
        }
        else if (is_active == true) {
            message = "是否发布新闻";
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
                        var obj = $('#sys_news_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/set_company_news_is_active', obj).done(function () {
                            $('#view_content tbody').empty();
                            orientation_query_company_news();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }
    window.addNews = function(){
    /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         * 提供空数据，兼容修改新闻，渲染栏目列表
         by: 王健 at:2015-06-12
         * 栏目查询优化
         by: 刘奕辰 at:2015-06-22
         * 优化
         by: 刘奕辰 at:2015-06-23
        * 优化添加：添加页面下拉框中只显示本条新闻所属栏目的父节点的所有子节点新闻
         * by:闫宇 at:2015-6-27
     * 添加初始化的栏目变量
     * by: 王健 at:2015-06-30
         */
        show_breadcrumb([{name: '创建企业新闻'}]);
        httpRequest('/cp/'+window.companyid+'/get_child_comapny_column_list', {flag:'GONGSIYEJI'}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('cp_manage/ejs/customer_service_news_create_and_update_news.ejs', {id:'', company_column_id:0,company_column:0, content:'', title: '', 'column_list': data.result});
        }, function () {
        }).done(function (html) {
        $('#view_content').html(html);
            window.viewDTD.resolve();
        })
    }
   window.customer_service_create_company_news_callback = function (form) {
        /**
         * 添加或修改公司业绩
         * by:闫宇 at:2015-6-27
         * 添加预览需要的栏目id
         * by: 王健 at:2015-06-30
         */
        var obj = form.serializeArray();

        httpRequest('/cp/'+window.companyid+'/create_company_news', obj).then(function (data) {
            $.simplyToast('修改成功', 'success');
             $('#news_id').val(data.result.id);
            $("#temp_column").val(data.result.company_column);
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
}