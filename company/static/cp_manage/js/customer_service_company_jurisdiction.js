 /**
 * Date: 15/6/11
 * Time: 16:12
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

function init_view_customer_service_company_jurisdiction() {
    /**
     * 用户类型管理页面
     by: 范俊伟 at:2015-06-11
     优化函数名称
     by：尚宗凯 at;2015-06-15
     */
    var company_id=window.companyid;
    showView();
    function showView() {
        /**
         * 显示视图
         by: 范俊伟 at:2015-06-12
         优化
         by：刘奕辰 at;2015-06-25
         优化功能
         by：刘奕辰 at;2015-06-26
         优化查询功能
         by：刘奕辰 at;2015-06-27
         */
        var powerlist = null;
        show_breadcrumb([{name: '权限设置'}]);
        httpRequest('/cp/' + company_id + '/get_permission', {}).then(function (data) {
            if (!data.result) {
                return "";
            }
            powerlist = data.result;
            show_breadcrumb([{name: data.result.name}]);
            return EJSTemplateRender('cp_manage/ejs/customer_service_company_jurisdiction.ejs', data.result);
        }).done(function (html) {
            window.viewDTD.resolve();
            window.loadNextPageCallback = null;
            $('#view_content').html(html);
                  $("input[type='checkbox']").each(function(i,el){
                     for(var k=0;k<powerlist.length;k++){
                         if($(el).val()==powerlist[k]){
                            $(el).prop("checked",true);
                             if($(el).attr('a').indexOf('_w')>=0){
                                 $("input[a='"+ $(el).attr('a').replace('_w', '_r') +"']").prop("checked",true);
                                 $("input[a='"+ $(el).attr('a').replace('_w', '_r') +"']").prop("disabled",true);
                             }
                         }
                     }
                  });

                  $("input[type='checkbox']").change(function(){
                      if($(this).attr('a')){
                          var a = $(this).attr('a');
                          if(a.indexOf("all")<0){
                              if(a.substring(a.length-1, a.length) == 'r'){
                                  return;
                              }else{
                                  if($(this).is(":checked")){
                                      $("input[a='"+ a.replace('_w', '_r') +"']").prop("checked",true);
                                      $("input[a='"+ a.replace('_w', '_r') +"']").prop("disabled",true);
                                  }else{
                                      $("input[a='"+a.replace('_w', '_r') +"']").prop("disabled",false);
                                  }
                              }
                              return;
                          }
                          a= a.replace("_all","");
                          var r= a.substring(0, a.length-2)+"_r";
                          var w=a;
                          //if(a.indexOf("_w")>0){
                          var self = this;


                              $("input[type='checkbox']").each(function(k,el){
                                  if(a.indexOf("_w")>0) {
                                      if ($(self).is(":checked")) {
                                          if ($(el).attr('a').indexOf(r) >= 0) {
                                              $(el).prop("checked", true);
                                              $(el).prop("disabled", true);
                                          }
                                          if ($(el).attr('a').indexOf(w) >= 0) {
                                              $(el).prop("checked", true);
                                          }
                                      } else {
                                          if ($(el).attr('a').indexOf(w) >= 0) {
                                              $(el).prop("checked", false);
                                          }
                                          if ($(el).attr('a').indexOf(r) >= 0) {
                                              $(el).prop("disabled", false);
                                          }
                                      }
                                  }else{
                                      if ($(self).is(":checked")) {
                                          if ($(el).attr('a').indexOf(a) >= 0) {
                                              $(el).prop("checked", true);
                                          }
                                      }else{
                                          if ($(el).attr('a').indexOf(a) >= 0) {
                                              $(el).prop("checked", false);
                                          }
                                      }

                                  }
                              });


                      }
                  });

        });
    }

 window.customer_service_company_update_jurisdiction = function (form) {
        /**
         修改权限
         by：刘奕辰 at：2015-06-27
         */
           var obj = form.serializeArray();


        httpRequest('/cp/'+company_id+'/update_permission', obj).then(function () {
                showView();
            $.simplyToast('执行成功', 'success');
        })
    };




}