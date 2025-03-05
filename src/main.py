from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, \
    MessageHandler, filters


def get_token_from_file():
    with open("token.txt", "r") as file:
        token = file.read().strip()
    return token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Выбрать задание"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Привет! Я бот для подготовки к ЕГЭ. Используй кнопки для навигации.',
                                    reply_markup=reply_markup)


async def choose_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = []
    row = []

    for i in range(1, 28):
        row.append(InlineKeyboardButton(f"Задание {i}", callback_data=f"task_{i}"))
        if len(row) == 2 or i == 27:
            keyboard.append(row.copy())
            row = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите номер задания:", reply_markup=reply_markup)


async def task_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    task_number = query.data.split("_")[1]

    keyboard = [
        [InlineKeyboardButton("Теория", callback_data=f"theory_{task_number}")],
        [InlineKeyboardButton("Лайфхаки", callback_data=f"lifehacks_{task_number}")],
        [InlineKeyboardButton("Задание", callback_data=f"exercise_{task_number}")],
        [InlineKeyboardButton("Вернуться к выбору задания", callback_data="back_to_tasks")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(f"Задание {task_number}. Выберите опцию:", reply_markup=reply_markup)


async def send_theory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    task_number = query.data.split("_")[1]

    file_path = f"./theory/{task_number}.pdf"
    try:
        loading_message = await query.message.reply_text("Ваш файл загружается")
        await query.message.reply_document(document=open(file_path, 'rb'))
        await loading_message.delete()
    except FileNotFoundError:
        await query.message.reply_text("Данное задание находится в разработке")


async def send_lifehacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    task_number = query.data.split("_")[1]

    file_path = f"./lifehacks/{task_number}.pdf"
    try:
        loading_message = await query.message.reply_text("Ваш файл загружается")
        await query.message.reply_document(document=open(file_path, 'rb'))
        await loading_message.delete()
    except FileNotFoundError:
        await query.message.reply_text("Данное задание находится в разработке")


async def send_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    task_number = query.data.split("_")[1]

    await query.message.reply_text(f"Вы можете потренироваться в решении задания {task_number} по ссылке\nhttps://examer.ru/ege_po_informatike/zadanie_{task_number}/")


async def back_to_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = []
    row = []

    for i in range(1, 28):
        row.append(InlineKeyboardButton(f"Задание {i}", callback_data=f"task_{i}"))
        if len(row) == 2 or i == 27:
            keyboard.append(row.copy())
            row = []

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выберите номер задания:", reply_markup=reply_markup)


def main():
    token = get_token_from_file()

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text(["Выбрать задание"]), choose_task))
    application.add_handler(CallbackQueryHandler(task_selected, pattern=r"^task_"))
    application.add_handler(CallbackQueryHandler(send_theory, pattern=r"^theory_"))
    application.add_handler(CallbackQueryHandler(send_lifehacks, pattern=r"^lifehacks_"))
    application.add_handler(CallbackQueryHandler(send_exercise, pattern=r"^exercise_"))
    application.add_handler(CallbackQueryHandler(back_to_tasks, pattern=r"^back_to_tasks$"))

    application.run_polling()


if __name__ == "__main__":
    main()
