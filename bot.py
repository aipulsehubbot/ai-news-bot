import os
import requests
import feedparser
from deep_translator import GoogleTranslator

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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
# 🖼 تصویر
# -------------------------
def image():
    return "https://source.unsplash.com/600x400/?news,technology,world"

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
# 🇮🇷 فارسی (پایدار واقعی)
# -------------------------
def news_fa():
    return fetch_news(
        "https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa",
        "📰"
    )

# -------------------------
# 🇬🇧 انگلیسی
# -------------------------
def news_en():
    return fetch_news(
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
        "🌍"
    )

# -------------------------
# 🇫🇷🇸🇦🇷🇺 ترجمه‌ها
# -------------------------
def news_fr():
    return translate(news_en(), "fr")

def news_ar():
    return translate(news_en(), "ar")

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
        return "💱 FX unavailable"

# -------------------------
# 📱 UI دکمه‌ای
# -------------------------
def menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="fa"),
            InlineKeyboardButton("🌍 English", callback_data="en")
        ],
        [
            InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
            InlineKeyboardButton("🇸🇦 عربي", callback_data="ar"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="ru")
        ],
        [
            InlineKeyboardButton("📰 All News", callback_data="all"),
            InlineKeyboardButton("💱 FX", callback_data="fx")
        ]
    ])

# -------------------------
# 🤖 START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 GLOBAL AI NEWS BOT\n👇 یکی رو انتخاب کن:",
        reply_markup=menu()
    )

# -------------------------
# 📱 BUTTON HANDLER
# -------------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data

    if data == "fa":
        text = news_fa()
    elif data == "en":
        text = news_en()
    elif data == "fr":
        text = news_fr()
    elif data == "ar":
        text = news_ar()
    elif data == "ru":
        text = news_ru()
    elif data == "fx":
        text = fx()
    else:
        text = (
            "📰 FA\n\n" + news_fa() +
            "\n\n🌍 EN\n\n" + news_en() +
            "\n\n💱 " + fx()
        )

    await q.edit_message_text(text)

# -------------------------
# 🚀 MAIN
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
