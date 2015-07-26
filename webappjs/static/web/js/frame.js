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
function getUserInfo(cb) {
    /**
     * 获取当期用户信息
     * by:范俊伟 at:2015-01-21
     * 兼容promise模式
     * by:范俊伟 at:2015-02-10
     * promise化
     by: 范俊伟 at:2015-03-09
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    var dtd = $.Deferred();
    if (window.userInfo === undefined) {
        httpRequest('/ns/update_userinfo').then(function (data) {
            window.userInfo = data.result;
            console.log('getUserInfo', window.userInfo);
            if (cb) {
                cb(window.userInfo);
            }
            dtd.resolve(window.userInfo);
        }, function (xhr, err, ex) {
            if (cb) {
                cb(null);
            }
            dtd.reject(ex);
        });
    }
    else {
        setTimeout(function () {
            if (cb) {
                cb(window.userInfo);
            }
            dtd.resolve(window.userInfo);
        }, 0);

    }
    return dtd.promise();
}
function getUserJifen(cb) {
    /**
     * 获取当期用户积分信息
     * by:范俊伟 at:2015-01-21
     * 取消此函数缓存
     by: 范俊伟 at:2015-03-09
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    var dtd = $.Deferred();
    httpRequest('/ns/query_my_jifen').then(function (data) {
        console.log('getUserJifen', data);
        window.userJifen = data.result;
        if (cb) {
            cb(window.userJifen);
        }
        dtd.resolve(window.userJifen);
    }, function (xhr, err, ex) {
        if (cb) {
            cb(null);
        }
        dtd.reject(ex);
    });


    return dtd.promise();
}

function getProjectInfo(cb) {
    /**
     * 获取当前项目信息
     * by:范俊伟 at:2015-01-21
     * 调用实际接口获取信息
     * by:范俊伟 at:2015-01-22
     * 修改回调函数调用方式
     * by:范俊伟 at:2015-02-03
     * 增加ajax错误信息输出
     * by:范俊伟 at:2015-02-03
     * promise化
     by: 范俊伟 at:2015-03-09
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    var dtd = $.Deferred();
    if (window.project_id) {
        if (window.projectInfo === undefined) {
            httpRequest('/ns/get_project', {project_id: window.project_id}).then(function (data) {
                console.log('getProjectInfo', data);
                window.projectInfo = data.result;
                window.projectInfo.city = getCityByID(window.projectInfo.address);
                if (cb) {
                    cb(window.projectInfo);
                }
                dtd.resolve(window.projectInfo);
            }, function (xhr, err, ex) {
                if (cb) {
                    cb(null);
                }
                dtd.reject(ex);
            });

        }
        else {
            setTimeout(function () {
                if (cb) {
                    cb(window.projectInfo);
                }
                dtd.resolve(window.projectInfo);
            }, 0);
        }
    }
    else {
        if (cb) {
            cb(null);
        }
        dtd.resolve(null);
    }
    return dtd.promise();
}
function getCurrentProjectUserGroups(cb, p_project_id) {
    /**
     * 获取当前项目用户组
     * by:范俊伟 at:2015-02-03
     * promist化
     by: 范俊伟 at:2015-03-09
     分组排序
     by: 范俊伟 at:2015-03-15
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     增加获取其他项目的功能
     by: 范俊伟 at:2015-04-07
     */
    var dtd = $.Deferred();
    if (p_project_id == undefined) {
        p_project_id = window.project_id;
    }
    if (p_project_id) {
        var url = '/ns/' + p_project_id + '/query_group';
        if (window.userGroup === undefined || p_project_id != window.project_id) {
            httpRequest(url).then(function (data) {
                var userGroup = _(data.result).sortBy('sorted');
                if (p_project_id == window.project_id) {
                    window.userGroup = userGroup;
                }
                console.log('getUserGroup', window.userGroup);
                if (cb) {
                    cb(userGroup);
                }
                dtd.resolve(userGroup);
            }, function (xhr, err, ex) {
                if (cb) {
                    cb(null);
                }
                dtd.reject(ex);
            });
        }
        else {
            setTimeout(function () {
                if (cb) {
                    cb(window.userGroup);
                }
                dtd.resolve(window.userGroup);
            }, 0);
        }
    }
    else {
        if (cb) {
            cb(null);
        }
        dtd.resolve(null);
    }
    return dtd.promise();
}
function checkManage(cb) {
    /**
     * 检测当前用户是否为项目管理员
     * by:范俊伟 at:2015-02-03
     * 修改管理员判断方式
     * by:范俊伟 at:2015-02-09
     * 兼容promise模式,修改返回结果
     by: 范俊伟 at:2015-03-01
     */
    var deferred = $.Deferred();
    if (window.project_id) {
        if (window.onManageGroup === undefined) {
            getProjectInfo(function (project_info) {
                if (project_info.manager == uid) {
                    window.onManageGroup = {on: true, say: true};
                    deferred.resolve(window.onManageGroup);
                    if (cb)
                        cb(window.onManageGroup);
                    return;
                }
                getCurrentProjectUserGroups(function (user_gruop) {
                    window.onManageGroup = {on: false, say: false};
                    for (var i = 0; i < user_gruop.length; i++) {
                        var group = user_gruop[i];
                        if (group.type == 'sys_manage') {
                            for (var j = 0; j < group.look_members.length; j++) {
                                if (uid == group.look_members[j]) {
                                    window.onManageGroup.on = true;
                                    window.onManageGroup.say = false;
                                }
                            }
                            for (var j = 0; j < group.say_members.length; j++) {
                                if (uid == group.say_members[j]) {
                                    window.onManageGroup.on = true;
                                    window.onManageGroup.say = true;
                                }
                            }
                            break;
                        }
                    }
                    deferred.resolve(window.onManageGroup);
                    if (cb)
                        cb(window.onManageGroup);
                });
            });

        }
        else {
            setTimeout(function () {
                deferred.resolve(window.onManageGroup);
                if (cb)
                    cb(window.onManageGroup);
            }, 0);
        }
    }
    return deferred.promise();
}

