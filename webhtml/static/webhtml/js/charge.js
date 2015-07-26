/**
 * Date: 15/2/13
 * Time: 16:34
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
function set_fp_view() {
    /**
     * 设置发票内容是否可见
     by: 范俊伟 at:2015-02-13
     */
    if ($('#has_fp').val() == '1') {
        $('#fp_view').show();
    }
    else {
        $('#fp_view').hide();
    }
}
function fp_form_check() {
    /**
     * 表单校验
     * by: 范俊伟 at:2015-02-13
     * 固定电话和手机选填其一
     by: 范俊伟 at:2015-03-08
     修改表单校验
     by: 范俊伟 at:2015-03-19
     */
    if ($('#has_fp').val() == '1') {
        var form = $('#fp_form');
        return checkForm(form);
    }
    else {
        return true;
    }
}

$(function () {
    /**
     * 页面初始化
     by: 范俊伟 at:2015-02-13
     */
    $('#has_fp').change(function () {
        set_fp_view();
    });
    set_fp_view();
});

