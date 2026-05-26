import smtplib
from email.message import EmailMessage
from config import Config


def send_email(to_email, subject, body):
    if not all([Config.SMTP_HOST, Config.SMTP_PORT, Config.SMTP_USER, Config.SMTP_PASSWORD, Config.EMAIL_FROM]):
        raise ValueError('SMTP configuration is incomplete.')

    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = Config.EMAIL_FROM
    message['To'] = to_email
    message.set_content(body)

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as smtp:
        if Config.SMTP_USE_TLS:
            smtp.starttls()
        smtp.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        smtp.send_message(message)