function checkSysGroupType(type) {
    /**
     * 检测当前用户是否在指定组中
     * by:范俊伟 at:2015-03-01
     */
    var deferred = $.Deferred();
    if (window.project_id) {
        getCurrentProjectUserGroups(function (user_gruop) {
            var data = {on: false, say: false};
            for (var i = 0; i < user_gruop.length; i++) {
                var group = user_gruop[i];
                if (group.type == type) {
                    for (var j = 0; j < group.look_members.length; j++) {
                        if (uid == group.look_members[j]) {
                            data.on = true;
                            data.say = false;
                        }
                    }
                    for (var j = 0; j < group.say_members.length; j++) {
                        if (uid == group.say_members[j]) {
                            data.on = true;
                            data.say = true;
                        }
                    }
                    break;
                }
            }
            deferred.resolve(data);
        });
    }
    return deferred.promise();
}

function getGroupByType(type) {
    /**
     * 根据组类型获取组信息
     * by:范俊伟 at:2015-03-01
     */
    var deferred = $.Deferred();
    if (window.project_id) {
        getCurrentProjectUserGroups(function (user_gruop) {
            for (var i = 0; i < user_gruop.length; i++) {
                var group = user_gruop[i];
                if (group.type == type) {
                    deferred.resolve(group);
                    return;
                }
            }
            deferred.resolve(null);
        });
    }
    return deferred.promise();
}
function setName(userInfo) {
    /**
     * 显示当前用户姓名
     * by:范俊伟 at:2015-01-21
     */
    $("#top_name").text(userInfo.name);
}

