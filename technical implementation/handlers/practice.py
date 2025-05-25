from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

async def send_quest(bot: Bot, chat_id: int, state: dict, practice_modules: dict):
    key = state["quest"]
    module = state.get("quest_module", 8)
    quest_data = practice_modules.get(module, {})
    node = quest_data.get(key)
    if not node:
        await bot.send_message(chat_id, "Произошла ошибка.")
        return

    options = node.get("options", {})
    state["options"] = options
    text = node["text"]
    keyboard = []

    if options:
        keyboard = [[KeyboardButton(opt)] for opt in options.keys()]
    elif "next" in node:
        state["next_after"] = node["next"]
        keyboard = [["➡️ Далее"]]
    else:
        keyboard = [["🏠 В меню"]]

    await bot.send_message(chat_id, text,
                           reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_quest(bot: Bot, chat_id: int, choice: str, state: dict, practice_modules: dict):
    options = state.get("options", {})
    if choice in options:
        state["quest"] = options[choice]
        await send_quest(bot, chat_id, state, practice_modules)
    else:
        await bot.send_message(chat_id, "Пожалуйста, выбери вариант из кнопок.")
