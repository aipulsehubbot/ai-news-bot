import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 📰 خبر AI (Google News RSS)
def ai_news():
    url = "https://news.google.com/rss/search?q=artificial+intelligence"
    r = requests.get(url)
    return r.text[:1000] if r.status_code == 200 else "خطا در دریافت خبر AI"

# 💰 قیمت طلا (نمونه API ساده)
def gold_price():
    url = "https://api.metals.live/v1/spot/gold"
    r = requests.get(url)
    return str(r.json()) if r.status_code == 200 else "خطا در قیمت طلا"

# 🚗 قیمت خودرو (نمونه خبری)
def car_news():
    url = "https://news.google.com/rss/search?q=car+price"
    r = requests.get(url)
    return r.text[:1000]

# 🌐 سایت‌های مفید
def useful_sites():
    return """
🌐 سایت‌های مفید:

1. https://github.com
2. https://stackoverflow.com
3. https://news.google.com
4. https://huggingface.co
"""

# 🤖 start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ربات خبری فعال شد")

# 📰 عمومی
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 اخبار:\n" + car_news())

# 🤖 AI news
async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 اخبار هوش مصنوعی:\n" + ai_news())

# 💰 gold
async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 قیمت طلا:\n" + gold_price())

# 🚗 car
async def car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 اخبار خودرو:\n" + car_news())

# 🌐 links
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(useful_sites())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("ai", ai))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(CommandHandler("car", car))
    app.add_handler(CommandHandler("links", links))

    app.run_polling()

if __name__ == "__main__":
    main()
