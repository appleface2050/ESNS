/**
 * Created by EasyShare004 on 2015/6/17.
 */
function init_view_customer_service_create_sys_column() {
    showView();
    function showView() {
        /**
         * 显示视图
         by:尚宗凯 at:2015-06-17
         */
        show_breadcrumb([{name: '创建系统栏目'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_create_sys_column.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
        });
    }

    window.customer_service_create_sys_column_callback = function (form) {
        var obj = form.serializeArray();
        httpRequest('/cp/create_sys_column', obj).then(function () {
            $.simplyToast('修改成功', 'success');
        }, function () {
        })
    }
}