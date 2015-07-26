/**
 * Created by fanjunwei on 14/11/23.
 */

/**
 * 兼容不支持console的浏览器,防止js调用出错
 * by:范俊伟 at:2015-01-21
 */
if (!window.console) console = {};
console.log = console.log || function () {
};
console.warn = console.warn || function () {
};
console.error = console.error || function () {
};
console.info = console.info || function () {
};
var showErrorMessage = function (data) {
    /**
     * 通用错误信息显示
     * by:范俊伟 at:2015-01-22
     */
    if (!data.success) {
        if (data.dialog == 0) {
            $.simplyToast(data.message, 'danger');
        }
        else {
            messageBox.showMessage('错误', data.message);
        }
    }


};
var hasPlaceholderSupport = function () {
    /**
     * 检测浏览器是否支持Placeholder功能
     * by:范俊伟 at:2015-01-21
     */
    var attr = "placeholder";
    var input = document.createElement("input");
    return attr in input;
};

var onFormCheckError = function () {
    /**
     * 表单检测失败后所调用的函数
     * by:范俊伟 at:2015-01-21
     * 定位到最上面的错误
     by: 范俊伟 at:2015-05-19
     修改定位位置
     by: 范俊伟 at:2015-05-19
     */
    var min = -1;
    $('[input-errors]').each(function () {
        var c = $(this);

        if (c.text()) {
            var top = c.offset().top;
            if (min < 0 || top < min) {
                min = top;
            }
        }
    });
    $("html,body").animate({scrollTop: min - 70}, 200);//平滑滚动到顶部 by:范俊伟 at:2015-01-21
};

var ajaxError = function (xhr, err, ex) {
    /**
     * ajax通用错误处理函数
     * by:范俊伟 at:2015-01-21
     * 采用错误输出函数
     * by: 范俊伟 at:2015-02-13
     */
    console.error(xhr, err, ex);
    var err_msg = [];
    err_msg.push('系统内部错误,请稍后重试或联系管理员');
    err_msg.push(xhr.status);
    err_msg.push(err);
    err_msg.push(ex);
    messageBox.showMessage('内部错误', err_msg.join('<br>'));
};

