# coding=utf-8
# Date: 15/3/4
# Time: 14:09
# Email:fanjunwei003@163.com

__author__ = u'范俊伟'

class UserAgentMiddleware(object):
    """
    UserAgent中间件
    by: 范俊伟 at:2015-03-04
    """
    def process_request(self, request):
        """
        页面请求
        browserGroup: 设备大分类,smart_phone:智能机 feature_phone:功能机 空字串:pc或其他
        browserType: 设备类型,iphone,ipad,android,wp(windows phone),blackberry(黑莓),nokia(分智能机和功能机),空字串为pc或其他
        by: 范俊伟 at:2015-03-04
        :param request:
        :return:
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        if not user_agent.find('iphone') == -1:
            request.browserType = 'iphone'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('ipad') == -1:
            request.browserType = 'ipad'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('android') == -1:
            request.browserType = 'android'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('windows phone') == -1:
            request.browserType = 'wp'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('blackberry') == -1:
            request.browserType = 'blackberry'
            if not user_agent.find('applewebkit') == -1:
                request.browserGroup = 'smart_phone'
            if not user_agent.find('opera') == -1:
                request.browserGroup = 'smart_phone'
            else:
                request.browserGroup = 'feature_phone'
        elif (not user_agent.find('symbian') == -1):
            request.browserType = 'nokia'
            if not user_agent.find('applewebkit') == -1:
                request.browserGroup = 'smart_phone'
            else:
                request.browserGroup = 'feature_phone'
        else:
            request.browserType = ''
            request.browserGroup = ''