/**
 * Created by wangjian on 15/6/22.
 */


function delete_user_by_id_to_company() {
    /**
     * 删除成员
     by: 刘奕辰    at:2015-07-02
     */

    var form = $('form');
    if (form.find('input[type=checkbox]:checked').length <= 0) {
        return;
    }
    var url = '/cp/' + company_id + '/delete_company_user';
    var obj = form.serializeArray();
    httpRequest(url, obj).done(function (data) {
        window.location.reload();
    });

}


function init_check() {
    /**
     * 设置选中状态
     by: 范俊伟 at:2015-06-24
     用于选中
      by: 刘奕辰    at:2015-07-02
     */
    $('input[type=checkbox]').each(function () {
        var checkbox = $(this);
        set_check_state(checkbox);
        checkbox.change(function () {
            set_check_state(checkbox);
        });
    });
}

function set_check_state(checkbox) {
    /**
     * 设置选中状态
     by: 范俊伟 at:2015-06-24
     用于选中
      by: 刘奕辰    at:2015-07-02
     */
    var p = checkbox.parent();
    var chk = p.find('[chk]');
    if (checkbox.is(':checked')) {
        chk.attr('class', 'ci_01');
    }
    else {
        chk.attr('class', 'ci_02');
    }
}

$(function(){
    init_check();
});