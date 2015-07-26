/**
 * Date: 15/1/30
 * Time: 17:18
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */


var logapp_date_array = [];
var logapp_date_array_reset = false;
var current_logapp_date = null;


function showLogApp() {
    /**
     * 显示工程日志总框架
     * by:范俊伟 at:2015-01-30
     */

    templateRender('web/mst/application_log.mst', {}, function (rendered) {
        $('#app_content').html(rendered);
        logapp_date_array = [];
        showLogAppDateList();
    });
}

function showLogAppDateList() {
    /**
     * 显示日志天气列表
     * by:范俊伟 at:2015-01-30
     * 该天无记录不显示该日期
     by: 范俊伟 at:2015-03-12
     */
    $('#log_content').empty();
    if (logapp_date_array_reset) {
        logapp_date_array = [];
        logapp_date_array_reset = false;
    }
    if (logapp_date_array.length > 0) {
        init_data = {result: logapp_date_array};
        appendLogAppDateList(init_data);
    }
    getLogAppDateList();
}


function getLogAppDateList() {
    /**
     * 获取日志天气列表
     * by:范俊伟 at:2015-01-30
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_log_date_list_old';
    var data = {};
    if (logapp_date_array.length > 0) {
        data['timeline'] = logapp_date_array[logapp_date_array.length - 1].timeline;
    }
    httpRequest(url, data).done(function (data) {
        if (data.result && data.result.length > 0) {
            logapp_date_array = logapp_date_array.concat(data.result);//数组合并
            appendLogAppDateList(data);
            setTimeout(getLogAppDateList, 0);
        }
    });
}

function appendLogAppDateList(data) {
    /**
     * 填充日志天气列表
     * by:范俊伟 at:2015-01-30
     */
    templateRender('web/mst/application_log_date_dataitem.mst', data, function (rendered) {
        $('#log_content').append(rendered);
    });
}


function showLogAppOneDay(id) {
    /**
     * 显示某一天的日志
     * by:范俊伟 at:2015-01-30
     */
    for (var i = 0; i < logapp_date_array.length; i++) {
        var date = logapp_date_array[i];
        if (date.id == id) {
            current_logapp_date = date;
            $('#log_content').empty();
            getLogAppOneDayList();
            break;
        }
    }

}


function getLogAppOneDayList() {
    /**
     * 获取某一天的日志列表
     * by:范俊伟 at:2015-01-30
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/query_log_list_by_date';
    var data = {
        sg_tq_id: current_logapp_date.id
    };
    httpRequest(url, data).done(function (data) {
        console.log('getLogAppOneDayList', data.result);
        current_logapp_date.result = data.result;
        appendLogAppOneDayList(current_logapp_date);
    });

}
var template_delete_log = function () {
    /**
     * 模板所需函数,删除日志按钮显示控制
     * by:范俊伟 at:2015-02-10
     * 修改日期转换函数
     by: 范俊伟 at:2015-03-13
     * @type {user|*|Strophe.Handler.user|Strophe.TimedHandler.user}
     */
    var create_user_id = this.user;
    var create_date = Date.CreateDateTime(this.create_time);
    var now = new Date();
    var log_id = this.id;
    var diff = now.getTime() - create_date.getTime();
    var tiemout = 1000 * 60 * 60 * 24;

    if (create_user_id == uid && diff < tiemout) {
        return '<button type="button" onclick="deleteLogById(\'' + log_id + '\')" class="btn btn-danger">删除</button>';
    }


};
function appendLogAppOneDayList(data) {
    /**
     * 填充日志某一天的日志
     * by:范俊伟 at:2015-01-30
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    if (window.projectInfo.city) {
        data.city_name = window.projectInfo.city.province_name + ' ' + window.projectInfo.city.city_name;
    }
    data.template_delete_log = template_delete_log;
    templateRender('web/mst/application_log_one_day.mst', data, function (rendered) {
        $('#log_content').html(rendered);
    });
}
function deleteLogById(id) {
    /**
     * 删除日志
     * by:范俊伟 at:2015-02-10
     * 该天无记录不显示该日期
     by: 范俊伟 at:2015-03-12
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + window.project_id + '/del_log_by_id';
    var data = {};
    data['id'] = id;
    httpRequest(url, data).done(function (data) {
        logapp_date_array_reset = true;
        $.simplyToast('删除成功', 'success');
        var num = current_logapp_date.num;
        if (num > 0) {
            num = num - 1;
        }
        current_logapp_date.num = num;
        //if (num <= 0) {
        //    showLogAppDateList();
        //}
        //else {
        //    showLogAppOneDay(current_logapp_date.id);
        //}
        showLogAppOneDay(current_logapp_date.id);
    });
}
function showCreateLogApp() {
    /**
     * 显示创建日志界面
     * by:范俊伟 at:2015-01-30
     * 创建时就显示天气
     by: 范俊伟 at:2015-03-10
     */
    getProjectInfo().then(function (project_info) {
        var data = {};
        if (project_info.address && project_info.address != '0') {
            data['address'] = project_info.address;
        }
        return data;
    }).then(function (address_data) {
        return getTodayWeather(address_data);
    }).done(function (data) {
        templateRender('web/mst/application_create_logapp.mst', data, function (rendered) {
            $('#app_content').html(rendered);
            initForm();
        });
    });

}

function submitCreateLogAppForm() {
    /**
     * 提交日志
     * by:范俊伟 at:2015-02-07
     * @type {string}
     */

}

function getTodayWeather(data) {
    /**
     * 获取当天天气
     by: 范俊伟 at:2015-03-10
     */
    var dtd = $.Deferred();
    httpRequest('/ns/get_today_weather', data).then(function (data) {
        console.log('get_today_weather', data.result);
        var weather = data.result.weather;
        var wind = data.result.WS;
        var qiwen = null;
        if (data.result.temp1 && data.result.temp2) {
            qiwen = data.result.temp1 + '-' + data.result.temp2;
        }
        else if (data.result.l_tmp && data.result.h_tmp) {
            qiwen = data.result.l_tmp + '-' + data.result.h_tmp;
        }
        console.log(weather, wind, qiwen);
        var weather_data = {};
        weather_data.weather = weather;
        weather_data.wind = wind;
        weather_data.qiwen = qiwen;
        dtd.resolve(weather_data);

    }, function (error) {
        dtd.reject(error);
    });
    return dtd.promise();
}

function createLogAppButtonClick() {
    /**
     * 创建日志保存按钮点击事件
     * by:范俊伟 at:2015-01-30
     * 获取天气数据
     * by:范俊伟 at:2015-02-07
     * @type {string}
     * 兼容百度天气接口
     by: 范俊伟 at:2015-02-26
     逻辑修改
     by: 范俊伟 at:2015-03-10
     */
    var url = '/ns/' + window.project_id + '/update_log_by_date';
    var form = $('#create_log_app_form');
    form.attr('action', url);
    form.submit();
}

function createLogAppFormCallback(data) {
    /**
     * 创建日志表单提交回调函数
     * by:范俊伟 at:2015-01-30
     */
    if (data.success) {
        confirmBox.showConfirm('完成', '新建成功', '确定', '', function () {
            showLogApp();
        }, null);
    }
    else {
        $('#form_error').text(data.message);
    }

}