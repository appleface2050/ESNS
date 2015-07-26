/**
 * Date: 15/1/30
 * Time: 21:45
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */


var gysaddress_array = [];


function showGysaddress() {
    /**
     * 显示供应名录商总框架
     * by:范俊伟 at:2015-01-30
     */

    templateRender('web/mst/application_gysaddress.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        gysaddress_array = [];
        showGysaddressList();
    });
}

function showGysaddressList() {
    /**
     * 显示供应商名录数据列表
     * by:范俊伟 at:2015-01-30
     */
    $('#table_data').empty();
    if (gysaddress_array.length > 0) {
        init_data = {result: gysaddress_array};
        appendGysaddressList(init_data);
    }
    getGysaddressList();
}


function getGysaddressList() {
    /**
     * 获取供应商名录数据
     * by:范俊伟 at:2015-01-30
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_gysaddress_by_group_old';
    var data = {flag: current_app_group.flag};
    if (gysaddress_array.length > 0) {
        data['timeline'] = gysaddress_array[gysaddress_array.length - 1].timeline;
    }
    httpRequest(url, data).done(function (data) {
        if (data.result && data.result.length > 0) {
            gysaddress_array = gysaddress_array.concat(data.result);//数组合并
            appendGysaddressList(data);
            setTimeout(getGysaddressList, 0);
        }
    });
}

function appendGysaddressList(data) {
    /**
     * 填充供应商名录列表
     * by:范俊伟 at:2015-01-30
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    templateRender('web/mst/application_gysaddress_dataitem.mst', data, function (rendered) {
        $('#table_data').append(rendered);
    });
}

function showGysaddressInfo(id) {
    /**
     * 显示供应商名录信息
     * by:范俊伟 at:2015-01-30
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    for (var i = 0; i < gysaddress_array.length; i++) {
        var gys = gysaddress_array[i];
        if (gys.id == id) {
            templateRender('web/mst/gysaddress_info.mst', gys, function (rendered) {
                messageBox.showMessage('供应商名录详细信息', rendered);
            });
        }
    }

}

function showSaveGysaddress(id) {
    /**
     * 显示创建日志界面
     * by:范俊伟 at:2015-01-30
     */
    var data = {};
    if (id != null && id != undefined) {
        for (var i = 0; i < gysaddress_array.length; i++) {
            var gys = gysaddress_array[i];
            if (gys.id == id) {
                data = gys;
            }
        }
    }
    data['flag'] = current_app_group.flag;
    templateRender('web/mst/application_create_gysaddress.mst', data, function (rendered) {
        $('#app_content').html(rendered);
        initForm();
    });
}

function createGysaddressButtonClick() {
    /**
     * 创建日志保存按钮点击事件
     * by:范俊伟 at:2015-01-30
     * @type {string}
     */
    var url = '/ns/' + window.project_id + '/create_gysaddress_by_group';
    var form = $('#gysaddress_form');
    form.attr('action', url);
    form.submit();
}

function createGysaddressFormCallback(data) {
    /**
     * 创建日志表单提交回调函数
     * by:范俊伟 at:2015-01-30
     */
    if (data.success) {
        confirmBox.showConfirm('完成', '保存成功', '确定', '', function () {
            showGysaddress();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }

}