import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.document:
        file = await message.document.get_file()
        file_id = message.document.file_id
        file_name = message.document.file_name or "file"

    elif message.video:
        file = await message.video.get_file()
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"

    else:
        return

    bot_username = context.bot.username

    link = f"https://t.me/{bot_username}?start={file_id}"

    await message.reply_text(
        f"✅ File received!\n\n"
        f"📁 {file_name}\n\n"
        f"🔗 File Link:\n{link}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to WASE File Link Bot!\n\n"
        "Send me a video or file and I will create a link for you."
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not configured.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
    app.add_handler(
        MessageHandler(
            filters.Document.ALL | filters.VIDEO,
            handle_file
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
