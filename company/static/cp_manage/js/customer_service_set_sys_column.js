/**
 * Created by EasyShare004 on 2015/6/17.
 */
function init_view_customer_service_set_sys_column() {
var page_start = 0;
    /**
     * 系统column
     by：尚宗凯 at;2015-06-16
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 尚宗凯 at:2015-06-16
         增加刷新页面自动查询页面信息
         by: 刘奕辰 at:2015-06-18
         */
        show_breadcrumb([{name: '设置系统栏目'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_set_sys_column.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
             page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.all_sys_column;
           loadNextPage();
        });
    }

    window.all_sys_column = function () {
        /**
		 查询系统栏目
         by：尚宗凯 at：2015-06-16
           优化查询功能 点击菜单自动查询
         by：刘奕辰 at：2015-06-18
         * @type {*|jQuery}
         */
//        var keyword = $('#search_keyword').val();
//        var user_type = $('#search_user_type').val();
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
        httpRequest('/cp/all_sys_column', {keyword: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_set_sys_column_table_data.ejs', data);
        }).then(function (html) {
             $('tbody').append(html);
            dtd.resolve();
        });
          return dtd.promise();
    };

 window.update_column = function(id){
        /**
         * 修改系统栏目页面
         * by:刘奕辰 at:2015-6-22
         */
        httpRequest('/cp/get_sys_column_by_column_id', {sys_column_id: id}).then(function (data) {
            if (!data.result) {
                return "";
            }
            show_breadcrumb([{name: data.result.name}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_update_column.ejs', data.result);
        }).then(function (html) {
            window.loadNextPageCallback = null;
            $('#view_content').html(html);
        });
    };
       window.customer_service_update_column_callback = function (form) {
        /**
         * 修改系统栏目
         * by:刘奕辰 at:2015-6-22
         */
        var obj = form.serializeArray();
        httpRequest('/cp/update_sys_column', obj).then(function () {
            $.simplyToast('修改成功', 'success');
        }, function () {
        })
    }


    window.DeleteSysColumn = function(){
        /**
         * 删除column
         * by：尚宗凯 at：2015-06-16
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
                        var obj = $('#sys_column_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
//                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/delete_sys_column', obj).done(function () {
                            $('#view_content tbody').empty();
                             page_start=0;
                            all_sys_column();


                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }


    window.SetSysColumnIsActive = function (is_active) {
        /**
         * 设置是否生效
         * by：尚宗凯 at：2015-06-16
         * 设置是否生效后刷新
         * by：刘奕辰 at：2015-07-01
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";
        if (is_active == false) {
            message = "设置column失效";
        }
        else if (is_active == true) {
            message = "设置column生效";
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
                        var obj = $('#sys_column_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/set_sys_column_is_active', obj).done(function () {
                            $('#view_content tbody').empty();
                             page_start=0;
                            all_sys_column();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }

     window.goNewsBack = function(){
        /**
        //返回视图界面
        //by:刘奕辰 at:2015-06-19
         */
        showView();
    }

}