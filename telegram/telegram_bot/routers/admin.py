from os import getenv
from aiogram import Bot, Dispatcher, Router
from aiogram.types import (
    CallbackQuery,
    Message
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import database as db
from keyboard import admin_kb
from count import count_pages_of_project

load_dotenv('\\Users\\Shadowraze\\Documents\\Python\\.env')

admin_router = Router()

bot = Bot(token=getenv("TG_TOKEN"))
dp = Dispatcher()


class AddAdmin(StatesGroup):
    get_id = State()


class RemoveAdmin(StatesGroup):
    get_id = State()


class AddAdminNick(StatesGroup):
    get_id = State()


class RemoveAdminNick(StatesGroup):
    get_id = State()


class get_id_by_nick(StatesGroup):
    get_id = State()


class Send_Message(StatesGroup):
    get_message = State()


class Send_Audio(StatesGroup):
    get_message = State()


class Note(StatesGroup):
    get_text = State()


@admin_router.callback_query(lambda callback: callback.data == 'admin')
async def handle_admin(callback: CallbackQuery) -> None:
    if await db.check_perm(callback.from_user.id):
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Admin panel:',
            reply_markup=await admin_kb(callback.from_user.id)
        )


@admin_router.callback_query(lambda callback: callback.data == 'add_admin')
async def call_add_admin(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter user id:'
    )

    await state.set_state(AddAdmin.get_id)


@admin_router.message(AddAdmin.get_id)
async def add_admin(message: Message, state: FSMContext):
    id = int(message.text.replace(' ', ''))

    try:
        if await db.check_user(id):
            await db.add_perm_by_id(id)
            await message.answer(f'User {id} successfully became admin!')
        else:
            await message.answer(f'User {id} not exists in database!')
    except Exception as ex:
        print(ex)
        await message.answer('error of becoming an admin user')
    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'remove_admin')
async def call_remove_admin(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter user id:'
    )

    await state.set_state(RemoveAdmin.get_id)


@admin_router.message(RemoveAdmin.get_id)
async def remove_admin(message: Message, state: FSMContext):
    id = int(message.text.replace(' ', ''))

    try:
        if await db.check_user(id):
            await db.rem_perm_by_id(id)
            await message.answer(f'User {id} successfully had default user!')
        else:
            await message.answer(f'User {id} not exists in database!')
    except Exception as ex:
        print(ex)
        await message.answer('Error')
    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'add_admin_by_nick')
async def call_add_admin_nick(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter user name\n\nFor example:\n@testname:'
    )

    await state.set_state(AddAdminNick.get_id)


@admin_router.message(AddAdminNick.get_id)
async def add_admin_nick(message: Message, state: FSMContext):
    name = str(message.text.replace(' ', ''))

    try:
        if await db.check_user_by_name(name):
            await db.add_perm_by_name(name)
            await message.answer(f'User {name} successfully became admin!')
        else:
            await message.answer(f'User {name} not exists in database!')
    except Exception as ex:
        print(ex)
        await message.answer('Error of becoming an admin user')
    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'remove_admin_by_nick')
async def call_remove_admin_nick(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter user name\n\nFor example:\n@testname:'
    )

    await state.set_state(RemoveAdminNick.get_id)


@admin_router.message(RemoveAdminNick.get_id)
async def remove_admin_nick(message: Message, state: FSMContext):
    name = str(message.text.replace(' ', ''))

    try:
        if await db.check_user_by_name(name):
            await db.rem_perm_by_name(name)
            await message.answer(f'User {name} successfully had default user!!')
        else:
            await message.answer(f'User {name} not exists in database!')
    except Exception as ex:
        print(ex)
        await message.answer('Error')
    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'all_users')
async def handle_all_users(callback: CallbackQuery):
    all_users = await db.get_all_users()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f'All users:\n{all_users}'
    )


@admin_router.callback_query(lambda callback: callback.data == 'check_id')
async def handle_check_id(callback: CallbackQuery):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Your id:\n{callback.from_user.id}'
    )


@admin_router.callback_query(lambda callback: callback.data == 'id_by_name')
async def call_get_id_by_name(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter user name:\n\nFor example:\n@testname'
    )

    await state.set_state(get_id_by_nick.get_id)


@admin_router.message(get_id_by_nick.get_id)
async def cmd_get_id_by_name(message: Message, state: FSMContext):
    text = message.text.replace(' ', '')

    if await db.get_id_by_name(text) is False:
        await message.answer(f'User {text} is not exists in database!')
    else:
        await message.answer(f'ID:\n{await db.get_id_by_name(text)}')

    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'send_message')
async def call_send_message(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter message:'
    )

    await state.set_state(Send_Message.get_message)


@admin_router.message(Send_Message.get_message)
async def send_message(message: Message, state: FSMContext):
    await db.send_message(message.text)

    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'note')
async def call_note(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter your note:'
    )

    await state.set_state(Note.get_text)


@admin_router.message(Note.get_text)
async def note(message: Message, state: FSMContext):
    with open('\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot\\media\\files\\test.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{message.text}')

    await bot.send_message(
        chat_id=message.from_user.id,
        text='Note was successfully added to file!'
    )

    await state.clear()


@admin_router.callback_query(lambda callback: callback.data == 'count')
async def count_pages(callback: CallbackQuery):
    pages = await count_pages_of_project()

    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f'All lines of project:\n{pages[1]} ({pages[0]})'
    )
    await callback.answer(f'All lines of project:\n{pages[0]}')


@admin_router.callback_query(lambda callback: callback.data == 'send_audio')
async def call_send_audio(callback: CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Enter text:'
    )
    await state.set_state(Send_Audio.get_message)


@admin_router.message(Send_Audio.get_message)
async def Send_audio(message: Message, state: FSMContext):
    if message.from_user.id in await db.get_all_perm_users():
        for id in await db.get_all_IDs():
            await bot.send_audio(
                chat_id=id,
                audio=await db.send_audio(message.text, 'uk'),
                performer='ShadowRaze',
                title='Google Text-To-Speech'
            )

    await state.clear()
