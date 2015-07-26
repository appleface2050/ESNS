/**
 * Created by wangjian on 15/6/22.
 */


function add_user_by_tel_to_company() {
    /**
     * 添加用户
     by: 范俊伟 at:2015-06-25
     优化结果逻辑
     by: 范俊伟 at:2015-06-25
     * @type {*|jQuery|HTMLElement}
     */

    var form = $('form');
    if (form.find('input[type=checkbox]:checked').length <= 0) {
        return;
    }
    var url = '/cp/' + company_id + '/add_user_by_tel_to_company';
    var obj = form.serializeArray();
    httpRequest(url, obj).done(function (data) {
        var list = [];
        var success_tels = data.result.success_tels;
        var error_tels = data.result.error_tels;
        var send_sms_tels = data.result.send_sms_tels;
        _(success_tels).each(function (tel) {
            var item = _(window.contracts).find(function (value) {
                return value.tel == tel;
            });
            item.status = 'success';
            list.push(item);
        });
        _(error_tels).each(function (tel) {
            var item = _(window.contracts).find(function (value) {
                return value.tel == tel;
            });
            item.status = 'error';
            list.push(item);
        });
        _(send_sms_tels).each(function (tel) {
            var item = _(window.contracts).find(function (value) {
                return value.tel == tel;
            });
            item.status = 'sms';
            list.push(item);
        });
        list = _(list).sortBy('pinyin');
        EJSTemplateRender('cp_manage/phone/ejs/user_manage_result.ejs', {list: list}).done(function (html) {
            $('#data').html(html);
            $("html,body").animate({scrollTop: 0}, 200);
            $('#add_bottom').hide();
            $('#result_bottom').show();
        })
    });

}

function check_user_registered(contracts) {
    /**
     * 检查用户是否注册
     by: 范俊伟 at:2015-06-25
     * @type {Array}
     */
    var obj = [];
    _(contracts).each(function (item) {
        obj.push({name: 'tel', value: item.tel});
    });
    httpRequest('/cp/check_user_registered', obj).done(function (data) {
        console.log(data);
        if (data.result) {
            _(data.result).each(function (id) {
                console.log(id);
                $('#registered_' + id).show();
            });
        }
    });

}
function fill_data(contracts) {
    /**
     * 填充数据
     by: 范俊伟 at:2015-06-24
     记录数据
     by: 范俊伟 at:2015-06-25
     处理手机号
     by: 范俊伟 at:2015-06-25
     * @type {*|jQuery|HTMLElement}
     */
    var data_area = $('#data');
    _(contracts).each(function (item) {
        if (item.tel) {
            item.tel = item.tel.replace("+86",'').replace(/\D/g,'');
        }
    });
    contracts = _(contracts).sortBy('pinyin');
    window.contracts = contracts;
    $('#add_bottom').show();
    $('#result_bottom').hide();
    EJSTemplateRender('cp_manage/phone/ejs/user_manage_select_user.ejs', {list: contracts}).done(function (html) {
        data_area.html(html);
        init_check();
        check_user_registered(contracts);
    })
}
function getContacts() {
    /**
     * 获取手机通讯录
     by: 范俊伟 at:2015-06-24
     */
    if (window.needApi) {
        var contracts = JSON.parse(window.needApi.getContacts());
        fill_data(contracts);
    }
    else if (window.bridge) {
        bridge.send('getContacts', function responseCallback(responseData) {
            fill_data(JSON.parse(responseData));
        })
    }

}

function set_check_state(checkbox) {
    /**
     * 设置选中状态
     by: 范俊伟 at:2015-06-24
     */
    var p = checkbox.parent();
    var chk = p.find('[chk]');
    if (checkbox.is(':checked')) {
        chk.attr('class', 'ci_01');
    }
    else {
        chk.attr('class', 'ci_02');
    }
}

function init_check() {
    /**
     * 设置选中状态
     by: 范俊伟 at:2015-06-24
     */
    $('input[type=checkbox]').each(function () {
        var checkbox = $(this);
        set_check_state(checkbox);
        checkbox.change(function () {
            set_check_state(checkbox);
        });
    });
}
window.init_callback = getContacts;
function back() {
    /**
     * 返回按钮事件
     by: 范俊伟 at:2015-06-25
     */
    window.history.go(-1);
}
function readd() {
    /**
     * 重新显示添加界面
     by: 范俊伟 at:2015-06-25
     */
    fill_data(window.contracts);
}
$(function () {
    getContacts();
    //fill_data([{name: "123", tel: "123", pinyin: "123"}, {name: "f", tel: "15618775252", pinyin: "f"}]);

});