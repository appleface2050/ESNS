/**
 * Created by EasyShare004 on 2015/6/23
 */


function init_view_customer_service_employee_manage() {

    var page_start = 0;
    /**
     * 员工管理
     by：闫宇 at;2015-6-23
     */
    var company_id=window.companyid;
    var manager="manager";
    var manager1="user";
    showView();
    function showView() {
         /**
         * 员工管理页面
         * by:闫宇 at:2015-6-23
         */
         show_breadcrumb([{name: '员工管理'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_employee_manage.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.find_our_company_user;
            loadNextPage();
        });

    }
    window.find_our_company_user = function () {
        /**
		 查询本公司员工
         * by:闫宇 at:2015-6-23
         * @type {*|jQuery}
         */
            $('#view_content tbody').empty();
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();
        window.loadNextPageCallback = null;
        httpRequest('/cp/'+company_id+'/get_user_by_company_id', {key: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {

                return "";
            }
            page_start+=data.result.length;
            data['company_id'] = company_id;
            return EJSTemplateRender('cp_manage/ejs/customer_service_employee_manage_table_data.ejs', data);
        }).then(function (html) {
            $('tbody').append(html);
            dtd.resolve();
        });
        return dtd.promise();
    };



    window.delete_our_company_user = function(){
        /**
         * 删除公司员工
         * by:闫宇 at:2015-6-24
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
                        var obj = $('#sys_news_list').serializeArray();

//                        obj.push({name: "user_type", value: user_type});
//                        obj.push({name: "is_active", value: is_active});

                        httpRequest('/cp/'+company_id+'/delete_company_user', obj).done(function () {
                            $('#view_content tbody').empty();

                           find_our_company_user();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }
   window.update_admin = function () {
        /**
         * 设置管理员
         * by:闫宇 at:2015-6-24
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";

            message = "是否设置管理员";

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
                        obj.push({name: "do", value: manager});

                        httpRequest('/cp/'+company_id+'/set_company_admin', obj).done(function () {
                            $('#view_content tbody').empty();
                            find_our_company_user();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }
     window.cancel_admin = function () {
        /**
         * 取消管理员
         * by:闫宇 at:2015-6-24
         * @type {*|{name, value}|jQuery}
         */
//        var message = "是否确认设置所选显示方式为：";

            message = "是否取消管理员";

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
                        obj.push({name: "do", value: manager1});

                        httpRequest('/cp/'+company_id+'/set_company_admin', obj).done(function () {
                           $('#view_content tbody').empty();
                           find_our_company_user();
                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }
   window.add_company_user=function(){
         //showModalDialog();
        //showModalDialog('page.html','height=10px','width=40px','top=500px');
      // showModalDialog('page.html','height=10px,width=40px,top=50,left=50,toolbar=no,menubar=no,scrollbars=no,resizable=no,location=no,status=no,resizable=no');
      // window.open ('page.html','newwindow','height=100,width=400,top=50%,left=50%,toolbar=no,menubar=no,scrollbars=no,resizable=no,location=no,status=no,resizable=no');

          //  window.showModalDialog("modal.htm","dialogWidth=100px;dialogHeight=100px");
    // showModalDialog('cp_manage/ejs/customer_service_employee_manage.ejs','dialogWidth:100px;dialogHeight:100px;center:yes;help:no;resizable:no;status:yes,toolbar=no');
          //var phone=prompt("请输入手机号","");

        //httpRequest('/cp/'+company_id+'/delete_company_user', {}).done(function () {
        //    $.simplyToast('设置成功', 'success');
        //})
    }
    window.add_our_company_user = function(){
        /**
         * 添加公司员工
         * by:闫宇 at:2015-6-30
         * @type {*|{name, value}|jQuery}
         */
        var tel=prompt("请输入手机号","");
        httpRequest('/cp/'+company_id+'/company_add_user_by_tel', {tel:tel}).done(function () {
            $.simplyToast('设置成功', 'success');
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
                find_our_company_user();
            }
     }

}