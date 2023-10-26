from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
import random
from keyboards.inline.main_admin import*
from aiogram.types.message import ContentType
from keyboards.default.main_reply import buy_menu, city_but, main_menu, staff_but
from keyboards.inline.main_inline import*
from data.config import*
from bot_text import*
from generate_id import*
from crypto_tracker import*
from banker import*
from handlers.users.qiwi_pay import*
from states.state import*
from lists_bot import*
from converter_time import*
from loader import dp, bot





@dp.message_handler(commands=['admin', 'adm', 'админ'])
async def admin_menu(message: types.Message):
    if str(message.chat.id) in ADMINS:
        await message.answer(f"👨‍⚖️ <b>Админ:</b> <code>{message.from_user.username}</code>", reply_markup=admin_but())
    else:
        pass

@dp.message_handler(lambda message: message.text == "💼 Профиль")
async def bot_send_user_profile(message: types.Message):
    photo = await bot.get_user_profile_photos(message.chat.id)
    cnt = photo.total_count
    if int(cnt) == 0:
        avatar = open('photos/cartel.jpg', 'rb')
    else:
        avatar = photo.photos[0][1]['file_id']

    await message.answer_photo(photo=avatar, caption=profile_text(message.chat.id, message.from_user.full_name), reply_markup=profile_but(message.chat.id))


