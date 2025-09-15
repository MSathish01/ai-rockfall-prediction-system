#!/usr/bin/env python3
"""
Simple Gmail Test for icanhelpyou009@gmail.com
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def test_gmail_alert():
    """Test Gmail SMTP for icanhelpyou009@gmail.com"""
    
    # Gmail credentials (update these)
    gmail_user = "icanhelpyou009@gmail.com"  # Your Gmail
    gmail_password = "your_app_password_here"  # Replace with 16-char app password
    
    print("📧 Testing Gmail SMTP Alert System")
    print("=" * 40)
    print(f"From: {gmail_user}")
    print(f"To: icanhelpyou009@gmail.com")
    
    # Create test message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = "icanhelpyou009@gmail.com"
    msg['Subject'] = "🧪 TEST - Rockfall Alert System"
    
    test_message = f"""
🧪 TEST ALERT - Rockfall Prediction System

This is a test email to verify your FREE Gmail SMTP alert system.

Test Details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- From: {gmail_user}
- To: icanhelpyou009@gmail.com
- Phone: +916384574029
- Status: Gmail SMTP Test ✅

🚨 SAMPLE ROCKFALL ALERT 🚨
Severity: HIGH
Probability: 78%
Location: Zone A - North Wall
Action Required: IMMEDIATE

If you receive this email, your alert system is working!

Dashboard: http://localhost:3000
Cost: ₹0 (100% FREE!)
    """
    
    msg.attach(MIMEText(test_message, 'plain'))
    
    try:
        # Gmail SMTP
        context = ssl.create_default_context()
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, "icanhelpyou009@gmail.com", text)
        
        print("✅ SUCCESS! Test email sent to icanhelpyou009@gmail.com")
        print("📱 Check your email inbox")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        print("\n🔧 Setup Instructions:")
        print("1. Enable 2FA on Gmail")
        print("2. Generate App Password")
        print("3. Update gmail_password in this script")
        return False

if __name__ == "__main__":
    test_gmail_alert()