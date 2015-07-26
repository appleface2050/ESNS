/**
 * Date: 15/2/5
 * Time: 14:11
 * Email:fanjunwei003@163.com
 * Author:范俊伟
 */
var project_user_group_map = {};
var conn = new Easemob.im.Connection();
var current_to_user_group = null;
var easemob_inited = false;
var easemob_opened = false;
var easemob_opening = false;
var project_message_map = {};
var side_column_state = 0;
function resize() {
    /**
     * 自适应高度
     * by:范俊伟 at:2015-02-05
     * 布局调整
     by: 范俊伟 at:2015-03-13
     bug修改
     by: 范俊伟 at:2015-03-13
     * @type {*|jQuery}
     */
    var point = $('#message_view_point').offset();
    if (point) {
        var message_view = $('#message_view');

        if (message_view.css('position') == 'absolute') {
            message_view.css('left', 5);
            message_view.css('top', 0);
        }
        else {
            message_view.css('left', point.left);
            message_view.css('top', point.top);
        }
    }


}

$(window).resize(function () {
    /**
     * 窗口大小改变事件
     * by:范俊伟 at:2015-02-05
     */
    resize();
});
var getLoacalTimeString = function getLoacalTimeString() {
    /**
     * 获取时间
     by: 范俊伟 at:2015-03-13
     * @type {Date}
     */
    var date = new Date();
    var time = date.getHours() + ":" + date.getMinutes() + ":"
        + date.getSeconds();
    return time;
};
function getMessageList(p_project_id, contact) {
    /**
     * 消息列表获取
     by: 范俊伟 at:2015-04-07
     */
    var message_map = project_message_map[p_project_id];
    if (!message_map) {
        message_map = {};
        project_message_map[p_project_id] = message_map;
    }
    var message_list = message_map[contact];
    if (!message_list) {
        message_list = [];
        message_map[contact] = message_list;
    }
    return message_list;
}
function getMessageUserGroupList(p_project_id) {
    /**
     * 消息组列表获取
     */
    var user_group_list = project_user_group_map[p_project_id];
    if (!user_group_list) {
        user_group_list = [];
        project_user_group_map[p_project_id] = user_group_list;
    }
    return user_group_list;
}
function showSideColumn() {
    /**
     * 显示侧栏
     * by:范俊伟 at:2015-02-05
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     只显示有成员的分组
     by: 范俊伟 at:2015-03-15
     1处理不同项目,2.更新消息标记
     by: 范俊伟 at:2015-04-07
     */
    if (side_column_state == 0) {
        getUserGroupList(function (group_list) {
            group_list = _(group_list).filter(function (group) {
                return (group.look_members.length + group.say_members.length) > 0;
            });
            templateRender('web/mst/message_user_group.mst', {group_list: group_list}, function (rendered) {
                $('#side_content').html(rendered);
            });
        });
    }
    else if (side_column_state == 1) {
        templateRender('web/mst/message_current_user.mst', {current_user_list: getMessageUserGroupList(window.project_id)}, function (rendered) {
            $('#side_content').html(rendered);
        });
    }
    showHasNewMessage();
}
function setSideColumnState(state) {
    /**
     * 改变侧栏状态
     by: 范俊伟 at:2015-03-13
     */
    if (side_column_state != state) {
        side_column_state = state;
        showSideColumn();
    }

}
function showHasNewMessage() {
    /**
     * 设置切换消息按钮是否有新消息
     by: 范俊伟 at:2015-03-13
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     * @type {boolean}
     */
    var hasNew = false;
    var user_group_list = getMessageUserGroupList(window.project_id);
    for (var i = 0; i < user_group_list.length; i++) {
        var user = user_group_list[i];
        if (user.has_hit_count) {
            hasNew = true;
            break;
        }
    }
    if (hasNew) {
        $('#current_message_btn').show();
    }
    else {
        $('#current_message_btn').hide();
    }
}
function selectUser(p_project_id, id, add_hit_count) {
    /**
     * 选择用户
     * by:范俊伟 at:2015-02-05
     * 布局调整
     by: 范俊伟 at:2015-03-13
     逻辑修改
     by: 范俊伟 at:2015-03-13
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */
    id = id.toString();
    getUserById(id, function (user) {
        console.log('p_project_id' + p_project_id);
        var user_group_list = getMessageUserGroupList(p_project_id);
        for (var i = 0; i < user_group_list.length; i++) {
            var item = user_group_list[i];
            if (item.id == id) {
                user_group_list.splice(i, 1);
                break;
            }

        }
        user_group_list.splice(0, 0, user);


        if (!add_hit_count) {
            current_to_user_group = user;
            $('#chart_user_name').text(user.name);
            user.hit_count = 0;
            user.has_hit_count = false;
            $('#chat_message_content').empty();
            var message_list = getMessageList(p_project_id, id);
            if (message_list) {
                appendLines(message_list);
                scrollDown();
            }
            showHasNewMessage();
        }
        else {
            if (user.hit_count === undefined) {
                user.hit_count = 0;
            }
            user.has_hit_count = true;
            user.hit_count += add_hit_count;
            showHasNewMessage();
        }
        if (side_column_state == 1) {
            showSideColumn();
        }

    }, p_project_id);
}

