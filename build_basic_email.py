#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter12/build_basic_email.py(作者github)
# (熊):原程式碼來自作者github，我只是加以修改

import email.message, email.policy, email.utils, sys

text = """Hello,
This is a basic message from Chapter 12.
 - Anonymous"""

def main():
    choose = input('是否有要設定"domain="(y/n) ')
    if choose == 'y' or choose == 'yes':
        message = email.message.EmailMessage(email.policy.SMTPUTF8)
    else:
        message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Test Message, Chapter 12'
    message['Date'] = email.utils.formatdate(localtime=True)
    if choose == 'y' or choose == 'yes': #要設定
        message['Message-ID'] = email.utils.make_msgid(domain='(*ˇωˇ*人)')
    else:
        message['Message-ID'] = email.utils.make_msgid()
    message.set_content(text)
    sys.stdout.buffer.write(message.as_bytes())
    
    print('\n\n這邊用來看as_bytes在幹嘛用的')
    print(message.as_bytes())
    print('\n{!r}'.format(text))

    import os, time
    print('\n\n看time、PID')
    print('time:', time.time()) #當前時間的時間戳記（1970 後經過的浮點秒數）
    print('PID:', os.getpid())

if __name__ == '__main__':
    main()

