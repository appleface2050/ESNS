/**
 * Created by EasyShare004 on 2015/6/16.
 */

function init_view_customer_service_create_sys_news() {
    showView();
    function showView() {
        /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         * 提供空数据，兼容修改新闻，渲染栏目列表
         by: 王健 at:2015-06-12
         添加初始化的栏目变量
     * by: 王健 at:2015-06-30

         */
        show_breadcrumb([{name: '创建系统新闻'}]);
        httpRequest('/cp/all_sys_column', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            return EJSTemplateRender('cp_manage/ejs/customer_service_create_sys_news.ejs', {id:'', sys_column_id:0, sys_column:0, content:'', title: '', 'column_list': data.result});
        }, function () {
        }).done(function (html) {
        $('#view_content').html(html);
            window.viewDTD.resolve();
        })

    }

//    window.checkPassword = function () {
//        /**
//         * 判断密码是否相同
//         by: 范俊伟 at:2015-06-12
//         判断修改
//         by: 范俊伟 at:2015-06-12
//         * @type {*|jQuery}
//         */
//        var new_password = $('input[name=new_password]').val();
//        var re_password = $('input[name=re_password]').val();
//        if (new_password && re_password && new_password != re_password) {
//            return "密码不匹配"
//        }
//
//    };
    window.customer_service_create_sys_news_callback = function (form) {
        /**
         修改密码
         by: 范俊伟 at:2015-06-12
		 修改url路径
         by：尚宗凯 at：2015-06-15
         新增新闻id 用于重复提交
         by：刘奕辰 at：2015-06-23
         添加预览需要的栏目id
         * by: 王健 at:2015-06-30
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

}