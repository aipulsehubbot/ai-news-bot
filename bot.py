import os
import requests
import feedparser
from deep_translator import GoogleTranslator

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🧠 خلاصه
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
    return "https://source.unsplash.com/600x400/?news,technology"

# -------------------------
# 🇮🇷 فارسی واقعی + فیلتر
# -------------------------
def is_persian(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)

def news_fa():
    feed = feedparser.parse("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa")

    items = []
    for e in feed.entries:
        if is_persian(e.title):
            items.append(
                f"📰 {e.title}\n🧠 {summarize(e.title)}\n🖼 {image()}"
            )
        if len(items) >= 5:
            break

    return "\n\n".join(items) if items else "⚠️ خبری پیدا نشد"

# -------------------------
# 🌍 انگلیسی
# -------------------------
def news_en():
    feed = feedparser.parse("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en")
    return "\n\n".join(
        [f"🌍 {e.title}\n🧠 {summarize(e.title)}\n🖼 {image()}" for e in feed.entries[:5]]
    )

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
# 📱 دکمه‌های شیشه‌ای
# -------------------------
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="fa"),
            InlineKeyboardButton("🌍 English", callback_data="en")
        ],
        [
            InlineKeyboardButton("📰 اخبار کامل", callback_data="all"),
        ],
        [
            InlineKeyboardButton("💱 ارز", callback_data="fx"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# -------------------------
# 🤖 START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Global AI News Bot Ready\n👇 یکی رو انتخاب کن:",
        reply_markup=main_menu()
    )

# -------------------------
# 📱 Callback handler
# -------------------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "fa":
        text = news_fa()
    elif data == "en":
        text = news_en()
    elif data == "fx":
        text = fx()
    else:
        text = (
            "📰 NEWS\n\n" +
            news_fa() +
            "\n\n" +
            news_en() +
            "\n\n" +
            fx()
        )

    await query.edit_message_text(text)

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
