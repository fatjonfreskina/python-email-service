from flask import Flask, request, jsonify
import requests
from email_service import *
from dotenv import load_dotenv
import logging, os, sys
from enum import Enum

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    backend_tokens = {
        os.getenv('AI_ASSISTANT_TOKEN')
    }
    
    app.config['SMTP_PASSWORD'] =   os.getenv('SMTP_PASSWORD')      # The password for the email application
    app.config['SMTP_USERNAME'] =   os.getenv('SMTP_USERNAME')      # The username for the email application
    app.config['RECEIVER'] =        os.getenv('RECEIVER')           # The email address where you want to receive emails

    # ! This is an unsafe endpoint. Should not be exposed to the internet.
    @app.route('/forward-email-website', methods=['POST'])
    def forward_email_contact_us():
        """Used for sending emails from the portfolio website. The sender is 'SMTP_USERNAME'
        and the receiver is 'RECEIVER' (will be he who owns the business of the website).
        
        
        Expected json format:
        {
            "subject": "subject",
            "text": "text",
            "name": "name",
            "from": "from"  # He who submitted the "Send email" form
        }
        """
        data = request.get_json()

        email_to = app.config['RECEIVER']
        email_subject = data['subject']
        email_body = data['text']
        name = data['name']
        email_from = data['from']
        
        if not email_to or not email_subject or not email_body or not name or not email_from:
            return jsonify({
                'message': 'Missing data',
                }), 400
        
        result = send_email(
            to=email_to,
            subject=email_subject,
            name=name,
            body=email_body,
            sender=email_from,
        )
        
        if result:
            return jsonify({
                'message': 'Email sent',
                }), 200
        else:
            return jsonify({
                'message': 'Email not sent', 
                }), 500
            
    @app.route('/forward-email-password-reset', methods=['POST'])
    def forward_email_password_reset():
        """Used for sending password reset emails. The sender is 'SMTP_USERNAME'
        
        Expected json format:
        {
            "email": "email",
            "link": "link",
            "token": "token"
        }

        Returns:
            _type_: _description_
        """
        
        data = request.get_json()
        
        if data.get('token', None) not in backend_tokens:
            return jsonify({
                'message': 'Unauthorized'
                }), 403
            
        to=data['email']
        email_subject = 'Password reset request'
        reset_link=data['link']
        
        if not to or not email_subject or not reset_link:
            return jsonify({
                'message': 'Missing data',
                }), 400
            
        result = send_reset_password_email(
            to=to,
            subject=email_subject,
            reset_link=reset_link,
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