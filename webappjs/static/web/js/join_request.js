/**
 * Date: 15/02/03
 * Time: 21:19
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
joinRequestList = [];
function getJoinRequest(address, key) {
    /**
     * 查询所有项目
     * by:范俊伟 at:2015-02-03
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    $('#table_data').empty();
    var url = '/ns/' + window.project_id + '/get_all_applyproject';
    httpRequest(url).then(function (data) {
        window.viewDTD.resolve();
        if (data) {
            if (data.result && data.result.length > 0) {
                joinRequestList = data.result;
                templateRender('web/mst/join_request_table.mst', data, function (rendered) {
                    $('#table_data').append(rendered);
                });
            }
        }
    }, function () {
        window.viewDTD.resolve();
    });
}
function reject_join(apply_id) {
    /**
     * 拒绝加入
     * by:范俊伟 at:2015-02-10
     */
    do_join_request(apply_id, 'false');
}

function joinRequestShowSelectGroup(apply_id) {
    /**
     * 显示选择组对话框
     * by:范俊伟 at:2015-02-09
     */
    getCurrentProjectUserGroups(function (groups) {
        var html = $('<select id="manage_select_user_group">');
        for (var i = 0; i < groups.length; i++) {
            var group = groups[i];
            if (group.type != 'root') {
                var option = $('<option>');
                option.val(group.id);
                option.text(group.name);
                html.append(option);
            }

        }
        confirmBox.showConfirm('接受请求', html, '确定', '取消', function () {
            var group_id = $('#manage_select_user_group  option:selected').val();
            do_join_request(apply_id, 'true', group_id);
        }, null);
    });

}


function do_join_request(apply_id, do_arg, group_id) {
    /**
     * 处理加入请求
     * by:范俊伟 at:2015-02-03
     * 兼容IE
     * by:范俊伟 at:2015-02-07
     * 加入后清空相关全局变量
     by: 范俊伟 at:2015-03-10
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/change_applyproject';
    var data = {};
    data['apply_id'] = apply_id;
    data['do'] = do_arg;
    if (group_id) {
        data['group_id'] = group_id;
    }
    httpRequest(url, data).done(function (data) {
        window.project_all_user = undefined;
        window.userGroup = undefined;
        $.simplyToast('处理成功', 'success');
        getJoinRequest();
    });
}

function init_view_join_request() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * @type {*|jQuery}
     */

    templateRender('web/mst/join_request_view.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        getJoinRequest();
    });
}