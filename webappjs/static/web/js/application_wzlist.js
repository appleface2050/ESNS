/**
 * Date: 15/1/30
 * Time: 17:18
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */


var wzlist_date_array = [];
var current_wzlist_date = null;
var wzlist_is_out = false;


function showWzlist() {
    /**
     * 显示物资框架
     * by:范俊伟 at:2015-01-31
     */
    if (current_app_group.typeflag == 'wuzioutlist') {
        wzlist_is_out = true;
    }
    else {
        wzlist_is_out = false;
    }
    templateRender('web/mst/application_wzlist.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        wzlist_date_array = [];
        showWzlistDateList();
    });
}

function showWzlistDateList() {
    /**
     * 显示物资日期列表
     * by:范俊伟 at:2015-01-31
     */
    $('#wzlist_content').empty();
    if (wzlist_date_array.length > 0) {
        init_data = {result: wzlist_date_array};
        appendWzlistDateList(init_data);
    }
    getWzlistDateList();
}


function getWzlistDateList() {
    /**
     * 获取物资日期列表
     * by:范俊伟 at:2015-01-31
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_record_date_by_group_old';
    var data = {flag: current_app_group.flag};
    if (wzlist_date_array.length > 0) {
        data['timeline'] = wzlist_date_array[wzlist_date_array.length - 1].timeline;
    }
    httpRequest(url, data).done(function (data) {
        if (data.result && data.result.length > 0) {
            wzlist_date_array = wzlist_date_array.concat(data.result);//数组合并
            appendWzlistDateList(data);
            setTimeout(getWzlistDateList, 0);
        }
    });
}

function appendWzlistDateList(data) {
    /**
     * 填充物资日期列表
     * by:范俊伟 at:2015-01-31
     */
    templateRender('web/mst/application_wzlist_date_dataitem.mst', data, function (rendered) {
        $('#wzlist_content').append(rendered);
    });
}


function showWzlistOneDay(id) {
    /**
     * 显示某一天的物资框架
     * by:范俊伟 at:2015-01-31
     */
    for (var i = 0; i < wzlist_date_array.length; i++) {
        var date = wzlist_date_array[i];
        if (date.id == id) {
            current_wzlist_date = date;
            $('#wzlist_content').empty();
            getWzlistOneDayList();
            break;
        }
    }
}

function getWzlistOneDayList() {
    /**
     * 获取某一天的物资列表
     * by:范俊伟 at:2015-01-31
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_wuzirecord_by_group';
    var data = {
        record_date_id: current_wzlist_date.id,
        flag: current_app_group.flag
    };
    httpRequest(url, data).done(function (data) {
        current_wzlist_date.result = data.result;
        appendWzlistOneDayList(current_wzlist_date);
    });
}

function appendWzlistOneDayList(data) {
    /**
     * 填充某一天的物资
     * by:范俊伟 at:2015-01-31
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    data['wzlist_is_out'] = wzlist_is_out;
    templateRender('web/mst/application_wzlist_one_day.mst', data, function (rendered) {
        $('#wzlist_content').html(rendered);
    });
}

function saveCreateWzlist(id) {
    /**
     * 显示创建物资界面
     * by:范俊伟 at:2015-01-31
     */
    var data = {};

    if (id != null && id != undefined) {
        var array = current_wzlist_date.result;
        for (var i = 0; i < array.length; i++) {
            var wz = array[i];
            if (wz.id == id) {
                data = wz;
            }
        }
    }
    data['flag'] = current_app_group.flag;
    data['wzlist_is_out'] = wzlist_is_out;
    templateRender('web/mst/application_create_wzlist.mst', data, function (rendered) {
        $('#app_content').html(rendered);
        initForm();
    });
}

function createWzlistButtonClick() {
    /**
     * 创建物资保存按钮点击事件
     * by:范俊伟 at:2015-01-31
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/create_wuzirecord_by_group';
    var form = $('#create_wzlist_form');
    form.attr('action', url);
    form.submit();
}

function createWzlistFormCallback(data) {
    /**
     * 创建物资表单提交回调函数
     * by:范俊伟 at:2015-01-31
     */
    if (data.success) {
        confirmBox.showConfirm('完成', '保存成功', '确定', '', function () {
            showWzlist();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }

}