function selectGroup(p_project_id, hxgroup_id, add_hit_count) {
    /**
     * 选择组
     * by:范俊伟 at:2015-02-05
     * 判断是否存在环信id,算法优化
     by: 范俊伟 at:2015-03-15
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */
    if (!hxgroup_id) {
        $.simplyToast('该组暂未开通群聊功能');
        return;
    }
    hxgroup_id = hxgroup_id.toString();
    getCurrentProjectUserGroups(null, p_project_id).done(function (groups) {
        var to_group = _(groups).find(function (group) {
            return group.hxgroup_id == hxgroup_id;
        });
        var user_group_list = getMessageUserGroupList(p_project_id);
        for (var i = 0; i < user_group_list.length; i++) {
            var item = user_group_list[i];
            if (item.hxgroup_id == hxgroup_id) {
                user_group_list.splice(i, 1);
                break;
            }
        }
        user_group_list.splice(0, 0, to_group);
        if (!add_hit_count) {
            current_to_user_group = to_group;
            $('#chart_user_name').text(to_group.group_name);
            to_group.hit_count = 0;
            to_group.has_hit_count = false;
            $('#chat_message_content').empty();
            var message_list = getMessageList(p_project_id, hxgroup_id);
            if (message_list) {
                appendLines(message_list);
                scrollDown();
            }
            showHasNewMessage();
        }
        else {
            if (to_group.hit_count === undefined) {
                to_group.hit_count = 0;
            }
            to_group.has_hit_count = true;
            to_group.hit_count += add_hit_count;
            showHasNewMessage();
        }
        if (side_column_state == 1) {
            showSideColumn();
        }
    });
}
function initEasemob() {
    /**
     * 初始化环信
     * by:范俊伟 at:2015-02-05
     * 连接完成后关闭遮罩
     by: 范俊伟 at:2015-03-13
     登录错误处理
     by: 范俊伟 at:2015-03-13
     修改错误提示
     by: 范俊伟 at:2015-03-13
     */
    console.log('initEasemob');
    conn.init({
            https: false,//非必填，url值未设置时有效，优先采用url配置的参数。默认采用http连接，地址为‘http://im-api.easemob.com/http-bind/’，启用https时传递此值，地址为：‘https://im-api.easemob.com/http-bind/’
            //url :'http://im-api.easemob.com/http-bind/',//非必填，默认聊天服务器地址，
            //domain: 'aa.com',//非必填，默认：‘easemob.com’
            //wait : '60',//非必填，连接超时，默认：60，单位seconds
            onOpened: function () {
                window.viewDTD.resolve();
                easemob_opened = true;
                easemob_opening = false;
                conn.setPresence();
                console.log('onOpened');
            },
            onClosed: function () {
                window.viewDTD.resolve();
                easemob_opened = false;
                easemob_opening = false;
                $.simplyToast('即时通信已断开连接', 'warning');
                //openEasemob();
                console.log('onClosed');
            },
            onTextMessage: function (message) {
                console.log('onTextMessage', message);
                /**处理文本消息，消息格式为：
                 {	type :'chat',//群聊为“groupchat”
                     from : from,
                     to : too,
                     data : { "type":"txt",
                         "msg":"hello from test2"
                     }
                 }
                 */
                handleTextMessage(message);
            },
            onEmotionMessage: function (message) {
                console.log('onEmotionMessage', message);
                /*处理表情消息,消息格式为：
                 {	type :'chat',//群聊为“groupchat”
                 from : from,
                 to : too,
                 data : [{ "type":"txt",
                 "msg":"hello from test2"
                 },
                 { "type":"emotion",
                 "msg":"data:image/png;base64, ……"//图片的base64编码
                 }]
                 }
                 执行接收表情函数
                 by: 范俊伟 at:2015-03-13
                 */
                handleEmotion(message);
            },
            onPictureMessage: function (message) {
                console.log('onPictureMessage', message);
                /**处理图片消息，消息格式为：
                 {	type :'chat',//群聊为“groupchat”
                     from : "test1",
                     to : "test2",
                     url : "http://s1.easemob.com/weiquan2/a2/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae",
                     secret : "NSgGYPCxEeOou00jZasg9e-GqKUZGdph96EFxJ4WxW-qkxV4",
                     filename : "logo.png",
                     thumb : "http://s1.easemob.com/weiquan2/a2/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae",
                     thumb_secret : "0595b06a-ed8b-11e3-9b85-93fade9c198c",
                     file_length : 42394,
                     width : 280,
                     height : 160,
                     filetype : "image/png",
                     accessToken :"YWMtjPPoovCqEeOQs7myPqqaOwAAAUaqNH0a8rRj4PwJLQju6-S47ZO6wYs3Lwo"
                 }
                 */

                //handlePictureMessage(message);
            },
            onAudioMessage: function (message) {
                console.log('onAudioMessage', message);
                /**处理音频消息，消息格式为：
                 {	type :'chat',//群聊为“groupchat”
                      from : "test1",
                      to : "test2",
                      url : "http://s1.easemob.com/weiquan2/a2/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae",
                      secret :"NSgGYPCxEeOou00jZasg9e-GqKUZGdph96EFxJ4WxW-qkxV4",
                      filename : "风雨无阻.mp3",
                      length :45223,
                      file_length : 304,
                      filetype : "mp3",
                      accessToken :"YWMtjPPoovCqEeOQs7myPqqaOwAAAUaqNH0a8rRj4PwJLQju6-S47ZO6wYs3Lwo"
                  }
                 */
                //handleAudioMessage(message);
            },
            //收到联系人订阅请求的回调方法
            onPresence: function (message) {
                console.log('onPresence', message);
                /**
                 {
                     from: "l2",
                     fromJid: "easemob-demo#chatdemoui_l2@easemob.com",
                 status: "下午11:44:47",
                 to: "test1",
                 toJid: "easemob-demo#chatdemoui_test1@easemob.com/13856640471403797405809685",
                 type: "subscribed"
                 }
                 */
                //handlePresence(message);
            },
            //收到联系人信息的回调方法
            onRoster: function (message) {
                console.log('onRoster', message);
                /**
                 [{
                groups: [{0: "default",
                        length: 1}],
                jid: "easemob-demo#chatdemoui_l2@easemob.com",
                 name: "l2",
                 subscription: "to"
                 }]
                 */
            },
            onError: function (e) {
                console.log('error', e);
                $.simplyToast('即时通信初始化失败', 'danger');
                window.viewDTD.resolve();
                easemob_opened = false;
                easemob_opening = false;
            }
        }
    );
    easemob_inited = true;
}

