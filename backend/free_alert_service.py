import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
import os
from datetime import datetime

class FreeAlertService:
    """Free alert service using Gmail SMTP and free SMS APIs"""
    
    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def send_gmail_alert(self, to_email, subject, message):
        """Send email alert using Gmail SMTP (100% Free)"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(message, 'plain'))
            
            # Gmail SMTP configuration
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                text = msg.as_string()
                server.sendmail(self.gmail_user, to_email, text)
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email failed to {to_email}: {e}")
            return False
    
    def send_free_sms_textbelt(self, phone, message):
        """Send SMS using TextBelt (1 free SMS per day per phone)"""
        try:
            url = "https://textbelt.com/text"
            data = {
                'phone': phone,
                'message': message,
                'key': 'textbelt'  # Free tier key
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('success'):
                print(f"✅ SMS sent successfully to {phone}")
                return True
            else:
                print(f"❌ SMS failed to {phone}: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ SMS error to {phone}: {e}")
            return False
    
    def send_free_sms_way2sms(self, phone, message):
        """Send SMS using Way2SMS (Free for Indian numbers)"""
        try:
            # This is a mock implementation - Way2SMS requires web scraping
            # which can be unreliable. Use TextBelt or other services instead.
            print(f"📱 SMS would be sent to {phone} via Way2SMS")
            print(f"   Message: {message}")
            return True
            
        except Exception as e:
            print(f"❌ Way2SMS error: {e}")
            return False
    
    def send_whatsapp_message(self, phone, message):
        """Send WhatsApp message using CallMeBot (Free)"""
        try:
            # CallMeBot WhatsApp API (Free but requires setup)
            # You need to add the bot to your WhatsApp first
            api_key = os.getenv('CALLMEBOT_API_KEY', 'your_api_key')
            
            url = f"https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': phone,
                'text': message,
                'apikey': api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                print(f"✅ WhatsApp sent successfully to {phone}")
                return True
            else:
                print(f"❌ WhatsApp failed to {phone}")
                return False
                
        except Exception as e:
            print(f"❌ WhatsApp error: {e}")
            return False
    
    def send_telegram_message(self, chat_id, message):
        """Send Telegram message (100% Free)"""
        try:
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            if not bot_token:
                print("❌ Telegram bot token not configured")
                return False
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data)
            result = response.json()
            
            if result.get('ok'):
                print(f"✅ Telegram sent successfully to {chat_id}")
                return True
            else:
                print(f"❌ Telegram failed: {result.get('description', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False
    
    def send_discord_webhook(self, webhook_url, message):
        """Send Discord message via webhook (100% Free)"""
        try:
            data = {
                'content': message,
                'username': 'Rockfall Alert System'
            }
            
            response = requests.post(webhook_url, json=data)
            
            if response.status_code == 204:
                print("✅ Discord message sent successfully")
                return True
            else:
                print(f"❌ Discord failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Discord error: {e}")
            return False
    
    def send_comprehensive_alert(self, alert_data):
        """Send alert through all available free channels"""
        contacts = self.load_emergency_contacts()
        results = []
        
        # Format messages
        email_subject = f"🚨 ROCKFALL ALERT - {alert_data['severity']} - {alert_data.get('location', 'Unknown')}"
        email_message = self.format_email_message(alert_data)
        sms_message = self.format_sms_message(alert_data)
        
        for contact in contacts:
            contact_result = {
                'name': contact['name'],
                'methods': []
            }
            
            # Send Email (Gmail SMTP)
            if contact.get('email') and self.gmail_user:
                success = self.send_gmail_alert(contact['email'], email_subject, email_message)
                contact_result['methods'].append({
                    'type': 'email',
                    'destination': contact['email'],
                    'success': success
                })
            
            # Send SMS (TextBelt - 1 free per day)
            if contact.get('phone'):
                success = self.send_free_sms_textbelt(contact['phone'], sms_message)
                contact_result['methods'].append({
                    'type': 'sms',
                    'destination': contact['phone'],
                    'success': success
                })
            
            # Send Telegram (if configured)
            if contact.get('telegram_chat_id'):
                success = self.send_telegram_message(contact['telegram_chat_id'], email_message)
                contact_result['methods'].append({
                    'type': 'telegram',
                    'destination': contact['telegram_chat_id'],
                    'success': success
                })
            
            results.append(contact_result)
        
        return results
    
    def load_emergency_contacts(self):
        """Load emergency contacts from configuration"""
        try:
            with open('config/emergency_contacts.json', 'r') as f:
                config = json.load(f)
                return config['emergency_contacts']
        except Exception as e:
            print(f"❌ Error loading contacts: {e}")
            return []
    
    def format_email_message(self, alert_data):
        """Format alert for email"""
        return f"""ROCKFALL ALERT SYSTEM - {alert_data['severity']} PRIORITY

🚨 IMMEDIATE ATTENTION REQUIRED 🚨

Alert Details:
- Type: {alert_data.get('alert_type', 'ROCKFALL_WARNING')}
- Severity: {alert_data['severity']}
- Probability: {alert_data.get('probability', 0):.1%}
- Location: {alert_data.get('location', 'Unknown')}
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Description:
{alert_data.get('message', 'High rockfall risk detected')}

Recommended Actions:
{chr(10).join(['• ' + rec for rec in alert_data.get('recommendations', ['Check dashboard for details'])])}

This is an automated alert from the AI-Based Rockfall Prediction System.
Please take immediate action according to safety protocols.

Dashboard: http://localhost:3000
System Status: http://localhost:5000/api/health

---
Sent via Free Gmail SMTP Alert System"""
    
    def format_sms_message(self, alert_data):
        """Format alert for SMS (keep under 160 characters)"""
        return f"""🚨 ROCKFALL ALERT
{alert_data['severity']} - {alert_data.get('probability', 0):.0%}
Location: {alert_data.get('location', 'Unknown')}
Time: {datetime.now().strftime('%H:%M')}
IMMEDIATE ACTION REQUIRED!
Check dashboard: localhost:3000"""