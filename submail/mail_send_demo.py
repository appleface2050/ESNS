'''
Submail mail/send API demo
SUBMAIL SDK Version 1.0.1 --python
copyright 2011 - 2014 SUBMAIL
'''
from mail_send import MAILSend
from app_configs import MAIL_CONFIGS

'''
init MESSAGEXsend class
'''
submail = MAILSend(MAIL_CONFIGS)

'''
Optional para
The First para: recipient email address
The second para: recipient name(optional)
@Multi-para
'''
submail.add_to('leo@submail.cn','leo')
submail.add_cc('mailer@submail.cn')
submail.add_bcc('leo@drinkfans.com')

'''
Optional para
set addressbook sign : Optional
add addressbook contacts to Multi-Recipients
@Multi-para
'''
#submail.add_address_book('subscribe')

'''
Optional para
set sender address and name
The First para: sender email address
The second para: sender display name (optional)
'''
submail.set_sender('no-reply@submail.cn','SUBMAIL')

'''
Optional para
set reply address
'''
submail.set_reply('service@submail.cn')

'''
Optional para
set email text content
'''
submail.set_text('test SDK text')

'''
Optional para
set email html content
'''
submail.set_html('test sdk html')

'''
Optional para
set email subject
'''
submail.set_subject('test SDK')


'''
Optional para
submail email text content filter
@Multi-para
'''
#submail.add_var('name','leo')
#submail.add_var('age','32')

'''
Optional para
submail email link content filter
@Multi-para
'''
#submail.add_link('developer','http://submail.cn/chs/developer')
#submail.add_link('store','http://submail.cn/chs/store')

'''
Optional para
email headers
@Multi-para
'''
#submail.add_headers('X-Accept','zh-cn')
#submail.add_headers('X-Mailer','leo App')

'''
Optional para
Attachment
@file path
@Multi-para
'''
submail.add_attachment('/root/test')
submail.add_attachment('/roo/test1')
print submail.send()