@dp.message_handler(lambda message: message.text == "🚑 Помощь при передозировках")
async def bot_send_city(message: types.Message):
    with open("photos/MGH.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="🏥 <code>Первая помощь при передозировках ПАВ - Mega Health</code>", reply_markup=svyr_but())

@dp.message_handler(lambda message: message.text == "🌇 Выбор города")
async def bot_send_city(message: types.Message):
    with open("photos/cartel.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="🤵‍♂️ <code>Выберите свой город...</code>", reply_markup=city_but())

    await MAKE_DEAL.city.set()

@dp.message_handler(lambda message: message.text == "👨‍⚖️ Поддержка")
async def bot_send_city(message: types.Message):
    with open("photos/support.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="📑 <code>Мы на связи 24/7 для решения ваших вопросов. Опишите вашу проблему со всеми деталями, что бы мы могли быстрее вам помочь</code>", reply_markup=support_but())

@dp.message_handler(lambda message: message.text in city_list, state=MAKE_DEAL.city)
async def bot_send_staff(message: types.Message, state=FSMContext):
    with open("photos/cartel.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="🤵‍♂️ <code>Выберите товар...</code>", reply_markup=staff_but())
    
    async with state.proxy() as data:
        data['city'] = message.text
    await MAKE_DEAL.staff.set()

@dp.message_handler(lambda message: message.text in staff_list, state=MAKE_DEAL.staff)
async def bot_send_rayon_info(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['staff'] = message.text
        with open("photos/cartel.jpg", "rb") as cartel:
            staff = message.text.split("—")[0]
            await message.answer_photo(photo=cartel, caption=f"<b>🌃 Выбран район:</b> <code>{data['city'][2:]}</code>\n"
            f"📦 <b>Выбран товар:</b> <code>{staff[2:]}</code>\n\n"
            "🌆 <i>Напишите (район или улицу вашего города)</i>\n"
            "🤖 <i>По этим данным наш бот найдет ближайший, актуальный GPS адрес с фото и его описанием.</i>\n\n"
            "📑 <b>Пример:</b> <code>Район Ленинский. | Улица Пушкина.</code>\n\n"
            "⚠️ <b>Если вы не указываете желаемое территориальное местоположение клада, или даете ложные придуманные районы улицы,то адрес будет выбран ботом автоматически в указанном вами городе!</b>", reply_markup=buy_menu())
    
    await MAKE_DEAL.rayon.set()

@dp.message_handler(lambda message: message.text == "📂 Главное меню", state="*")
async def bot_back_menu(message: types.Message, state=FSMContext):
    await state.finish()
    with open("photos/cartel.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="📂 <code>Главное меню...</code>", reply_markup=main_menu())

@dp.message_handler(lambda message: message.text == "🌃 Вернутся к выбору города", state="*")
async def bot_back_city(message: types.Message, state=FSMContext):
    await state.finish()
    with open("photos/cartel.jpg", "rb") as cartel:
        await message.answer_photo(photo=cartel, caption="🤵‍♂️ <code>Выберите свой город...</code>", reply_markup=city_but())
    await MAKE_DEAL.city.set()



@dp.message_handler(state=MAKE_DEAL.rayon)
async def send_buy_info(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        k = 0
        c = 0
        city = data['city']
        staff_info = data['staff']
        staff_info = staff_info.split("—")
        staff = staff_info[0]
        price = staff_info[1]
        summa = price.split(" ")[1]
        price_btc = round((int(summa) / curs_btc()), 8)
        staff_id = generate_id()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=60)
        end_date = end_date.strftime("%Y-%m-%d %H:%M")
        type_klad = ["Магнит", "Тайник", "Прикоп"]
        klad_type = random.choice(type_klad)
        find_message = ["🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса...","🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса...",
        "🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса...","🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса...",
        "🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса...","🔴 Идет поиск адреса.", "🟡 Идет поиск адреса..", "🟣 Идет поиск адреса..."]
        await state.finish()
        await message.answer_sticker("CAACAgIAAxkBAAEDVVphmnFulD5yLjGlHd8mSoNA-7odAgACSQIAAladvQoqlwydCFMhDiIE", reply_markup=main_menu())
        msg = await message.answer("🔍 <code>Поиск адреса займёт некоторое время, ожидайте...</code>")
        await asyncio.sleep(1)
        for mes in find_message:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"<code>{mes}</code>")
            k = random.randint(1,1)
            c += 1
            await asyncio.sleep(0.4)
        if c == len(find_message):
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        
        with open("photos/cartel.jpg", "rb") as cartel:
            if k % 1 == 0:
                info_pay = create_payment_link(summa)
                add_new_buy(message.chat.id, staff_id, summa, price_btc, staff, klad_type, city, end_date)
                await message.answer_photo(photo=cartel, caption="🔥 <code>Найден адрес в базе...</code>\n\n"
                f"🆔 <b>Товара:</b> <code>{staff_id}</code>\n"
                f"🌃 <b>Район:</b> <code>{city[2:]}</code>\n"
                f"📦 <b>Товар:</b> <code>{staff[2:]}</code>\n"
                f"⛏ <b>Тип клада:</b> <code>{klad_type}</code>\n"
                f"📄 <b>Формат адреса:</b> <code>Фото с описанием + геопозиция</code>\n"
                f"🏦 <b>Цена:</b> <code>{price[1:]} | {price_btc} btc</code>\n\n"
                f"⌛️ <b>Время на оплату:</b> <code>60 мин.</code>", reply_markup=pay_menu(staff_id,info_pay[0], info_pay[1]))
               
                await bot.send_message(chat_id=LOGS_CHAT, text=f"🧙‍♂️ Пользователь <a href='tg://user?id={message.chat.id}'>{message.from_user.full_name}</a> находится в меню оплаты\n"
                f"└@{message.from_user.username}\n\n"
                f"🌃 <b>Район:</b> <code>{city[2:]}</code>\n"
                f"🎆 <b>Район:</b> <code>{message.text}</code>\n"
                f"📦 <b>Товар:</b> <code>{staff[2:]}</code>\n"
                f"🏦 <b>Цена:</b> <code>{price[1:]} | {price_btc} btc</code>", reply_markup=auto_rayon(message.chat.id))
           # else:
            #    await message.answer_photo(photo=cartel, caption="☹️ <code>По близости нет адресов</code>\n\n"
            #    "👨‍⚖️ <code>Для более подробной информации Вы можете связаться с нашим оператором.</code>")







@dp.message_handler(state=BALANCE.summa)
async def payment_link(message: types.Message, state=FSMContext):
    try:
        await message.delete()
        async with state.proxy() as data:
            if message.text.isdigit():
                pay_info = create_payment_link(message.text)
                await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'],caption="<b>⚡️Счёт на оплату успешно сформирован. Чтобы оплатить перейдите по ссылке оплаты, которая находится в кнопке.\n\n"
                "ℹ️ Реквизиты действительны в течении 30 минут, по истечению этого времени деньги не будут зачислены на ваш баланс! Если вы оплатили, но платеж не зачислился направьте информацию Оператору продаж по кнопке ниже\n"
                 "➖➖➖➖➖➖➖➖➖\n"
               # f"🥝 <b>Реквизиты QIWI:</b> <code>+(Номер телефона)</code>\n"
                f"🔖 <b>Комментарий к платежу:</b> <code>{random.randint(9999999,1000000000)}</code>\n"
                f"💰 Сумма к оплате:</b> <code>{message.text} руб.</code>\n"
               #  "➖➖➖➖➖➖➖➖➖\n"
                f"💳 <b>Реквизиты карты:</b> <code>2204 1202 0005 3078</code>\n"
             #   f"💰 <b>Сумма к оплате:</b> <code> {message.text} руб.</code>\n\n"
              #  f"🌐 <b>Реквизиты действительны в течении 30 минут, по истечению этого времени деньги не будут зачислены на ваш баланс! Если вы оплатили, но платеж не зачислился направьте информацию Оператору продаж по кнопке ниже</b>\n"
                
                
                ,reply_markup=pay_link_button(pay_info[0], pay_info[1], message.text))
                await state.finish()
            else:
                await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption=f"⚠️ <b>Не верный формат ввода:</b> <code>{message.text}</code>\n\n"
                "🤵‍♂️ <code>Повторите ввод или нажмите на кнопку отмены</code>",reply_markup=cancel_payment())

    except:
        pass





@dp.message_handler(state=BALANCE.btc_ticket)
async def get_btc_check(message: types.Message, state = FSMContext):
    await message.delete()
    try:
        async with state.proxy() as data:
            if "BTC_CHANGE_BOT" in message.text:
                ticket = message.text.split("=")[1]
                banker_response = await checked_btc(ticket)
                if banker_response == False:
                    await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption="☹️ <b>Упс, кажется, данный чек успел обналичить кто-то другой</b>\n\n"
                                                                                                                    "🤵‍♂️ <code>Отправьте другой чек или нажмите на кнопку отмены</code>",reply_markup=cancel_payment())
                else:
                    amount = round(float(banker_response) * curs_btc())
                    add_balance(message.chat.id, amount)
                    photo = await bot.get_user_profile_photos(message.chat.id)
                    cnt = photo.total_count
                    if int(cnt) == 0:
                        avatar = open('photos/cartel.jpg', 'rb')
                    else:
                        avatar = photo.photos[0][1]['file_id']

                    await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption=f"💸 <b>Ваш баланс был успешно пополнен на сумму <code>{amount} руб.</code></b>")
                    await message.answer_photo(photo=avatar, caption=profile_text(message.chat.id, message.from_user.full_name), reply_markup=profile_but())
                    await state.finish()

            else:
                await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption=f"☹️ <b>Не верный формат чека:</b> <code>{message.text}</code>\n\n"
                                                                                                                "🤵‍♂️ <code>Отправьте другой чек или нажмите на кнопку отмены</code>",reply_markup=cancel_payment())

    except Exception as err:
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption="☹️ <b>Не удалось обналичить ваш чек.</b>\n\n"                                                                                    "🤵‍♂️ <code>Отправьте другой чек или нажмите на кнопку отмены</code>",reply_markup=cancel_payment())
        logging.exception(err)