function openEasemob() {
    /**
     * 打开环信连接
     * by:范俊伟 at:2015-02-05
     * 初始化逻辑修改
     by: 范俊伟 at:2015-03-13
     */
    if (!easemob_opening && !easemob_opened) {
        easemob_opening = true;
        conn.open({
            user: window.hx_username,
            pwd: window.hx_password,
            appKey: window.hx_appkey//开发者APPKey
        });
    }

}
function sendMessage() {
    /**
     * 发送消息
     * by:范俊伟 at:2015-02-05
     * 用户id转为字符串
     * by:范俊伟 at:2015-02-07
     * 修改环信调用参数
     by: 范俊伟 at:2015-02-13
     逻辑修改
     by: 范俊伟 at:2015-03-13
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     环信未开通状态提示
     by: 范俊伟 at:2015-03-13
     判断是否有群组发言权限
     by: 范俊伟 at:2015-03-15
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */
    if (!window.hx_username || !window.hx_password) {
        $.simplyToast('暂未开通通信功能', 'danger');
        return;
    }
    if (easemob_opened) {
        var message = $('#chat_input_box').val();
        if (current_to_user_group) {
            var to;
            var isGroupMessage = false;
            if (current_to_user_group.hxgroup_id) {
                to = current_to_user_group.hxgroup_id;
                isGroupMessage = true;
                console.log(current_to_user_group.current_user_say);
                if (!current_to_user_group.current_user_say) {
                    $.simplyToast('您无权限在该组发送消息', 'danger');
                    return;
                }
            }
            else {
                to = current_to_user_group.id;
            }
            var options = {
                to: to,
                msg: message,
                type: "chat",
                ext: {"project_id": window.project_id}
            };
            if (isGroupMessage) {
                options.type = 'groupchat';
            }
            conn.sendTextMessage(options);
            var msgtext = message.replace(/\n/g, '<br>');
            appendMsg(uid, to, msgtext, options.type, window.project_id);
            $('#chat_input_box').val('');

        }
        else {
            $.simplyToast('未选择发送对象', 'danger')
        }
    } else {
        $.simplyToast('还未建立连接', 'danger')
    }

}

