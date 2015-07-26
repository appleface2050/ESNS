/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_company_news() {

    var page_start = 0;
    /**
     * 客服管理
     by：尚宗凯 at;2015-06-16
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 尚宗凯 at:2015-06-16
         * 修改提示文字
         by: 尚宗凯 at:2015-06-16
         * 加载新闻界面后，自动加载列表，支持分页加载
         by: 王健 at:2015-06-17
           * 优化查询
         by: 刘奕辰 at:2015-06-22
           * 优化查询，增加查询条件sys_column_id栏目id
         by: 闫宇 at:2015-06-25
         */
        show_breadcrumb([{name: '新闻列表'}]);

         httpRequest('/cp/'+window.companyid+'/get_company_column', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_news.ejs', { company_column_id:0, 'column_list': data.result});
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
		 查询系统新闻
         by：尚宗凯 at：2015-06-16
         优化查询系统，支持分页加载
         by：王健 at：2015-06-17
         查询企业新闻
         by：刘奕辰 at：2015-06-22
         优化查询系统，增加查询条件company_column_id栏目id
         by：闫宇 at：2015-06-25
         优化查询系统，增加查询条件is_active是否已发布
         by：闫宇 at：2015-06-25
         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var company_id=window.companyid;
        var key = $('#search_keyword').val();
        var company_column_id = $('#form-field-company_column_id').val();
        var is_active = $('#form-field-is_active').val();
        //var obj = $('#query_sys_news_list').serializeArray();
        //obj.push({name: "company_column_id", value: company_column_id});

//        var user_type = $('#search_user_type').val();

        httpRequest('/cp/get_company_news', {company_id: company_id, page_start:page_start,key:key,company_column_id:company_column_id,is_active:is_active}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_news_table_data.ejs', data);
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
         * 修改新闻
         * by:王健 at:2015-6-17
         * 修改企业新闻
         * by:刘奕辰 at:2015-6-22
         * 优化修改企业新闻
         * by:刘奕辰 at:2015-6-23
         */
        httpRequest('/cp/get_company_news_by_id', {id: news_id}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.title}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_create_company_news.ejs', data.result);
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


}