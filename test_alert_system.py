#!/usr/bin/env python3
"""
Test Alert System - Send test alerts to configured contacts
"""

import sys
import os
import json
from datetime import datetime
import requests

# Add backend to path
sys.path.append('backend')

def load_emergency_contacts():
    """Load emergency contacts from configuration"""
    try:
        with open('config/emergency_contacts.json', 'r') as f:
            config = json.load(f)
            return config['emergency_contacts']
    except Exception as e:
        print(f"❌ Error loading contacts: {e}")
        return []

def send_test_sms(phone, message):
    """Send test SMS (mock implementation)"""
    print(f"📱 SMS Alert Sent to {phone}:")
    print(f"   Message: {message}")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("   Status: ✅ Delivered (Simulated)")
    print("-" * 50)

def send_test_email(email, subject, message):
    """Send test email (mock implementation)"""
    print(f"📧 Email Alert Sent to {email}:")
    print(f"   Subject: {subject}")
    print(f"   Message: {message}")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("   Status: ✅ Delivered (Simulated)")
    print("-" * 50)

def create_test_alert():
    """Create a test rockfall alert"""
    return {
        'alert_type': 'ROCKFALL_WARNING',
        'severity': 'HIGH',
        'probability': 0.78,
        'location': 'Zone A - North Wall',
        'coordinates': {'lat': -23.5505, 'lng': -46.6333},
        'timestamp': datetime.now(),
        'message': 'High rockfall risk detected in Zone A. Probability: 78%. Immediate attention required.',
        'recommendations': [
            'Evacuate personnel from Zone A immediately',
            'Halt all operations in the affected area',
            'Deploy emergency response team',
            'Monitor conditions continuously'
        ]
    }

def format_sms_message(alert):
    """Format alert for SMS"""
    return f"""🚨 ROCKFALL ALERT 🚨
Severity: {alert['severity']}
Location: {alert['location']}
Probability: {alert['probability']:.0%}
Time: {alert['timestamp'].strftime('%H:%M')}

{alert['message']}

IMMEDIATE ACTION REQUIRED!
Check dashboard for details."""

def format_email_message(alert):
    """Format alert for email"""
    recommendations_text = '\n'.join([f"• {rec}" for rec in alert['recommendations']])
    
    return f"""ROCKFALL ALERT SYSTEM - {alert['severity']} PRIORITY

Alert Details:
- Type: {alert['alert_type']}
- Severity: {alert['severity']}
- Probability: {alert['probability']:.1%}
- Location: {alert['location']}
- Coordinates: {alert['coordinates']['lat']}, {alert['coordinates']['lng']}
- Time: {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}

Description:
{alert['message']}

Recommended Actions:
{recommendations_text}

This is an automated alert from the AI-Based Rockfall Prediction System.
Please take immediate action according to safety protocols.

Dashboard: http://localhost:3000
API Status: http://localhost:5000/api/health"""

def main():
    """Main function to test alert system"""
    print("🚨 AI-Based Rockfall Prediction System - Alert Test")
    print("=" * 60)
    
    # Load contacts
    contacts = load_emergency_contacts()
    if not contacts:
        print("❌ No emergency contacts found!")
        return
    
    print(f"📋 Loaded {len(contacts)} emergency contacts")
    print()
    
    # Create test alert
    alert = create_test_alert()
    
    # Format messages
    sms_message = format_sms_message(alert)
    email_subject = f"🚨 ROCKFALL ALERT - {alert['severity']} - {alert['location']}"
    email_message = format_email_message(alert)
    
    # Send alerts to all contacts
    print("📤 Sending test alerts...")
    print()
    
    for contact in contacts:
        print(f"👤 Contact: {contact['name']} ({contact['role']})")
        
        # Send SMS
        if contact.get('phone'):
            send_test_sms(contact['phone'], sms_message)
        
        # Send Email
        if contact.get('email'):
            send_test_email(contact['email'], email_subject, email_message)
    
    print("✅ Alert test completed!")
    print()
    print("📝 Note: This is a simulation. To send real alerts, configure:")
    print("   - Twilio credentials for SMS")
    print("   - SendGrid API key for email")
    print("   - Update .env file with your API keys")

if __name__ == "__main__":
    main()