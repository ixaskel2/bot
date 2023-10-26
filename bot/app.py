from aiogram import executor
import asyncio
from handlers.users.echo import timer
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.create_db import*
from utils.db_api.baza import*


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    create_db()
    admins_setting_info()
    loop = asyncio.get_event_loop()
    loop.create_task(timer(60))
    executor.start_polling(dp, on_startup=on_startup)