function getAllUser(cb, p_project_id) {
    /**
     * 获取项目内所有用户
     * by:范俊伟 at:2015-01-30
     * 使用回调方式返回数据
     * by:范俊伟 at:2015-02-04
     * @type {string}
     * promise化
     by: 范俊伟 at:2015-03-09
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     增加获取其他项目的功能
     by: 范俊伟 at:2015-04-07
     */
    if (p_project_id === undefined) {
        p_project_id = window.project_id;
    }
    var dtd = $.Deferred();
    if (window.project_id) {
        if (window.project_all_user === undefined || p_project_id != window.project_id) {
            var url = '/ns/' + p_project_id + '/query_person';
            var data = {};
            httpRequest(url).then(function (data) {
                console.log('getAllUser', data.result);
                if (p_project_id == window.project_id) {
                    window.project_all_user = data.result;
                }
                if (cb) {
                    cb(data.result);
                }
                dtd.resolve(data.result);
            }, function (xhr, err, ex) {
                if (cb) {
                    cb(null);
                }
                dtd.reject(ex);
            });
        }
        else {
            setTimeout(function () {
                if (cb) {
                    cb(window.project_all_user);
                }
                dtd.resolve(window.project_all_user);
            }, 0);
        }
    }
    else {
        if (cb) {
            cb(null);
        }
        dtd.reject(ex);
    }
    return dtd.promise();
}

function getUserById(id, cb, p_project_id) {
    /**
     * 根据ID获取用户信息
     * by:范俊伟 at:2015-01-30
     * 使用回调方式返回数据
     * by:范俊伟 at:2015-02-04
     * 使用回调方式返回数据
     * by:范俊伟 at:2015-02-04
     * 增加获取其他项目的功能
     by: 范俊伟 at:2015-04-07
     */
    getAllUser(function (all_user) {
        for (var i = 0; i < all_user.length; i++) {
            var user = all_user[i];
            if (user.id == id) {
                cb(user);
            }
        }
    }, p_project_id);

}

function canShowDeleteFromProject(user, isManageGroup, manager) {
    /**
     * 判断是否可删除
     by: 范俊伟 at:2015-03-10
     */
    if (user.id == manager) {
        user.canDelete = false;
    }
    else if (uid != manager && isManageGroup) {
        user.canDelete = false;
    }
    else {
        user.canDelete = true;
    }
}

function linkUserToGroup(group, all_user, manager) {
    /**
     * 用户和组关联
     * by:范俊伟 at:2015-02-05
     * 删除按钮控制
     by: 范俊伟 at:2015-03-10
     使用underscore.js优化算法
     by: 范俊伟 at:2015-03-15
     * @type {Array}
     */
    group.user_list = [];
    group.user_count = 0;
    group.group_id = group.id;
    group.group_name = group.name;
    group.current_user_in = false;
    group.current_user_say = false;
    var isManageGroup = false;
    if (group.type == 'sys_manage') {
        isManageGroup = true;
    }
    _(group.look_members).each(function (user_id) {
        var user = _(all_user).find(function (obj) {
            return obj.id == user_id;
        });
        if (user) {
            if (user.group_list === undefined) {
                user.group_list = [];
            }
            if (user.id == uid) {
                group.current_user_in = true;
            }
            canShowDeleteFromProject(user, isManageGroup, manager);
            user.group_list.push($.extend({}, {can_say: false}, group));
            group.user_list.push(user);
            group.user_count++;
        }
    });

    _(group.say_members).each(function (user_id) {
        var user = _(all_user).find(function (obj) {
            return obj.id == user_id;
        });
        if (user) {
            if (user.group_list === undefined) {
                user.group_list = [];
            }
            if (user.id == uid) {
                group.current_user_in = true;
                group.current_user_say = true;
            }
            canShowDeleteFromProject(user, isManageGroup, manager);
            user.group_list.push($.extend({}, {can_say: true}, group));
            group.user_list.push(user);
            group.user_count++;
        }
    });

    group.has_group_chat = (group.current_user_in && group.is_needhx);

}

