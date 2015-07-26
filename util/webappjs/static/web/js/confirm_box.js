/**
 * Created by fanjunwei003 on 15/1/10.
 */
function ConfirmBox() {
    /**
     * 对话框类
     * by:范俊伟 at:2015-01-21
     * @type {*|jQuery|HTMLElement}
     */
    this.popup = $('#confirmBoxModal');
    this.popup_body = this.popup.find('.modal-body');
    this.popup_title = this.popup.find('.modal-title');
    this.button1 = this.popup.find('#confirmBoxModal_button1');
    this.button2 = this.popup.find('#confirmBoxModal_button2');
    _button1_cb = null;
    _button2_cb = null;

    this.showConfirm = function (title, message, button1_text, button2_text, button1_cb, button2_cb) {
        /**
         * 显示对话框
         * by:范俊伟 at:2015-01-21
         */
        this.popup_title.html(title);
        this.popup_body.html(message);
        if (button1_text) {
            this.button1.html(button1_text);
            _button1_cb = button1_cb;
            this.button1.show();
        }
        else {
            this.button1.hide();
        }
        if (button2_text) {
            this.button2.html(button2_text);
            _button2_cb = button2_cb;
            this.button2.show();
        }
        else {
            this.button2.hide();
        }
        var height = $(window).height() * 0.7;
        this.popup_body.css('max-height', height + 'px');
        this.popup.modal('show');
    };

    this.button1.click(function () {
        if (_button1_cb)
            _button1_cb();
    });
    this.button2.click(function () {
        if (_button2_cb)
            _button2_cb();
    });

}

var confirmBox;
$(function () {
    confirmBox = new ConfirmBox();
});