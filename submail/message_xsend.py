#coding=utf-8
import threading
from message import Message
import json

class MESSAGEXsend:
    '''
    @set vars start
    '''
    def __init__(self, configs):
        '''
        Submail mail appid
        @type string
        '''
        self.appid = configs['appid']

        '''
        Submail mail appkey
        @type string
        '''
        self.appkey = configs['appkey']

        '''
        sign type (Optional)
        @options: normal or md5 or sha1
        '''
        self.sign_type = ''
        if configs.has_key('sign_type') == True:
            self.sign_type = configs['sign_type']

        '''
        to: email recipient
        @array to rfc 822
        '''
        self.to = []

        '''
        add email recipient from addressbook
        @array to string
        '''
        self.address_book = []

        '''
        email project sign
        '''
        self.project = ''

        '''
        vars: the submail email text content filter
        @type array to json string
        '''
        self.vars = {}

    '''
    addTo function
    add message cellphone number
    '''
    def add_to(self, address):
        self.to.append(address)

    '''
    AddAddressbook function
    set addressbook sign to array
    '''
    def add_address_book(self,address_book):
        self.address_book.append(address_book)

    '''
    Set email project
    '''
    def set_project(self, project):
        self.project = project

    '''
    AddVar function
    set var to array
    '''
    def add_var(self, key, val):
        self.vars[key] = val

    '''
    build request array
    '''
    def build_request(self):
        request = {}
        '''
        convert To array to rfc 822 format
        '''
        if len(self.to) != 0: 
            request['to'] = ''
            for to in self.to:
                request['to'] += to + ','
            request['to'] = request['to'][:-1]
        
        '''
        convert Addressbook array to string
        '''
        if len(self.address_book) != 0:
            request['addressbook'] = '' 
            for address_book in self.address_book:
                request['addressbook'] += address_book+','
            request['addressbook'] = request['addressbook'][:-1]
      
        '''
        set project sign
        '''
        request['project'] = self.project

        '''
        convert vars array to json string, if is not empty
        '''
        if len(self.vars) != 0:
            request['vars'] = json.dumps(self.vars)

        return request
     
    '''
    xsend email
    '''
    def xsend(self):
        '''
        set appid and appkey
        使用新的线程 发送短信
        '''
        message_configs = {}
        message_configs['appid'] = self.appid
        message_configs['appkey'] = self.appkey

        '''
        set sign_type,if is set
        '''
        if self.sign_type != '':
            message_configs['sign_type'] = self.sign_type

        '''
        init mail class
        '''
        message = Message(message_configs)

        '''
        build request and send email and return the result
        '''
        result = message.xsend(self.build_request())
        # MessageThread(message).start()
        return result



class MessageThread(threading.Thread):
    """
    异步发送短信
    by:王健 at:2015-1-25
    """
    def __init__(self, message):
        self.message = message

        threading.Thread.__init__(self)

    def run(self):
        self.message.xsend(self.message.build_request())
