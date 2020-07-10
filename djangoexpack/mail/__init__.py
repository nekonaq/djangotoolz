import email.parser
from django.core import mail
from django.core.mail.message import (
    utf8_charset,                          # utf-8, base64
    utf8_charset_qp,                       # utf-8, quoted pritable
)
from django.template.loader import render_to_string

__all__ = (
    'utf8_charset',
    'utf8_charset_qp',
    'EmailTemplated',
)


class EmailTemplated(mail.EmailMultiAlternatives):
    template_name = None

    def __init__(self, template_name=None, context=None, encoding=None, from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, alternatives=None,
                 cc=None, reply_to=None):

        # テンプレートを render() した結果を解析して subject と from を取り出す
        body_text = render_to_string(template_name or self.template_name, context=context)
        body_message = email.parser.Parser().parsestr(body_text)

        super().__init__(
            body='',
            subject=body_message.get('subject', ''),
            from_email=from_email or body_message.get('from', ''),
            to=to, bcc=bcc, connection=connection,
            attachments=attachments, headers=headers, cc=cc, reply_to=reply_to,
        )
        self.encoding = encoding or utf8_charset_qp
        self.alternatives.insert(0, (body_message.get_payload(), 'text/plain'))


'''
# EmailTemplated を使ってテンプレートからメッセージを組み立てる
>>> from djangoexpack.mail import EmailTemplated

>>> import pyotp
>>> authcode = '-'.join([pyotp.random_base32(length=4) for _ in range(2)])
>>> authcode

>>> msg = EmailTemplated(template_name='sendemail/message.eml', context={'authcode': authcode}, to=['feel.nak@gmail.com'])
>>> print(msg.message())

>>> msg.send()

'''

'''
# テンプレートからメッセージを組み立てる //OK
>>> from django.template.loader import get_template
>>> to = get_template('sendemail/message.eml')

>>> import pyotp
>>> authcode = '-'.join([pyotp.random_base32(length=4) for _ in range(2)])
>>> authcode

>>> text = to.render({'authcode': authcode})
>>> print(text)

>>> from email.parser import Parser
>>> msgorig = Parser().parsestr(text)
>>> msgorig_from = msg['from'] or ''
>>> msgorig_from
'"MN-Station クラウドサービス" <mnstation@nekonaq.com>'

>>> msgorig_subj = msgorig['subject'] or ''
>>> msgorig_subj
'MN-Station クラウド確認コード'

>>> from django.core import mail
>>> msg = mail.EmailMultiAlternatives(subject=msgorig['subject'] or '', from_email=msgorig['from'] or '', to=['feel.nak@gmail.com'])
>>> msg.encoding = mail.message.utf8_charset_qp
>>> msg.attach_alternative(msgorig.get_payload(), 'text/plain')
>>> print(msg.message())

>>> msg.send()

'''


'''
# EmailMultiAlternatives を使いたい#2 //送信まわりはこれでOK
# - multipart/alternatives の MIME part で utf-8 quoted-printable なメッセージ本体とするやり方。
>>> from django.core import mail

>>> msg = mail.EmailMultiAlternatives(subject='Hello', to=['feel.nak@gmail.com'])
>>> msg.encoding = mail.message.utf8_charset_qp  # alternative の内容を quoted-printable にする
>>> msg.attach_alternative("めっせーじひあ", 'text/plain')
>>> print(msg.message())
>>> msg.send()

'''

'''
# EmailMultiAlternatives を使いたい#1
# EmailMultiAlternatives.attach_alternatives(content, mimietype)
# でアタッチした content の MIME part は次のメソッドで変換する。
# _create_mime_attachment(content, mimetype)
# そこで、このメソッドで意図通りの MIME part が生成できるか調査する。
#   => mimetype のベースタイプが 'text' であれば SafeMIMEText(content, subtype, encoding) が返るはず。

>>> from django.core import mail
>>> msg = mail.EmailMultiAlternatives(subject='Hello', body='Body goes here', to=['feel.nak@gmail.com'])

#// encoding を指定してうまくいった。
# settings.DEFAULT_CHARSET でデフォルトの encoding を指定できるが、
# HttpResponse に影響してしまうので Email オブジェクトで指定する。

>>> msg.encoding = mail.message.utf8_charset_qp
>>> mm = msg._create_mime_attachment("めっせーじひあ", 'text/plain')
>>> print(mm.as_string())
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable

=E3=82=81=E3=81=A3=E3=81=9B=E3=83=BC=E3=81=98=E3=81=B2=E3=81=82

#-------------------------------------------------------
# デフォルトの状態
>>> mm = msg._create_mime_attachment("めっせーじひあ", 'text/plain')
>>> print(mm.as_string())
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit

めっせーじひあ

'''

'''
# SafeMIMEText で text/plan; utf-8; quoted-printable なメッセージを組み立てる

>>> from django.core import mail
>>> mt = mail.SafeMIMEText("めっせーじひあ")
>>> print(mt.as_string())
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit

めっせーじひあ

>>> mt = mail.SafeMIMEText("めっせーじひあ", _charset=mail.message.utf8_charset_qp)
>>> print(mt.as_string())
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable

=E3=82=81=E3=81=A3=E3=81=9B=E3=83=BC=E3=81=98=E3=81=B2=E3=81=82

'''

'''
# EmailMessage または EmailMultiAlternatives を send() してメールを送信する

>>> from django.core.mail import EmailMessage, EmailMultiAlternatives

>>> msg = EmailMultiAlternatives(subject='Hello', body='Body goes here', to=['feel.nak@gmail.com'])
>>> msg.send()

#// use settings.DEFAULT_FROM_EMAIL
# NOTE: EmailMessage() の引数は名前付きにしたほうがトラブルを回避しやすい。

>>> msg = EmailMessage(subject='Hello', body='Body goes here', to=['feel.nak@gmail.com'])
>>> msg.send()

#-----------------------------------------------------------------------------
>>> msg = EmailMessage('Hello', 'Body goes here', '"MN-Station Cloud Service" <mnstation@nekonaq.com>', ['feel.nak@gmail.com'])
>>> msg = EmailMessage('Hello', 'Body goes here', 'MN-Station クラウド<mnstation@nekonaq.com>', ['feel.nak@gmail.com'])
>>> msg = EmailMessage('Hello', 'Body goes here', 'mnstation@nekonaq.com', ['feel.nak@gmail.com'])
>>> msg = EmailMessage('Hello', 'Body goes here', 'from@example.com', ['to@example.com'])

'''
