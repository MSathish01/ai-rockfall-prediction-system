#!/usr/bin/env python3
"""
Test Free Alert System - Send alerts using 100% free services
"""

import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append('backend')

try:
    from free_alert_service import FreeAlertService
except ImportError:
    print("❌ Could not import FreeAlertService")
    sys.exit(1)

def main():
    """Test all free alert methods"""
    print("🆓 Testing FREE Alert System")
    print("=" * 50)
    
    # Initialize free alert service
    alert_service = FreeAlertService()
    
    # Test alert data
    test_alert = {
        'alert_type': 'ROCKFALL_WARNING',
        'severity': 'HIGH',
        'probability': 0.78,
        'location': 'Zone A - North Wall',
        'message': 'High rockfall risk detected in Zone A. Immediate attention required.',
        'recommendations': [
            'Evacuate personnel from Zone A immediately',
            'Halt all operations in the affected area',
            'Deploy emergency response team',
            'Monitor conditions continuously'
        ]
    }
    
    print("📧 Testing Gmail SMTP (Free Email)...")
    if alert_service.gmail_user:
        success = alert_service.send_gmail_alert(
            "icanhelpyou009@gmail.com",
            "🚨 TEST ALERT - Rockfall Prediction System",
            alert_service.format_email_message(test_alert)
        )
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print("   ⚠️ Gmail not configured (set GMAIL_USER and GMAIL_APP_PASSWORD)")
    
    print("\n📱 Testing TextBelt SMS (1 Free SMS/Day)...")
    success = alert_service.send_free_sms_textbelt(
        "+916384574029",
        alert_service.format_sms_message(test_alert)
    )
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    print("\n💬 Testing Telegram Bot (Free)...")
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if telegram_token:
        success = alert_service.send_telegram_message(
            "YOUR_CHAT_ID",  # Replace with actual chat ID
            alert_service.format_email_message(test_alert)
        )
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print("   ⚠️ Telegram not configured (set TELEGRAM_BOT_TOKEN)")
    
    print("\n🎮 Testing Discord Webhook (Free)...")
    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook:
        success = alert_service.send_discord_webhook(
            discord_webhook,
            f"🚨 **ROCKFALL ALERT** 🚨\n\n{alert_service.format_email_message(test_alert)}"
        )
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print("   ⚠️ Discord not configured (set DISCORD_WEBHOOK_URL)")
    
    print("\n📲 Testing WhatsApp CallMeBot (Free)...")
    callmebot_key = os.getenv('CALLMEBOT_API_KEY')
    if callmebot_key:
        success = alert_service.send_whatsapp_message(
            "+916384574029",
            alert_service.format_sms_message(test_alert)
        )
        print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    else:
        print("   ⚠️ WhatsApp not configured (set CALLMEBOT_API_KEY)")
    
    print("\n" + "=" * 50)
    print("🎉 Free Alert System Test Completed!")
    print("\n📋 Setup Instructions:")
    print("1. Read FREE_ALERT_SETUP.md for detailed setup")
    print("2. Configure .env file with your credentials")
    print("3. Test each service individually")
    print("\n💰 Total Cost: $0.00 (100% FREE!)")

if __name__ == "__main__":
    main()