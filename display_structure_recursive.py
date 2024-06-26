import argparse, email.policy, sys


def walk(part, prefix=''):
    line = '{} type={}'.format(prefix, part.get_content_type())
    if not part.is_multipart():
        content = part.get_content()
        line += ' {} len={}'.format(type(content).__name__, len(content))
        cd = part['Content-Disposition']
        is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
        if is_attachment:
            line += ' attachment'
        filename = part.get_filename()
        if filename is not None:
            line += ' filename={!r}'.format(filename)
    print(line)

    for i, subpart in enumerate(part.iter_parts()): #go through its subpart
        walk(subpart, prefix + '.{}'.format(i))

def main(binary_file):
    policy = email.policy.SMTP
    message = email.message_from_binary_file(binary_file, policy=policy)
    walk(message) # recursive

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display MIME structure')
    parser.add_argument('filename', nargs='?', help='File containing an email')
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)
    else:
        with open(args.filename, 'rb') as f:
            main(f)
