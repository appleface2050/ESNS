/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_news_company_news() {

    var page_start = 0;
     /**
     * 新闻管理
     by：闫宇 at;2015-06-27
     */

    showView();
    function showView() {
        /**
         * 显示企业资讯视图
         by: 闫宇 at:2015-06-26
         * 优化查询
         by: 闫宇 at:2015-06-27
         */
        show_breadcrumb([{name: '企业资讯'}]);

        EJSTemplateRender('cp_manage/ejs/customer_service_news_company_news.ejs', { company_column_id:0, column_list: null}).done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_company_news;
            loadNextPage();
        });

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
		 按是否已发布和关键词查询企业资讯
         by：闫宇 at：2015-06-27
         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var company_id=window.companyid;
        var key = $('#search_keyword').val();
        var company_column_id = '';
        var is_active = $('#form-field-is_active').val();
        //var obj = $('#query_sys_news_list').serializeArray();
        //obj.push({name: "company_column_id", value: company_column_id});

//        var user_type = $('#search_user_type').val();

        httpRequest('/cp/'+company_id+'/get_qiyezixun_news', { page_start:page_start,key:key,is_active:is_active}).then(function (data) {
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
         * 修改企业资讯
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
         * 跳转到添加企业资讯页面
         * by:闫宇 at:2015-6-27
     * 添加初始化的栏目变量
     * by: 王健 at:2015-06-30
         */
        show_breadcrumb([{name: '创建企业新闻'}]);
         //document.getElementById("column_select").style.visibility="hidden";
         EJSTemplateRender('cp_manage/ejs/customer_service_news_create_and_update_news.ejs', {id:'', content:'', company_column:0, title: '',column_list: null}).done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
        });
    }
    window.customer_service_create_company_news_callback = function (form) {
        /**
         * 添加或修改企业资讯
         * by:闫宇 at:2015-6-27
         * 添加预览需要的栏目id
         * by: 王健 at:2015-06-30
         */
        var obj = form.serializeArray();
        httpRequest('/cp/'+window.companyid+'/get_company_column_by_flag', {flag:'QIYEZIXUN'}).then(function (data) {
           var com_column_id=data.result.company_column_id;
             obj.push({name: "com_column_id", value: com_column_id});
            httpRequest('/cp/'+window.companyid+'/create_company_news', obj).then(function (data) {
                $.simplyToast('修改成功', 'success');
                $('#news_id').val(data.result.id);
                $("#temp_column").val(data.result.company_column);
            })
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