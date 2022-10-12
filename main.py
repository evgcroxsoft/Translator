import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

lingvo = os.environ.get('Lingvo')
URL_AUTH = 'https://developers.lingvolive.com/api/v1.1/authenticate'
HEADERS_PARAMETERES = {'Authorization': f'{lingvo}'}

URL_TRANSL = 'https://developers.lingvolive.com/api/v1/Minicard'
ENG, RUS = 1033, 1049


bot = Bot(os.environ.get('Bot'))
dp = Dispatcher(bot)

# check cyrillic alphabet
def hascyr(word):
    lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return lower.intersection(word.lower()) != set()

@dp.message_handler()
async def echo_send(message : types.message):
    auth = requests.post(url=URL_AUTH, headers=HEADERS_PARAMETERES)
    if auth.status_code == 200:
        token = auth.text
    else:
        print('Error!')
    translate_header = {'Authorization': 'Bearer ' + token}
    word = message.text
    if word:
        if hascyr(word) == True:
            params1 = {'text': word, 'srcLang': 1049,  'dstLang': 1033}
            params2 = {'text': word, 'srcLang': 1049,  'dstLang': 1034}
        
            translate = requests.get(url=URL_TRANSL, headers=translate_header, params=params1)
            res1 = translate.json()
            translate2 = requests.get(url=URL_TRANSL, headers=translate_header, params=params2)
            res2 = translate2.json()

            try:
                result1 = res1['Translation']['Translation']
                result2 = res2['Translation']['Translation']
                await message.answer(f'ENGLISH - {result1}')
                await message.answer(f'SPAIN - {result2}')
            except:
                await message.answer("Try again, can't find in dictionary")

        elif hascyr(word) == False:
            params1 = {'text': word, 'srcLang': 1033,  'dstLang': 1049}

            translate = requests.get(url=URL_TRANSL, headers=translate_header, params=params1)
            res1 = translate.json()
 
            try:
                result1 = res1['Translation']['Translation']
                await message.answer(f'ENGLISH - {result1}')
            except:
                await message.answer("Try again, can't find in dictionary")

types.message

executor.start_polling(dp, skip_updates=True)


