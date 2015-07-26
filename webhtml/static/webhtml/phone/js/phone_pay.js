$(function () {
    initAddressV2();
});
$(function () {
    var fptt = $('#fptt');
    var fptt_helper = $("#fptt_helper");

    fptt.focus(function () {
        fptt_helper.show();
    });

    fptt.blur(function () {
        fptt_helper.hide();
    });

});

$(function () {
    var fptt = $('#yjdz');
    var fptt_helper = $("#yjdz_helper");

    fptt.focus(function () {
        fptt_helper.show();
    });

    fptt.blur(function () {
        fptt_helper.hide();
    });

});

function xy_must_check() {
    if (!$("#xy_check")[0].checked) {
        return "请阅读协议";
    }
    else {
        return null;
    }

}
function taocan_check() {
    if (!$("#taocan").val()) {
        return "未选择套餐";
    }
    else {
        return null;
    }
}
$(function () {
    var fptt = $('#jdxqdz');
    var fptt_helper = $("#jdxqdz_helper");

    fptt.focus(function () {
        fptt_helper.show();
    });

    fptt.blur(function () {
        fptt_helper.hide();
    });

});
