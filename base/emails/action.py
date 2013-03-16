import smtplib
from email.mime.text import MIMEText
from threading import Thread
from base.emails.default_config import GMAIL_USERNAME, GMAIL_PASSWD, GMAIL_NAME


GMAIL_SMTP_SERVER = 'smtp.gmail.com:587'


def send_email(to_email_addr, subject, text, async=True):
    __send_email(GMAIL_USERNAME, GMAIL_PASSWD, GMAIL_NAME, GMAIL_USERNAME, to_email_addr, subject, text, async)


def __send_email(username, password, from_name, from_email, to_email_opt_lis, subject, text, async=True):
    msg = MIMEText(text, 'html')
    msg["Subject"] = subject
    msg["To"] = to_email_opt_lis
    msg["From"] = "%s <%s>" % (from_name, from_email)
    if async:
        t = Thread(target=_send_gmail, args=(username, password, from_email, to_email_opt_lis, msg.as_string()))
        t.setDaemon(False)
        t.start()
    else:
        _send_gmail(username, password, from_email, to_email_opt_lis, msg.as_string())


def _send_gmail(username, password, from_addr, to_addr, msg):
    server = smtplib.SMTP(GMAIL_SMTP_SERVER)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, msg)
    server.quit()