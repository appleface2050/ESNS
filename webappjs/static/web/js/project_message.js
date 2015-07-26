/**
 * Date: 15/2/28
 * Time: 18:24
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var project_message_date_array = [];
function init_view_project_message() {
    /**
     * 初始化系统消息
     by: 范俊伟 at:2015-02-28
     * @type {Array}
     */
    showBrowserProjectMessage();

}

function showBrowserProjectMessage() {
    /**
     * 显示项目消息列表
     by: 范俊伟 at:2015-03-01
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * @type {Array}
     */
    project_message_date_array = [];

    templateRender('web/mst/project_message_view.mst', {}, function (rendered) {
        console.log('showBrowserProjectMessage', rendered);
        $('#view_content').html(rendered);

        getGroupByType('sys_xmjl').done(function (group) {
            getProjectMessageDateList(group.id);
        });

    });

}

function getProjectMessageDateList(group_id) {
    /**
     * 获取项目消息
     by: 范俊伟 at:2015-03-01
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/query_project_message_old';
    var data = {group_id: group_id};
    if (project_message_date_array.length > 0) {
        data['timeline'] = project_message_date_array[project_message_date_array.length - 1].timeline;
    }
    httpRequest(url, data).then(function (data) {
        window.viewDTD.resolve();
        if (data.result && data.result.length > 0) {
            console.log('getProjectMessageDateList', data.result);
            project_message_date_array = project_message_date_array.concat(data.result);//数组合并
            appendProjectMessageDateList(data);
            setTimeout(function () {
                getProjectMessageDateList(group_id);
            }, 0);
        }
        else if (project_message_date_array.length == 0) {
            var html = '<div class="well">暂无消息</div>';
            $('#project_message_content').html(html);
        }
    }, function (err) {
        window.viewDTD.resolve();
    });
}

function appendProjectMessageDateList(data) {
    /**
     * 显示项目消息
     by: 范俊伟 at:2015-03-01
     */
    templateRender('web/mst/project_message_dataitem.mst', data, function (rendered) {
        $('#project_message_content').append(rendered);
    });
}

function showCreateProjectMessage() {
    /**
     * 显示创建项目消息界面
     * by:范俊伟 at:2015-01-30
     */
    templateRender('web/mst/project_message_create.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        initForm();
    });
}

function createProjectMessageButtonClick() {
    /**
     * 提交创建项目消息
     * by:范俊伟 at:2015-02-07
     * @type {string}
     */
    getGroupByType('sys_xmjl').done(function (group) {
        var url = '/ns/' + window.project_id + '/create_project_message';
        $('#group_id').val(group.id);
        var form = $('#create_project_message_form');
        form.attr('action', url);
        form.submit();
    });

}

function createProjectMessageFormCallback(data) {
    /**
     * 创建项目消息表单提交回调函数
     * by:范俊伟 at:2015-03-01
     */
    if (data.success) {
        confirmBox.showConfirm('完成', '新建成功', '确定', '', function () {
            showBrowserProjectMessage();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }

}
