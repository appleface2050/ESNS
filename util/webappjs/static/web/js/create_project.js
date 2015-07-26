/**
 * Date: 15/1/21
 * Time: 13:59
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */

function formCallback(data) {
    /**
     * 表单ajax提交回调函数
     * by:范俊伟 at:2015-01-21
     * 表单提交成功后清空相关数据.表单提交失败后,平滑滚动到顶部,以便查看错误信息
     * by:范俊伟 at:2015-01-21
     */
    if (data.success) {

        $('#form_error').text('');
        $('#project_from')[0].reset();
        initCity();
        messageBox.showMessage('创建项目', '创建成功');
    }
    else {
        onFormCheckError();
        $('#form_error').text(data.message);
    }
}
function showCreateProject() {
    /**
     * 显示工程修改界面
     * by:范俊伟 at:2015-02-03
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     */
    templateRender('web/mst/project_save.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        window.viewDTD.resolve();
        initForm();
        initDateTimePicker();
        initCity();
    });
}

function createProjectButtonClick() {
    /**
     * 保存工程按钮事件
     * by:范俊伟 at:2015-02-03
     */
    $('#project_from').submit();
}
function init_view_create_project() {
    showCreateProject();
    saveProjectButtonClick = createProjectButtonClick;
}