/**
 * Created by EasyShare004 on 2015/6/16.
 */

function init_view_customer_service_set_sys_banner() {

    /**
     * 系统banner
     by：尚宗凯 at;2015-06-16
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 尚宗凯 at:2015-06-16
             优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         */
        show_breadcrumb([{name: '系统banner设置'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_set_sys_banner.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
              page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.all_sys_banner;
            loadNextPage();
        });
    }

    window.all_sys_banner = function () {
        /**
		 查询系统新闻
         by：尚宗凯 at：2015-06-16
          优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         * @type {*|jQuery}
         */
//        var keyword = $('#search_keyword').val();
//        var user_type = $('#search_user_type').val();
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
        httpRequest('/cp/all_sys_banner',{keyword: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                 window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_set_sys_banner_table_data.ejs', data);
        }).then(function (html) {
             $('tbody').append(html);
            dtd.resolve();
        });
         return dtd.promise();
    };







    window.DeleteSysBanner = function(){
        /**
         * 删除banner
         * by：尚宗凯 at：2015-06-16
         * 删除后刷新页面
         * by：刘奕辰 at：2015-07-01
         * @type {*|{name, value}|jQuery}
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
                        var obj = $('#sys_banner_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
//                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/delete_sys_banner', obj).done(function () {
                             $('#view_content tbody').empty();
                             page_start=0;
                            all_sys_banner();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }


    window.SetSysBannerIsActive = function (is_active) {
        /**
         * 设置是否生效
         * by：尚宗凯 at：2015-06-16
         * 设置生效后刷新
         * by：刘奕辰 at：2015-07-01
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";
        if (is_active == false) {
            message = "设置banner失效";
        }
        else if (is_active == true) {
            message = "设置banner生效";
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
                        var obj = $('#sys_banner_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/set_sys_banner_is_active', obj).done(function () {
                             $('#view_content tbody').empty();
                             page_start=0;
                            all_sys_banner();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }


}