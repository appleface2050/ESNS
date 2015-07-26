/**
 * Created by EasyShare004 on 2015/6/16.
 */


function init_view_customer_service_sys_news() {

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
         * 优化查询，增加查询条件sys_column_id栏目id
         by: 闫宇 at:2015-06-25
         */
        show_breadcrumb([{name: '系统新闻设置'}]);
        //EJSTemplateRender('cp_manage/ejs/customer_service_sys_news.ejs').done(function (html) {
        //    $('#view_content').html(html);
        //    window.viewDTD.resolve();
        //    page_start=0;
        //    $('#view_content tbody').empty();
        //    window.loadNextPageCallback = window.query_sys_news;
        //    loadNextPage();
        //});

         httpRequest('/cp/all_sys_column', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('cp_manage/ejs/customer_service_sys_news.ejs', { 'column_list': data.result});
        }, function () {
        }).done(function (html) {
        $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_sys_news;
            loadNextPage();
        })
    }


    window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:王健 at:2015-06-17
         */
        showView();
    }

    window.query_sys_news = function () {
        /**
		 查询系统新闻
         by：尚宗凯 at：2015-06-16
         优化查询系统，支持分页加载
         by：王健 at：2015-06-17
         优化查询系统，增加查询条件sys_column_id栏目id
         by：闫宇 at：2015-06-25
         * @type {*|jQuery}
         */
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
        var sys_column_id = $('#form-field-sys_column_id').val();
//        var user_type = $('#search_user_type').val();

        httpRequest('/cp/query_sys_news', {keyword: keyword, page_start:page_start,sys_column_id:sys_column_id}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_sys_news_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();

    };
      window.orientation_query_sys_news = function () {
        /**
		 查询按钮查询系统新闻设置
         by：刘奕辰 at：2015-06-19
         * @type {*|jQuery}
         */
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.query_sys_news;
            loadNextPage();

    };

    window.update_sys_news = function(news_id){
        /**
         * 修改新闻
         * by:王健 at:2015-6-17
         */
        httpRequest('/cp/get_sys_news_by_id', {id: news_id}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.title}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_create_sys_news.ejs', data.result);
        }).then(function (html) {
            window.loadNextPageCallback = null;
            $('#view_content').html(html);
        });
    };

    window.SetSysNewsIsActive = function (is_active) {
        /**
         * 设置是否发布
         * by：尚宗凯 at：2015-06-16
         * 设置是否发布 然后刷新页面
         * by：刘奕辰 at：2015-07-01
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

                        httpRequest('/cp/set_sys_news_is_active', obj).done(function () {
                             $('#view_content tbody').empty();
                            orientation_query_sys_news();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }
    window.customer_service_create_sys_news_callback = function (form) {
        /**
         修改密码
         by: 范俊伟 at:2015-06-12
		 修改url路径
         by：尚宗凯 at：2015-06-15
         新增新闻id 用于重复提交
         by：刘奕辰 at：2015-06-23
         添加预览需要的功能
         by: 王健 at:2015-06-30
         */
        var obj = form.serializeArray();
        httpRequest('/cp/create_sys_news', obj).then(function (data) {
            $.simplyToast('修改成功', 'success');
            if(data.result.id){
                $("#news_id").val(data.result.id);
                $("#temp_column").val(data.result.sys_column);
            }
        }, function () {
        })
    };


window.enterIn = function(evt){
         /**
          *回车查询
          * by：刘奕辰 at：2015-07-01
          */
       var evt=evt?evt:(window.event?window.event:null);//兼容IE和FF
            if (evt.keyCode==13){

                $('#view_content tbody').empty();
                orientation_query_sys_news();
            }
     }


}