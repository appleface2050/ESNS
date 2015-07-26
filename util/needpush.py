# coding=utf-8
from Need_Server.settings import _jpush,PUSH_ON,JPUSH_MESSAGE,ENVIRONMENT
import jpush as jpush
import json
import threading
from django.core.cache import cache
from util import PROJECT_INFO
from django.conf import settings
from util.jsonresult import MyEncoder

class NeedPush(threading.Thread):
    """
    极光推送消息类
    by:尚宗凯 at：2015-04-02
    修改tag发送方式
    by:尚宗凯 at：2015-04-03
    极光推送ios修改
    by:尚宗凯 at：2015-04-07
    极光推送增加默认tag=None
    by:尚宗凯 at：2015-04-07
    极光推送修改
    by:尚宗凯 at：2015-04-09
    改变测试代码
    by:尚宗凯 at：2015-04-09
    使用多线程
    by:尚宗凯 at：2015-04-16
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.push_android = _jpush.create_push()
        self.push_ios = _jpush.create_push()

    def send(self, msg_content, title, content_type, extras, tag=None):
        # self.push_android = _jpush.create_push()
        # self.push_ios = _jpush.create_push()
        # self.push.platform = jpush.all_
        self.push_android.platform = "android"
        self.push_ios.platform = "ios"
        if tag:
            self.push_android.audience = jpush.audience(
                # jpush.tag("p_44","p_45")
                jpush.tag(tag)
            )
            self.push_ios.audience = jpush.audience(
                jpush.tag(tag)
            )
        else:
            self.push_android.audience = jpush.all_
            self.push_ios.audience = jpush.all_
        self.push_android.message = jpush.message(msg_content=msg_content, title=title, content_type=content_type, extras=json.dumps(extras))
        self.push_ios.notification = jpush.notification(alert=msg_content)
        try:
            if PUSH_ON:
                self.push_android.send()
                self.push_ios.send()
        except Exception as e:
            print e

    def send2(self, msg_content, title, content_type, extras, tag=None, alias=None):
        """
        增加alias发送方法
        by: 尚宗凯 at：2015-04-09
        修改alias用法
        by: 尚宗凯 at：2015-04-09
        ios通知无声
        by:尚宗凯 at：2015-04-10
        解决ios无法收到推送的问题
        by:尚宗凯 at：2015-04-15
        修改ios alert内容
        by:尚宗凯 at：2015-04-16
        修改ios 推送增加字段
        by:尚宗凯 at：2015-04-22
        修改ios 推送alias
        by:尚宗凯 at：2015-04-23
        增加badge+1
        by:尚宗凯 at：2015-04-29
        如果alias为空则不发送
        by:尚宗凯 at：2015-04-04
        极光推送改为+1
        by：尚宗凯 at：2015-05-18
        """
        if not alias:
            return False
        self.push_android.platform = "android"
        self.push_ios.platform = "ios"
        if ENVIRONMENT == 'aliyun':
            self.push_ios.options = {"apns_production":True}     #生产环境
        else:
            self.push_ios.options = {"apns_production":False}    #开发环境
        if tag:
            self.push_android.audience = jpush.audience(
                # jpush.tag("p_44","p_45")
                jpush.tag(tag)
            )
            self.push_ios.audience = jpush.audience(
                jpush.tag(tag)
            )
        elif alias:
            self.push_android.audience = jpush.alias(
                alias
            )
            self.push_ios.audience = jpush.alias(
                alias
            )
        # else:
        #     self.push_android.audience = jpush.all_
        #     self.push_ios.audience = jpush.all_
        self.push_android.message = jpush.message(msg_content=msg_content, title=title, content_type=content_type, extras=json.dumps(extras))
        self.push_ios.sound_disable=True
        ios_msg = jpush.ios(alert=u'%s,%s'%(title, msg_content), extras=extras, badge="+1")
        self.push_ios.notification = jpush.notification(alert=u'%s,%s'%(title, msg_content), ios=ios_msg)
        self.start()

    @classmethod
    def new(cls):
        return cls()

    @staticmethod
    def send_jpush(flag, project_id, title, msg, alias, file_group):
        """
        项目状态为关闭，已删除的情况不发
        by：尚宗凯 at：2015-05-31
        """

        project = cache.get(PROJECT_INFO % project_id)
        if project is None:
            from needserver.models import Project
            if Project.objects.filter(pk=project_id).exists():
                project = Project.objects.get(pk=project_id)
                project = MyEncoder.default(project)
                cache.set(PROJECT_INFO % project_id, project, settings.CACHES_TIMEOUT)
            else:
                return False
        if int(project["status"]) not in (0,1):
            return False
        else:
            msg_content = msg + JPUSH_MESSAGE
            data = {"title":title,
                    'message':msg_content,
                    "project_id":project_id,
                    "type":"refresh",
                    "flag":flag,
                    "push_type":"jpush",
                    "file_group":file_group
                    }
            NeedPush.new().send2(msg_content=msg_content,title=title,content_type=u"content_type",extras=data,alias=alias)

    def run(self):
        if PUSH_ON:
            try:
                self.push_android.send()
            except Exception as e:
                print "android push error:",e
            try:
                self.push_ios.send()
            except Exception as e:
                print "android push error:",e


if __name__ == '__main__':
    data = {"title":"依子轩办公大楼","message":"施工日志有了新变化","project_id":1,"type":"refresh", "flag":"gong_cheng_xing_xiang_jin_du"}
    # NeedPush.new().send(msg_content=u"施工日志有了新变化",title=u"施工日志有了新变化",content_type=u"content_type",extras=data,tag="p_"+str(44))
    NeedPush.send_jpush(flag="gong_cheng_xing_xiang_jin_du",
                        project_id=11,
                        title="title",
                        msg="msg",
                        alias=["10297","10003"],
                        file_group={"a":1,"b":2}
                        )