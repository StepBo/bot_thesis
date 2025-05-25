
import os
import json
import asyncio
from telegram import Bot
from loader.state import s3, BUCKET_NAME

async def send_daily_reminder(bot: Bot, chat_ids: list):
    for chat_id in chat_ids:
        try:
            await bot.send_message(
                chat_id,
                "🔔 Напоминание: не забудьте пройти следующий шаг в боте по финансовой грамотности!"
            )
        except Exception as e:
            print(f"Не удалось отправить напоминание пользователю {chat_id}: {e}")

def get_all_chat_ids_from_s3():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="users/")
        objects = response.get("Contents", [])
        return [obj["Key"].split("/")[1].replace(".json", "") for obj in objects if obj["Key"].endswith(".json")]
    except Exception as e:
        print(f"Ошибка при получении списка пользователей: {e}")
        return []

def handler(event, context):
    async def main():
        bot = Bot(token=os.environ["BOT_TOKEN"])
        chat_ids = get_all_chat_ids_from_s3()
        await send_daily_reminder(bot, chat_ids)

    asyncio.run(main())
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Reminders sent"})
    }
