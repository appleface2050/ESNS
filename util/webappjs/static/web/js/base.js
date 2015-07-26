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

    $("html,body").animate({scrollTop: 0}, 200);//平滑滚动到顶部 by:范俊伟 at:2015-01-21
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


function initMaxLengthTooltips(selector) {
    /**
     * 最大字符实时提示
     * @type {*|jQuery|HTMLElement}
     */
        //console.log(selector);
        //selector.each(function () {
        //    /**
        //     * 创建提示div
        //     */
        //
        //
        //});

    selector.unbind('keyup').keyup(function () {
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

    selector.unbind('blur').blur(function () {
        /**
         * 失去焦点隐藏
         */
        if (this.maxlengthTooltip) {
            this.maxlengthTooltip.hide();
        }
    });
    selector.unbind('focus').focus(function () {
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
}

function initForm() {
    /**
     * 对标记有ajax属性的form绑定通用提交事件,对所有input绑定通用校验事件
     * by:范俊伟 at:2015-01-21
     * 增加错误状态码的全局处理
     * by:范俊伟 at:2015-01-21
     * 表单检查失败后,平滑滚动到顶部,以便查看错误信息
     * by:范俊伟 at:2015-01-21
     * 初始化textarea的最大字符提示
     by: 范俊伟 at:2015-03-13
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

    $('input').each(function () {
        var input_check = $(this).attr('input-check');
        var id = $(this).attr('id');
        if (input_check) {
            $(this).unbind('blur').blur(function () {
                checkField(id);
            });
        }
    });
    initMaxLengthTooltips($('textarea'));
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
/**
 * 添加初始化函数
 * by:范俊伟 at:2015-01-21
 */
initQueue.push(initDateTimePicker);
initQueue.push(initForm);
initQueue.push(initCity);

function initPage() {
    /**
     * 页面初始化全局函数,通过调用初始化队列中的函数完成页面初始化
     * by:范俊伟 at:2015-01-21
     * promise化
     * by: 范俊伟 at:2015-03-09
     */
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

$(function () {
    /**
     * 页面载入完成后执行
     * by:范俊伟 at:2015-01-21
     * 逻辑修改
     by: 范俊伟 at:2015-03-10
     */
    if (!window.onFrame) {
        initPage();
    }
});