function getUserGroupList(cb) {
    /**
     * 将组和用户关联,并找出未分组用户
     * by:范俊伟 at:2015-02-05
     * 未分组用户修改
     * by:范俊伟 at:2015-02-09
     * 去掉未分组
     * by:范俊伟 at:2015-02-10
     * 重新设计权限逻辑
     by: 范俊伟 at:2015-03-10
     使用underscore.js优化算法
     by: 范俊伟 at:2015-03-15
     */
    if (window.group_list === undefined) {
        console.log('getUserGroupList');
        $.when(getAllUser(), getCurrentProjectUserGroups(), getProjectInfo()).done(function (all_user, all_groups, project_info) {
            all_user = all_user.concat();
            all_groups = _(all_groups).reject(function (group) {
                /**
                 * 过滤掉root组
                 by: 范俊伟 at:2015-03-15
                 */
                return group.type == 'root';
            });
            _(all_groups).each(function (group) {
                linkUserToGroup(group, all_user, project_info.manager);
            });
            console.log('group_list', group_list);
            window.group_list = _(all_groups).sortBy('sorted');
            cb(window.group_list);
        });

    }
    else {
        setTimeout(function () {
            cb(window.group_list);
        }, 0);
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
     */
    var def = $.Deferred();
    var manager = {on: false, say: false};
    var xmjl = {on: false, say: false};


    if (window.project_id) {
        $.when(checkManage(), checkSysGroupType('sys_xmjl')).done(function (res_manager, res_xmjl) {
            manager = res_manager;
            xmjl = res_xmjl;
            var data = {menu_groups: project_menu};
            def.resolve(data);
        });
    }
    else {
        setTimeout(function () {
            var data = {menu_groups: no_project_menu};
            def.resolve(data);
        }, 0);
    }

    def.done(function (data) {
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
        templateRender('web/mst/sitemenu.mst', data, function (rendered) {
            $('#left-side-menu').html(rendered);
            if (!isIE()) {
                $('[view-id]').removeClass('active');
                $('[view-id=' + current_view_id + ']').addClass('active');
            }
        });
    });


}

var displayJifenMessage = function (data) {
    var html = createJifenMessage(data);
    if (html) {
        $.simplyToast(html, 'success');
    }

};
initQueue.push(function () {
    /**
     * 相关初始化功能加入初始化列表
     * by:范俊伟 at:2015-01-21
     * 权限控制,如果在管理员组则显示隐藏的菜单
     * by:范俊伟 at:2015-02-03
     * 菜单加载修改
     * by: 范俊伟 at:2015-02-14
     * 信息修改
     by: 范俊伟 at:2015-02-16
     * 修改初始化队列
     by: 范俊伟 at:2015-03-09
     优化数据缓存
     by: 范俊伟 at:2015-03-10
     */
    console.log('frame_init');
    window.onManageGroup = undefined;
    window.group_list = undefined;
});
initQueue.push(function () {
    /**
     * 初始化队列
     by: 范俊伟 at:2015-03-09
     */
    var deferred = $.Deferred();
    getUserInfo().done(function (userInfo) {
        if (userInfo) {
            setName(userInfo);
        }
        deferred.resolve();
    });
    return deferred.promise();
});
initQueue.push(function () {
    /**
     * 初始化队列
     by: 范俊伟 at:2015-03-09
     当前项目显示修改
     by: 范俊伟 at:2015-03-18
     */
    var deferred = $.Deferred();
    if (window.project_id) {
        getProjectInfo().done(function (projectInfo) {
            $("#project_name").text(projectInfo.name);
            $('#project_dropdown_menu').show();
            deferred.resolve();
        });

    }
    else {
        $('#project_dropdown_menu').hide();
        $("#project_name").empty();
        deferred.resolve();
    }

    return deferred.promise();
});
initQueue.push(function () {
    /**
     * 初始化队列
     by: 范俊伟 at:2015-03-09
     */
    var deferred = $.Deferred();

    if (window.project_id) {
        getAllUser(function () {
            deferred.resolve();
        });
    }
    else {
        deferred.resolve();
    }
    return deferred.promise();
});
initQueue.push(function () {
    /**
     * 初始化队列
     by: 范俊伟 at:2015-03-09
     */
    return getCurrentProjectUserGroups();
});
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

$(function () {
    /**
     * 登陆后默认进入所有项目
     by: 范俊伟 at:2015-03-08
     */
    openView('all_project');
});