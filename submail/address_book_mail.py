from mail import Mail
class ADDRESSBOOKMail:
    '''
    Init appid,appkey,sign_type(Optional)
    '''
    def __init__(self,configs):
        self.configs = configs
        self.appid = configs['appid']
        self.appkey = configs['appkey']
        self.sign_type = ''
        if configs['sign_type'] != '':
            self.sign_type = configs['sign_type']
        self.address = ''
        self.target = ''
    
    '''
    set name and address
    '''
    def set_address(self, address, name=''):
        self.address = name+'<'+address+'>'

    '''
    set target
    '''
    def set_address_book(self, target):
        self.target = target

    '''
    build request array
    '''
    def build_request(self):
        request = {}
        '''
        set subscribe address
        '''
        request['address'] = self.address

        '''
        set target addressbook
        '''
        if self.target != '':
            request['target'] = self.target
        return request

    '''
    @subscribe
    '''
    def subscribe(self):
        mail_configs = {}
        '''
        set appid and appkey
        '''
        mail_configs['appid'] = self.appid
        mail_configs['appkey'] = self.appkey

        '''
        set sign_type,if is set
        '''
        if self.sign_type != '':
            mail_configs['sign_type'] = self.sign_type

        '''
        init mail class
        '''
        addressbook = Mail(mail_configs)

        '''
        build request and send email and return the result
        '''
        return addressbook.subscribe(self.build_request())

    '''
    @unsubscribe
    '''
    def unsubscribe(self):
        mail_configs = {}
        '''
        set appid and appkey
        '''
        mail_configs['appid'] = self.appid
        mail_configs['appkey'] = self.appkey

        '''
        set sign_type,if is set
        '''
        if self.sign_type != '':
            mail_configs['sign_type'] = self.sign_type

        '''
        init mail class
        '''
        addressbook = Mail(mail_configs)

        '''
        build request and send email and return the result
        '''
        return addressbook.unsubscribe(self.build_request())

