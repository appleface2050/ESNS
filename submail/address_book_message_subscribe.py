'''
Submail addressbook/message/unsubscribe API demo
SUBMAIL SDK Version 1.0.1 --python
copyright 2011 - 2014 SUBMAIL
'''
from app_configs import MESSAGE_CONFIGS
from address_book_message import ADDRESSBOOKMessage
'''
init MESSAGEXsend class
'''
addressbook = ADDRESSBOOKMessage(MESSAGE_CONFIGS)

'''
Required para
The First para: recipient email address
The second para: recipient name(optional)
'''
addressbook.set_address('18616761889')

'''
Optional para
set target addressbook sign : Optional
default value: subscribe
'''
#addressbook.set_address_book('subscribe')
print addressbook.subscribe()
