/**
 * Date: 15/6/11
 * Time: 16:12
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
function init_view_user_type_manage() {
    /**
     * 用户类型管理页面
     by: 范俊伟 at:2015-06-11
     */

    showViwe();
    function showViwe() {
        /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         */
        show_breadcrumb([{name: '用户类型管理'}]);
        EJSTemplateRender('ns_manage/ejs/user_type_manage.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
        });
    }

    window.query_user = function () {
        /**
         * 查询用户
         by: 范俊伟 at:2015-06-12
         增加查询方式
         by: 范俊伟 at:2015-06-12
         * @type {*|jQuery}
         */
        var keyword = $('#search_keyword').val();
        var user_type = $('#search_user_type').val();
        httpRequest('/ns_manage/query_user', {keyword: keyword, user_type: user_type}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('ns_manage/ejs/user_type_manage_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').html(html);
        });
    };

    window.setUserType = function (user_type) {
        /**
         * 设置用户类型
         by: 范俊伟 at:2015-06-12
         对话框
         by: 范俊伟 at:2015-06-12
         * @type {*|{name, value}|jQuery}
         */
        var message = "是否确认设置所选用户类型为：";
        if (user_type == -1) {
            message += "无";
        }
        else if (user_type == 0) {
            message += "客服";
        }
        else if (user_type == 1) {
            message += "会计";
        }
        else if (user_type == 2) {
            message += "推广员";
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
                        var obj = $('#user_list').serializeArray();
                        obj.push({name: "user_type", value: user_type});
                        httpRequest('/ns_manage/set_user_type', obj).done(function () {
                            query_user();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }


}