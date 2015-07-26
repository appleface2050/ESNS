/**
 * Date: 15/1/21
 * Time: 13:53
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

function getAllProject(address, key) {
    /**
     * 查询所有项目
     * by:范俊伟 at:2015-01-22
     * 去掉template_option调用,在templateRender统一调用
     * by:范俊伟 at:2015-02-03
     * 布局修改
     by: 范俊伟 at:2015-03-10
     分页bug修改
     by: 范俊伟 at:2015-03-10
     分页修错误,恢复之前的
     by: 范俊伟 at:2015-03-14
     使用通用http请求函数
     by: 范俊伟 at:2015-03-15
     */
    httpRequest('/ns/query_project', {
        start: projectList.length,
        address: address,
        key: key
    }).then(function (data) {
        window.viewDTD.resolve();
        if (data) {
            if (data.result && data.result.length > 0) {
                projectList = projectList.concat(data.result);//数组合并
                data.option = option;
                templateRender('web/mst/all_project_dataitem.mst', data, function (rendered) {
                    $('#table_data').append(rendered);
                    setTimeout(function () {
                        getAllProject(address, key);
                    }, 0);

                });
            }
        }
    }, function () {
        window.viewDTD.resolve();
    });
}
function search() {
    /**
     * 搜索项目
     * by:范俊伟 at:2015-02-02
     */

    projectList = [];
    $('#table_data').empty();
    var keyword = $('#keyword').val();
    var city_id = $('#city').val();
    getAllProject(city_id, keyword);
}
var project_names = function (q, cb) {
    /**
     * 自动补全检索函数
     by: 范俊伟 at:2015-03-15
     */
    httpRequest('/ns/query_project_name', {key: q}, 'post', true, true).done(function (data) {
        var matchs = [];
        if (data && data.success && data.result) {
            for (var i = 0; i < data.result.length; i++) {
                matchs.push({value: data.result[i]});
            }
            cb(matchs);
        }
    });
};
function init_view_all_project() {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     载入第一页后再隐藏遮罩
     by: 范俊伟 at:2015-03-10
     增加自动补全功能
     by: 范俊伟 at:2015-03-15
     * @type {*|jQuery}
     */

    templateRender('web/mst/all_project_view.mst', {}, function (rendered) {
            $('#view_content').html(rendered);
            initCity();
            $('#keyword').typeahead({
                    hint: true,
                    highlight: true,
                    minLength: 1
                },
                {
                    name: 'project',
                    source: project_names
                });
            projectList = [];
            $('#table_data').empty();
            getAllProject();
        }
    );
}