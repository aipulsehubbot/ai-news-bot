import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🌍 ترجمه
# -------------------------
def translate(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# -------------------------
# 🖼 تصویر ثابت پایدار
# -------------------------
def image():
    return "https://images.unsplash.com/photo-1504711434969-e33886168f5c"

# -------------------------
# 📰 خبر فارسی (پایدار)
# -------------------------
def news_fa():
    feed = feedparser.parse("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa")
    return "\n\n".join(
        [f"📰 {e.title}\n🖼 {image()}" for e in feed.entries[:5]]
    )

# -------------------------
# 🤖 AI News
# -------------------------
def news_ai():
    feed = feedparser.parse("https://news.google.com/rss/search?q=artificial+intelligence")
    return "\n\n".join(
        [f"🤖 {e.title}\n🖼 {image()}" for e in feed.entries[:5]]
    )

# -------------------------
# 🚗 خودرو
# -------------------------
def news_car():
    feed = feedparser.parse("https://news.google.com/rss/search?q=car+technology")
    return "\n\n".join(
        [f"🚗 {e.title}\n🖼 {image()}" for e in feed.entries[:3]]
    )

# -------------------------
# 💰 طلا (نسخه امن بدون API خراب)
# -------------------------
def gold():
    try:
        r = requests.get("https://api.allorigins.win/raw?url=https://goldprice.org")
        if r.status_code == 200:
            return "💰 Gold: live data available (visit goldprice.org)"
        return "💰 Gold: unavailable"
    except:
        return "💰 Gold: unavailable"

# -------------------------
# 💱 ارز (پایدار)
# -------------------------
def usd():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD→IRR: {r.json()['rates']['IRR']}"
    except:
        return "💱 FX unavailable"

# -------------------------
# 🤖 start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI News Bot Ready\n"
        "/fa - فارسی\n"
        "/en - English\n"
        "/news - اخبار کامل"
    )

# -------------------------
# 🇮🇷 فارسی
# -------------------------
async def fa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_fa())

# -------------------------
# 🇬🇧 انگلیسی
# -------------------------
async def en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(translate(news_fa(), "en"))

# -------------------------
# 📰 همه خبرها
# -------------------------
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 NEWS\n\n"
        + news_fa()
        + "\n\n🤖 AI\n" + news_ai()
        + "\n\n🚗 CAR\n" + news_car()
        + "\n\n💰 " + gold()
        + "\n" + usd()
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
