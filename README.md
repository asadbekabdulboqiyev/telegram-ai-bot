# Telegram AI Bot

Python + Groq API (Llama 3.3) asosida ishlaydigan Telegram bot.

## O'rnatish

```bash
pip install -r requirements.txt
```

## Sozlash

1. `.env.example` faylini `.env` ga nusxalang:
   ```bash
   cp .env.example .env
   ```

2. `.env` faylni to'ldiring:
   - `TELEGRAM_BOT_TOKEN` - @BotFather dan olingan token
   - `GROQ_API_KEY` - https://console.groq.com dan olingan API kalit

## Bot token olish

1. Telegram'da @BotFather ni toping
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Bot username kiriting
5. Berilgan token'ni `.env` faylga joylashtiring

## Groq API kalit olish

1. https://console.groq.com ga kiring
2. Ro'yxatdan o'ting
3. API Keys bo'limiga boring
4. Yangi kalit yarating

## Ishga tushirish

```bash
python bot.py
```

## Buyruqlar

- `/start` - Botni qayta ishga tushirish
- `/clear` - Suhbat tarixini tozalash
- `/help` - Yordam
