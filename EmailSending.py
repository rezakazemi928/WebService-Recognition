import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sending_email(receiver, subject, token_id,sender = 'rezakazemy1377@gmail.com'):
    message = MIMEMultipart()
    message['from'] = sender
    message['to'] = receiver
    message['subject'] = subject
    message.attach(MIMEText(token_id + f' for {receiver}'))

    with smtplib.SMTP(host = 'smtp.gmail.com', port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, 'password')
        text = message.as_string()
        smtp.sendmail(sender, receiver, text)
        print(' An email has been Sent for the client')
