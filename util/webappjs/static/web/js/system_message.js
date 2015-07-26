/**
 * Date: 15/2/28
 * Time: 18:24
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var system_message_date_array = [];
function init_view_system_message() {
    /**
     * 初始化系统消息
     by: 范俊伟 at:2015-02-28
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * @type {Array}
     */
    system_message_date_array = [];
    var html = '<div id="system_message_content"></div>';
    $('#view_content').html(html);

    getSystemMessageDateList();
}

function getSystemMessageDateList() {
    /**
     * 获取系统消息
     by: 范俊伟 at:2015-02-28
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/query_sysmessage_old';
    var data = {};
    if (system_message_date_array.length > 0) {
        data['timeline'] = system_message_date_array[system_message_date_array.length - 1].timeline;
    }
    httpRequest(url, data).then(function (data) {
        window.viewDTD.resolve();
        if (data) {
            if (data.result && data.result.length > 0) {
                console.log('getSystemMessageDateList', data.result);
                system_message_date_array = system_message_date_array.concat(data.result);//数组合并
                appendSystemMessageDateList(data);
                setTimeout(getSystemMessageDateList, 0);
            }
            else if (system_message_date_array.length == 0) {
                var html = '<div class="well">暂无消息</div>';
                $('#system_message_content').html(html);
            }
        }
    }, function () {
        window.viewDTD.resolve();
        var html = '<div class="well">暂无消息</div>';
        $('#system_message_content').html(html);
    });
}

function appendSystemMessageDateList(data) {
    /**
     * 显示系统消息
     by: 范俊伟 at:2015-02-28
     */
    templateRender('web/mst/system_message_dataitem.mst', data, function (rendered) {
        $('#system_message_content').append(rendered);
    });
}
