import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🌍 ترجمه ساده
# -------------------------
def translate(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# -------------------------
# 🖼 عکس برای خبر (placeholder)
# -------------------------
def get_image():
    return "https://source.unsplash.com/600x400/?news,technology"

# -------------------------
# 📰 خبر فارسی
# -------------------------
def persian_news():
    feed = feedparser.parse("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa")
    news = []
    for e in feed.entries[:3]:
        news.append(f"📰 {e.title}\n🖼 {get_image()}")
    return "\n\n".join(news)

# -------------------------
# 🤖 AI news
# -------------------------
def ai_news():
    feed = feedparser.parse("https://news.google.com/rss/search?q=artificial+intelligence")
    news = []
    for e in feed.entries[:3]:
        news.append(f"🤖 {e.title}\n🖼 {get_image()}")
    return "\n\n".join(news)

# -------------------------
# 💰 طلا
# -------------------------
def gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU")
        return f"💰 Gold: {r.json()['price']} USD"
    except:
        return "Gold error"

# -------------------------
# 💱 ارز
# -------------------------
def usd_price():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD: {r.json()['rates']['IRR']} IRR"
    except:
        return "FX error"

# -------------------------
# 🚗 خودرو
# -------------------------
def car_news():
    feed = feedparser.parse("https://news.google.com/rss/search?q=car+iran")
    return "\n".join([f"🚗 {e.title}\n🖼 {get_image()}" for e in feed.entries[:3]])

# -------------------------
# 🤖 start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🤖 Bot Ready

Commands:
/fa - فارسی
/en - English
/news - Full news
"""
    await update.message.reply_text(msg)

# -------------------------
# 🇮🇷 فارسی
# -------------------------
async def fa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 فارسی:\n\n" + persian_news()
    )

# -------------------------
# 🇬🇧 انگلیسی
# -------------------------
async def en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = persian_news()
    await update.message.reply_text(
        "NEWS EN:\n\n" + translate(text, "en")
    )

# -------------------------
# 📰 همه چیز
# -------------------------
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 NEWS\n\n"
        + persian_news()
        + "\n\n🤖 AI\n" + ai_news()
        + "\n\n💰 " + gold_price()
        + "\n" + usd_price()
        + "\n\n🚗 " + car_news()
    )
    await update.message.reply_text(msg)

# -------------------------
# 🚀 main
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fa", fa))
    app.add_handler(CommandHandler("en", en))
    app.add_handler(CommandHandler("news", news))

    app.run_polling()

if __name__ == "__main__":
    main()
