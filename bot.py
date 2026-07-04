import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🧠 خلاصه ساده
# -------------------------
def summarize(text):
    return text[:140] + "..."

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
    return "https://source.unsplash.com/600x400/?news,world,technology"

# -------------------------
# 📰 RSS helper
# -------------------------
def fetch_news(url, emoji):
    feed = feedparser.parse(url)
    items = []

    for e in feed.entries[:5]:
        items.append(
            f"{emoji} {e.title}\n"
            f"🧠 {summarize(e.title)}\n"
            f"🖼 {image()}"
        )

    return "\n\n".join(items)

# -------------------------
# 🇮🇷 فارسی واقعی
# -------------------------
def news_fa():
    return fetch_news(
        "https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa",
        "📰"
    )

# -------------------------
# 🇬🇧 انگلیسی واقعی
# -------------------------
def news_en():
    return fetch_news(
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "🌍"
    )

# -------------------------
# 🇫🇷 فرانسوی
# -------------------------
def news_fr():
    return translate(news_en(), "fr")

# -------------------------
# 🇸🇦 عربی
# -------------------------
def news_ar():
    return translate(news_en(), "ar")

# -------------------------
# 🇷🇺 روسی
# -------------------------
def news_ru():
    return translate(news_en(), "ru")

# -------------------------
# 💱 ارز
# -------------------------
def fx():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD→IRR: {r.json()['rates']['IRR']}"
    except:
        return "💱 FX error"

# -------------------------
# 🤖 START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 GLOBAL NEWS BOT READY\n\n"
        "/fa 🇮🇷 فارسی\n"
        "/en 🇬🇧 English\n"
        "/fr 🇫🇷 Français\n"
        "/ar 🇸🇦 عربي\n"
        "/ru 🇷🇺 Русский\n"
        "/all 🌍 All News"
    )

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
# 🌍 ALL
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
