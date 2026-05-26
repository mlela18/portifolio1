from flask import Blueprint, request, jsonify
from datetime import datetime
from config import Config
from database import insert_contact, fetch_all_contacts, fetch_contact_by_id, set_contact_reply
from mailer import send_email

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/contact', methods=['POST'])
def contact():
    """
    Handle contact form submissions
    Expected JSON: {
        "name": "string",
        "email": "string",
        "message": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'error': 'Missing required fields: name, email, message'}), 400

        timestamp = datetime.utcnow().isoformat()
        contact_id = insert_contact(
            name=data['name'],
            email=data['email'],
            message=data['message'],
            timestamp=timestamp
        )

        return jsonify({
            'success': True,
            'message': 'Contact message received',
            'id': contact_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/contact/all', methods=['GET'])
def get_all_contacts():
    """Get all contact submissions (for admin purposes)"""
    try:
        contacts = fetch_all_contacts()
        return jsonify({
            'success': True,
            'count': len(contacts),
            'contacts': contacts
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/contact/reply', methods=['POST'])
def reply_contact():
    """Send a reply to a contact message and save the reply."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['id', 'reply']):
            return jsonify({'error': 'Missing required fields: id, reply'}), 400

        contact = fetch_contact_by_id(data['id'])
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404

        reply_text = data['reply']
        reply_timestamp = datetime.utcnow().isoformat()
        updated = set_contact_reply(data['id'], reply_text, reply_timestamp)

        if updated == 0:
            return jsonify({'error': 'Unable to save reply'}), 500

        email_body = data.get('email_body') or (
            f"Hello {contact['name']},\n\n"
            f"Thank you for your message.\n\n{reply_text}\n\n"
            "Best regards,\nYour Portfolio Team"
        )
        subject = data.get('subject', 'Re: Your portfolio message')

        if Config.SMTP_HOST and Config.SMTP_USER and Config.SMTP_PASSWORD and Config.EMAIL_FROM:
            send_email(contact['email'], subject, email_body)
            email_status = 'Email notification sent.'
        else:
            email_status = 'Reply saved. SMTP not configured, email not sent.'

        return jsonify({
            'success': True,
            'message': 'Reply saved.',
            'email_status': email_status
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'API is running'}), 200
