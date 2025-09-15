# 🚨 Alert System Setup Guide

## Overview
Your contact information has been configured:
- **Phone**: +916384574029
- **Email**: icanhelpyou009@gmail.com

## Current Status
✅ **Configured**: Emergency contacts updated
✅ **Tested**: Alert system simulation completed
⚠️ **Pending**: Real SMS/Email service configuration

## To Enable Real Alerts

### 1. SMS Alerts (Twilio)

#### Step 1: Create Twilio Account
1. Go to [Twilio.com](https://www.twilio.com)
2. Sign up for a free account
3. Get $15 free credit for testing

#### Step 2: Get Credentials
1. From Twilio Console, copy:
   - Account SID
   - Auth Token
   - Phone Number (from Twilio)

#### Step 3: Update .env File
```bash
# Add to your .env file
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### 2. Email Alerts (SendGrid)

#### Step 1: Create SendGrid Account
1. Go to [SendGrid.com](https://sendgrid.com)
2. Sign up for free account
3. Get 100 emails/day free

#### Step 2: Create API Key
1. Go to Settings > API Keys
2. Create new API key with "Full Access"
3. Copy the API key

#### Step 3: Update .env File
```bash
# Add to your .env file
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=your_verified_sender_email@domain.com
```

### 3. Alternative: Gmail SMTP (Free Option)

#### For Email via Gmail:
```bash
# Add to your .env file
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_gmail@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_gmail@gmail.com
```

**Note**: Use Gmail App Password, not regular password.

## Test Real Alerts

### Method 1: Run Test Script
```bash
python test_alert_system.py
```

### Method 2: API Test
```bash
curl -X POST http://localhost:5000/api/test-alert
```

### Method 3: Trigger from Dashboard
1. Go to http://localhost:3000
2. Navigate to Alerts section
3. Click "Send Test Alert" button

## Alert Triggers

Alerts are automatically sent when:
- **HIGH Risk**: Probability > 50%
- **CRITICAL Risk**: Probability > 75%
- **Sensor Failures**: When sensors go offline
- **Manual Triggers**: From dashboard or API

## Message Examples

### SMS Alert Format:
```
🚨 ROCKFALL ALERT 🚨
Severity: HIGH
Location: Zone A - North Wall
Probability: 78%
Time: 19:35

High rockfall risk detected. Immediate attention required.

IMMEDIATE ACTION REQUIRED!
Check dashboard for details.
```

### Email Alert Format:
```
Subject: 🚨 ROCKFALL ALERT - HIGH - Zone A - North Wall

ROCKFALL ALERT SYSTEM - HIGH PRIORITY

Alert Details:
- Type: ROCKFALL_WARNING
- Severity: HIGH
- Probability: 78.0%
- Location: Zone A - North Wall
- Time: 2025-09-15 19:35:29

Recommended Actions:
• Evacuate personnel immediately
• Halt operations in affected area
• Deploy emergency response team
• Monitor conditions continuously

Dashboard: http://localhost:3000
```

## Cost Estimates

### Twilio SMS:
- **Free Tier**: $15 credit (~500 SMS)
- **Pay-as-you-go**: $0.0075 per SMS
- **Monthly**: ~$10-20 for typical mine

### SendGrid Email:
- **Free Tier**: 100 emails/day
- **Essentials**: $14.95/month (50,000 emails)

## Security Best Practices

1. **Environment Variables**: Never commit API keys to code
2. **Restricted Access**: Limit API key permissions
3. **Rate Limiting**: Prevent spam/abuse
4. **Encryption**: Use HTTPS for all communications
5. **Backup Contacts**: Multiple notification methods

## Troubleshooting

### Common Issues:
1. **SMS not delivered**: Check phone number format (+country_code)
2. **Email in spam**: Verify sender domain
3. **API errors**: Check credentials and quotas
4. **Rate limits**: Implement delays between messages

### Debug Commands:
```bash
# Test Twilio connection
python -c "from twilio.rest import Client; print('Twilio OK')"

# Test SendGrid connection
python -c "import sendgrid; print('SendGrid OK')"

# Check environment variables
python -c "import os; print(os.getenv('TWILIO_ACCOUNT_SID', 'Not set'))"
```

## Support

- **Twilio Support**: [support.twilio.com](https://support.twilio.com)
- **SendGrid Support**: [support.sendgrid.com](https://support.sendgrid.com)
- **System Issues**: Check logs in `logs/` directory

---

**Your alert system is configured and ready! Configure the API keys above to enable real SMS and email notifications.** 🚀