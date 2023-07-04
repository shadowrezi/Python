from time import sleep  # for stop program on any time :192:
from os import getenv, system  # getenv: get token from env :177: :193:
import sys  # for logging :188:
import urllib  # download image from url :108:
from asyncio import run  # run async functions :195:
from logging import basicConfig, INFO  # for logging :188:
from random import randint  # for get random filename :107:
from aiogram import (
    Bot,
    Dispatcher,
    Router
)
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from win10toast import ToastNotifier  # send windows OS message
import openai  # chatgpt, dall-e bots
from dotenv import load_dotenv  # set virtual environment
from rich.console import Console  # beautiful print (log)
from routers.admin import admin_router
from routers.others import others_router
import database as db  # control database (sqllite3)
from keyboard import bot_kb
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


# chatgpt context
messages = [
    {
        "role": "system",
        "content": "Answer fast, intelligently."
    }
]


async def update(messages, role, content):
    messages.append({"role": role, "content": content})


async def reset_messages():
    messages.clear()
    messages.append({
        "role": "system",
        "content": "You are a programming assistant at Proghunter.ru, helping users with Python and JavaScript programming with popular frameworks."
    })



@main_router.message(Command(commands=['bot'], ignore_case=True))
async def bot(message: Message):
    bot = Bot(token=getenv('TG_TOKEN'))

    await bot.send_animation(
        chat_id=message.chat.id,
        animation=FSInputFile('\\Users\\ShadowRaze\\Desktop\\test.gif'),
        caption='Select AI which you need:',
        reply_markup=await bot_kb()
    )

    await bot.session.close()


@main_router.callback_query(lambda callback: callback.data == 'chatgpt')
async def call_chatgpt(callback: CallbackQuery, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter your question:'
    )

    await state.set_state(ChatGPT.get_response)


@main_router.message(Command(commands=['reset'], ignore_case=True))
async def reset_context():
    await reset_messages()


@main_router.message(ChatGPT.get_response)
async def chatgpt(message: Message, state: FSMContext):
    try:
        await update(messages, 'user', message.text)

        response = openai.ChatCompletion.create(
            messages=messages,
            model='gpt-3.5-turbo',
            max_tokens=1111,
        )
        tokens = response['usage']['total_tokens']
        if tokens >= 4096:
            await message.answer(f'Too many tokens: {tokens},\nMemory was cleared up!')
            await reset_messages()

        await message.answer(response['choices'][0]['message']['content'], parse_mode="markdown")

    except Exception as ex:
        print(ex)
        await message.answer(ex)

    await state.clear()


@main_router.callback_query(lambda callback: callback.data == 'dalle')
async def call_dalle(callback: CallbackQuery, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter your request:'
    )

    await state.set_state(Dalle.get_response)


@main_router.message(Dalle.get_response)
async def dalle(message: Message, state: FSMContext):
    image_response = openai.Image.create(
        prompt=str(message.text).replace('dall-e', ''),
        n=5,
        size='1024x1024'
    )

    for count in range(5):
        await message.answer(image_response['data'][count]['url'])
    for i in range(5):
        name = f'\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot\\media\\images\\{randint(-100_000, 100_000)}.png'
        urllib.request.urlretrieve(str(image_response['data'][i]['url']), filename=name)

    await state.clear()


@main_router.callback_query(lambda callback: callback.data == 'gtts')
async def call_gtts(callback: CallbackQuery, state: FSMContext):
    bot = Bot(token=getenv('TG_TOKEN'))
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter your request:'
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

    await state.clear()
    await bot.session.close()


async def on_startup(botter):
    await db.db_start()
    await db.add_perm_by_id(int(getenv('id')))

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

    dp.include_routers(main_router, admin_router, others_router)

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
