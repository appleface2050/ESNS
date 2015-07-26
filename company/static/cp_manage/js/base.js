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
     * 500错误不弹框
     by: 范俊伟 at:2015-06-12
     */
    console.error(xhr, err, ex);
    var err_msg = [];
    err_msg.push('系统内部错误,请稍后重试或联系管理员');
    err_msg.push(xhr.status);
    err_msg.push(err);
    err_msg.push(ex);
};

var ajaxErrorNotShowMessage = function (xhr, err, ex) {
    /**
     * ajax通用错误处理函数,只输出log
     * by:范俊伟 at:2015-01-29
     */
    console.error(xhr, err, ex);
};
function findInputGroup(input) {
    /**
     * 查找输入分组
     by: 范俊伟 at:2015-06-10
     */
    while (input.parent().length > 0) {
        var parent = input.parent();
        if (parent.is('[input-group]')) {
            return parent;
        }
        else {
            input = parent;
        }
    }
}
function checkField(input) {
    /**
     * 通用input校验函数
     * by:范俊伟 at:2015-01-21
     * email校验
     * by:范俊伟 at:2015-02-06
     * 身份证号校验
     * by:范俊伟 at:2015-02-06
     * 修改校验
     by: 范俊伟 at:2015-06-10
     * @type {*|jQuery|HTMLElement}
     */
    var input_errors;
    var input_check_attr = input.attr('input-check');
    var errors = [];
    var input_group = findInputGroup(input);
    if (input_group) {
        input_errors = input_group.find("[input-errors]");
    }
    else {
        input_errors = input.parent().find("[input-errors]");
    }

    if (input_errors.length <= 0) {
        var width = input.width();
        var position = input.position();
        if (position) {
            input_errors = $('<div></div>');
            input_errors.attr("input-errors", "");
            input_errors.addClass("error_tip");
            input_errors.css('top', position.top + 1);
            input_errors.css('left', position.left + width - 50);
            input.after(input_errors);
        }
    }
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
                    if (isNaN(value)) {
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
        if (input_errors) {
            input_errors.show();
            input_errors.html(errors.join());
            if (input_errors.is('.error_tip')) {
                var input_width = input.width();
                var error_width = input_errors.width();
                var input_position = input.position();
                console.log(input_width);
                console.log(error_width);
                input_errors.css('left', input_position.left + input_width - error_width - 3);
            }


        }
        return errors.join(',');
    }
    else {
        if (input_group)
            input_group.removeClass("has-error");
        if (input_errors) {
            input_errors.html("");
            input_errors.hide();
        }
        return null;
    }


}

