/**
 * Date: 15/6/11
 * Time: 16:56
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
function init_view_home() {
    /**
     * 初始化Home页面
     by: 范俊伟 at:2015-06-11
     增加个欢迎使用
     by：尚宗凯 at：2015-06-15
     */
    show_breadcrumb(null, true);
//    $('#view_content').html('home');
    $('#view_content').html('<h1 class="text-center">欢迎使用</h1>');
    window.viewDTD.resolve();
}