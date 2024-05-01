from flask import Flask, request
import requests
from email_service import *
from dotenv import load_dotenv
import logging, os, sys

load_dotenv()
password = os.getenv('SMTP_PASSWORD')                   # The password for the email application
receiver = 'fatjonfreskina@gmail.com'                   # The email address where you want to receive emails
portfolio_token = os.getenv('PORTFOLIO_TOKEN')          # The token for the RDSRLS email service

tokens_to_email = {}
tokens_to_email[portfolio_token] =  "fatjonfreskina@gmail.com"

app = Flask(__name__)

@app.route('/forward-email', methods=['POST'])
def incoming_email():
    """Expected json format:
    {
        "token": "token",
        "subject": "subject",
        "text": "text",
        "name": "name",
        "from": "from"
    }
    """
    email = request.get_json()
    # Check if the token is valid
    if email['token'] not in tokens_to_email:
        return 'Invalid token', 401

    email_subject = email['subject']
    email_body = email['text']
    name = email['name']
    email_from = email['from']

    last_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    result = send_email(to=tokens_to_email[email['token']], subject=email_subject, name=name, body=email_body, sender=email_from ,smtp_password=password)
    if result:
        return 'Email sent', 200
    else:
        return 'Email not sent', 500

@app.route('/test', methods=['GET'])
def test():
    return 'Test successful', 200
    
if __name__ == '__main__':
    app.run()