function checkForm(form) {
    /**
     * 在提交前调用此函数,遍历该form的所有input
     * by:范俊伟 at:2015-01-21
     * 逻辑修改
     by: 范俊伟 at:2015-06-10
     * @type {boolean}
     */
    var check = true;
    form.find('input').each(function () {
        var error = checkField($(this));
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

function initDateTimePicker() {
    /**
     * 初始化时间日期控件
     * by:范俊伟 at:2015-01-21
     * 修改时间日期控件
     by: 范俊伟 at:2015-07-01
     日期控件修改为中文
     by: 范俊伟 at:2015-07-01
     */
    $('[role=timepicker]').timepicker({
        minuteStep: 1,
        showSeconds: true,
        showMeridian: false
    }).next().on(ace.click_event, function () {
        $(this).prev().focus();
    });

    $('[role=datepicker]').datepicker({autoclose: true,language: 'cn'}).next().on(ace.click_event, function () {
        $(this).prev().focus();
    });
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
     * 显示成功信息
     by: 范俊伟 at:2015-04-23
     不显示成功信息
     by: 范俊伟 at:2015-06-12
     */
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
function EJSTemplateRender(templatePath, data) {
    /**
     * 通用js模板渲染
     * templatePath:模板路径,相对于static_url
     * data:模板数据
     * cb:回调函数
     * by:范俊伟 at:2015-01-22
     * template_option在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * 测试时，忽略缓存
     * by:王健 at:2015-06-17
     */
    console.log('EJSTemplateRender');
    var defer = $.Deferred();
    if (window.ejsTemplateCache === undefined || is_debug) {
        window.ejsTemplateCache = {};
    }
    if (window.ejsTemplateCache[templatePath]) {
        var rendered = window.ejsTemplateCache[templatePath].render(data);
        defer.resolve(rendered);
    }
    else {
        var url = staticUrl + templatePath;
        if (is_debug) {
            url = url + "?t=" + Math.random();
        }
        $.ajax({
            url: url,
            type: 'get',
            success: function (ejsStr) {
                var template = new EJS({text: ejsStr});
                window.ejsTemplateCache[templatePath] = template;
                var rendered = template.render(data);
                defer.resolve(rendered);
            },
            error: function (xhr, err, ex) {
                console.error(xhr, err, ex);
                defer.resolve(null);
            }
        });
    }
    return defer.promise();
}


window.initMaxLengthTooltips = function () {
    /**
     * 最大字符实时提示
     * 事件绑定
     by: 范俊伟 at:2015-06-11
     * @type {*|jQuery|HTMLElement}
     */
    var selector = 'textarea[maxlength]';
    $(document).on('keyup', selector, function () {
        /**
         * 按键弹起执行
         * @type {*|jQuery|HTMLElement}
         */
        var self = $(this);
        var maxlength = self.attr('maxlength');
        var text = self.val().length + '/' + maxlength;

        if (this.maxlengthTooltip) {
            var div_div_2 = this.maxlengthTooltip.find('.tooltip-inner').text(text);
        }
    });

    $(document).on('blur', selector, function () {
        /**
         * 失去焦点隐藏
         */
        if (this.maxlengthTooltip) {
            this.maxlengthTooltip.hide();
        }
    });
    $(document).on('focus', selector, function () {
        /**
         * 获得焦点显示
         */
        if (!this.maxlengthTooltip) {
            var self = $(this);
            var width = self.width();
            var position = self.position();
            var div = $('<div></div>');
            div.attr('class', 'tooltip fade top in');
            div.attr('role', 'tooltip');
            div.attr('style', 'display: none;');
            div.css('top', position.top - 32);
            div.css('left', width / 2 + "px");
            var div_div_1 = $('<div></div>');
            div_div_1.attr('class', 'tooltip-arrow');
            div_div_1.attr('style', 'left: 50%;');
            var div_div_2 = $('<div></div>');
            div_div_2.attr('class', 'tooltip-inner');
            var maxlength = self.attr('maxlength');
            var text = self.val().length + '/' + maxlength;
            div_div_2.text(text);
            div.append(div_div_1);
            div.append(div_div_2);
            self.after(div);
            this.maxlengthTooltip = div;
        }
        if (this.maxlengthTooltip) {
            this.maxlengthTooltip.show();
        }
    });
    window.initMaxLengthTooltips = function () {
    };
};

window.initForm = function () {
    /**
     * 对标记有ajax属性的form绑定通用提交事件,对所有input绑定通用校验事件
     * by:范俊伟 at:2015-01-21
     * 增加错误状态码的全局处理
     * by:范俊伟 at:2015-01-21
     * 表单检查失败后,平滑滚动到顶部,以便查看错误信息
     * by:范俊伟 at:2015-01-21
     * 初始化textarea的最大字符提示
     by: 范俊伟 at:2015-03-13
     修改form提交方式
     by: 范俊伟 at:2015-04-23
     兼容模式
     by: 范俊伟 at:2015-04-23
     逻辑修改
     by: 范俊伟 at:2015-06-10
     * 事件绑定
     by: 范俊伟 at:2015-06-11
     */
    $(document).on('submit', 'form[ajax_old]', function () {
        var form = $(this);
        var url = form.attr('action');
        var callback = form.attr('callback');
        if (!callback) {
            return;
        }
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
    $(document).on('submit', 'form[ajax]', function () {
            var form = $(this);
            var callback = form.attr('callback');
            if (!callback) {
                return false;
            }
            if (checkForm(form)) {
                try {
                    eval(callback + '(form);');
                }
                catch (e) {
                    console.error(e.stack);
                }
            }
            else {
                onFormCheckError();
            }
            return false;
        }
    );
    $(document).on('submit', 'form[auto-check]', function () {
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
    $(document).on('blur', 'input[input-check]', function () {
        checkField($(this));
    });
    initMaxLengthTooltips();
    window.initForm = function () {
    };
};
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
/**
 * 添加初始化函数
 * by:范俊伟 at:2015-01-21
 */
//initQueue.push(initDateTimePicker);
initQueue.push(initCity);

function initPage() {
    /**
     * 页面初始化全局函数,通过调用初始化队列中的函数完成页面初始化
     * by:范俊伟 at:2015-01-21
     * promise化
     * by: 范俊伟 at:2015-03-09
     */
    console.log("initPage");
    var defer = $.Deferred();
    defer.resolve();
    var promise = defer.promise();
    console.log('all fun', initQueue.length);
    var factory = function (func, index) {
        return function () {
            try {
                console.log('run func', index);
                return func();
            }
            catch (e) {
                console.error(e);
            }
        };

    };
    for (var i = 0; i < initQueue.length; i++) {
        promise = promise.then(factory(initQueue[i], i));
    }
    return promise;
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

var showErrorMessage = function (data) {
    /**
     * 通用错误信息显示
     * by:范俊伟 at:2015-01-22
     * 判断在有message的情况下再提示错误信息
     by: 范俊伟 at:2015-03-08
     修改meessageBox调用
     by: 范俊伟 at:2015-06-12
     */
    if (!data.success) {
        if (data.message) {
            if (data.dialog == 0) {
                $.simplyToast(data.message, 'danger');
            }
            else {
                showMessage('错误', data.message);
            }
        }
    }


};

function httpRequest(url, data, method, notShowErrorMessage, notShowServerError) {
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
            if (globalStateCheck(data)) {
                if (notShowErrorMessage) {
                    dtd.resolve(data);
                }
                else {
                    if (data.success) {
                        dtd.resolve(data);
                    }
                    else {
                        showErrorMessage(data);
                        dtd.reject(null, data);
                    }
                }
            }
            else {
                dtd.reject(null, data);
            }
        },
        function (xhr, err, ex) {
            if (notShowServerError) {
                ajaxErrorNotShowMessage(xhr, err, ex);
            }
            else {
                ajaxError(xhr, err, ex);
            }
            dtd.reject(ex, err, xhr);
        }
    );
    return dtd.promise();
}
function format_int_money(content) {
    if (content != '') {
        content = parseFloat(content) / 100;
        return $.formatMoney(content);
    }
    else {
        return '';
    }
}

function int_money_value(content) {
    if (content != '') {
        content = parseFloat(content) / 100;
        return content;
    }
    else {
        return '';
    }
}
Date.CreateDateTime = function (s) {
    /**
     * 日期转换函数,以兼容IE
     by: 范俊伟 at:2015-03-13
     * @type {Array|{index: number, input: string}|*}
     */
    var strInfo = s.match(/\d+/g);
    var d = new Date(), r = [d.getFullYear(), d.getMonth() + 1, d.getDate(), 0, 0, 0];

    for (var i = 0; i < 6 && i < strInfo.length; i++)
        r[i] = strInfo[i].length > 0 ? strInfo[i] : r[i];
    return new Date(r[0], r[1] - 1, r[2], r[3], r[4], r[5]);
};
function tableSelectAll() {
    /**
     * 表格全选功能
     by: 范俊伟 at:2015-06-11
     */
    $(document).on('click', 'table th input[select_all]:checkbox', function () {
        var that = this;
        $(this).closest('table').find('tr > td:first-child input[select_all]:checkbox')
            .each(function () {
                this.checked = that.checked;
                $(this).closest('tr').toggleClass('selected');
            });

    });
}
function showMessage(title, message) {
    /**
     *meessageBox
     by: 范俊伟 at:2015-06-12
     */
    bootbox.dialog({
        title: title,
        message: message,
        buttons: {
            "button": {
                "label": "确定",
                "className": "btn-sm"
            }
        }
    });
}
$(function () {
    /**
     * 页面载入完成后执行
     * by:范俊伟 at:2015-01-21
     * 逻辑修改
     by: 范俊伟 at:2015-03-10
     逻辑修改
     by: 范俊伟 at:2015-04-23
     * 事件绑定
     by: 范俊伟 at:2015-06-11
     * 表格全选功能
     by: 范俊伟 at:2015-06-11
     */
    initPage();
    initForm();
    tableSelectAll();
});

