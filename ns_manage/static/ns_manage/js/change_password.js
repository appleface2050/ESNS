/**
 * Date: 15/6/12
 * Time: 12:23
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
function init_view_change_password() {
    showViwe();
    function showViwe() {
        /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         */
        show_breadcrumb([{name: '修改密码'}]);
        EJSTemplateRender('ns_manage/ejs/change_password.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
        });
    }

    window.checkPassword = function () {
        /**
         * 判断密码是否相同
         by: 范俊伟 at:2015-06-12
         判断修改
         by: 范俊伟 at:2015-06-12
         * @type {*|jQuery}
         */
        var new_password = $('input[name=new_password]').val();
        var re_password = $('input[name=re_password]').val();
        if (new_password && re_password && new_password != re_password) {
            return "密码不匹配"
        }

    };
    window.change_password_callback = function (form) {
        /**
         修改密码
         by: 范俊伟 at:2015-06-12
         */
        var obj = form.serializeArray();
        httpRequest('/ns_manage/change_password', obj).then(function () {
            $.simplyToast('修改成功', 'success');
        }, function () {
        })
    }
}