@dp.message_handler(state=SPAM_DATA.text)
async def get_text_for_spam(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        msg = await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="🖇 Введите данные для кнопки под текстом. Формат ввода (текст ссылка) если хотите отправить без кнопки введите просто 0.",reply_markup=cancel_but())
        data['message_id'] = msg.message_id
        data['text'] = message.text
        await SPAM_DATA.but_info.set()


@dp.message_handler(state=SPAM_DATA.photo, content_types=ContentType.ANY)
async def get_photo_for_spam(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if message.content_type == "photo":
            file_id =  message.photo[0].file_id
            msg = await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💠 Введите текст под фото",reply_markup=cancel_but())
            data['photo'] = file_id
            data["message_id"] = msg.message_id
            await SPAM_DATA.caption.set()
        else:
            msg = await message.answer("Отправьте фото!")
            await asyncio.sleep(1)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)



@dp.message_handler(state=SPAM_DATA.video, content_types=ContentType.ANY)
async def get_video_for_spam(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if message.content_type == "video":
            file_id =  message.video.file_id
            msg = await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💠 Введите текст под видео",reply_markup=cancel_but())
            data['video'] = file_id
            data["message_id"] = msg.message_id
            await SPAM_DATA.caption.set()
        else:
            msg = await message.answer("Отправьте видео!")
            await asyncio.sleep(1)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

@dp.message_handler(state=SPAM_DATA.animation, content_types=ContentType.ANY)
async def get_animation_for_spam(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if message.content_type == "animation":
            file_id =  message.animation.file_id
            msg = await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💠 Введите текст под гифку",reply_markup=cancel_but())
            data['animation'] = file_id
            data["message_id"] = msg.message_id
            await SPAM_DATA.caption.set()
        else:
            msg = await message.answer("Отправьте гифку!")
            await asyncio.sleep(1.5)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)



@dp.message_handler(state=SPAM_DATA.caption)
async def get_caption(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        msg = await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="🖇 Введите данные для кнопки под текстом. Формат ввода (текст ссылка) если хотите отправить без кнопки введите просто 0.",reply_markup=cancel_but())
        data['message_id'] = msg.message_id
        data['caption'] = message.text
        await SPAM_DATA.but_info.set()



@dp.message_handler(state=SPAM_DATA.but_info)
async def get_info_for_but(message: types.Message, state=FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            if "http" in message.text.split(" ")[1]:
                data['but_info'] = message.text
                key = spam_with_but(message.text.split(" ")[0], message.text.split(" ")[1])
        except:
            data['but_info'] = 0
            key = spam_withot_but()

            
        if data["check_spam_type"] == "txt":
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            msg = await message.answer("Проверьте данные для рассылки.\n\n"
            f"{data['text']}\n\n"
            "Чтобы отправить рассылку отправьте + | чтобы отменить рассылку отправьте -", reply_markup=key)
            data['message_id'] = msg.message_id
            await SPAM_DATA.confirm_spam.set()
        
        elif data["check_spam_type"] == "photo":
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            msg = await message.answer_photo(photo=data['photo'], caption="Проверьте данные для рассылки.\nЧтобы отправить рассылку отправьте + | чтобы отменить рассылку отправьте -\n\n"
            f"{data['caption']}", reply_markup=key)
            data['message_id'] = msg.message_id
            await SPAM_DATA.confirm_spam.set()
        
        elif data["check_spam_type"] == "video":
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            msg = await message.answer_video(video=data['video'], caption="Проверьте данные для рассылки.\nЧтобы отправить рассылку отправьте + | чтобы отменить рассылку отправьте -\n\n"
            f"{data['caption']}", reply_markup=key)
            data['message_id'] = msg.message_id
            await SPAM_DATA.confirm_spam.set()
        
        elif data["check_spam_type"] == "animation":
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            msg = await message.answer_animation(animation=data['animation'], caption="Проверьте данные для рассылки.\nЧтобы отправить рассылку отправьте + | чтобы отменить рассылку отправьте -\n\n"
            f"{data['caption']}", reply_markup=key)
            data['message_id'] = msg.message_id
            await SPAM_DATA.confirm_spam.set()


@dp.message_handler(state=SPAM_DATA.confirm_spam)
async def get_confirm(message: types.Message, state=FSMContext):
    await message.delete()
    if "+" in message.text:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            if data['but_info'] == 0:
                key = spam_withot_but()
            else:
                info = data['but_info'].split(" ")
                key = spam_with_but(info[0], info[1])
            
            if data["check_spam_type"] == "txt":
                text_for_spam = data['text']
                await state.finish()
                users = users_id_for_spam()
                k = 0
                l = 0
                msg = await message.answer("⚡️ Рассылка текстом успешно запущена.")
                for userid in users:
                    try:
                        await bot.send_message(chat_id=userid[0], text=text_for_spam,parse_mode="html", reply_markup=key)
                        k += 1
                        await asyncio.sleep(0.1)
                    except Exception as err:
                        l += 1
                        if "bot was blocked by the user" in str(err):
                            clear_bd(userid[0])
                        else:
                            logging.exception(err)
                        
                await message.answer(f"✅ Рассылка текстом завершена.\n\n"
                f"🔥 Доставлено: {k} смс\n"
                f"💢 Не доставлено {l} смс", reply_markup=spam_withot_but())
            
            elif data["check_spam_type"] == "photo":
                file_id = data['photo']
                caption = data['caption']
                await state.finish()
                users = users_id_for_spam()
                k = 0
                l = 0
                msg = await message.answer("⚡️ Рассылка фото успешно запущена.")
                for userid in users:
                    try:
                        await bot.send_photo(chat_id=userid[0], photo=file_id,caption=caption,parse_mode="html", reply_markup=key)
                        k += 1
                        await asyncio.sleep(0.1)
                    except Exception as err:
                        l += 1
                        if "bot was blocked by the user" in str(err):
                            clear_bd(userid[0])
                        else:
                            logging.exception(err)
                await message.answer(f"✅ Рассылка фото завершена.\n\n"
                f"🔥 Доставлено: {k} смс\n"
                f"💢 Не доставлено {l} смс", reply_markup=spam_withot_but())

            
            elif data["check_spam_type"] == "video":
                file_id = data['video']
                caption = data['caption']
                await state.finish()
                users = users_id_for_spam()
                k = 0
                l = 0

                msg = await message.answer("⚡️ Рассылка видео успешно запущена.")
                for userid in users:
                    try:
                        await bot.send_video(chat_id=userid[0], video=file_id,parse_mode="html", reply_markup=key)
                        k += 1
                        await asyncio.sleep(0.1)
                    except Exception as err:
                        l += 1
                        if "bot was blocked by the user" in str(err):
                            clear_bd(userid[0])
                        else:
                            logging.exception(err)
                await message.answer(f"✅ Рассылка видео завершена.\n\n"
                f"🔥 Доставлено: {k} смс\n"
                f"💢 Не доставлено {l} смс", reply_markup=spam_withot_but())

            elif data["check_spam_type"] == "animation":
                file_id = data['animation']
                caption = data['caption']
                await state.finish()
                users = users_id_for_spam()
                k = 0
                l = 0 
                msg = await message.answer("⚡️ Рассылка гифкой успешно запущена.")
                for userid in users:
                    try:
                        await bot.send_animation(chat_id=userid[0], animation=file_id,parse_mode="html", reply_markup=key)
                        k += 1
                        await asyncio.sleep(0.1)
                    except Exception as err:
                        l += 1
                        if "bot was blocked by the user" in str(err):
                            clear_bd(userid[0])
                        else:
                            logging.exception(err)
                await message.answer(f"✅ Рассылка гифкой завершена.\n\n"
                f"🔥 Доставлено: {k} смс\n"
                f"💢 Не доставлено {l} смс", reply_markup=spam_withot_but())
            await asyncio.sleep(5)
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
            await message.answer("⚡️ Рассылка успешно отменена.", reply_markup=admin_but())

        await state.finish()



@dp.message_handler(state=ADMIN_INFO.p2p)
async def bot_change_p2p(message: types.Message, state=FSMContext):
    await message.delete()
    p2p = message.text
    async with state.proxy() as data:
        if set_p2p(p2p) == True:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="✅ <i>P2P ключ был успешно установлен.</i>", reply_markup=admin_but())
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💢 <i>P2P ключ не установился.</i>", reply_markup=admin_but())

    await state.finish()

@dp.message_handler(state=ADMIN_INFO.btc)
async def bot_change_btc(message: types.Message, state=FSMContext):
    await message.delete()
    btc = message.text
    async with state.proxy() as data:
        if set_btc(btc) == True:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="✅ <i>BTC adress был успешно установлен.</i>", reply_markup=admin_but())
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💢 <i>BTC adress не установился.</i>", reply_markup=admin_but())

    await state.finish()

