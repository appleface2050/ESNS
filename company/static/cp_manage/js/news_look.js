/**
 * Created by wangjian on 15/6/27.
 */

function news_look_by_url(){

}
(function () {

    window.news_look_by_url_with_brower = function (url) {
        /**
         * 打开对话页面
         by: 王健 at:2015-06-27
         添加时间参数防止手机端缓存
         by: 王健 at:2015-06-30
         * @type {string}
         */
            url = window.location.href.substring(0, window.location.href.indexOf('/', 10)) + url+"?t="+(new Date()).toString();
        //console.log(url);
        var p = "height=600,width=320,directories=no,location=no,menubar=no,resizable=yes,status=no,toolbar=no,top=100,left=200";
        try {
            if(window.look_browser &&window.look_browser.location &&window.look_browser.location.href){
                window.look_browser.location.href = url;
            }else{
                window.look_browser = window.open(url, '' + (+new Date()), p);
            }
            window.look_browser.focus();
        } catch (e) {

        }
    };

    window.news_look_by_url = function(url){
        /**
         * 添加二维码手机端 预览
         * by:王健 at:2015-06-30
         */
        bootbox.dialog({
            title: "提示",
            message: "请扫描二维码在手机端预览：<img src='http://qr.liantu.com/api.php?text="+window.location.href.substring(0, window.location.href.indexOf('/', 10)) +url+"?t="+(new Date()).toString()+"'/>",
            buttons: {
                "cancel": {
                    "label": "取消",
                    "className": "btn-sm"
                },
                "button": {
                    "label": "确定",
                    "className": "btn-sm",
                    "callback": function () {
                        news_look_by_url_with_brower(url);
                    }
                }
            }
        });
    };
    window.show_news_look = function(){
        window.news_look_by_url('/cp/show_sys_phone_news_look/'+$('#temp_column').val()+'/'+$("#news_id").val());
    }
    window.show_news_look_company = function(){
        window.news_look_by_url('/cp/show_phone_news_look/'+window.companyid+'/'+$('#temp_column').val()+'/'+$("#news_id").val());
    }


})();