
import os
import json
from telegram import Bot, Update, ReplyKeyboardMarkup
from storage.state import get_user_state, save_user_state
from handlers.theory import send_theory
from handlers.practice import send_quest, handle_quest
from loader.modules import load_theory_modules, load_practice_modules, load_tutorial

bot = Bot(token=os.environ["BOT_TOKEN"])
theory_modules = load_theory_modules()
practice_modules = load_practice_modules()
TUTORIAL_TEXT = load_tutorial()

WELCOME_TEXT = (
    "👋 Добро пожаловать в обучающий бот по финансовой грамотности!\n\n"
    "📌 Здесь вы сможете:\n"
    "— изучать теоретические материалы по важнейшим темам;\n"
    "— пройти интерактивные практические квесты для закрепления знаний.\n\n"
    "⚠️ Проходя этот бот, вы подтверждаете согласие на участие в исследовании и на обработку ваших данных в обезличенном виде. Все данные используются исключительно в учебных и исследовательских целях.\n\n"
    "👇 Выберите, с чего начать:"
)

async def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    update = Update.de_json(body, bot)
    message = body.get("message") or body.get("edited_message")

    if not message:
        return {"statusCode": 200, "body": "No message found"}

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()
    if not chat_id or not text:
        return {"statusCode": 200, "body": "Empty chat_id or text"}

    state = get_user_state(str(chat_id)) or {}

    if text == "/start" or text == "🏠 В меню":
        state.clear()
        await bot.send_message(
            chat_id,
            WELCOME_TEXT,
            reply_markup=ReplyKeyboardMarkup(
                [["📚 Теория", "🧩 Практика", "📖 Туториал"]],
                resize_keyboard=True
            )
        )

    elif text == "📚 Теория":
        await bot.send_message(
            chat_id,
            "Выбери модуль:",
            reply_markup=ReplyKeyboardMarkup(
                [[f"Модуль {i}" for i in range(1, 5)],
                 [f"Модуль {i}" for i in range(5, 9)],
                 ["🏠 В меню"]],
                resize_keyboard=True
            )
        )

    elif text == "🧩 Практика":
        await bot.send_message(
            chat_id,
            "Выбери модуль:",
            reply_markup=ReplyKeyboardMarkup(
                [[f"Квест {i}" for i in range(1, 5)],
                 [f"Квест {i}" for i in range(5, 9)],
                 ["🏠 В меню"]],
                resize_keyboard=True
            )
        )

    elif text == "📖 Туториал":
        await bot.send_message(
            chat_id,
            TUTORIAL_TEXT,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup([["🏠 В меню"]], resize_keyboard=True)
        )

    elif text.startswith("Модуль"):
        try:
            module_number = int(text.split()[-1])
            state["theory_module"] = module_number
            state["theory_index"] = 0
            await send_theory(bot, chat_id, state, theory_modules)
        except ValueError:
            await bot.send_message(chat_id, "Некорректный номер модуля.")

    elif text.lower() == "далее":
        await send_theory(bot, chat_id, state, theory_modules)

    elif text.startswith("Квест"):
        try:
            mod_num = int(text.split()[-1])
            if mod_num in practice_modules:
                state["quest"] = "1"
                state["quest_module"] = mod_num
                await send_quest(bot, chat_id, state, practice_modules)
            else:
                await bot.send_message(chat_id, "Квест не найден.")
        except ValueError:
            await bot.send_message(chat_id, "Некорректный номер квеста.")

    elif text == "➡️ Далее":
        state["quest"] = state.pop("next_after", "1")
        await send_quest(bot, chat_id, state, practice_modules)

    else:
        await handle_quest(bot, chat_id, text, state, practice_modules)

    save_user_state(str(chat_id), state)
    return {"statusCode": 200}
