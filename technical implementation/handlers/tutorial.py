
from telegram import Bot, ReplyKeyboardMarkup

async def send_tutorial(bot: Bot, chat_id: int, tutorial_text: str):
    """Отправить текст туториала."""
    await bot.send_message(
        chat_id,
        tutorial_text,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([["🏠 В меню"]], resize_keyboard=True)
    )
