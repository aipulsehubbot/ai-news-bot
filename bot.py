import os
import requests
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -------------------------
# 🧠 AI Summary ساده (فعلاً بدون API)
# بعداً وصلش می‌کنیم به OpenAI
# -------------------------
def ai_summarize(text):
    return text[:300] + "..."

# -------------------------
# 📰 خبر فارسی واقعی (RSS)
# -------------------------
def persian_news():
    url = "https://news.google.com/rss?hl=fa&gl=IR&ceid=IR:fa"
    feed = feedparser.parse(url)

    news_list = []
    for entry in feed.entries[:5]:
        news_list.append(f"📰 {entry.title}")

    return "\n".join(news_list)

# -------------------------
# 💰 قیمت طلا و ارز (نمونه واقعی API)
# -------------------------
def gold_price():
    try:
        r = requests.get("https://api.metals.live/v1/spot/gold")
        return f"💰 طلا: {r.json()}"
    except:
        return "خطا در دریافت طلا"

def usd_price():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        return f"💱 USD: {r.json()['rates']['IRR']} IRR"
    except:
        return "خطا در ارز"

# -------------------------
# 🚗 خودرو (خبر محور)
# -------------------------
def car_news():
    url = "https://news.google.com/rss/search?q=car+iran&hl=fa&gl=IR&ceid=IR:fa"
    feed = feedparser.parse(url)

    return "\n".join([f"🚗 {e.title}" for e in feed.entries[:3]])

# -------------------------
# 🤖 start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ربات خبری حرفه‌ای فعال شد")

# -------------------------
# 📰 همه خبرها
# -------------------------
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📰 اخبار فارسی:\n\n" + persian_news() +
        "\n\n" + gold_price() +
        "\n\n" + usd_price() +
        "\n\n" + car_news()
    )
    await update.message.reply_text(msg)

# -------------------------
# 🌐 auto news (هر ساعت)
# -------------------------
async def auto_news(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    msg = (
        "⏰ خبر ساعتی:\n\n"
        + persian_news() +
        "\n\n" + gold_price()
    )

    await context.bot.send_message(chat_id=chat_id, text=msg)

async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    context.job_queue.run_repeating(
        auto_news,
        interval=3600,  # هر 1 ساعت
        first=5,
        chat_id=chat_id
    )

    await update.message.reply_text("⏰ ارسال ساعتی فعال شد")

# -------------------------
# 🌍 links
# -------------------------
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 سایت‌ها:\n"
        "- https://news.google.com\n"
        "- https://tsetmc.com\n"
        "- https://github.com\n"
    )

# -------------------------
# 🚀 main
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("auto", start_auto))
    app.add_handler(CommandHandler("links", links))

    app.run_polling()

if __name__ == "__main__":
    main()
