/**
 * Date: 15/6/10
 * Time: 21:38
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
(function () {
    window.login_callback = function (form) {
        /**
         * 用户登录
         by: 范俊伟 at:2015-06-10
         */
        var obj = form.serializeArray();
        httpRequest('/cp/login', obj).then(function (data) {
            if (data.result.url) {
                window.location.href = data.result.url;
            }
        }, function () {
        });
    };
})();