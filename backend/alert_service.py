import os
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
from datetime import datetime

class AlertManager:
    def __init__(self):
        # Twilio configuration
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # SendGrid configuration
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'alerts@rockfall-system.com')
        
        # Initialize clients
        self.twilio_client = None
        self.sendgrid_client = None
        
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        
        if self.sendgrid_api_key:
            self.sendgrid_client = SendGridAPIClient(api_key=self.sendgrid_api_key)
        
        # Load contact list
        self.contacts = self.load_contacts()
    
    def load_contacts(self):
        """Load emergency contacts from configuration"""
        try:
            with open('config/emergency_contacts.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default contacts for demonstration
            return {
                'emergency_contacts': [
                    {
                        'name': 'Mine Safety Manager',
                        'phone': '+1234567890',
                        'email': 'safety@mine.com',
                        'role': 'primary'
                    },
                    {
                        'name': 'Operations Manager',
                        'phone': '+1234567891',
                        'email': 'operations@mine.com',
                        'role': 'secondary'
                    }
                ]
            }
    
    def send_alert(self, alert):
        """Send alert via SMS and email"""
        message = self.format_alert_message(alert)
        
        # Send to all emergency contacts
        for contact in self.contacts['emergency_contacts']:
            # Send SMS
            if self.twilio_client and contact.get('phone'):
                self.send_sms(contact['phone'], message)
            
            # Send Email
            if self.sendgrid_client and contact.get('email'):
                self.send_email(contact['email'], f"Rockfall Alert - {alert.severity}", message)
        
        print(f"Alert sent: {alert.alert_type} - {alert.severity}")
    
    def send_sms(self, phone_number, message):
        """Send SMS alert"""
        try:
            if self.twilio_client:
                message = self.twilio_client.messages.create(
                    body=message,
                    from_=self.twilio_phone_number,
                    to=phone_number
                )
                print(f"SMS sent to {phone_number}: {message.sid}")
            else:
                print(f"SMS would be sent to {phone_number}: {message}")
        except Exception as e:
            print(f"Error sending SMS: {e}")
    
    def send_email(self, to_email, subject, content):
        """Send email alert"""
        try:
            if self.sendgrid_client:
                message = Mail(
                    from_email=self.from_email,
                    to_emails=to_email,
                    subject=subject,
                    html_content=self.format_email_content(content)
                )
                response = self.sendgrid_client.send(message)
                print(f"Email sent to {to_email}: {response.status_code}")
            else:
                print(f"Email would be sent to {to_email}: {subject}")
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def format_alert_message(self, alert):
        """Format alert message for SMS"""
        timestamp = alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        location_info = ""
        
        if alert.location:
            try:
                location_data = json.loads(alert.location)
                if location_data:
                    location_info = f" at coordinates {location_data[0].get('lat', 'N/A')}, {location_data[0].get('lng', 'N/A')}"
            except:
                pass
        
        message = f"""
🚨 ROCKFALL ALERT 🚨
Severity: {alert.severity}
Type: {alert.alert_type}
Time: {timestamp}
Location: {location_info}
Message: {alert.message}

Please take immediate action as per safety protocols.
        """.strip()
        
        return message
    
    def format_email_content(self, content):
        """Format content for email with HTML"""
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #d32f2f;">🚨 Rockfall Alert System</h2>
            <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0;">
                <pre style="font-family: Arial, sans-serif; white-space: pre-wrap;">{content}</pre>
            </div>
            <p><strong>This is an automated alert from the AI-Based Rockfall Prediction System.</strong></p>
            <p>For more information, please check the dashboard or contact the system administrator.</p>
        </body>
        </html>
        """
        return html_content
    
    def send_test_alert(self):
        """Send a test alert to verify system functionality"""
        from models import Alert
        
        test_alert = Alert(
            alert_type='SYSTEM_TEST',
            severity='LOW',
            message='This is a test alert to verify the notification system is working correctly.',
            location='{"test": true}'
        )
        
        self.send_alert(test_alert)
        return "Test alert sent successfully"