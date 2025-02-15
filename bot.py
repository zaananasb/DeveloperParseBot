import os
import logging
from telegram import Update, ReplyKeyboardMarkup, BotCommand, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

# 2. Кастомная клавиатура
def get_keyboard():

    """    buttons = [
    [KeyboardButton("🚀 Старт"), KeyboardButton("📛 Мой ник")]
    ]"""
    return ReplyKeyboardMarkup(
        [
            ["🚀 Старт", "📛 Мой ник",], 
            ["Парсинг"]
        ],
        resize_keyboard=True
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "🚀 Старт":
        await start(update, context)
    elif text == "📛 Мой ник":
        await type_name(update, context)
    elif text == "Парсинг":
        await start_parse(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Привет! Я твой бот-прототип. Пока что я мало что умею.',
        reply_markup=get_keyboard()  # Подключаем клавиатуру
    )

async def type_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user = update.message.from_user

    username = (
        f"@{user.username}" if user.username 
        else f"{user.first_name} {user.last_name}" if user.last_name 
        else user.first_name
    )
    await update.message.reply_text(f"Твой ник: {username}")

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text(update.message.text)

async def start_parse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Парсинг появится чуть позже :)"
    )

def main() -> None:
    
    token = "TELEGRAM_TOKEN"
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("type_name", type_name))
    application.add_handler(CommandHandler("parse", start_parse))
    application.add_handler(MessageHandler(filters.Text(["🚀 Старт", "📛 Мой ник", "Парсинг"]), handle_buttons))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    application.run_polling()

if __name__ == "__main__":
    main()
