/**
 * Date: 15/1/21
 * Time: 14:02
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 * window.project_id = "{{ project_id }}";
 */
var exitViewCallback = null;
var viewOpenedFlag = {};
var current_view_id = null;
window.onFrame = true;
function openView(view_id, out_project) {
    /**
     * 打开view
     * by:范俊伟 at:2015-02-06
     * 菜单加载修改
     by: 范俊伟 at:2015-02-14
     菜单显示预处理
     by: 范俊伟 at:2015-03-09
     promise化
     by: 范俊伟 at:2015-03-09
     逻辑修改
     by: 范俊伟 at:2015-03-10
     优化加载
     by: 范俊伟 at:2015-03-10
     增加退出项目参数,优化函数逻辑
     by: 范俊伟 at:2015-03-18
     */
    if (out_project) {
        window.project_id = null;
    }
    preShowSiteMenu(view_id);
    if (current_view_id === view_id) {
        return;
    }
    var last_view_id = current_view_id;
    current_view_id = view_id;
    window.viewDTD = $.Deferred();
    console.log('openView');
    if (window.viewMaskTimer) {
        clearTimeout(window.viewMaskTimer);
    }
    hideMask();
    var showDtd = $.Deferred();

    window.viewMaskTimer = setTimeout(function () {
        showMask();
        setTimeout(function () {
            showDtd.resolve();
        }, 1500)
    }, 500);

    //window.viewMaskTimer = setTimeout(function () {
    //
    //    window.viewDTD.done(function () {
    //        clearTimeout(window.viewMaskTimer);
    //        hideMask();
    //        console.log('complate openView');
    //    });
    //}, 500);
    window.viewDTD.promise().done(function () {
        clearTimeout(window.viewMaskTimer);
        if (window.hasShowMask) {
            showDtd.promise().done(function () {
                hideMask();
            });
        }

        console.log('complate openView');
    });


    initPage().done(function () {
        if (exitViewCallback) {
            exitViewCallback();
            exitViewCallback = null;
        }
        var first_open = true;
        if (viewOpenedFlag[view_id]) {
            first_open = false;
        }
        else {
            viewOpenedFlag[view_id] = true;
        }

        var init_view_fun = 'init_view_' + view_id + '(first_open)';
        try {
            eval(init_view_fun);
        }
        catch (e) {
            console.warn(e);
            $('#view_content').empty();
            window.viewDTD.resolve();
        }
        current_view_id = view_id;
        initSiteMenu();
    });

}
function refreshView() {
    /**
     * 刷新view
     * by:范俊伟 at:2015-02-06
     * 逻辑修改
     by: 范俊伟 at:2015-03-09
     优化数据缓存
     by: 范俊伟 at:2015-03-10
     */
    window.userInfo = undefined;

    window.projectInfo = undefined;
    window.project_all_user = undefined;
    window.userGroup = undefined;
    if (current_view_id) {
        var view_id = current_view_id;
        current_view_id = null;
        initPage();
        openView(view_id);
    }
}
var showErrorMessage = function (data) {
    /**
     * 通用错误信息显示
     * by:范俊伟 at:2015-01-22
     * 判断在有message的情况下再提示错误信息
     by: 范俊伟 at:2015-03-08
     */
    if (!data.success) {
        if (data.message) {
            if (data.dialog == 0) {
                $.simplyToast(data.message, 'danger');
            }
            else {
                messageBox.showMessage('错误', data.message);
            }
        }
    }


};

function preShowSiteMenu(view_id) {
    if (!isIE()) {
        $('[view-id]').removeClass('active');
        $('[view-id=' + view_id + ']').addClass('active');
    }
}

function initSiteMenu() {
    /**
     * 初始化菜单
     * by:范俊伟 at:2015-02-06
     * 修改菜单加载方式
     by: 范俊伟 at:2015-02-14
     改用checkManage,修改菜单权限控制
     by: 范俊伟 at:2015-03-01
     权限控制
     by: 范俊伟 at:2015-03-10
     */
    console.log("initSiteMenu");

    var manager = {on: false, say: false};
    var xmjl = {on: false, say: false};

    var data = {menu_groups: menu_data};

    for (var i = 0; i < data.menu_groups.length; i++) {
        var menu_goup = data.menu_groups[i];
        for (var j = 0; j < menu_goup.menus.length; j++) {

            var menu = menu_goup.menus[j];
            if (menu) {
                var permission = null;
                try {
                    permission = menu.permission;
                }
                catch (e) {
                }

                var show = true;
                if (permission) {
                    var sp = permission.split(',');
                    for (var k = 0; k < permission.length; k++) {
                        var p = sp[k];
                        if (p == 'manager' && (!manager.on || !manager.say)) {
                            show = false;
                        }
                        if (p == 'xmjl' && !xmjl.on) {
                            show = false;
                        }

                    }
                }
                menu.show = show;
            }

        }
    }
    console.log('sitemenu', data);
    templateRender('wx_admin/mst/sitemenu.mst', data, function (rendered) {
        $('#left-side-menu').html(rendered);
        if (!isIE()) {
            $('[view-id]').removeClass('active');
            $('[view-id=' + current_view_id + ']').addClass('active');
        }
    });


}
window.hasShowMask = false;
function showMask() {
    /**
     * 显示遮罩
     by: 范俊伟 at:2015-03-09
     */
    if (!window.hasShowMask) {
        $('body').css("overflow", "hidden");
        $("#cover").show();
        window.hasShowMask = true;
    }

}

function hideMask() {
    /**
     * 隐藏遮罩
     by: 范俊伟 at:2015-03-09
     */
    if (window.hasShowMask) {
        $('body').css("overflow", "visible");
        $("#cover").hide();
        window.hasShowMask = false;
    }
}