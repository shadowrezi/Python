from os import getenv
from random import randint
import sqlite3 as sq
from aiogram import Bot
from aiogram.types import FSInputFile
from gtts import gTTS

db = sq.connect('\\Users\\ShadowRaze\\Documents\\Python\\telegram\\telegram_bot\\telegram.db')
cursor = db.cursor()


async def db_start():
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "tg_id INTEGER, "
            "permission TEXT, "
            "sending TEXT)")

    db.commit()


async def cmd_db_start(user_id, username):
    user = cursor.execute(f"SELECT * FROM users WHERE tg_id == {user_id}").fetchone()

    if not user:
        cursor.execute(f"INSERT INTO users (tg_id, name, permission, sending) VALUES ({user_id}, '@{username}', 'False', 'True')")
        db.commit()


async def check_user(id):
    user = cursor.execute(f"SELECT tg_id FROM users WHERE tg_id == {id}").fetchone()

    if user is None:
        return False
    else:
        return True


async def check_user_by_name(name):
    user = cursor.execute(f"SELECT name FROM users WHERE name == '{name}'").fetchone()

    if user is None:
        return False
    else:
        return True


async def add_perm_by_id(id):
    user = cursor.execute(f"SELECT permission FROM users WHERE tg_id == {id}")

    if user:
        cursor.execute(f"UPDATE users SET permission='True' WHERE tg_id == {id}")
        db.commit()
    else:
        pass


async def rem_perm_by_id(id):
    user = cursor.execute(f"SELECT permission FROM users WHERE tg_id == {id}")

    if user:
        cursor.execute(f"UPDATE users SET permission='False' WHERE tg_id == {id}")
        db.commit()
    else:
        pass


async def add_perm_by_name(name):
    user = cursor.execute(f"SELECT permission FROM users WHERE name == '{name}'")

    if user:
        cursor.execute(f"UPDATE users SET permission='True' WHERE name == '{name}'")
        db.commit()
    else:
        pass


async def rem_perm_by_name(name):
    user = cursor.execute(f"SELECT permission FROM users WHERE name == '{name}'")

    if user:
        cursor.execute(f"UPDATE users SET permission='False' WHERE name == '{name}'")
        db.commit()
    else:
        pass


async def get_all_users():
    all_users = cursor.execute("SELECT name, tg_id, permission, sending FROM users").fetchall()

    x = []

    for user in all_users:
        x.append(f'{user[0]} / {user[1]} / permission: {user[2]} / sending: {user[3]}')

    i = '\n'.join(x)

    return i


async def check_perm(id):
    user = cursor.execute("SELECT permission FROM users").fetchone()

    if str(user[0]) == 'True':
        return True
    elif str(user) == 'False':
        return False


async def get_all_IDs():
    all_IDs = cursor.execute("SELECT tg_id FROM users").fetchall()

    x = []

    for id in all_IDs:
        x.append(int(id[0]))

    return x


async def get_all_sending_IDs():
    all_IDs = cursor.execute("SELECT tg_id FROM users WHERE sending == 'True'").fetchall()

    x = []

    for id in all_IDs:
        x.append(int(id[0]))

    return x


async def get_all_perm_users():
    users = cursor.execute("SELECT tg_id FROM users WHERE permission == 'True'").fetchall()

    return users[0]


async def disable_sending(id):
    cursor.execute(F"UPDATE users SET sending='False' WHERE tg_id == {id}")
    db.commit()


async def enable_sending(id):
    cursor.execute(f"UPDATE users SET sending='True' WHERE tg_id == {id}")
    db.commit()


async def check_sending(id):
    user = cursor.execute(f'SELECT sending FROM users WHERE tg_id == {id}').fetchone()

    if user[0] == 'True':
        return True
    if user[0] == 'False':
        return False


async def get_id_by_name(name):
    user = cursor.execute(f"SELECT tg_id FROM users WHERE name == '{name}'").fetchone()

    if user is not None:
        return user[0]
    elif user is None:
        return False


async def send_message(message):
    bot = Bot(token=getenv('TG_TOKEN'))  # type: ignore
    for id in await get_all_sending_IDs():
        try:
            if await check_sending(id):
                await bot.send_message(
                    chat_id=id,
                    text=message
                )
            else:
                pass
        except Exception as ex:
            print(ex)


async def send_audio(audio_text, lang):
    file_name = f'{randint(-100_000, 100_000)}.mp3'
    file_path = f'\\Users\\Shadowraze\\Documents\\Python\\telegram\\telegram_bot\\media\\audios\\{file_name}'

    audio = gTTS(text=audio_text, lang=lang)
    audio.save(file_path)

    return FSInputFile(file_path)
