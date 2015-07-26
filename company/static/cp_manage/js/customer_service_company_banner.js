/**
 * Created by EasyShare004 on 2015/6/16.
 */
 var company_id=window.companyid;
function init_view_customer_service_company_banner() {

    /**
     * 公司banner
     by：尚宗凯 at;2015-06-16
     */

    showView();
    function showView() {
        /**
         * 显示视图
         by: 尚宗凯 at:2015-06-16
           * 优化公司banner
         by: 刘奕辰 at:2015-06-23
         */
        show_breadcrumb([{name: '公司banner'}]);
        EJSTemplateRender('cp_manage/ejs/customer_service_company_banner.ejs').done(function (html) {
            $('#view_content').html(html);
            window.viewDTD.resolve();
              page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.all_company_banner;
            loadNextPage();
        });
    }

    window.all_company_banner = function () {
        /**
		 查询公司banner
         by：尚宗凯 at：2015-06-16
         * 优化公司banner查询
         by: 刘奕辰 at:2015-06-23
         * @type {*|jQuery}
         */
//        var keyword = $('#search_keyword').val();
//        var user_type = $('#search_user_type').val();
        var dtd = $.Deferred();
        var keyword = $('#search_keyword').val();

       httpRequest('/cp/'+company_id+'/company_banner',{keyword: keyword, page_start:page_start}).then(function (data) {
            if (!data.result||data.result.length == 0) {
                 window.loadNextPageCallback = null;
                return "";
            }
            page_start+=data.result.length;
            return EJSTemplateRender('cp_manage/ejs/customer_service_set_company_banner_table_data.ejs', data);
        }).then(function (html) {
             $('tbody').append(html);
            dtd.resolve();
        });
         return dtd.promise();
    };

    window.DeleteCompanyBanner = function(){
        /**
         * 删除banner
         * by：尚宗凯 at：2015-06-16
         *  *  优化
         * by：刘奕辰 at：2015-06-23
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

                        httpRequest('/cp/'+company_id+'/delete_company_banner', obj).done(function () {
                            $('#view_content tbody').empty();

                           orientation_all_company_banner();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });
    }


    window.SetCompanyBannerIsActive = function (is_active) {
        /**
         * 设置是否生效
         * by：尚宗凯 at：2015-06-16
         *  优化
         * by：刘奕辰 at：2015-06-23
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

                        httpRequest('/cp/'+company_id+'/set_company_banner_is_active', obj).done(function () {
                           $('#view_content tbody').empty();

                           orientation_all_company_banner();

                            $.simplyToast('设置成功', 'success');
                        })
                    }
                }
            }
        });

    }
 window.orientation_all_company_banner = function () {
        /**
		 查询按钮查询公司banner
         by：刘奕辰 at：2015-06-23
         * @type {*|jQuery}
         */
            page_start=0;
            $('#view_content tbody').empty();
            window.loadNextPageCallback = window.all_company_banner;
            loadNextPage();

    };

}