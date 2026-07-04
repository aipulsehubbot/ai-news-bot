import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🧠 خلاصه (AI ساده + قابل ارتقا)
# -------------------------
def summarize(text):
    return text[:180] + "..."

# -------------------------
# 🌍 ترجمه
# -------------------------
def translate(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# -------------------------
# 🖼 تصویر (خبر محور)
# -------------------------
def image():
    return "https://source.unsplash.com/600x400/?news,technology,ai"

# -------------------------
# 📰 خبر فارسی
# -------------------------
def news_fa():
    feed = feedparser.parse("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa")
    items = []

    for e in feed.entries[:5]:
        items.append(f"📰 {e.title}\n{summarize(e.title)}\n🖼 {image()}")

    return "\n\n".join(items)

# -------------------------
# 🤖 AI News
# -------------------------
def news_ai():
    feed = feedparser.parse("https://news.google.com/rss/search?q=artificial+intelligence")
    items = []

    for e in feed.entries[:5]:
        items.append(f"🤖 {e.title}\n{summarize(e.title)}\n🖼 {image()}")

    return "\n\n".join(items)

# -------------------------
# 🚗 خودرو
# -------------------------
def news_car():
    feed = feedparser.parse("https://news.google.com/rss/search?q=car+technology")
    return "\n\n".join([f"🚗 {e.title}\n🖼 {image()}" for e in feed.entries[:4]])

# -------------------------
# 💰 طلا
# -------------------------
def gold():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU")
        return f"💰 Gold: {r.json()['price']} USD"
    except:
        return "💰 Gold: error"

# -------------------------
# 💱 ارز
# -------------------------
def usd():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD→IRR: {r.json()['rates']['IRR']}"
    except:
        return "💱 FX error"

# -------------------------
# 🤖 start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI News Bot Pro Active\n\n"
        "/fa - فارسی\n"
        "/en - English\n"
        "/news - Full News\n"
        "/auto - Hourly News"
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
        + "\n\n🤖 AI NEWS\n" + news_ai()
        + "\n\n🚗 CAR NEWS\n" + news_car()
        + "\n\n💰 " + gold()
        + "\n" + usd()
    )
    await update.message.reply_text(msg)

# -------------------------
# ⏰ ارسال خودکار هر ساعت
# -------------------------
async def auto_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    msg = (
        "⏰ Hourly AI News\n\n"
        + news_fa()
        + "\n\n💰 " + gold()
        + "\n" + usd()
    )

    await context.bot.send_message(chat_id=chat_id, text=msg)

async def auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    context.job_queue.run_repeating(
        auto_job,
        interval=3600,
        first=5,
        chat_id=chat_id
    )

    await update.message.reply_text("⏰ Auto News Enabled (Hourly)")

# -------------------------
# 🚀 MAIN
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fa", fa))
    app.add_handler(CommandHandler("en", en))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("auto", auto))

    app.run_polling()

if __name__ == "__main__":
    main()
