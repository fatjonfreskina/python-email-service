import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging
from flask import current_app as app
from formatters import format_to_html_website, format_to_html_password_reset

logging.basicConfig(level=logging.INFO)

def send_email_unsafe(to, subject, name, body, sender) -> bool:
    """
    Sends an email to the specified recipient with the specified subject and body.
    """
    # Set up email headers
    smtp_username = app.config['SMTP_USERNAME']
    smtp_password = app.config['SMTP_PASSWORD']
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to
    msg['Subject'] = subject

    # Convert email body to HTML
    html_body = format_to_html_website(subject=subject, body=body, name=name, sender=sender)
    # Add email body as plain text
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Set up SMTP connection and send email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(from_address, to, msg.as_string())
        smtp_connection.quit()
        return True
    except Exception as e:
        logging.INFO(f"Error sending email: {e}")
        return False
    
def send_reset_password_email(to, subject, reset_link) -> bool:
    """
    Sends an email to the specified recipient with the specified subject and body.
    """
    # Set up email headers
    smtp_username = app.config['SMTP_USERNAME']
    smtp_password = app.config['SMTP_PASSWORD']
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to
    msg['Subject'] = subject

    # Convert email body to HTML
    html_body = format_to_html_password_reset(reset_link)
    # Add email body as plain text
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Set up SMTP connection and send email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(smtp_username, to, msg.as_string())
        smtp_connection.quit()
        return True
    except Exception as e:
        logging.INFO(f"Error sending email: {e}")
        return False