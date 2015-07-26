/**
 * Date: 15/1/23
 * Time: 14:47
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var applicationList = [];
var applicationGroup = {};
var app_name = '应用';
var father_id = null;
var typeflag = 'list';
var current_app_group = null;

var click_path = [];


function openApplication(id) {
    /**
     * 打开应用
     * by:范俊伟 at:2015-01-23
     * 使用underscore.js优化算法
     by: 范俊伟 at:2015-03-15
     * @type {null}
     */
    current_app_group = null;
    if (id != null) {

        current_app_group = _(applicationList).find(function (obj) {
            return obj.id == id;
        });
        if (current_app_group) {
            last_arg = {};
            last_arg['app_name'] = app_name;
            last_arg['father_id'] = father_id;
            last_arg['typeflag'] = typeflag;
            last_arg['index'] = click_path.length;

            click_path.push(last_arg);
            app_name = current_app_group.name;
            father_id = current_app_group.id;
            typeflag = current_app_group.typeflag;
            showApplication();

        }
    }

}
function openHistory(index) {
    /**
     * 打开导航历史应用
     * by:范俊伟 at:2015-01-23
     */
    if (index >= 0 && index < click_path.length) {
        app_name = click_path[index].app_name;
        father_id = click_path[index].father_id;
        typeflag = click_path[index].typeflag;
        click_path = click_path.splice(0, index);
        showApplication();
    }
}
function showApplication() {
    /**
     * 显示应用列表
     * by:范俊伟 at:2015-01-23
     * 使用underscore.js优化算法
     by: 范俊伟 at:2015-03-15
     * @type {Array}
     */
    var selectAPP = applicationGroup[father_id];


    var data = {
        click_path: click_path,
        result: selectAPP
    };
    data['last_name'] = app_name;

    templateRender('web/mst/application_top.mst', data, function (rendered) {
        $('#app_top').html(rendered);

    });
    console.log(typeflag);
    if (typeflag == 'list' || typeflag == 'columnlist') {
        templateRender('web/mst/application_content.mst', data, function (rendered) {
            $('#app_content').html(rendered);

        });
    }
    else if (typeflag == 'files') {
        show_browse_filelist();
    }
    else if (typeflag == 'images' || typeflag == 'bgimages') {
        show_browse_imagelist();
    }
    else if (typeflag == 'log') {
        showLogApp();
    }
    else if (typeflag == 'gyslist') {
        showGysaddress();
    }
    else if (typeflag == 'wuzilist' || typeflag == 'wuzioutlist') {
        showWzlist();
    }
    else if (typeflag == 'jc') {
        show_browse_jc();
    }
    else {
        $('#app_content').empty();
    }

}
function getApplication() {
    /**
     * 查询项目内应用
     * by:范俊伟 at:2015-01-23
     * 使用无提示框的错误处理函数
     * by:范俊伟 at:2015-02-02
     载入数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     修改载入方式
     by: 范俊伟 at:2015-03-14
     * 使用underscore.js优化算法
     by: 范俊伟 at:2015-03-15
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    var url = '/ns/' + window.project_id + '/query_app_list';
    httpRequest(url).then(function (data) {
        window.viewDTD.resolve();
        if (data) {
            if (data.result && data.result.length > 0) {
                applicationList = data.result;
                applicationGroup = _(applicationList).groupBy('father');
                showApplication();
            }
        }
    }, function () {
        window.viewDTD.resolve();
    });

}

function init_view_application() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入列表后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * @type {*|jQuery}
     */

    templateRender('web/mst/application_view.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        getApplication();
    });
}