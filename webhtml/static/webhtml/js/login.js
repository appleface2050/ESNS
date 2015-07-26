/**
 * Date: 15/1/21
 * Time: 14:07
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 * var adminHomeUrl = "{% url 'web:home' %}";
 */
function formCallback(data) {
    /**
     * 表单ajax提交回调函数
     * by:范俊伟 at:2015-01-21
     */
    if (data.success) {
        var html = createJifenMessage(data);
        if (html) {
            addDjangoMessage(html, 'success', function () {
                window.location.href = homeUrl;
            });
        }
        else {
            window.location.href = homeUrl;
        }

    }
    else if (data.status_code == 9) {
        window.location.href = regTelUrl;
    }
    else {
        $('#form_error').text(data.message);
    }
}