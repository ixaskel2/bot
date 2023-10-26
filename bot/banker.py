from time import sleep
from telethon import TelegramClient
import asyncio
import re


api_id = 28508489
api_hash = '8d48cca9afb813797d01710b0745cef9'
me_id = 6687139834
client = TelegramClient('banker', api_id, api_hash, device_model="Iphone", system_version="6.12.0",
                        app_version="10 P (28)")

client.start()

async def checked_btc(cheque):
    await client.send_message('BTC_CHANGE_BOT', '/start ' + cheque)
    await asyncio.sleep(0.2)
    response = await get_last_message()
    if "Упс, кажется, данный чек успел обналичить кто-то другой 😟" in response:
            return False
    try:
        response = float(re.findall(r'Вы получили (\d+\.\d+) BTC', response)[0])
    except IndexError or ValueError:
        return False
    return response
    
async def get_last_message():
        while True:
            message = (await client.get_messages("BTC_CHANGE_BOT", limit=1))[0]
            if message.message.startswith("Приветствую,"):
                sleep(0.5)
                continue
            if message.from_id is not None:
                if message.from_id.user_id == me_id:
                    sleep(0.5)
                    continue
            else:
                return message.message
                
