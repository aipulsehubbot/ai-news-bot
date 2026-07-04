import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🌍 ترجمه هوشمند
# -------------------------
def translate(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# -------------------------
# 🖼 تصویر
# -------------------------
def image():
    return "https://source.unsplash.com/600x400/?news,ai,technology"

# -------------------------
# 📰 RSS helper
# -------------------------
def get_news(url, prefix):
    feed = feedparser.parse(url)
    return "\n\n".join([
        f"{prefix} {e.title}\n🧠 {e.title[:120]}...\n🖼 {image()}"
        for e in feed.entries[:4]
    ])

# -------------------------
# 📰 فارسی
# -------------------------
def news_fa():
    return get_news("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa", "📰")

# -------------------------
# 🌍 انگلیسی
# -------------------------
def news_en():
    return get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "🌍")

# -------------------------
# 🇫🇷 فرانسوی
# -------------------------
def news_fr():
    return get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "🇫🇷")

# -------------------------
# 🇸🇦 عربی
# -------------------------
def news_ar():
    return get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "🇸🇦")

# -------------------------
# 🇷🇺 روسی
# -------------------------
def news_ru():
    return get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "🇷🇺")

# -------------------------
# 💱 ارز
# -------------------------
def fx():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD→IRR: {r.json()['rates']['IRR']}"
    except:
        return "FX error"

# -------------------------
# 🤖 START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 GLOBAL NEWS BOT\n\n"
        "/fa فارسی\n"
        "/en English\n"
        "/fr Français\n"
        "/ar عربي\n"
        "/ru Русский\n"
        "/all همه زبان‌ها"
    )
    await update.message.reply_text(msg)

# -------------------------
# 🇮🇷
# -------------------------
async def fa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_fa())

# -------------------------
# 🇬🇧
# -------------------------
async def en(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_en())

# -------------------------
# 🇫🇷
# -------------------------
async def fr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_fr())

# -------------------------
# 🇸🇦
# -------------------------
async def ar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_ar())

# -------------------------
# 🇷🇺
# -------------------------
async def ru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(news_ru())

# -------------------------
# 🌍 ALL LANGUAGES
# -------------------------
async def all_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 FA\n" + news_fa() +
        "\n\n🌍 EN\n" + news_en() +
        "\n\n🇫🇷 FR\n" + news_fr() +
        "\n\n🇸🇦 AR\n" + news_ar() +
        "\n\n🇷🇺 RU\n" + news_ru() +
        "\n\n" + fx()
    )
    await update.message.reply_text(msg)

# -------------------------
# 🚀 MAIN
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fa", fa))
    app.add_handler(CommandHandler("en", en))
    app.add_handler(CommandHandler("fr", fr))
    app.add_handler(CommandHandler("ar", ar))
    app.add_handler(CommandHandler("ru", ru))
    app.add_handler(CommandHandler("all", all_news))

    app.run_polling()

if __name__ == "__main__":
    main()
