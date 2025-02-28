from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


def get_token_from_file():
    with open("token.txt", "r") as file:
        token = file.read().strip()
    return token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я твой новый бот.')


def main():
    token = get_token_from_file()

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()
