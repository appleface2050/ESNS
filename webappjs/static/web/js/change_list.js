/**
 * Created by fanjunwei003 on 14/11/22.
 */
function init_object_table_select() {
    /**
     * 初始化,实现table行的选择高亮
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery|HTMLElement}
     */
    var object_table = $('#object_table');
    var top_check = object_table.find('thead').find('input[type=checkbox]');
    var item_checks = object_table.find('tbody').find('input[type=checkbox]');
    top_check.unbind('change').change(function () {

        if ($(this).is(":checked") == true) {

            item_checks.attr("checked", true);
            item_checks.prop("checked", true);
        }
        else {
            item_checks.attr("checked", false);
            item_checks.prop("checked", false);

        }
        item_checks.change();
    });


    item_checks.unbind('change').change(function () {

        var row = $(this).parent().parent();

        if ($(this).is(":checked") == true) {
            row.attr('class', 'info');
        }
        else {
            row.attr('class', '');
        }
    });

    if (/msie/.test(navigator.userAgent.toLowerCase())) {
        top_check.unbind('click').click(function () {
            this.blur();
            this.focus();
        });

        item_checks.unbind('click').click(function () {
            this.blur();
            this.focus();
        });
    }

}
function init_delete_confirm() {
    /**
     * 初始化删除提示框
     * by:范俊伟 at:2015-01-21
     */
    $('[name=delete]').click(function () {
        $('#delModal').modal('show');
        return false;
    });

}

$(
    function () {
        /**
         * 页面初始化后执行
         * by:范俊伟 at:2015-01-21
         */
        init_object_table_select();
        init_delete_confirm();
    }
);
