/**
 * Date: 15/2/2
 * Time: 18:33
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var saveProjectButtonClick = null;
var projectList = [];
function showProjectInfo(id) {
    /**
     * 显示工程详情消息框
     * by:范俊伟 at:2015-01-21
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * 增加关注按钮
     by: 范俊伟 at:2015-03-16
     */
    if (projectList.length > 0) {
        for (i = 0; i < projectList.length; i++) {
            var p_id = projectList[i].id;
            if (p_id == id) {
                templateRender('web/mst/project_info.mst', projectList[i], function (rendered) {
                    confirmBox.showConfirm('工程详细信息', rendered, '关注', '关闭', function () {
                        guanzhu_project(id, 'join');
                    });
                });
            }
        }
    }

}
function enterProject(project_id) {
    /**
     * 进入指定项目
     * by:范俊伟 at:2015-02-06
     * 进入项目后默认打开应用界面
     by: 范俊伟 at:2015-03-08
     取消不必要的刷新
     by: 范俊伟 at:2015-03-10
     优化数据缓存
     by: 范俊伟 at:2015-03-10
     */
    window.project_id = project_id;
    window.projectInfo = undefined;
    window.project_all_user = undefined;
    window.userGroup = undefined;
    openView('application');
}
function guanzhu_project(project_id, do_arg) {
    /**
     * 关注或取消关注项目
     * by:范俊伟 at:2015-02-02
     * 兼容IE
     * by:范俊伟 at:2015-02-07
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var data = {
        project_id: project_id
    };
    data['do'] = do_arg;
    httpRequest('/ns/guanzhu_project', data).done(function (data) {
        if (data.message) {
            $.simplyToast(data.message, 'success');
        }
        window.userInfo = undefined;
        getUserInfo(function () {
            setOptionButton(project_id);
        });
    });

}
var option = function () {

    /**
     * 模板所需函数,根据当前用户不同状态显示不同按钮
     * by:范俊伟 at:2015-01-22
     * 项目的manager与当前用户相等时也为参与项目
     by: 范俊伟 at:2015-03-12
     */
    var item = this;
    var id = item.id;
    var manager = item.manager;
    setOptionButton(id, manager);
    var html = '<div option_project_id="' + id + '"></div>';
    return html;

};
function setOptionButton(id, manager) {
    /**
     * 填充修改操作按钮
     * by:范俊伟 at:2015-02-02
     * 项目的manager与当前用户相等时也为参与项目
     by: 范俊伟 at:2015-03-12
     */

    getUserInfo(function (info) {
        var div = $('div[option_project_id=' + id + ']');
        var guanzhuprojectlist = info.guanzhuprojectlist;
        var canyuprojectlist = info.canyuprojectlist;

        var guanzhu = false;
        var canyu = false;
        for (var i = 0; i < guanzhuprojectlist.length; i++) {
            if (id == guanzhuprojectlist[i]) {
                guanzhu = true;
            }
        }
        for (var i = 0; i < canyuprojectlist.length; i++) {
            if (id == canyuprojectlist[i]) {
                canyu = true;
            }
        }
        if (uid == manager) {
            canyu = true;
        }
        if (canyu) {
            var html = '<button onclick="enterProject(/id/)" class="btn btn-default">进入项目</button>';
            html = html.replace('/id/', id);
            div.html(html);
        }
        else {
            if (guanzhu) {
                var html = '<div class="btn-group"><button onclick="show_apply_project(/id/)" class="btn btn-primary">申请加入</button>' +
                    '<button onclick="guanzhu_project(/id/,\'out\')" class="btn btn-danger">取消关注</button></div>';
                html = html.replace(/\/id\//g, id);
                div.html(html);
            }
            else {
                var html = '<div class="btn-group"><button onclick="show_apply_project(/id/)" class="btn btn-primary">申请加入</button>' +
                    '<button onclick="guanzhu_project(/id/,\'join\')" class="btn btn-success">关注</button></div>';
                html = html.replace(/\/id\//g, id);
                div.html(html);
            }
        }
    });
}

function show_apply_project(project_id) {
    /**
     * 显示输入验证信息对话框
     * by:范俊伟 at:2015-01-22
     * 限制字串长度
     by: 范俊伟 at:2015-03-11
     提示最大字符
     by: 范俊伟 at:2015-03-13
     */
    confirmBox.showConfirm('输入验证信息', '<br><textarea maxlength="50" style="width:100%" id="apply_text" rows="3"></textarea>', '确定', '取消', function () {
        apply_project(project_id, $('#apply_text').val());
    }, null);
    initMaxLengthTooltips($('textarea'));

}
function apply_project(project_id, text) {
    /**
     * 申请加入项目
     * by:范俊伟 at:2015-01-22
     * 使用通用http请求函数
     by: 范俊伟 at:2015-03-16
     */
    var url = '/ns/' + project_id + '/apply_project';
    var data = {text: text};
    httpRequest(url, data).done(function (data) {
        console.log(data);
        $.simplyToast('申请成功', 'success')
    });
}