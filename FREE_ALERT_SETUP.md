# 🆓 **100% FREE Alert System Setup**

## Overview
Set up completely free alert notifications using:
- ✅ **Gmail SMTP** (Unlimited free emails)
- ✅ **TextBelt** (1 free SMS per day per phone)
- ✅ **Telegram Bot** (Unlimited free messages)
- ✅ **Discord Webhook** (Unlimited free messages)
- ✅ **WhatsApp via CallMeBot** (Free with setup)

---

## 🔧 **Setup Instructions**

### **1. Gmail SMTP (100% Free Email)**

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com)
2. Security → 2-Step Verification → Turn On

#### Step 2: Generate App Password
1. Go to Security → App passwords
2. Select app: "Mail"
3. Select device: "Other" → Enter "Rockfall System"
4. Copy the 16-character password

#### Step 3: Update .env File
```bash
# Gmail SMTP (100% Free)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
```

---

### **2. TextBelt SMS (1 Free SMS/Day)**

#### No Setup Required!
- **Free Tier**: 1 SMS per day per phone number
- **Cost**: $0.00
- **Limitation**: 1 message per day per recipient
- **Perfect for**: Critical alerts only

#### Usage:
```python
# Automatically works - no API key needed
send_free_sms_textbelt("+916384574029", "Alert message")
```

---

### **3. Telegram Bot (Unlimited Free)**

#### Step 1: Create Bot
1. Open Telegram app
2. Search for "@BotFather"
3. Send `/newbot`
4. Choose bot name: "Rockfall Alert Bot"
5. Choose username: "rockfall_alert_bot"
6. Copy the bot token

#### Step 2: Get Chat ID
1. Add your bot to a group or chat with it
2. Send a message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat_id in the response

#### Step 3: Update .env File
```bash
# Telegram (100% Free)
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

#### Step 4: Update contacts.json
```json
{
  "name": "Primary Contact",
  "phone": "+916384574029",
  "email": "icanhelpyou009@gmail.com",
  "telegram_chat_id": "your_chat_id_here"
}
```

---

### **4. Discord Webhook (Unlimited Free)**

#### Step 1: Create Discord Server
1. Create a Discord server (free)
2. Create a channel for alerts

#### Step 2: Create Webhook
1. Channel Settings → Integrations → Webhooks
2. Create Webhook
3. Copy webhook URL

#### Step 3: Update .env File
```bash
# Discord (100% Free)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```

---

### **5. WhatsApp via CallMeBot (Free)**

#### Step 1: Add Bot to WhatsApp
1. Add phone number: +34 644 59 71 67
2. Send message: "I allow callmebot to send me messages"
3. Wait for confirmation with your API key

#### Step 2: Update .env File
```bash
# WhatsApp CallMeBot (Free)
CALLMEBOT_API_KEY=your_api_key_from_whatsapp
```

---

## 📱 **Complete .env Configuration**

```bash
# Gmail SMTP (Unlimited Free Emails)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# Telegram Bot (Unlimited Free Messages)
TELEGRAM_BOT_TOKEN=your_bot_token

# Discord Webhook (Unlimited Free Messages)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook

# WhatsApp CallMeBot (Free Messages)
CALLMEBOT_API_KEY=your_api_key

# Database
DATABASE_URL=sqlite:///rockfall_system.db
```

---

## 🧪 **Test Free Alerts**

### Create Test Script:
```python
from backend.free_alert_service import FreeAlertService

# Initialize service
alert_service = FreeAlertService()

# Test alert data
test_alert = {
    'severity': 'HIGH',
    'probability': 0.78,
    'location': 'Zone A - North Wall',
    'message': 'High rockfall risk detected - immediate attention required',
    'recommendations': [
        'Evacuate personnel immediately',
        'Halt operations in affected area',
        'Deploy emergency response team'
    ]
}

# Send comprehensive alert
results = alert_service.send_comprehensive_alert(test_alert)
print("Alert results:", results)
```

---

## 💰 **Cost Breakdown**

| Service | Free Tier | Cost | Limitations |
|---------|-----------|------|-------------|
| **Gmail SMTP** | Unlimited | $0.00 | Gmail account required |
| **TextBelt SMS** | 1/day/phone | $0.00 | 1 SMS per day per number |
| **Telegram** | Unlimited | $0.00 | Recipients need Telegram |
| **Discord** | Unlimited | $0.00 | Recipients need Discord |
| **WhatsApp** | Unlimited | $0.00 | Setup required |

**Total Monthly Cost: $0.00** 🎉

---

## 🚀 **Recommended Free Setup**

### **For Your Contact (+916384574029 / icanhelpyou009@gmail.com):**

1. **Primary**: Gmail SMTP (unlimited emails)
2. **Secondary**: TextBelt SMS (1 critical alert per day)
3. **Backup**: Telegram (unlimited, instant)
4. **Team**: Discord (for team notifications)

### **Alert Priority:**
- **CRITICAL**: All channels
- **HIGH**: Email + SMS + Telegram
- **MEDIUM**: Email + Telegram
- **LOW**: Email only

---

## 🔧 **Integration with Your System**

### Update backend/app.py:
```python
from free_alert_service import FreeAlertService

# Initialize free alert service
free_alerts = FreeAlertService()

# In your alert generation code:
if risk_level in ['HIGH', 'CRITICAL']:
    alert_data = {
        'severity': risk_level,
        'probability': probability,
        'location': 'Zone A',
        'message': f"Rockfall risk detected. Probability: {probability:.1%}",
        'recommendations': recommendations
    }
    
    # Send free alerts
    results = free_alerts.send_comprehensive_alert(alert_data)
```

---

## ✅ **Setup Checklist**

- [ ] Gmail App Password generated
- [ ] Telegram bot created and chat ID obtained
- [ ] Discord webhook URL copied
- [ ] WhatsApp CallMeBot API key received
- [ ] .env file updated with credentials
- [ ] Test alerts sent successfully
- [ ] Emergency contacts updated with new channels

---

**🎉 Your completely FREE alert system is ready! No monthly costs, no credit cards required!**