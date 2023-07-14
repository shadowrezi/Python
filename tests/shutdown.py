from os import getenv
from PyPDF2 import PdfReader
from gtts import gTTS
import openai
from dotenv import load_dotenv


def read_pdf(path):
    reader = PdfReader(open(path, 'rb'))
    text_of_pdf = ''.join(page.extract_text() for page in reader.pages)
    
    return text_of_pdf, path


def google_text_to_speech(path, text, lang):
    gTTS(
        text=text,
        lang=lang,
        slow=False
    ).save(path + '_google.mp3')
    return path + '_google.mp3'


def openai_speech_to_text(path, text, lang):
    print(load_dotenv())
    
    file = open(path, 'rb')
    text = openai.Audio.transcribe(
        model='whisper-1',
        file=file,
        language=lang,
        api_key=getenv('OPENAI_TOKEN')
    ).text
    return text


def main():
    text, path = read_pdf(r'\Users\ShadowRaze\Desktop\test.pdf')
    print(f'{text = }')
    path = path.split('.')[0]
    print('gTTS: ')
    path = google_text_to_speech(path, text, 'ru')
    print('OPENAI STT: ')
    print(openai_speech_to_text(path, text, 'ru'))


if __name__ == '__main__':
    main()
