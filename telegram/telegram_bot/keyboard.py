from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import database as db


async def main_kb(id):
    kbs = [
        [InlineKeyboardButton(text='🆘 Help', callback_data='help')],
        [InlineKeyboardButton(text='❌ Disable sending', callback_data='dis_sending'), InlineKeyboardButton(text='✅ Enable sending', callback_data='ena_sending')],
    ]

    if await db.check_perm(id):
        kbs.append([InlineKeyboardButton(text='🕹 Admin panel', callback_data='admin')])

    return InlineKeyboardMarkup(inline_keyboard=kbs)


async def admin_kb(id):
    kb_admin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🆔 Check id', callback_data='check_id')],
        [InlineKeyboardButton(text='👾 Get id by name', callback_data='id_by_name')],
        [InlineKeyboardButton(text='✅ Add admin by id', callback_data='add_admin'), InlineKeyboardButton(text='🚫 Remove admin by id', callback_data='remove_admin')],
        [InlineKeyboardButton(text='✅ Add admin by nickname', callback_data='add_admin_by_nick'), InlineKeyboardButton(text='🚫 Remove admin by nickname', callback_data='remove_admin_by_nick')],
        [InlineKeyboardButton(text='✋ Send message to all users', callback_data='send_message')],
        [InlineKeyboardButton(text='🎤 Send audio to all users', callback_data='send_audio')],
        [InlineKeyboardButton(text='👀 Count all project pages', callback_data='count')],
        [InlineKeyboardButton(text='🙍‍♂️ All Users', callback_data='all_users')],
        [InlineKeyboardButton(text='🗒 Note', callback_data='note')]
    ])

    if await db.check_perm(id):
        return kb_admin
    elif not await db.check_perm(id):
        return


async def bot_kb():
    kbs_bot = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='chatgpt', callback_data='chatgpt')],
        [InlineKeyboardButton(text='dall-e', callback_data='dalle')],
        [InlineKeyboardButton(text='gTTS', callback_data='gtts')]
    ])

    return kbs_bot
