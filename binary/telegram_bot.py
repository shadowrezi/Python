import os
from logging import basicConfig, INFO
import sys
import asyncio
import json
import openai
import soundfile as sf
from dotenv import load_dotenv
from aiogram import Router
from aiogram import (
    Bot,
    Dispatcher,
    Router
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, ContentType
from aiogram.filters import Command

load_dotenv()

openai.api_key = os.getenv('OPENAI_TOKEN')

form = Router()
bot = Bot(token=os.getenv('TG_TOKEN'))

dialogue_context = {}


def transcribe_speech(audio_file_path):
    data, samplerate = sf.read(audio_file_path)
    output = os.path.basename(audio_file_path).split('.')[0] + '.wav'
    sf.write(output, data, samplerate)

    response = openai.Audio.transcribe(
        "whisper-1",
        open(output, 'rb'),
        language=['uk', 'ru'], # "en-US",
        enable_automatic_punctuation=True
    )
    os.remove(output)
    return str(response).encode().decode('unicode_escape').encode('utf-8').decode('utf-8')


@form.message()
async def handle_voice_message(message: Message):
    user_id = message.from_user.id

    if not message.voice == None:
        if user_id not in dialogue_context:
            dialogue_context[user_id] = [
                {'role': 'system', 'content': 'ты миленькая тяночка)'}
            ]

        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "123.mp3")

        text = json.loads(transcribe_speech('123.mp3'))['text']
        print(text)

        dialogue_context[user_id].append({'role': 'user', 'content': text})

        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'<a href="tg://user?id=1076908330">{text}</a>',
            reply_to_message_id=message.message_id,
            parse_mode=ParseMode(ParseMode.HTML)
        )

        r = openai.ChatCompletion.create(
            n=1,
            max_tokens=1000,
            model='gpt-3.5-turbo',
            messages=dialogue_context[message.from_user.id]
        )
        generated_text = r.choices[0].message.content.strip()

        dialogue_context[user_id].append({'role': 'assistant', 'content': generated_text})

        await bot.send_message(message.from_user.id, f'<b>{generated_text}</b>', parse_mode=ParseMode(ParseMode.HTML))
    else:
        if user_id not in dialogue_context:
            dialogue_context[user_id] = [
                {'role': 'system', 'content': 'Ты очень полезный ассистент!'},
            ]

        print(message.text)
        
        r = openai.ChatCompletion.create(
            n=1,
            max_tokens=1000,
            model='gpt-3.5-turbo',
            messages=dialogue_context[user_id]
        )
        generated_text = r.choices[0].message.content.strip()
        print(dialogue_context[user_id])

        await bot.send_message(
            message.from_user.id,
            f'<b>{generated_text}</b>',
            reply_to_message_id=message.message_id,
            parse_mode=ParseMode(ParseMode.HTML)
        )
        dialogue_context[user_id].append({'role': 'assistant', 'content': generated_text})


async def main():
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()

    dp.include_router(form)

    await dp.start_polling(bot)


basicConfig(level=INFO, stream=sys.stdout)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    os.remove('123.mp3')
    asyncio.run(bot.session.close())
    os.system('cls')
