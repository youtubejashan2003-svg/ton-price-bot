from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import requests
import asyncio

TOKEN = "8687375975:AAFGPyRcPInn3NhuSWf3zTybPkynn7QLEmQ"

CHANNEL_ID = "-1003775021632"

OWNER_ID = 8715707181

interval = 60
running = False


async def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"

    data = requests.get(url).json()

    return float(data["the-open-network"]["usd"])


async def auto_price(app):
    global running
    global interval

    while running:
        try:
            price = await get_ton_price()

            text = f"<b>{price:.2f}$</b>"

            await app.bot.send_message(
                chat_id=CHANNEL_ID,
                text=text,
                parse_mode="HTML"
            )

        except Exception as e:
            print(e)

        await asyncio.sleep(interval)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 Welcome To TON Price Bot\n\n"
        "This bot provides live TON price updates.\n\n"
        "Commands:\n"
        "/price\n\n"
        "Join For Live Updates:\n"
        "@tonnprice\n\n"
        "👨‍💻 Developer: @tumlu"
    )


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    if update.effective_user.id != OWNER_ID:
        return

    if running:
        await update.message.reply_text("Already Running ✅")
        return

    running = True

    context.application.create_task(
        auto_price(context.application)
    )

    await update.message.reply_text("Started ✅")


async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global interval

    if update.effective_user.id != OWNER_ID:
        return

    try:
        sec = int(context.args[0])

        interval = sec

        await update.message.reply_text(
            f"Time Set To {sec} sec ✅"
        )

    except:
        await update.message.reply_text(
            "Use:\n/settime 60"
        )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ton_price = await get_ton_price()

    await update.message.reply_text(
        f"<b>{ton_price:.2f}$</b>",
        parse_mode="HTML"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("run", run))
app.add_handler(CommandHandler("settime", settime))
app.add_handler(CommandHandler("price", price))

print("Bot Running...")

app.run_polling()
