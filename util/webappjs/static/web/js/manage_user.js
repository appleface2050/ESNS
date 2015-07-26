/**
 * Date: 15/2/5
 * Time: 14:11
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */


function manageUserShowGroup() {
    /**
     * 显示分组列表
     * by:范俊伟 at:2015-02-09
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     */
    getUserGroupList(function (group_list) {
        templateRender('web/mst/manage_user_group.mst', {group_list: group_list}, function (rendered) {
            $('#view_content').html(rendered);
            window.viewDTD.resolve();
        });
    });
}
function manageShowSelectGroup(user_id) {
    /**
     * 显示选择组对话框
     * by:范俊伟 at:2015-02-09
     */
    getCurrentProjectUserGroups(function (groups) {
        var html = $('<select id="manage_select_user_group">');
        for (var i = 0; i < groups.length; i++) {
            var group = groups[i];
            if (group.type != 'root') {
                var option = $('<option>')
                option.val(group.id);
                option.text(group.name);
                html.append(option);
            }

        }
        confirmBox.showConfirm('分组管理', html, '确定', '取消', function () {
            var group_id = $('#manage_select_user_group  option:selected').val();
            manageChangeUserGroup(user_id, group_id, 'join');
        }, null);
    });

}
function manageConfirmDeleteFromGroup(user_id, group_id, name, group_name) {
    /**
     * 提示是否确认从组中删除
     * by:范俊伟 at:2015-02-09
     * @type {string}
     */
    var message = '是否确认将' + name + '从' + group_name + '中删除?';
    confirmBox.showConfirm('分组管理', message, '确定', '取消', function () {
        manageChangeUserGroup(user_id, group_id, 'out');
    }, null);
}
function manageChangeUserGroup(user_id, group_id, do_arg) {
    /**
     * 加入分组或从分组中移除
     * by:范俊伟 at:2015-02-09
     * 优化数据缓存
     by: 范俊伟 at:2015-03-10
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/change_user_group';
    var data = {
        user_id: user_id,
        group_id: group_id
    };
    data['do'] = do_arg;
    httpRequest(url, data).done(function (data) {
        window.userInfo = undefined;
        window.project_all_user = undefined;
        window.userGroup = undefined;
        $.simplyToast('操作成功', 'success');
        refreshView();
    });
}
function manageConfirmRemoveUserFromProject(user_id, name) {
    /**
     * 提示是否确认从组中删除
     * by:范俊伟 at:2015-02-09
     * @type {string}
     */
    var message = '是否确认将' + name + '从当前项目中移除?';
    confirmBox.showConfirm('成员管理', message, '确定', '取消', function () {
        manageRemoveUserFromProject(user_id);
    }, null);
}
function manageRemoveUserFromProject(user_id) {
    /**
     * 从项目中移除用户
     * by:范俊伟 at:2015-02-09
     * 优化数据缓存
     by: 范俊伟 at:2015-03-10
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/remove_person';
    var data = {
        user_id: user_id
    };
    httpRequest(url, data).done(function (data) {
        window.userInfo = undefined;
        window.project_all_user = undefined;
        window.userGroup = undefined;
        $.simplyToast('操作成功', 'success');
        refreshView();
    });
}

function show_add_person_by_tel_dial(group_id) {
    /**
     * 显示添加手机号对话框
     by: 范俊伟 at:2015-03-14
     */

    confirmBox.showConfirm('输入要添加的手机号', '<input type="text" maxlength="50" style="width:100%" id="person_tel"><div class="help-block">多个手机以逗号分隔</div>', '添加', '取消', function () {
        add_person_by_tel(group_id, $('#person_tel').val());
    }, null);
}


function add_person_by_tel(group_id, tel) {
    /**
     * 通过手机号添加用户
     by: 范俊伟 at:2015-03-14
     * @type {string}
     */

    var url = '/ns/' + window.project_id + '/add_person_by_tel';
    var data = {
        tel: tel,
        group_id: group_id
    };
    httpRequest(url, data).done(function (data) {
        console.log('add_person_by_tel ok', data);
        if (data) {
            $.simplyToast(data.message, 'success');
            refreshView();
        }
    });
}

function init_view_manage_user() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * @type {*|jQuery}
     */
    manageUserShowGroup();
}