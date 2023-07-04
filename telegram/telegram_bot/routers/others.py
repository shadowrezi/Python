from os import getenv
import sys
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import (
    Command
)
from aiogram.types import (
    CallbackQuery,
    Message
)
from dotenv import load_dotenv
sys.path.append('../')
import database as db
from keyboard import main_kb

load_dotenv('\\Users\\Shadowraze\\Documents\\Python\\.env')

others_router = Router()

bot = Bot(token=getenv("TG_TOKEN"))
dp = Dispatcher()


@others_router.message(Command(commands='start', prefix='!/'))
async def start(message: Message) -> None:
    await db.cmd_db_start(message.from_user.id, message.from_user.username)

    await message.answer(
        text='Welcome, do You need help?',
        reply_markup=await main_kb(message.from_user.id)
    )



@others_router.callback_query(lambda callback: callback.data == 'help')
async def handle_help(callback: CallbackQuery) -> None:
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='''
How to use this bot:
Write /bot and select bot which you need
chatgpt - can answer your any questions
dall-e - can draw any picture
gtts - can voice your request (by default language set Ukrainian
to change language write it in start of message
for example:
en Hello, world!
ru Привет, мир!
)
        '''
    )


@others_router.callback_query(lambda callback: callback.data == 'dis_sending')
async def dis_sending(callback: CallbackQuery):
    await db.disable_sending(callback.from_user.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Sending was disabled!'
    )


@others_router.callback_query(lambda callback: callback.data == 'ena_sending')
async def ena_sending(callback: CallbackQuery):
    id = callback.from_user.id
    if await db.check_user(id):
        await db.enable_sending(id)
        await bot.send_message(
            chat_id=id,
            text='Sending was enabled!'
        )
    elif not await db.check_user(id):
        await bot.send_message(
            chat_id=id,
            text=f'User {id} not exists in database!'
        )


@others_router.message(Command(commands=['stop']))
async def stop(message: Message):
    input()


@others_router.message()
async def i_dont_understand_you(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="I don't understand you!"
    )
