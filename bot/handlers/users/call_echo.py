import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.input_media import InputMedia, InputFile
from keyboards.inline.main_inline import*
from keyboards.default.main_reply import*
from keyboards.inline.main_admin import*
from datetime import datetime
from bot_text import*
from states.state import*
from handlers.users.qiwi_pay import*
from converter_time import*
from crypto_tracker import*
import random
from loader import dp, bot


@dp.callback_query_handler(text="accept_rules")
async def bot_send_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_caption("🇲🇽 <code>Mexican Cartel</code>")
    await call.message.answer("⚡️", reply_markup=main_menu())

@dp.callback_query_handler(text="add_balance")
async def bot_send_payment_menu(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_caption("💸 <b>Выбирите метод пополнения баланса</b>", reply_markup=payment_menu())

@dp.callback_query_handler(text="back_to_profile")
async def bot_back_to_profile(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_caption(profile_text(call.message.chat.id, call.from_user.full_name), reply_markup=profile_but(call.message.chat.id))

@dp.callback_query_handler(text="my_buys")
async def bot_send_my_buys(call: types.CallbackQuery):
    await call.answer("☹️ У вас не было покупок")


@dp.callback_query_handler(text="close_spam")
async def bot_close_spam(call: types.CallbackQuery):
    try:
        await call.answer()
        await call.message.delete()
    except:
        await call.answer("💢")


@dp.callback_query_handler(text="hide_adm")
async def bot_hide_admin(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("🧛‍♀️ <code>Админ панель скрыта...</code>")

@dp.callback_query_handler(text="check_pay")
async def bot_check_pay(call: types.CallbackQuery):
    await call.answer("💢 Платеж не найден")
    await bot.send_message(chat_id=LOGS_CHAT, text=f'✅ Пользователь: <a href="tg://user?id={call.message.chat.id}">{call.from_user.full_name}</a>, подтвердил оплату по реквизитам!\n'
                                            f'└@{call.from_user.username}\n')
    await asyncio.sleep(1)


@dp.callback_query_handler(text="back_to_admin")
async def bot_hide_admin(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(f"👨‍⚖️ <b>Админ:</b> <code>{call.from_user.full_name}</code>", reply_markup=admin_but())


@dp.callback_query_handler(text="set_p2p")
async def bot_set_p2p(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    msg = await call.message.edit_text("🔑 <b>Введите p2p ключ</b>", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await ADMIN_INFO.p2p.set()

@dp.callback_query_handler(text="set_btc")
async def bot_set_p2p(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    msg = await call.message.edit_text("🔑 <b>Введите btc адрес</b>", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await ADMIN_INFO.btc.set()

@dp.callback_query_handler(text="set_usdt")
async def bot_set_p2p(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    msg = await call.message.edit_text("🔑 <b>Введите usdt адрес</b>", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
    await ADMIN_INFO.usdt.set()

@dp.callback_query_handler(text="stata")
async def statistik_info(call: types.CallbackQuery):
    try:
        await call.message.edit_text(f"🤵‍♂️ На данный момент в боте {count_users()} чел.", reply_markup=admin_but())
    except:
        await bot.answer_callback_query(call.id, "Users info👇")

@dp.callback_query_handler(text="settings")
async def statistik_info(call: types.CallbackQuery):
    try:
        await call.message.edit_text(f"🔑 <b>P2P ключ:</b> <code>{admins_setting_info()[0]}</code>\n\n"
        f"⚒ <b>BTC adress:</b> <code>{admins_setting_info()[1]}</code>\n\n"
        f"🛠 <b>USDT adress:</b> <code>{admins_setting_info()[2]}</code>", reply_markup=admin_but())
    except Exception as err:
        logging.exception(err)
        await bot.answer_callback_query(call.id, "Settings👇")



@dp.callback_query_handler(text="spam")
async def choose_types_spam(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text("✨ Выберите тип рассылки. Как будем отсылать?", reply_markup=spam_types())

@dp.callback_query_handler(text="spam_text")
async def send_text_for_spam(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer()
    msg = await call.message.answer("🌐 Введите текст для рассылки.", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        data['check_spam_type'] = "txt"
    await SPAM_DATA.text.set()

@dp.callback_query_handler(text="spam_pic")
async def send_pic_for_spam(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer()
    msg = await call.message.answer("🎆 Отправьте картинку для рассылки.", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        data['check_spam_type'] = "photo"
    await SPAM_DATA.photo.set()

@dp.callback_query_handler(text="spam_video")
async def send_video_for_spam(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer()
    msg = await call.message.answer("📹 Отправьте видео для рассылки.", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        data['check_spam_type'] = "video"
    await SPAM_DATA.video.set()

@dp.callback_query_handler(text="spam_gif")
async def send_gif_for_spam(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    await call.answer()
    msg = await call.message.answer("🌄 Отправьте гифку для рассылки.", reply_markup=cancel_but())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        data['check_spam_type'] = "animation"
    await SPAM_DATA.animation.set()


@dp.callback_query_handler(text="basket")
async def basket_info(call: types.CallbackQuery):
    try:
        lenth = len(get_busket_info(call.message.chat.id))
        if lenth == 0:
            await call.answer("💢 Нет товара в корзине")
        else:
            await call.message.edit_caption(f"🗑 <b>Товаров в корзине:</b> <code>{lenth} шт.</code>", reply_markup=busket_but(get_busket_info(call.message.chat.id)))
    except:
        pass


@dp.callback_query_handler(text="cancel_payment", state="*")
async def bot_cancel_payment(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    photo = await bot.get_user_profile_photos(call.message.chat.id)
    cnt = photo.total_count
    if int(cnt) == 0:
        await call.message.edit_media(InputMedia(media=InputFile("photos/cartel.jpg"), caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but(call.message.chat.id))
    else:
        avatar = photo.photos[0][1]['file_id']
        await call.message.edit_media(InputMedia(media=avatar, caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but(call.message.chat.id))

    await state.finish()    


@dp.callback_query_handler(text="add_qiwi")
async def payment_qiwi(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    msg = await call.message.edit_media(InputMedia(media=InputFile("photos/card_qiwi.png"), caption="💠 <b>Платежный метод пополнения:</b>\n\n"
                                                                                                    "💳  <b>Карта - Перевод</b>\n"
                                                                                                    "♻️ <code>Введите сумму пополнения.</code>"), reply_markup=cancel_payment())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        await BALANCE.summa.set()


@dp.callback_query_handler(text="add_banker")
async def payment_banker(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    msg = await call.message.edit_media(InputMedia(media=InputFile("photos/banker.jpg"), caption="💬 Создайте чек в рублях на любую сумму, которую хотите пополнить на счет. Чек можно создать в @BTC_CHANGE_BOT во вкладке <b>Кошелёк - BTC чек</b>"), reply_markup=cancel_payment())
    async with state.proxy() as data:
        data['message_id'] = msg.message_id
        await BALANCE.btc_ticket.set()

@dp.callback_query_handler(text="add_btc")
async def payment_btc(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_media(InputMedia(media=InputFile("photos/btc.jpg"), caption="💠 <b>Платежный метод пополнения:</b> <code>BTC</code>\n\n"
                                                                                        f"🛠 <b>BTC адрес для пополнения:</b> <code>{admins_setting_info()[1]}</code>\n\n"
                                                                                        "🆎 <i>Средства зачисляться на Ваш баланс автоматически, после второго подтверждения транзакции.</i>"), reply_markup=cancel_payment())
    

@dp.callback_query_handler(text="add_usdt")
async def payment_btc(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_media(InputMedia(media=InputFile("photos/usdt.jpg"), caption="💠 <b>Платежный метод пополнения:</b> <code>USDT</code>\n\n"
                                                                                        f"🛠 <b>USDT адрес для пополнения (ERC20):</b> <code>{admins_setting_info()[2]}</code>\n\n"
                                                                                        "🆎 <i>Средства зачисляться на Ваш баланс автоматически, после подтверждения транзакции.</i>"), reply_markup=cancel_payment())
    




@dp.callback_query_handler(state="*")
async def call_answer(call: types.CallbackQuery, state=FSMContext):
    action = call.data.split("+")

    if call.data == "cansel_spam":
        await call.answer()
        await call.message.edit_text("💢 <code>Дейсвтвия отменено...</code>", reply_markup=admin_but())
        await state.finish()


    if action[0] == "reject_payment":
        reject_payment_form(action[1])
        await state.finish()  
        await call.answer("💢")
        photo = await bot.get_user_profile_photos(call.message.chat.id)
        cnt = photo.total_count
        if int(cnt) == 0:
            await call.message.edit_media(InputMedia(media=InputFile("photos/cartel.jpg"), caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but())
        else:
            avatar = photo.photos[0][1]['file_id']
            await call.message.edit_media(InputMedia(media=avatar, caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but(call.message.chat.id))
          
    elif action[0] == "payed":
        if check_payment(action[1]) == "PAID":
            await call.answer("⚡️ Оплата найдена")
            add_balance(call.message.chat.id, action[2])
            photo = await bot.get_user_profile_photos(call.message.chat.id)
            cnt = photo.total_count
            if int(cnt) == 0:
                await call.message.edit_media(InputMedia(media=InputFile("photos/cartel.jpg"), caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but(call.message.chat.id))
            else:
                avatar = photo.photos[0][1]['file_id']
                await call.message.edit_media(InputMedia(media=avatar, caption=profile_text(call.message.chat.id, call.from_user.full_name)), reply_markup=profile_but(call.message.chat.id))

        else:
            await bot.answer_callback_query(call.id, "⚡️ Оплата не найдена")
    
    elif action[0] == "staff":
        
        info = staff_info(action[1])
        if info is None:
            await call.answer("💢 Товар не найден")
        else:
            await call.answer()
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            t1 = info[7]
            t2 = str(now)
            date_format = "%Y-%m-%d %H:%M"
            t1_object = to_datetime_object(t1, date_format)
            t2_object = to_datetime_object(t2, date_format)
            check_time = t1_object - t2_object
            check_time = str(check_time)
            time_to_pay = check_time.split(":")[1]
            link_info = create_payment_link(info[2])
            await call.message.edit_media(InputMedia(media=InputFile("photos/cartel.jpg"), caption=f"🔥 <code>Товар #{info[1]}</code>\n\n"
                                                                                                    f"🌃 <b>Район:</b> <code>{info[6][2:]}</code>\n"
                                                                                                    f"📦 <b>Товар:</b> <code>{info[4][2:]}</code>\n"
                                                                                                    f"⛏ <b>Тип клада:</b> <code>{info[5]}</code>\n"
                                                                                                    f"📄 <b>Формат адреса:</b> <code>Фото с описанием + геопозиция</code>\n"
                                                                                                    f"🏦 <b>Цена:</b> <code>{info[2]} руб. | {info[3]} btc</code>\n\n"
                                                                                                    f"⌛️ <b>Время на оплату:</b> <code>{time_to_pay} мин.</code>"), reply_markup=pay_menu(info[1],link_info[0], link_info[1]))
                
    elif action[0] == "cancel_pay":
        await call.answer()
        try:
            delete_basket(action[2])
            reject_payment_form(action[1])
        except:
            pass
        await call.message.edit_caption("💢 <code>Покупка товара отменена...</code>")
    
    elif action[0] == "hide_buy":
        await call.answer()
        try:
            reject_payment_form(action[1])
        except:
            pass
        await call.message.edit_caption("🧛‍♀️ <code>Окно оплаты товара скрыто...</code>\n\n"
        "🗑 <b>Ваш товар находится в корзине</b>")
    

    elif action[0] == "from_btc":
        try:
            info = staff_info(action[1])
            if info is None:
                await call.answer("💢 Время на оплату прошло")
            else:
                await call.answer()
                reject_payment_form(action[2])
                btc = admins_setting_info()[1]
                await call.message.edit_caption(f"🛠 <b>Адрес btc:</b> <code>{btc}</code>\n"
                f"🏦 <b>Сумма к оплате:</b> <code>{info[3]} btc</code>\n\n"
                "🆎 <i>Средства зачисляться автоматически, после второго подтверждения транзакции.</i>", reply_markup=cancel_payment())
        except:
            pass

    elif action[0] == "from_usdt":
        try:
            info = staff_info(action[1])
            if info is None:
                await call.answer("💢 Время на оплату прошло")
            else:
                await call.answer()
                reject_payment_form(action[2])
                usdt = admins_setting_info()[2]
                summa_usdt = round((int(info[2]) / curs_usd()),2)
                await call.message.edit_caption(f"🛠 <b>Адрес usdt:</b> <code>{usdt}</code>\n"
                f"🏦 <b>Сумма к оплате:</b> <code>{summa_usdt} usdt</code>\n\n"
                "🆎 <i>Средства зачисляться автоматически, после подтверждения транзакции.</i>", reply_markup=cancel_payment())
        except:
            pass

    elif action[0] == "from_balance":
        try:
            info = staff_info(action[1])
            if info is None:
                await call.answer("💢 Время на оплату прошло")
            else:
                balance = get_user_info(call.message.chat.id)[1]
                if int(info[2]) > int(balance):
                    await call.answer("⚠️ Недостаточно баланса")
                else:
                    await call.answer()
                    minus_balance(call.message.chat.id, info[2])
                    await call.message.edit_caption("✅ <code>Товар был успешно оплачен с баланса</code>\n\n"
                    "⌛️ <code>Ожидайте адрес в течении минуты...</code>")
        except:
            pass
    
    elif action[0] == "from_req":
        try:
            info = staff_info(action[1])
            if info is None:
                await call.answer("💢 Время на оплату прошло")
            else:
                await call.answer()
                reject_payment_form(action[2])
                await call.message.edit_caption("🧾 <b>Оплата по реквизатам</b>\n"
                f"📦 <b>Товар:</b> <code>{info[4][2:]}</code>\n"
                "➖➖➖➖➖➖➖➖➖\n"
              #  f"🥝 <b>Реквизиты QIWI:</b> <code>(Номертелефона)</code>\n"
              # f"🔖 <b>Комментарий к платежу:</b> <code>{random.randint(9999999,1000000000)}</code>\n"
              #  f"🏦 <b>Сумма к оплате:</b> <code>{info[2]} руб.</code>\n"
              #  "➖➖➖➖➖➖➖➖➖\n"
                f"💳 <b>Реквизиты карты:</b> <code>2204 1202 0005 3078</code>\n"
                f"💳 <b>Вы должны перевести ровно указанную сумму, иначе ваш платеж зачислен не будет!</b>\n"
                f"🏦 <b>Сумма к оплате:</b> <code>{info[2]} руб.</code>\n", reply_markup=check_payment_but())
        except Exception as err:
            logging.exception(err)
    
    elif action[0] == "auto":
        await call.answer("💥")
        await bot.send_message(chat_id=action[1], text="♻️ <code>Район выбран автоматически...</code>")
    




