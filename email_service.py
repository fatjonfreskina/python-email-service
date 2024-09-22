import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import logging

logging.basicConfig(level=logging.INFO)

def format_to_html(subject: str, body: str, sender:str, name: str) -> str:
    """
    Converts a plain text email body to HTML.
    """
    return """
    <html>
    <head></head>
    <body>
        <h1>Hai un nuovo messagio di posta dal sito web.</h1>
        <h2>Oggetto: {}</h2>
        <p>Nome: {}</p>
        <p>Email: {}</p>
        <p>Testo: {}</p>
    </body>
    </html>
    """.format(subject, name, sender, body)


def send_email(to, subject, name, body, sender, smtp_password) -> bool:
    """
    Sends an email to the specified recipient with the specified subject and body.
    """
    # Set up email headers
    from_address = 'fatjon.developer@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to
    msg['Subject'] = subject

    # Convert email body to HTML
    html_body = format_to_html(subject=subject, body=body, name=name, sender=sender)
    # Add email body as plain text
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Set up SMTP connection and send email
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'fatjon.developer@gmail.com'
        smtp_password = smtp_password
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)
        smtp_connection.sendmail(from_address, to, msg.as_string())
        smtp_connection.quit()
        return True
    except Exception as e:
        logging.INFO(f"Error sending email: {e}")
        return False