var ajaxErrorNotShowMessage = function (xhr, err, ex) {
    /**
     * ajax通用错误处理函数,只输出log
     * by:范俊伟 at:2015-01-29
     */
    console.error(xhr, err, ex);
};
function checkField(input) {
    /**
     * 通用input校验函数
     * by:范俊伟 at:2015-01-21
     * email校验
     * by:范俊伟 at:2015-02-06
     * 身份证号校验
     * by:范俊伟 at:2015-02-06
     * @type {*|jQuery|HTMLElement}
     */
    var field_id = null;
    if (input instanceof jQuery) {
        field_id = input.attr('id');
    }
    else {
        field_id = input;
        input = $('#' + field_id);
    }

    var input_check_attr = input.attr('input-check');
    var errors = [];
    var input_group = $('[input-group=' + field_id + "]");
    var input_errors = $('[input-errors=' + field_id + "]");
    if (input_check_attr) {
        var input_checks = input_check_attr.split(',');
        for (var i = 0; i < input_checks.length; i++) {
            var input_check = input_checks[i];
            var value = input.val();

            if (input_check == 'required') {
                if (!value) {
                    errors.push('不能为空');
                }
            }
            else if (input_check == 'number') {
                if (value) {
                    if (isNaN(parseInt(value, 10))) {
                        errors.push('请输入数字');
                    }
                }
            }
            else if (input_check == 'idcard') {
                if (value) {
                    if (!/(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(value)) {
                        errors.push('请输入正确的身份证号');
                    }
                }
            }
            else if (input_check == 'int') {
                if (value) {
                    if (!/^\d+$/.test(value)) {
                        errors.push('请输入整数');
                    }
                }
            } else if (input_check == 'email') {
                if (value) {
                    if (!/\w@\w*\.\w/.test(value)) {
                        errors.push('请输入正确的邮件地址');
                    }
                }
            }
            else if (input_check) {
                var e = eval(input_check);
                if (e) {
                    errors.push(e);
                }

            }
        }
    }
    if (errors.length > 0) {
        if (input_group)
            input_group.addClass("has-error");
        if (input_errors)
            input_errors.html(errors.join());
        return errors.join(',');
    }
    else {
        if (input_group)
            input_group.removeClass("has-error");
        if (input_errors)
            input_errors.html("");
        return null;
    }


}

function checkForm(form) {
    /**
     * 在提交前调用此函数,遍历该form的所有input
     * by:范俊伟 at:2015-01-21
     * @type {boolean}
     */
    var check = true;
    form.find('input').each(function () {
        var field_id = $(this).attr('id');
        var error = checkField(field_id);
        if (error) {
            check = false;
        }
    });
    form.find('textarea').each(function () {
        var error = checkField($(this));
        if (error) {
            check = false;
        }
    });
    return check;
}
/**
 * 初始化队列,保存页面初始化所需执行的函数,页面载入完成后依次执行
 * by:范俊伟 at:2015-01-21
 * @type {Array}
 */
var initQueue = [];

function initTooltip() {
    /**
     * 对于不支持Placeholder的浏览器使用tooltip方式显示
     * by:范俊伟 at:2015-01-21
     */
    if (!hasPlaceholderSupport()) {
        $('input').tooltip();
    }
}
function initDateTimePicker() {
    /**
     * 初始化时间日期控件
     * by:范俊伟 at:2015-01-21
     */
    $('[role=datetimepicker-date]').datetimepicker({
        format: 'yyyy-MM-dd',
        language: 'zh-CN',
        pickDate: true,
        pickTime: false,
        hourStep: 1,
        minuteStep: 15,
        secondStep: 30,
        inputMask: true
    });

    $('[role=datetimepicker-time]').datetimepicker({
        format: 'hh:mm:ss',
        language: 'zh-CN',
        pickDate: false,
        pickTime: true,
        hourStep: 1,
        minuteStep: 15,
        secondStep: 30,
        inputMask: true
    });
}
function addDjangoMessage(message, tag, cb) {
    /**
     * 向django的messages模块添加消息,跨页显示
     * by:范俊伟 at:2015-01-21
     */
    if (message && tag) {
        $.ajax({
            url: '/web/add_django_message',
            data: {message: message, tag: tag},
            type: 'post',
            success: function (data) {
                if (cb) {
                    cb(data);
                }
            },
            error: ajaxError
        });
    }

}
var createJifenMessage = function (data) {
    /**
     * 创建积分显示内容
     * by:范俊伟 at:2015-01-21
     */
    if (data.jifen_msg) {
        var html = '<div class="jifen"><span class="toast_jifen">/jifen/<span>/jifen_msg/</div>';
        return html.replace('/jifen/', data.jifen).replace('/jifen_msg/', data.jifen_msg);
    }
};
var displayJifenMessage = function (data) {
    /**
     * 显示积分信息,frame会重写此方法
     * by:范俊伟 at:2015-01-21
     */
};
function globalStateCheck(data) {
    /**
     * 全局错误状态码检测,返回true则继续进行其他处理
     * by:范俊伟 at:2015-01-21
     * 全局处理积分显示
     * by:范俊伟 at:2015-02-11
     */
    displayJifenMessage(data);
    if (data.status_code == 1) {
        window.location.href = loginUrl;
        return false;
    }
    else if (data.status_code == 9) {
        window.location.href = regTelUrl;
        return false;
    }
    return true;

}
function templateRender(templatePath, data, cb) {
    /**
     * 通用js模板渲染
     * templatePath:模板路径,相对于static_url
     * data:模板数据
     * cb:回调函数
     * by:范俊伟 at:2015-01-22
     * template_option在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     */
    if (data) {
        template_option(data);
    }
    if (window.templateCache === undefined) {
        window.templateCache = {};
    }
    if (window.templateCache[templatePath]) {
        var rendered = Mustache.render(window.templateCache[templatePath], data);
        cb(rendered);
    }
    else {
        var url = staticUrl + templatePath;
        if (is_debug) {
            url = url + "?t=" + Math.random();
        }
        $.ajax({
            url: url,
            type: 'get',
            success: function (template) {
                Mustache.parse(template);
                window.templateCache[templatePath] = template;
                var rendered = Mustache.render(template, data);
                cb(rendered);
            },
            error: ajaxError
        });
    }
}
function initForm() {
    /**
     * 对标记有ajax属性的form绑定通用提交事件,对所有input绑定通用校验事件
     * by:范俊伟 at:2015-01-21
     * 增加错误状态码的全局处理
     * by:范俊伟 at:2015-01-21
     * 表单检查失败后,平滑滚动到顶部,以便查看错误信息
     * by:范俊伟 at:2015-01-21
     * 非ajax提交表单校验
     * by: 范俊伟 at:2015-02-13
     */
    $('form[ajax]').unbind('submit').submit(function () {
        var form = $(this);
        var url = form.attr('action');
        var callback = form.attr('callback');
        if (checkForm(form)) {
            $.ajax({
                url: url,
                data: $(this).serialize(),
                type: $(this).attr('method'),
                success: function (data) {
                    if (globalStateCheck(data)) {
                        eval(callback + '(data)');
                    }

                },
                error: ajaxError
            });
        }
        else {
            onFormCheckError();
        }
        return false;
    });

    $('form[auto-check]').unbind('submit').submit(function () {
        var form = $(this);
        var url = form.attr('action');
        var callback = form.attr('callback');
        if (checkForm(form)) {
            return true;
        }
        else {
            onFormCheckError();
        }
        return false;
    });
    $('input').each(function () {
        var input_check = $(this).attr('input-check');
        var id = $(this).attr('id');
        if (input_check) {
            $(this).unbind('blur').blur(function () {
                checkField(id);
            });
        }
    });
}
function initCity() {
    /**
     * 初始化城市二级联动下拉列表
     * by:范俊伟 at:2015-02-02
     * @type {*|jQuery|HTMLElement}
     */
    $('[role=city_group]').each(
        function () {
            var select_province = $(this).find('[role=select_province]');
            var select_city = $(this).find('[role=select_city]');
            var default_city_id = $(this).attr('default');
            var empty_value = $(this).attr('empty');
            if (!empty_value) {
                empty_value = '所有';
            }
            var default_province_id = null;
            select_province.empty();
            var all = '<option value="0">' + empty_value + '</option>';
            select_province.append(all);
            select_city.append(all);
            if (default_city_id) {
                var default_city = getCityByID(default_city_id);
                if (default_city) {
                    default_province_id = default_city.province_id;
                }
                else {
                    default_city_id = null;
                }
            }
            select_city.hide();
            for (var i = 0; i < city_data.province_list.length; i++) {
                var province = city_data.province_list[i];
                var item = $('<option value="' + province.province_id + '">' + province.province_name + '</option>');
                if (default_province_id && default_province_id == province.province_id) {
                    item.attr('selected', 'selected');
                }
                select_province.append(item);
            }

            if (default_province_id && default_province_id != '' && default_province_id != '0') {
                select_city.show();
                select_city.empty();
                for (var i = 0; i < city_data.city_list.length; i++) {
                    var city = city_data.city_list[i];
                    if (city.province_id == default_province_id) {
                        var item = $('<option value="' + city.city_id + '">' + city.city_name + '</option>');
                        if (default_city_id && default_city_id == city.city_id) {
                            item.attr('selected', 'selected');
                        }
                        select_city.append(item);
                    }
                }
            }
            select_province.unbind('change').change(function () {
                var select_option = select_province.children('option:selected');
                var province_id = select_option.val();
                if (province_id == '0') {
                    select_city.hide();
                    select_city.empty();
                    select_city.append(all);

                }
                else {
                    select_city.show();
                    select_city.empty();
                    for (var i = 0; i < city_data.city_list.length; i++) {
                        var city = city_data.city_list[i];
                        if (city.province_id == province_id) {
                            var item = '<option value="' + city.city_id + '">' + city.city_name + '</option>';
                            select_city.append(item);
                        }
                    }
                }
            });


        }
    );

}

function httpRequest(url, data, method) {
    /**
     * 通用http请求函数
     by: 范俊伟 at:2015-03-10
     */
    if (method === undefined) {
        method = 'post';
    }
    var dtd = $.Deferred();
    $.ajax({
        url: url,
        data: data,
        type: method
    }).then(
        function (data) {
            if (data.success) {
                dtd.resolve(data);
            }
            else {
                dtd.reject(null, data);
            }
        },
        function (xhr, err, ex) {
            console.error(xhr, err, ex);
            dtd.reject(ex, err, xhr);
        }
    );
    return dtd.promise();
}

function initAddressV2() {
    /**
     * 初始化三级联动下拉列表
     * by:范俊伟 at:2015-02-02
     * @type {*|jQuery|HTMLElement}
     */
    console.log('initAddressV2');
    var empty_option = '<option value="0">请选择</option>';
    $('[role=address_group]').each(
        function () {

            var select_province = $(this).find('[role=select_province]');
            var select_city = $(this).find('[role=select_city]');
            var select_county = $(this).find('[role=select_county]');
            var default_county_id = $(this).attr('default');
            var default_city_id = null;
            var default_province_id = null;
            select_province.empty();
            select_province.append(empty_option);

            select_city.empty();
            select_city.append(empty_option);
            select_city.hide();

            select_county.empty();
            select_county.append(empty_option);
            select_county.hide();
            var dtd = $.Deferred();
            if (default_county_id) {
                httpRequest('/get_address_by_id', {id: default_county_id}).then(function (data) {
                    default_city_id = data.result.city_id;
                    default_province_id = data.result.province_id;
                    dtd.resolve();
                }, function () {
                    dtd.resolve();
                })
            }
            else {
                dtd.resolve();
            }

            dtd.promise().done(function () {
                httpRequest('/get_provinces').done(function (data) {
                    _(data.result).each(function (province) {
                        var option = $('<option></option>');
                        option.attr('value', province.id);
                        option.text(province.name);
                        if (default_province_id == province.id) {
                            option.attr('selected', 'selected');
                        }
                        select_province.append(option);
                    })
                });
                if (default_province_id) {
                    select_city.show();
                    httpRequest('/get_cities', {province_id: default_province_id}).done(function (data) {
                        _(data.result).each(function (city) {
                            var option = $('<option></option>');
                            option.attr('value', city.id);
                            option.text(city.name);
                            if (default_city_id == city.id) {
                                option.attr('selected', 'selected');
                            }
                            select_city.append(option);
                        })
                    });
                }

                if (default_city_id) {
                    select_county.show();
                    httpRequest('/get_counties', {city_id: default_city_id}).done(function (data) {
                        _(data.result).each(function (county) {
                            var option = $('<option></option>');
                            option.attr('value', county.id);
                            option.text(county.name);
                            if (default_county_id == county.id) {
                                option.attr('selected', 'selected');
                            }
                            select_county.append(option);
                        })
                    });
                }
            });

            select_province.unbind('change').change(function () {
                var select_option = select_province.children('option:selected');
                var province_id = select_option.val();
                if (province_id == '0') {
                    select_city.hide();
                    select_county.hide();

                    select_city.empty();
                    select_city.append(empty_option);
                    select_county.empty();
                    select_county.append(empty_option);
                }
                else {

                    httpRequest('/get_cities', {province_id: province_id}).done(function (data) {
                        if (data.result && data.result.length > 0) {
                            select_city.show();
                            select_county.hide();
                            select_city.empty();
                            select_city.append(empty_option);
                            select_county.empty();
                            select_county.append(empty_option);
                            _(data.result).each(function (city) {
                                var option = $('<option></option>');
                                option.attr('value', city.id);
                                option.text(city.name);
                                select_city.append(option);
                            })
                        }

                    });
                }
            });


            select_city.unbind('change').change(function () {
                var select_option = select_city.children('option:selected');
                var city_id = select_option.val();
                if (city_id == '0') {
                    select_county.hide();
                    select_county.empty();
                    select_county.append(empty_option);
                }
                else {
                    httpRequest('/get_counties', {city_id: city_id}).done(function (data) {
                        if (data.result && data.result.length > 0) {
                            select_county.show();
                            select_county.empty();
                            select_county.append(empty_option);
                            _(data.result).each(function (city) {
                                var option = $('<option></option>');
                                option.attr('value', city.id);
                                option.text(city.name);
                                select_county.append(option);
                            })
                        }

                    });
                }
            });

        }
    );

}
/**
 * 添加初始化函数
 * by:范俊伟 at:2015-01-21
 */
initQueue.push(initTooltip);
//initQueue.push(initDateTimePicker);
initQueue.push(initForm);
//initQueue.push(initCity);

function initPage() {
    /**
     * 页面初始化全局函数,通过调用初始化队列中的函数完成页面初始化
     * by:范俊伟 at:2015-01-21
     */
    for (i in initQueue) {
        try {
            initQueue[i]();
        }
        catch (e) {
            console.error(e);
        }

    }
}

function getCityByID(id) {
    /**
     * 根据城市ID获取城市信息
     * by:范俊伟 at:2015-01-31
     * @type {city_data.city_list|*}
     */
    var city_list = city_data.city_list;
    for (var i = 0; i < city_list.length; i++) {
        var city = city_list[i];
        if (city.city_id == id) {
            return city;
        }
    }
    return null;

}

function isIE() {
    /**
     * 判断是否为IE
     * by:范俊伟 at:2015-02-07
     */
    if (!+[1,]) {
        return true;
    }
    else {
        return false;
    }
}

$(function () {
    /**
     * 页面载入完成后执行
     * by:范俊伟 at:2015-01-21
     */
    initPage();
});