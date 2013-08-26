from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class Mail:
    """
    Helper class for structuring the SMTP mail sending layer
    """

    def __init__(self,
                 user_real_name,
                 user_email,
                 **kwargs):

        #smtp settings
        self.smtp_server_host = "smtp.mandrillapp.com"
        self.smtp_server_port = 587
        self.smtp_username = None
        self.smtp_passwd = None

        #user settings
        self.user_real_name = user_real_name
        self.reply_to = user_email

        #internal
        self._s = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def _msg(self, recipient_email, subject):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "%s <%s>" % (self.user_real_name, self.reply_to)
        msg['To'] = recipient_email
        msg.add_header('reply-to', self.reply_to)
        return msg

    def _smtp(self):
        if self._s is None:
            self._s = smtplib.SMTP(self.smtp_server_host, self.smtp_server_port)
            self._s.login(self.smtp_username, self.smtp_passwd)
        return self._s

    def close(self):
        if self._s is not None:
            self._s.quit()
            self._s = None

    def wrap(self, http_text):
        return "<font face='sans-serif'>%s</font>" % (http_text)

    def send(self, recipient_email, subject, html_text):
        wrapped_text = self.wrap(html_text)
        msg = self._msg(recipient_email, subject)
        mime_text = MIMEText(wrapped_text, 'html', 'utf-8')
        msg.attach(mime_text)
        print "Sending email to %s" % (recipient_email)
        self._smtp().sendmail(msg['From'], msg['To'], msg.as_string())