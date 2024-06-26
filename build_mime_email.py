#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter12/build_mime_email.py
# (熊):原程式碼來自作者github，我只是加以修改
import argparse, email.message, email.policy, email.utils, mimetypes, sys

plain = """Hello,
This is a MIME message from Chapter 12.
- Anonymous"""

html = """<p>Hello,</p>
<p>This is a <b>test message</b> from Chapter 12.</p>
<p>- <i>Anonymous</i></p>"""

img = """<p>This is the smallest possible blue GIF:</p>
<img src="cid:{}" height="80" width="80">"""

# Tiny example GIF from http://www.perlmonks.org/?node_id=7974
# 複製網址提供的程式碼，放到.pl檔
# 可以輸入'perl blue_dot.pl > blue_dot.gif'得到圖片(說實在我不知道這是在幹嘛)
blue_dot = (b'GIF89a1010\x900000\xff000,000010100\x02\x02\x0410;'
            .replace(b'0', b'\x00').replace(b'1', b'\x01'))

def main(args):
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'Test Recipient <recipient@example.com>'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Foundations of Python Network Programming'
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()
    boundary = '\033[33m============^^==========\033[0m'

    if not args.i:
        message.set_content(html, subtype='html')
        message.add_alternative(plain)
    else:
        # 此話來自課本
        # uses make_msgid() because the email module provides no specific facility for building unique content IDs
        cid = email.utils.make_msgid()  # RFC 2392: must be globally unique!
        message.set_content(html + img.format(cid.strip('<>')), subtype='html')
        message.add_related(blue_dot, 'image', 'gif', cid=cid,
                            filename='blue-dot.gif')
        message.add_alternative(plain)

    # 用以確保在設置 boundary 之前已經設置了 Content-Type 標頭
    # 不然先設置會造成email.errors.HeaderParseError
    # 在呼叫方法時內容類型未知，則 set_boundary() 方法將引發此錯誤
    message.set_boundary(boundary)

    for filename in args.filename:
        mime_type, encoding = mimetypes.guess_type(filename)
        if encoding or (mime_type is None):
            mime_type = 'application/octet-stream'
        main, sub = mime_type.split('/')
        if main == 'text':
            with open(filename, encoding='utf-8') as f:
                text = f.read()
            message.add_attachment(text, sub, filename=filename)
        else:
            with open(filename, 'rb') as f:
                data = f.read()
            message.add_attachment(data, main, sub, filename=filename)
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build, print a MIME email')
    parser.add_argument('-i', action='store_true', help='Include GIF image')
    parser.add_argument('filename', nargs='*', help='Attachment filename')
    main(parser.parse_args())
