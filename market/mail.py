import json
import os
import smtplib

from email.message import EmailMessage


def send_email(to_email, subject, body):
    message = EmailMessage()
    message['To'] = to_email
    message['From'] = 'tilde_market'
    message['Subject'] = subject
    message.set_content(body)

    smtp = smtplib.SMTP('localhost')
    smtp.send_message(message)
    smtp.quit()


def send_template_email(username, template_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_dir, 'templates/email')
    template_filename = os.path.join(template_dir, f"{template_name}.json")
    with open(template_filename) as template_file:
        template_data = json.load(template_file)
        subject = template_data['subject'].format(username=username)
        body = template_data.format(username=username)
        send_email(username, subject, body)
