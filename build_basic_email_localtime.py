#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter12/build_basic_email.py

# 目的 : 自定義時間

import email.message, email.policy, email.utils, sys
import time
text = """Hello,
This is a basic message from Chapter 12.
 - Anonymous"""

def main():
    choose = input('請問是否要自定義時間?(y/n)')
    now = None
    if choose == 'y' or choose == 'yes':
        now = time.mktime((2024,4,1,14,30,0,0,0,0))
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Test Message, Chapter 12'
    message['Date'] = email.utils.formatdate(localtime=True, timeval=now)
    message['Message-ID'] = email.utils.make_msgid()
    message.set_content(text)
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    main()
