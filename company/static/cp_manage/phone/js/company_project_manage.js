/**
 * Created by wangjian on 15/6/22.
 */


function create_company_project_manage() {
    /**
     * 创建项目
     by: 刘奕辰    at:2015-07-02
     */

          EJSTemplateRender('cp_manage/phone/ejs/company_create_project.ejs',{id:null}).done(function (html) {
            $('body').html(html);

               //initDateTimePicker();
               initCity();
        });
    };




function company_create_project_callback() {
        /**
           创建项目 提交
         by: 刘奕辰 at:2015-06-30
         */
        var form = $('form');
        var obj = form.serializeArray();
         obj.push({name: "company_id", value: company_id});
        var url='/ns/reg_project_by_company';
       //  var company_id=window.companyid;

        httpRequest(url, obj).done(function (data) {
        window.location.reload();
    });


    }

$(function(){
    create_company_project_manage();
});