/**
 * Date: 15/5/21
 * Time: 14:45
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
(function () {

    window.openwin = function () {
        /**
         * 打开对话页面
         by: 范俊伟 at:2015-05-21
         * @type {string}
         */
        var url = kf_url + "/client?sessionid=" + sessionid;
        console.log(url);
        var p = "height=600,width=500,directories=no,location=no,menubar=no,resizable=yes,status=no,toolbar=no,top=100,left=200";
        try {
            var m = window.open(url, '' + (+new Date()), p);
            m.focus()
        } catch (e) {

        }
    };

    function get_online_state() {
        /**
         * 初始化状态
         by: 范俊伟 at:2015-05-21
         */
        $.ajax({
            type: "get",
            url: kf_url + "/client/get_online_state",
            dataType: "jsonp",
            jsonp: "callback",//服务端用于接收callback调用的function名的参数
            jsonpCallback: "success_jsonpCallback",//callback的function名称
            success: function (json) {
                if (json.kf_online_state == "1") {
                    $('#kf_panel').addClass("kf_panel_online");
                }
                else {
                    $('#kf_panel').addClass("kf_panel_offline");
                }
                $('#kf_panel').show();

            },
            error: function () {
                console.error(json);
            }
        });
    }

    $(function () {
        get_online_state();
    });
})();