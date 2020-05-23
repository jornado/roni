"""For sending mail."""
from __future__ import absolute_import

from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time

from config import Config

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SUBJECT = "The Rona Report: "
DATE_FORMAT = "%a %b %d"
EMAIL_SPACE = ", "
EMAIL_LIST = "./data/email_list.txt"


class Sender(object):
    """Email/Password struct."""

    def __init__(self):
        """Set up email/pass."""
        config = Config.get_config()
        self.email = config["gmail_email"]
        self.pswd = config["gmail_pswd"]


class Mailer(object):
    """Mail sending class."""

    def __init__(self):
        """Set up sender, recipients, date."""
        self.sender = self._get_sender()
        self.recipients = self._get_emails()
        self.date = date.today().strftime(DATE_FORMAT)

    @classmethod
    def get_subject(cls):
        return EMAIL_SUBJECT + " %s" % date.today().strftime(DATE_FORMAT)

    def login(self):
        """Log into Gmail."""
        self.gmail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self.gmail.ehlo()
        self.gmail.starttls()
        self.gmail.login(self.sender.email, self.sender.pswd)

    def send(self, to, msg):
        """Log in and send the email"""
        print "Emailing %s" % to
        self.gmail.sendmail(self.sender.email, [to], msg)

    def format_message(self, email, html):
        """Contruct the multipart email message."""
        msg = MIMEMultipart('alternative')
        text = "This is the Rona Report text."
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')

        msg.attach(part1)
        msg.attach(part2)

        msg['Subject'] = Mailer.get_subject()
        msg['From'] = self.sender.email
        msg['To'] = email

        return msg

    def send_to_list(self, html="Hi"):
        """Send the email."""
        print "Sending emails!"

        self.login()

        for email in self.recipients:
            if not email:
                continue

            # We must construct the full email here in the loop, else the 
            # To line contains all the addresses for some reason
            msg = self.format_message(email, html)
            self.send(email, msg.as_string())
            time.sleep(2)

        self.gmail.quit()

    def _get_sender(self):
        return Sender()

    def _get_emails(self):
        with open(EMAIL_LIST) as fh:
            return fh.read().split("\n")


if __name__ == "__main__":
    m = Mailer()
    data = """ \
<html><body>Hi</body></html>
        """
    m.send_to_list(data)
