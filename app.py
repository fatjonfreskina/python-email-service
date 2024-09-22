from flask import Flask, request, jsonify
import requests
from email_service import *
from dotenv import load_dotenv
import logging, os, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    # TODO: setup envs to work with .env file
    load_dotenv()
    app.config['SMTP_PASSWORD'] =   os.getenv('SMTP_PASSWORD')      # The password for the email application
    app.config['PORTFOLIO_TOKEN'] = os.getenv('PORTFOLIO_TOKEN')    # The token for the RDSRLS email service
    app.config['RECEIVER'] =        os.getenv('RECEIVER')           # The email address where you want to receive emails
    app.config['TOKENS_TO_EMAIL'] = {}
    app.config['TOKENS_TO_EMAIL'].update({app.config['PORTFOLIO_TOKEN']: app.config['RECEIVER']})
    
    for key in os.environ.keys():
        logging.info(f"Key: {key}, Value: {os.environ[key]}")

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
        if email['token'] not in app.config['TOKENS_TO_EMAIL']:
            return 'Invalid token', 401

        email_subject = email['subject']
        email_body = email['text']
        name = email['name']
        email_from = email['from']

        last_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        logging.info(f"Calling send_email with parameters \
            {app.config['TOKENS_TO_EMAIL'].get(email['token'])}, \
            {email_subject}, \
            {name}, \
            {email_body}, \
            {email_from}")
         
        result = send_email(
            to=app.config['TOKENS_TO_EMAIL'].get(email['token']),
            subject=email_subject, 
            name=name, 
            body=email_body, 
            sender=email_from,
            smtp_password=app.config['SMTP_PASSWORD'],
            )
        
        if result:
            return jsonify({
                'message': 'Email sent',
                }), 200
        else:
            return jsonify({
                'message': 'Email not sent', 
                }), 500
    return app