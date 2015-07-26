'''
Submail addressbook/mail/unsubscribe API demo
SUBMAIL SDK Version 1.0.1 --python
copyright 2011 - 2014 SUBMAIL
'''
from app_configs import MAIL_CONFIGS
from address_book_mail import ADDRESSBOOKMail
'''
init MESSAGEXsend class
'''
addressbook = ADDRESSBOOKMail(MAIL_CONFIGS)

'''
Required para
The First para: recipient email address
The second para: recipient name(optional)
'''
addressbook.set_address('leo@apple.cn','leo')

'''
Optional para
set target addressbook sign : Optional
default value: subscribe
'''
#addressbook.set_address_book('unsubscribe')
print addressbook.unsubscribe()
