import time

from scripts import *
from aiogram import Bot, Dispatcher, types, executor

TOKEN = "6475140627:AAEN1UhefpAdDDF5jzjdJpHiusWObu09YU0"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

WB = WbCards()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await bot.send_message(message.chat.id, 'Добро пожаловать. Этот бот отслеживает лучшие товары на Озоне и Вайлдберриз,'
                                            ' для использования выполните напишите любую вещь, в которой вы нуждаетесь и он'
                                            ' вам покажет то, что вы ищете')

@dp.message_handler()
async def searchInfo(message:types.Message):
    await bot.send_message(message.chat.id, 'Запрос обрабатывается, подожите...')

    count = 0
    try:
        cards = WB.UploadInfo(message.text)
        for id, info in cards.items():
            text = f'''Название: {info['name']}\nРейтинг: {info['rate']}⭐️️\n<b>Стоимость: {info['price']}</b>\nСсылка: {info['link']}'''
            await bot.send_message(message.chat.id, text)
            time.sleep(0.75)
            count += 1
            if count == 10:
                break
        if len(cards) == 0:
            await bot.send_message(message.chat.id, 'Ничего не удалось найти по данному запросу')
    except Exception as ex:
        await bot.send_message(message.chat.id, 'Запрос не был выполнен 😔\nПопробуйте составить его по-другому')

def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()