import hashlib
import urllib2
import urllib

class Mail:
    '''
    @init
    '''
    def __init__(self, mail_configs):
        self.sign_type = 'normal'
        self.mail_configs = mail_configs
        self.signature = ''
    
    '''
    @createSignature
    '''
    def __create_signature(self, request):
        if self.sign_type == 'normal':
            self.signature = self.mail_configs['appkey']
        else:
            self.__build_signature(request)

    '''
    @buildSignature
    '''
    def __build_signature(self, request):
        appid = self.mail_configs['appid']
        appkey = self.mail_configs['appkey']
        para_keys = request.keys();
        para_keys.sort()
        sign_str = ''
        for key in para_keys:
            if key.find('attachments') == -1:
                sign_str += "%s=%s&"%(key,request[key])
        sign_str = appid+appkey+sign_str[:-1]+appid+appkey
        if self.sign_type == 'md5':
            hash=hashlib.md5()
            hash.update(sign_str)
            self.signature = hash.hexdigest()
        elif self.sign_type == 'sha1':
            hash=hashlib.sha1() 
            hash.update(sign_str)
            self.signature = hash.hexdigest()

    def __http_get(self,url):
        return eval(urllib2.urlopen(url = url).read())

    def __http_post(self, url, para):
        data = urllib.urlencode(para) 
        return eval(urllib2.urlopen(url=url,data = data).read())
         
    '''
    @getTimestamp
    '''
    def get_timestamp(self):
        api = 'https://api.submail.cn/service/timestamp.json'
        resp = self.__http_get(api)
        return resp['timestamp']

    '''
    @Send
    '''
    def send(self,request):
        '''
        @setup API httpRequest URI
        '''
        api = 'https://api.submail.cn/mail/send.json'

        '''
        create final API post query Start
        '''
        request['appid'] = self.mail_configs['appid']

        '''
        @get timestamp from server
        '''
        request['timestamp'] = self.get_timestamp()

        '''
        @setup sign_type
        '''
        sign_type_state = ['normal','md5','sha1']
        if self.mail_configs.has_key('sign_type') == False:
            self.sign_type = 'normal'
        elif self.mail_configs['sign_type'] not in sign_type_state:
            self.sign_type = 'normal'
        else:
            self.sign_type = self.mail_configs['sign_type'] 
            request['sign_type'] = self.mail_configs['sign_type']

        '''
        @create signature
        '''
        self.__create_signature(request)
        request['signature'] = self.signature

        '''
        create final API post query End
        '''

        print request
        '''
        @send request
        '''
        return self.__http_post(api, request)
        
    '''
    @xsend
    '''
    def xsend(self, request):
        '''
        @setup API httpRequest URI
        '''
        api = 'https://api.submail.cn/mail/send.json'


        '''
        create final API post query Start
        '''
        request['appid'] = self.mail_configs['appid']

        '''
        @get timestamp from server
        '''
        request['timestamp'] = self.get_timestamp()

        '''
        @setup sign_type
        '''
        sign_type_state = ['normal','md5','sha1']
        if self.mail_configs.has_key('sign_type') == False:
            self.sign_type = 'normal'
        elif self.mail_configs['sign_type'] not in sign_type_state:
            self.sign_type = 'normal'
        else:
            self.sign_type = self.mail_configs['sign_type'] 
            request['sign_type'] = self.mail_configs['sign_type']

        '''
        @create signature
        '''
        self.__create_signature(request)
        request['signature'] = self.signature

        '''
        create final API post query End
        '''

        '''
        @send request
        '''
        return self.__http_post(api, request)

    '''
    addressbook/mail/subscribe
    '''
    def subscribe(self, request):
        '''
        @setup API httpRequest URI
        '''
        api='https://api.submail.cn/addressbook/mail/subscribe.json'

        '''
        create final API post query Start
        '''
        request['appid'] = self.mail_configs['appid']

        '''
        @get timestamp from server
        '''
        request['timestamp'] = self.get_timestamp()
        
        '''
        @setup sign_type
        '''
        sign_type_state = ['normal','md5','sha1']
        if self.mail_configs.has_key('sign_type') == False:
            self.sign_type = 'normal'
        elif self.mail_configs['sign_type'] not in sign_type_state:
            self.sign_type = 'normal'
        else:
            self.sign_type = self.mail_configs['sign_type'] 
            request['sign_type'] = self.mail_configs['sign_type']

        '''
        @create signature
        '''
        self.__create_signature(request)
        request['signature'] = self.signature

        '''
        '''

        '''
        @subscribe request
        '''
        return self.__http_post(api, request)

    '''
    addressbook/mail/unsubscribe
    '''
    def unsubscribe(self, request):
        '''
        @setup API httpRequest URI
        '''
        api='https://api.submail.cn/addressbook/mail/unsubscribe.json'

        '''
        create final API post query Start
        '''
        request['appid'] = self.mail_configs['appid']

        '''
        @get timestamp from server
        '''
        request['timestamp'] = self.get_timestamp()
        
        '''
        @setup sign_type
        '''
        sign_type_state = ['normal','md5','sha1']
        if self.mail_configs.has_key('sign_type') == False:
            self.sign_type = 'normal'
        elif self.mail_configs['sign_type'] not in sign_type_state:
            self.sign_type = 'normal'
        else:
            self.sign_type = self.mail_configs['sign_type'] 
            request['sign_type'] = self.mail_configs['sign_type']

        '''
        @create signature
        '''
        self.__create_signature(request)
        request['signature'] = self.signature

        '''
        create final API post query End
        '''

        '''
        @unsubscribe request
        '''
        return self.__http_post(api, request)



'''
if __name__ == '__main__':
       mail_obj = Mail()
       print mail_obj.get_timestamp()
'''
