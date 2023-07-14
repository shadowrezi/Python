import os
from logging import basicConfig, INFO
import sys
import asyncio
import json
import openai
import soundfile as sf
from dotenv import load_dotenv
from aiogram import (
    Bot,
    Dispatcher,
    Router
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, ContentType

load_dotenv()

openai.api_key = os.getenv('OPENAI_TOKEN')

form = Router()
bot = Bot(token=os.getenv('TG_TOKEN'))

def transcribe_speech(audio_file_path):

    data, samplerate = sf.read(audio_file_path)

    output = os.path.basename(audio_file_path).split('.')[0] + '.wav'
    sf.write(output, data, samplerate)

    response = openai.Audio.transcribe(
        "whisper-1",
        open(output, 'rb'),
        language='uk', # "en-US",
        enable_automatic_punctuation=True
    )
    os.remove(output)
    return str(response).encode().decode('unicode_escape').encode('utf-8').decode('utf-8') # ['transcriptions'][0]['text']



@form.message()
async def handle_voice_message(message: Message):
	if not message.voice == None:
		file_id = message.voice.file_id
		file = await bot.get_file(file_id)
		file_path = file.file_path
		await bot.download_file(file_path, "123.mp3")

		print(text := json.loads(transcribe_speech('123.mp3'))['text'])

		await bot.send_message(
			chat_id=message.from_user.id,
			text=f'<a href="tg://user?id=1076908330">{text}</a>',
			reply_to_message_id=message.message_id,
			parse_mode=ParseMode(ParseMode.HTML)
		)

		r = openai.Completion.create(
			n=1,
			max_tokens=1000,
			model='text-davinci-003',
			prompt=text
		)
		print(r.choices[0].text.strip())

		mess = f'<b>{r.choices[0].text}</b>'
		await bot.send_message(message.from_user.id, mess, parse_mode=ParseMode(ParseMode.HTML))
	else:
		r = openai.Completion.create(
			n=1,
			max_tokens=1000,
			model='text-davinci-003',
			temperature=1,
			prompt=str(message.text)
		)
		print(r.choices[0].text.strip())
		await bot.send_message(
			message.from_user.id,
			f'<b>{r.choices[0].text}</b>',
			reply_to_message_id=message.message_id,
			parse_mode=ParseMode(ParseMode.HTML)
		)


async def main():
	bot = Bot(token=os.getenv('TG_TOKEN'))
	dp = Dispatcher()

	dp.include_router(form)

	await dp.start_polling(bot)

if __name__ == '__main__':
	basicConfig(level=INFO, stream=sys.stdout)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		os.remove('123.mp3')
		asyncio.run(bot.session.close())
		os.system('cls')
