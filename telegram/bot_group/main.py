from time import sleep  # for stop program on any time :192:
from os import getenv, system  # getenv: get token from env :177: :193:
import sys  # for logging :188:
import urllib  # download image from url :108:
from asyncio import run  # run async functions :195:
from logging import basicConfig, INFO  # for logging :188:
from random import randint  # for get random filename :107:
from gtts import gTTS
from aiogram import (
    Bot,
    Dispatcher,
    Router
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from win10toast import ToastNotifier  # send windows OS message
import openai  # chatgpt, dall-e bots
from dotenv import load_dotenv  # set virtual environment
from rich.console import Console  # beautiful print (log)
from count import count_pages_of_project


load_dotenv('\\Users\\Shadowraze\\Documents\\Python\\.env')

openai.api_key = getenv('OPENAI_TOKEN')

main_router = Router()


class ChatGPT(StatesGroup):
    get_response = State()


class Dalle(StatesGroup):
    get_response = State()


class GTTS(StatesGroup):
    get_response = State()


@main_router.message(Command(commands=['chatgpt'], ignore_case=True))
async def call_chatgpt(message: Message, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))

    await bot.send_animation(
        chat_id=message.chat.id,
        animation=FSInputFile('\\Users\\ShadowRaze\\Desktop\\test.gif'),
        caption='Enter your request:',
    )

    await state.set_state(ChatGPT.get_response)

    await bot.session.close()


@main_router.message(ChatGPT.get_response)
async def chatgpt(message: Message, state: FSMContext):
    response = openai.Completion.create(
        prompt=str(message.text).replace('chatgpt', '').strip(),
        model='text-davinci-003',
        temperature=0,
        max_tokens=1000,
        n=1
    )

    await message.answer(response['choices'][0]['text'])

    await state.clear()


@main_router.message(Command(commands=['dall_e'], ignore_case=True))
async def call_dalle(message: Message, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))

    await bot.send_animation(
        chat_id=message.chat.id,
        animation=FSInputFile('\\Users\\ShadowRaze\\Desktop\\test.gif'),
        caption='Enter your request:',
    )

    await state.set_state(Dalle.get_response)


@main_router.message(Dalle.get_response)
async def dalle(message: Message, state: FSMContext):
    image_response = openai.Image.create(
        prompt=str(message.text).replace('dall-e', ''),
        n=1,
        size='1024x1024'
    )

    await message.answer(image_response['data'][0]['url'])
    
    name = f'\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot\\media\\images\\{randint(-100_000, 100_000)}.png'
    urllib.request.urlretrieve(str(image_response['data'][0]['url']), filename=name)

    await state.clear()


@main_router.message(Command(commands=['GTTS'], ignore_case=True))
async def call_gtts(message: Message, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))

    await bot.send_animation(
        chat_id=message.chat.id,
        animation=FSInputFile('\\Users\\ShadowRaze\\Desktop\\test.gif'),
        caption='Enter your request:',
    )

    await state.set_state(GTTS.get_response)


@main_router.message(GTTS.get_response)
async def gtts(message: Message, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))
    text = str(message.text).strip()

    if text.startswith('ru'):
        language = 'ru'
        text = text.replace('ru', '').strip()
    if message.text.startswith('en'):
        language = 'en'
        text = text.replace('en', '').strip()
    else:
        language = 'uk'

    file_name = f'{randint(-100_000, 100_000)}.mp3'
    file_path = f'\\Users\\Shadowraze\\Documents\\Python\\telegram\\telegram_bot\\media\\audios\\{file_name}'

    audio = gTTS(text=text, lang=language)
    audio.save(file_path)

    file = FSInputFile(file_path)    
    
    await bot.send_audio(
        chat_id=message.chat.id,
        audio=file,
        performer='ShadowRaze',
        title='Google Text-To-Speech'
    )

    await state.clear()

    await bot.session.close()


async def on_startup(botter):
    ''' # send message to all users
    for id in await db.get_all_sending_IDs():
        try:
            if await db.check_sending(id):
                await botter.send_message(
                    chat_id=id,
                    text='Bot was started up!'
                )
            else:
                print(119)
        except Exception as ex:
            print(ex)
    '''

    lines = await count_pages_of_project()

    ToastNotifier().show_toast(  # show windows notify when bot start
        title='I was started up!',
        msg=f'Aiogram bot was started up!\n\n{lines[-1]}',
        duration=15,
        icon_path='C:\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot\\media\\telegram.ico'
    )

    print('I was started up!')


async def main():
    bot = Bot(token=getenv("TG_TOKEN"))
    dp = Dispatcher()

    await on_startup(bot)

    dp.include_router(main_router)

    await dp.start_polling(bot)

    await bot.session.close()


if __name__ == "__main__":
    basicConfig(level=INFO, stream=sys.stdout)
    try:
        run(main())  # asyncio
    except KeyboardInterrupt:
        sleep(3)
        system('cls')  # clear console if you stop bot (CTRL + C)
    except:
        Console().print_exception()  # print beautiful exception