function handleTextMessage(message) {
    /**处理文本消息，消息格式为：
     *
     {	type :'chat',//群聊为“groupchat”
         from : from,
         to : too,
         data : "message"
     }
     by:范俊伟 at:2015-02-05
     逻辑修改
     by: 范俊伟 at:2015-03-13
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */

    var from = message.from;//消息的发送者
    var to = message.to;
    var mestype = message.type;//消息发送的类型是群组消息还是个人消息
    var messageContent = message.data;//文本消息体
    //TODO  根据消息体的to值去定位那个群组的聊天记录
    var room = message.to;
    var p_project_id = message.ext.project_id;
    if (mestype == 'groupchat') {
        appendMsg(message.from, message.to, messageContent, mestype, p_project_id);
    } else {
        appendMsg(from, from, messageContent, 'chat', p_project_id);
    }

}

var handleEmotion = function (message) {
    /**
     * 表情处理函数
     by: 范俊伟 at:2015-03-13
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */
    var from = message.from;
    var room = message.to;
    var mestype = message.type;//消息发送的类型是群组消息还是个人消息
    var p_project_id = message.ext.project_id;
    if (mestype == 'groupchat') {
        appendMsg(message.from, message.to, message, mestype, p_project_id);
    } else {
        appendMsg(from, from, message, 'chat', p_project_id);
    }

};
function scrollDown() {
    /**
     * 滚动到底部
     * by:范俊伟 at:2015-02-05
     */
    $("#chat_message").scrollTop($("#chat_message_content").height());
}

