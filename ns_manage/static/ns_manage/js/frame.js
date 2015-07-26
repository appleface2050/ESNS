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
    initSiteMenu();
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
            $('#view_content').empty();
            eval(init_view_fun);
        }
        catch (e) {
            console.warn(e);

            window.viewDTD.resolve();
        }
        current_view_id = view_id;
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
     修改菜单加载
     by: 范俊伟 at:2015-06-12
     */
    var data = eval(user_type + "_menu_data");
    var sidebar = $('#left-sidebar');
    EJSTemplateRender('ns_manage/ejs/sitemenu.ejs', {list: data}).done(function (rendered) {
        sidebar.html(rendered);
        sidebar.find('li').removeClass('active');
        sidebar.find('li').removeClass('open');
        var active = $('li[view-id=' + current_view_id + ']');
        active.addClass('active');
        var p_view_id = active.attr('p-view-id');
        var p1 = $('li[view-id=' + p_view_id + ']');
        p1.addClass('active');
        p1.addClass('open');
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

function show_breadcrumb(list, is_home) {
    EJSTemplateRender('ns_manage/ejs/breadcrumb.ejs', {list: list, is_home: is_home}).done(function (rendered) {
        $('#breadcrumb').html(rendered);
    });
}