from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.baza import*
from data.config import*
from datetime import datetime
from keyboards.inline.main_inline import*
from keyboards.default.main_reply import*
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    userid = message.chat.id
    with open("photos/cartel.jpg", "rb") as cartel:
        if check_new_user(userid) == True:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_new_user(userid,date)
            await message.answer_photo(photo=cartel, caption=f"<b>{message.from_user.full_name}, Вас приветствует бот автопродаж Hot Tropics</b> 🇲🇽\n\n"
                                                            "👨‍⚖️ <code>Ознакомьтесь с правилами шопа!</code>", reply_markup=start_menu())
            await bot.send_message(chat_id=LOGS_CHAT, text=f'🐘 В нашем боте новый пользователь: <a href="tg://user?id={message.chat.id}">{message.from_user.full_name}</a>\n'
                                                        f'└@{message.from_user.username}')

        else:
            await message.answer_photo(photo=cartel, caption=f"<b>{message.from_user.full_name}, Приветствуем Вас снова, Мы вас ждали❤️</b> 🇲🇽",reply_markup=main_menu())
    
        

        