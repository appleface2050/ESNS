/**
 * Date: 15/1/21
 * Time: 14:10
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 * var projectEnterUrl = "{% url 'web:contacts' '' %}";
 */

function getMyProject(timeline) {
    /**
     * 查询我的项目
     * by:范俊伟 at:2015-01-23
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * 布局修改
     by: 范俊伟 at:2015-03-10
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    httpRequest('/ns/my_project').then(function (data) {
        window.viewDTD.resolve();
        if (data) {
            if (data.result && data.result.length > 0) {
                console.log('my_project', data.result);
                projectList = projectList.concat(data.result);//数组合并
                data.option = option;
                templateRender('web/mst/my_project_dataitem.mst', data, function (rendered) {
                    $('#table_data').append(rendered);
                });
            }
        }
    }, function () {
        window.viewDTD.resolve();
    });
}

function init_view_my_project() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入第一页数据后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     * @type {*|jQuery}
     */
    templateRender('web/mst/my_project_view.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        $('#table_data').empty();
        getMyProject();
    });
}