var appendMsg = function (who, contact, message, chattype, p_project_id) {
    /**
     * 追加消息
     by: 范俊伟 at:2015-03-13
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     根据项目处理消息
     by: 范俊伟 at:2015-04-07
     */
    who = who.toString();
    contact = contact.toString();
    console.log('appendMsg', who, contact, message, chattype);
    var localMsg = null;
    if (typeof message == 'string') {
        localMsg = Easemob.im.Helper.parseTextMessage(message);
        localMsg = localMsg.body;
    } else {
        localMsg = message.data;
    }
    var message_list = getMessageList(p_project_id, contact);
    getUserById(who, function (user) {

        //data.name = user.name;
        //data.id = user.id;
        //data.get_message = get_message;
        // 消息体 {isemotion:true;body:[{type:txt,msg:ssss}{type:emotion,msg:imgdata}]}
        var headstr = ["<p1>" + user.name + "   <span></span>" + "   </p1>",
            "<p2>" + getLoacalTimeString() + "<b></b><br/></p2>"];
        var header = $(headstr.join(''));

        var lineDiv = document.createElement("div");
        for (var i = 0; i < header.length; i++) {
            var ele = header[i];
            lineDiv.appendChild(ele);
        }
        var messageContent = localMsg;
        for (var i = 0; i < messageContent.length; i++) {
            var msg = messageContent[i];
            var type = msg.type;
            var data = msg.data;
            if (type == "emotion") {
                var eletext = "<p3><img src='" + data + "'/></p3>";
                var ele = $(eletext);
                for (var j = 0; j < ele.length; j++) {
                    lineDiv.appendChild(ele[j]);
                }
            } else if (type == "pic" || type == 'audio' || type == 'video') {
                var filename = msg.filename;
                var fileele = $("<p3>" + filename + "</p3><br>");
                for (var j = 0; j < fileele.length; j++) {
                    lineDiv.appendChild(fileele[j]);
                }
                lineDiv.appendChild(data);
            } else {
                var eletext = "<p3>" + data + "</p3>";
                var ele = $(eletext);
                ele[0].setAttribute("class", "chat-content-p3");
                ele[0].setAttribute("className", "chat-content-p3");
                if (uid == who) {
                    ele[0].style.backgroundColor = "#EBEBEB";
                }
                for (var j = 0; j < ele.length; j++) {
                    lineDiv.appendChild(ele[j]);
                }
            }
        }

        if (uid == who) {
            lineDiv.style.textAlign = "right";
        } else {
            lineDiv.style.textAlign = "left";
        }
        message_list.push(lineDiv);
        if (current_to_user_group && window.project_id == p_project_id && (contact == current_to_user_group.id || contact == current_to_user_group.hxgroup_id)) {
            appendLines([lineDiv]);
            scrollDown();
        }
        else {
            if (chattype == 'groupchat') {
                selectGroup(p_project_id, contact, 1);
            }
            else {
                selectUser(p_project_id, contact, 1);
            }

        }

    }, p_project_id);
};

function appendLines(html_lines) {
    /**
     * 追加消息显示
     * by:范俊伟 at:2015-02-05
     * 逻辑修改
     by: 范俊伟 at:2015-03-13
     * @type {{list: *}}
     */
    for (var i = 0; i < html_lines.length; i++) {
        $('#chat_message_content').append(html_lines[i]);
    }

}
initQueue.push(function () {
    /**
     * 相关初始化功能加入初始化列表
     * by:范俊伟 at:2015-02-05
     */

});
function exit_view_message() {
    /**
     * 群组消息逻辑
     by: 范俊伟 at:2015-03-13
     * @type {null}
     */
    current_to_user_group = null;
}
function initEnterSend() {
    /**
     * 回车发送消息
     by: 范俊伟 at:2015-03-13
     */
    $('#chat_input_box').keydown(function (e) {
        if (e.keyCode == 13) {
            sendMessage();
            return false;
        }
    });
}
function init_view_message(first_open) {
    /**
     * 页面初始化
     * by:范俊伟 at:2015-02-06
     * 遮罩逻辑
     by: 范俊伟 at:2015-03-09
     布局调整
     by: 范俊伟 at:2015-03-13
     回车发送消息
     by: 范俊伟 at:2015-03-13
     初始化逻辑修改
     by: 范俊伟 at:2015-03-13
     隐藏遮罩逻辑修改
     by: 范俊伟 at:2015-03-13
     * @type {*|jQuery}
     */
    exitViewCallback = exit_view_message;
    templateRender('web/mst/message_view.mst', {}, function (rendered) {
        $('#view_content').html(rendered);
        resize();
        showSideColumn();
        initEnterSend();
        if (first_open) {
            if (window.hx_username && window.hx_password) {
                initEasemob();
            }
            else {
                $.simplyToast('暂未开通通信功能', 'danger');
            }
        }
        if (easemob_inited) {
            openEasemob();
        }
        if (!easemob_opening) {
            window.viewDTD.resolve();
        }
    });
}