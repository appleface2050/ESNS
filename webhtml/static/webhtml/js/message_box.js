/**
 * Created by fanjunwei003 on 15/1/10.
 */
function MessageBox() {
    /**
     * 消息框类
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery|HTMLElement}
     */
    this.popup = $('#messageBoxModal');
    this.popup_body = this.popup.find('.modal-body');
    this.popup_title = this.popup.find('.modal-title');
    this.showMessage = function (title, message) {
        /**
         * 显示消息框
         * by:范俊伟 at:2015-01-21
         */
        this.popup_title.html(title);
        this.popup_body.html(message);
        var height = $(window).height() * 0.7;
        this.popup_body.css('max-height', height + 'px');
        this.popup.modal('show');
    }
}

var messageBox;
$(function () {
    messageBox = new MessageBox();
});