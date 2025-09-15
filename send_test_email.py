#!/usr/bin/env python3
"""
Send test email to icanhelpyou009@gmail.com
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_test_rockfall_alert():
    """Send a test rockfall alert email"""
    
    # Email configuration
    sender_email = "icanhelpyou009@gmail.com"  # Your Gmail
    sender_password = "your_app_password_here"  # Replace with your 16-char app password
    recipient_email = "icanhelpyou009@gmail.com"
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "🚨 TEST ALERT - AI Rockfall Prediction System"
    message["From"] = sender_email
    message["To"] = recipient_email
    
    # Create the HTML content
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center;">
          <h1>🚨 ROCKFALL ALERT SYSTEM TEST 🚨</h1>
        </div>
        
        <div style="padding: 20px;">
          <h2 style="color: #dc3545;">HIGH PRIORITY ALERT</h2>
          
          <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 10px 0;">
            <h3>Alert Details:</h3>
            <ul>
              <li><strong>Type:</strong> ROCKFALL_WARNING</li>
              <li><strong>Severity:</strong> HIGH</li>
              <li><strong>Probability:</strong> 78.0%</li>
              <li><strong>Location:</strong> Zone A - North Wall</li>
              <li><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
              <li><strong>Coordinates:</strong> -23.5505, -46.6333</li>
            </ul>
          </div>
          
          <div style="background-color: #f8d7da; padding: 15px; border-left: 4px solid #dc3545; margin: 10px 0;">
            <h3>🚨 IMMEDIATE ACTIONS REQUIRED:</h3>
            <ol>
              <li><strong>Evacuate personnel</strong> from Zone A immediately</li>
              <li><strong>Halt all operations</strong> in the affected area</li>
              <li><strong>Deploy emergency response team</strong></li>
              <li><strong>Monitor conditions</strong> continuously</li>
            </ol>
          </div>
          
          <div style="background-color: #d1ecf1; padding: 15px; border-left: 4px solid #17a2b8; margin: 10px 0;">
            <h3>📊 System Information:</h3>
            <p><strong>Dashboard:</strong> <a href="http://localhost:3000">http://localhost:3000</a></p>
            <p><strong>API Status:</strong> <a href="http://localhost:5000/api/health">http://localhost:5000/api/health</a></p>
            <p><strong>Alert System:</strong> FREE Gmail SMTP</p>
            <p><strong>Cost:</strong> ₹0.00 (100% FREE!)</p>
          </div>
          
          <hr>
          <p style="color: #6c757d; font-size: 12px;">
            This is an automated alert from the AI-Based Rockfall Prediction System.<br>
            Recipient: icanhelpyou009@gmail.com | Phone: +916384574029<br>
            System: 100% FREE Gmail SMTP Alert Service
          </p>
        </div>
      </body>
    </html>
    """
    
    # Convert to MIMEText
    part = MIMEText(html, "html")
    message.attach(part)
    
    try:
        # Create secure connection and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print("✅ SUCCESS! Test alert sent to icanhelpyou009@gmail.com")
        print("📧 Check your email inbox for the test alert")
        print("💰 Cost: ₹0.00 (100% FREE!)")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("\n🔧 To fix this:")
        print("1. Go to https://myaccount.google.com")
        print("2. Security → 2-Step Verification → Enable")
        print("3. Security → App passwords → Generate")
        print("4. Replace 'your_app_password_here' with the 16-char password")

if __name__ == "__main__":
    send_test_rockfall_alert()