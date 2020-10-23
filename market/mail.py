import json
import os
import smtplib

from market import settings
from email.message import EmailMessage


def send_email(to_email, subject, body):
    smtp_host = getattr(settings, 'SMTP_HOST', None)
    if smtp_host is None:
        return

    message = EmailMessage()
    message['To'] = to_email
    message['From'] = 'tilde_market'
    message['Subject'] = subject
    message.set_content(body)

    smtp = smtplib.SMTP(smtp_host)
    smtp.send_message(message)
    smtp.quit()


def send_template_email(username, template_name, **kwargs):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates/email')
    template_filename = os.path.join(template_dir, f"{template_name}.json")
    with open(template_filename) as template_file:
        template_data = json.load(template_file)
        subject = template_data['subject'].format(username=username, **kwargs)
        body = template_data['body'].format(username=username, **kwargs)
        send_email(username, subject, body)