@dp.message_handler(state=ADMIN_INFO.usdt)
async def bot_change_usdt(message: types.Message, state=FSMContext):
    await message.delete()
    usdt = message.text
    async with state.proxy() as data:
        if set_usdt(usdt) == True:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="✅ <i>USDT adress был успешно установлен.</i>", reply_markup=admin_but())
        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text="💢 <i>USDT adress  не установился.</i>", reply_markup=admin_but())

    await state.finish()

async def timer(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        info = all_buscket()
        if len(info) == 0:
            pass
        else:
            for i in info:
                info_staff = staff_info(i[0])
                now = datetime.now().strftime('%Y-%m-%d %H:%M')
                t1 = info_staff[7]
                t2 = str(now)
                date_format = "%Y-%m-%d %H:%M"
                t1_object = to_datetime_object(t1, date_format)
                t2_object = to_datetime_object(t2, date_format)
                check_time = t1_object - t2_object
                check_time = str(check_time)
                if "day" in check_time or "days" in check_time:
                    arr = check_time.split(" ")
                    if int(arr[0]) <= 0:
                        delete_basket(info_staff[1])
                else:
                    time_to_pay = check_time.split(":")[1]
                    if time_to_pay in time_list:
                        await bot.send_message(chat_id=info_staff[0], text=f"🤵‍♂️ <code>Заказ #{info_staff[1]} | {info_staff[4][2:]} осталось {time_to_pay} мин. на оплату...</code>")
                    else:
                        pass

