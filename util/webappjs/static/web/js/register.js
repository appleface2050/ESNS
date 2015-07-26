/**
 * Date: 15/1/21
 * Time: 14:11
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 * var loginUrl = "{% url 'web:login' %}";
 */
function checkPasswordRe() {
    /**
     * 密码确认字段校验
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery}
     */
    var password_re = $('#password_re').val();
    var password = $('#password').val();
    if (!password_re) {
        return '不能为空';
    }
    else if (password != password_re) {
        return '密码不匹配'
    }
    return undefined;
}
function checkTel() {
    /**
     * 手机号字段校验
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery}
     */
    var tel = $('#tel').val();
    var reg = /^\d{11}$/;
    if (!tel) {
        return '不能为空';
    }
    else if (!reg.test(tel)) {
        return '电话号码格式错误!'
    }
    return undefined;
}
function formCallback(data) {
    /**
     * 表单ajax提交回调函数
     * by:范俊伟 at:2015-01-21
     */

    if (data.success) {
        confirmBox.showConfirm('完成', '成功', '确定', '', function () {
            window.location.href = loginUrl;
        }, null);

    }
    else {
        $('#form_error').text(data.message);
    }
}
var seconds;
var interval;
function btnTick() {
    /**
     * 计时器回调函数,显示几秒后可以重复短信
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery|HTMLElement}
     */
    var sms_btn = $('#sms_btn');
    seconds--;
    if (seconds > 0) {
        sms_btn.text("发送成功," + seconds + '秒后可重发');
    }
    else {
        sms_btn.attr("disabled", false);
        sms_btn.text("获取验证码");
        clearInterval(interval);
    }
}
function beginTick() {
    /**
     * 开始计时
     * by:范俊伟 at:2015-01-21
     * @type {number}
     */
    seconds = 60;
    var sms_btn = $('#sms_btn');
    sms_btn.attr("disabled", true);
    sms_btn.text("发送成功," + seconds + '秒后可重发');
    interval = setInterval("btnTick()", 1000);
}
function sendsms() {
    /**
     * 发送短信验证码
     * by:范俊伟 at:2015-01-21
     */
    if (checkField('tel')) {
        return;
    }
    var tel = $('#tel').val();
    if (tel.length == 11) {
        $.post('/ns/send_sms_code', {'tel': tel}, function (response, status) {
            if (status == 'success') {
                if (response.success) {
                    beginTick();
                } else {
                    messageBox.showMessage('短信验证', response.message)
                }
            }
        }, 'json');
    }
}