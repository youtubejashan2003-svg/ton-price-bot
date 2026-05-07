from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import requests
import asyncio

TOKEN = "8687375975:AAFGPyRcPInn3NhuSWf3zTybPkynn7QLEmQ"

CHANNEL_ID = "@tonnprice"

interval = 60
running = False
last_price = None


async def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"

    data = requests.get(url).json()

    return float(data["the-open-network"]["usd"])


async def auto_price(app):
    global running
    global interval
    global last_price

    while running:
        try:
            price = await get_ton_price()

            if last_price is None:
                status = "START"

            elif price > last_price:
                status = "UPPER 📈"

            elif price < last_price:
                status = "DOWN 📉"

            else:
                status = "SAME"

            text = f"{price}$\n{status}"

            await app.bot.send_message(
                chat_id=CHANNEL_ID,
                text=text
            )

            last_price = price

        except Exception as e:
            print(e)

        await asyncio.sleep(interval)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "TON BOT ACTIVE\n\n"
        "/run\n"
        "/stop\n"
        "/settime 60\n"
        "/price"
    )


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    if running:
        await update.message.reply_text("Already Running")
        return

    running = True

    context.application.create_task(
        auto_price(context.application)
    )

    await update.message.reply_text("Started")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running

    running = False

    await update.message.reply_text("Stopped")


async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global interval

    try:
        sec = int(context.args[0])

        interval = sec

        await update.message.reply_text(
            f"Time Set: {sec} sec"
        )

    except:
        await update.message.reply_text(
            "Use:\n/settime 60"
        )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_price

    price = await get_ton_price()

    if last_price is None:
        status = "START"

    elif price > last_price:
        status = "UPPER 📈"

    elif price < last_price:
        status = "DOWN 📉"

    else:
        status = "SAME"

    await update.message.reply_text(
        f"{price}$\n{status}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("run", run))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("settime", settime))
app.add_handler(CommandHandler("price", price))

print("Bot Running...")

app.run_polling()
