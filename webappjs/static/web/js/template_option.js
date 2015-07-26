/**
 * Date: 15/2/2
 * Time: 22:18
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var format_text_break_line = function () {
    return function (text, render) {
        /**
         * 模板所需函数,实现换行显示
         * by:范俊伟 at:2015-01-30
         */
        var content = render(text);
        content = content.replace(/\n/g, '<br/>');
        return content;
    };
};

var format_true_false = function () {
    return function (text, render) {
        /**
         * 模板所需函数,是否显示
         * by:范俊伟 at:2015-01-31
         */
        var content = render(text);
        if (content != '') {
            if (content == 'true') {
                return '是';
            }
            else {
                return '否';
            }
        }

    };
};

var format_sex = function () {
    return function (text, render) {
        /**
         * 模板所需函数,显示男女
         * by:范俊伟 at:2015-01-31
         */
        var content = render(text);
        if (content != '') {
            if (content == 'true') {
                return '男';
            }
            else {
                return '女';
            }
        }

    };
};

var select_option_sex = function () {
    return function (text, render) {
        /**
         * 模板所需函数,显示男女
         * by:范俊伟 at:2015-01-31
         */
        var content = render(text);
        var option = [];
        if (!content) {
            content = 'true';
        }

        if (content == 'true') {
            option.push('<option selected="selected" value="true">男</option>');
            option.push('<option value="false">女</option>');
        }
        else {
            option.push('<option value="true">男</option>');
            option.push('<option selected="selected" value="false">女</option>');
        }

        return option.join('');

    };
};
var format_address = function () {
    return function (text, render) {
        /**
         * 模板所需函数,显示男女
         * by:范俊伟 at:2015-01-31
         */
        var content = $.trim(render(text));
        if (content != '') {
            var city = getCityByID(content);
            if (city) {
                return city.province_name + ' ' + city.city_name;
            }
        }
    };
};

var createUserName = function () {
    return function (text, render) {
        /**
         * 模板所需函数,显示创建者姓名
         * by:范俊伟 at:2015-01-30
         * 使用回调函数显示方式
         * by:范俊伟 at:2015-02-04
         */
        var id = render(text);
        getUserById(id, function (user) {
            $('span[user_display=' + id + ']').text(user.name);
        });
        return '<span user_display="' + id + '"></span>';
    };
};
//0:未选择5:高中6:大专7:本科8:研究生9:博士
var xueli_arrya = [
    ['0', ''],
    ['5', '高中'],
    ['6', '大专'],
    ['7', '本科'],
    ['8', '研究生'],
    ['9', '博士']
];
var format_xueli = function () {
    return function (text, render) {
        /**
         * 模板所需函数
         * by:范俊伟 at:2015-01-31
         */
        var content = $.trim(render(text));
        if (content != '') {
            for (var i = 0; i < xueli_arrya.length; i++) {
                var value = xueli_arrya[i][0];
                if (value == content) {
                    return xueli_arrya[i][1];
                }
            }

        }

    };
};

var select_option_xueli = function () {
    return function (text, render) {
        /**
         * 模板所需函数
         * by:范俊伟 at:2015-01-31
         */
        var content = render(text);
        var option = [];


        for (var i = 0; i < xueli_arrya.length; i++) {
            var value = xueli_arrya[i][0];
            var text = xueli_arrya[i][1];
            if (value == content) {
                option.push('<option selected="selected" value="' + value + '">' + text + '</option>');
            }
            else {
                option.push('<option value="' + value + '">' + text + '</option>');
            }
        }
        return option.join('');

    };
};


//'wei':未婚'yihun':已婚'liyi':离异'sang':丧偶
var hunyin_arrya = [
    ['', ''],
    ['wei', '未婚'],
    ['yihun', '已婚'],
    ['liyi', '离异'],
    ['sang', '丧偶']
];
var format_hunyin = function () {
    return function (text, render) {
        /**
         * 模板所需函数
         * by:范俊伟 at:2015-01-31
         */
        var content = $.trim(render(text));
        if (content != '') {
            for (var i = 0; i < hunyin_arrya.length; i++) {
                var value = hunyin_arrya[i][0];
                if (value == content) {
                    return hunyin_arrya[i][1];
                }
            }

        }

    };
};

var select_option_hunyin = function () {
    return function (text, render) {
        /**
         * 模板所需函数
         * by:范俊伟 at:2015-01-31
         */
        var content = render(text);
        var option = [];


        for (var i = 0; i < hunyin_arrya.length; i++) {
            var value = hunyin_arrya[i][0];
            var text = hunyin_arrya[i][1];
            if (value == content) {
                option.push('<option selected="selected" value="' + value + '">' + text + '</option>');
            }
            else {
                option.push('<option value="' + value + '">' + text + '</option>');
            }
        }
        return option.join('');

    };
};
var weather_icon_map = {
    "晴": "qing",
    "晴朗": "qing",
    "多云": "",
    "阴": "",
    "阵雨": "yu",
    "雷阵雨": "yu",
    "雷阵雨伴有冰雹": "yu",
    "雨夹雪": "yu",
    "小雨": "yu",
    "中雨": "yu",
    "大雨": "yu",
    "暴雨": "yu",
    "大暴雨": "yu",
    "特大暴雨": "yu",
    "阵雪": "xue",
    "小雪": "xue",
    "中雪": "xue",
    "大雪": "xue",
    "暴雪": "xue",
    "雾": "wu",
    "冻雨": "yu",
    "小到中雨": "yu",
    "中到大雨": "yu",
    "大到暴雨": "yu",
    "暴雨到大暴雨": "yu",
    "大暴雨到特大暴雨": "yu",
    "小到中雪": "xue",
    "中到大雪": "xue",
    "大到暴雪": "xue",
    "浮尘": "yangsha",
    "扬沙": "yangsha",
    "沙尘暴": "yangsha",
    "强沙尘暴": "yangsha",
    "特强沙尘暴": "yangsha",
    "轻雾": "wu",
    "浓雾": "wu",
    "强浓雾": "wu",
    "轻微霾": "wu",
    "轻度霾": "wu",
    "中度霾": "wu",
    "重度霾": "wu",
    "特强霾": "wu",
    "霰": "wu"
};
var weather_icon = function () {
    return function (text, render) {
        /**
         * 模板所需函数,显示天气图标
         * by:范俊伟 at:2015-02-09
         */

        var content = $.trim(render(text));
        var icon_name = weather_icon_map[content];
        if (icon_name) {
            var icon_url = staticUrl + 'web/img/weather/' + icon_name + '@3x.png';
            return '<img src="' + icon_url + '" class="weather_icon">';
        }
        return '';

    };
};
function template_option(data) {
    /**
     * 附加模板处理函数
     * by:范俊伟 at:2015-01-31
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * @type {Function}
     */
    data.format_true_false = format_true_false;
    data.format_sex = format_sex;
    data.format_address = format_address;
    data.format_text = format_text_break_line;
    data.createUserName = createUserName;
    data.select_option_sex = select_option_sex;
    data.format_xueli = format_xueli;
    data.select_option_xueli = select_option_xueli;
    data.format_hunyin = format_hunyin;
    data.select_option_hunyin = select_option_hunyin;
    data.weather_icon = weather_icon;

}