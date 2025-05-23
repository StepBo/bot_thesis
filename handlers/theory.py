from telegram import Bot, ReplyKeyboardMarkup

async def send_theory(bot: Bot, chat_id: int, state: dict, theory_modules: dict):
    module = state.get("theory_module")
    index = state.get("theory_index", 0)
    blocks = theory_modules.get(module, [])

    if index < len(blocks):
        block = blocks[index]
        state["theory_index"] = index + 1
        await bot.send_message(chat_id, block)

        if state["theory_index"] < len(blocks):
            await bot.send_message(
                chat_id, "Нажми «далее» для продолжения.",
                reply_markup=ReplyKeyboardMarkup([["далее"]], resize_keyboard=True)
            )
        else:
            await bot.send_message(
                chat_id, f"📘 Теория модуля {module} завершена.",
                reply_markup=ReplyKeyboardMarkup([["🏠 В меню"]], resize_keyboard=True)
            )
    else:
        await bot.send_message(chat_id, f"📘 Теория модуля {module} завершена.")
