from os import getenv, system
from logging import basicConfig, INFO
import sys
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = getenv('OPENAI_TOKEN')

form = Router()
bot = Bot(getenv('TG_TOKEN'))

context = {}


@form.message()
async def call_chatgpt(message: Message):
    if message.from_user.id not in context:
        context[message.from_user.id] = []

    context[message.from_user.id].append({'role': 'user', 'content': message.text})
    print(context)

    msg_id = await bot.send_message(
        chat_id=message.chat.id,
        text='.'
    )
    msg_id = msg_id.message_id

    resp = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        n=1,
        temperature=0,
        messages=context[message.from_user.id]
    )
    text = ''
    for chunk in resp:
        s = chunk # ['choices'][0]['delta']
        print(s)
        if 'content' in s:
            text += s # ['content']
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg_id,
                text='das'
            )
            print(s, end=' ')

    context[message.from_user.id].append({'role': 'assistant', 'content': text})



async def main():
	bot = Bot(token=getenv('TG_TOKEN'))
	dp = Dispatcher()

	dp.include_router(form)

	await dp.start_polling(bot)


if __name__ == '__main__':
	basicConfig(level=INFO, stream=sys.stdout)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		asyncio.run(bot.session.close())
		system('cls')
