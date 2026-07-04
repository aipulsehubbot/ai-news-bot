import os
import requests
import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🧠 خلاصه ساده (بعداً AI میشه)
# -------------------------
def summarize(text):
    return text[:200] + "..."

# -------------------------
# 🌍 ترجمه
# -------------------------
def translate(text, lang):
    try:
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except:
        return text

# -------------------------
# 🖼 تصویر برای خبر
# -------------------------
def image():
    return "https://source.unsplash.com/600x400/?news,technology"

# -------------------------
# 📰 خبر فارسی
# -------------------------
def news_fa():
    feed = feedparser.parse("https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa")
    out = []
    for e in feed.entries[:4]:
        out.append(f"📰 {e.title}\n🖼 {image()}")
    return "\n\n".join(out)

# -------------------------
# 🤖 AI news
# -------------------------
def news_ai():
    feed = feedparser.parse("https://news.google.com/rss/search?q=artificial+intelligence")
    out = []
    for e in feed.entries[:4]:
        out.append(f"🤖 {e.title}\n🖼 {image()}")
    return "\n\n".join(out)

# -------------------------
# 🚗 خودرو
# -------------------------
def news_car():
    feed = feedparser.parse("https://news.google.com/rss/search?q=car+iran")
    return "\n\n".join([f"🚗 {e.title}\n🖼 {image()}" for e in feed.entries[:3]])

# -------------------------
# 💰 طلا
# -------------------------
def gold():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU")
        return f"💰 Gold: {r.json()['price']} USD"
    except:
        return "Gold error"

# -------------------------
# 💱 ارز
# -------------------------
def usd():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD→IRR: {r.json()['rates']['IRR']}"
    except:
        return "FX error"

# -------------------------
# 🤖 start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 AI News Bot Active\n\n/fa فارسی\n/en English\n/news همه خبرها"
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
# ⏰ ارسال خودکار هر ساعت
# -------------------------
async def auto_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    msg = (
        "⏰ Hourly News\n\n"
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

    await update.message.reply_text("⏰ Auto News Enabled")

# -------------------------
# 🚀 main
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
