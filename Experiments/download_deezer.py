from sys import argv
import os
from deezer import Client
from pydeezer import Deezer, Downloader
from dotenv import load_dotenv

args = ' '.join(argv[1:])

try:
    track = Client().search(query=args)[0]
except IndexError:
    print(f'track "{args}" not found')
    exit()

id = track.link.split('/')[-1]

load_dotenv()

arl = os.getenv('deezer_arl')

deezer = Deezer(arl=arl)

Downloader(deezer, [id], './').start()

for file in os.listdir('.'):
    if file.endswith(".lrc"):
        file_path = os.path.join('.', file)
        os.remove(file_path)

    if \
            (file.endswith('.mp3') and file.startswith(' ')) \
            or file == '.mp3' \
            or file == '-.mp3':
        track_data = f'{track.artist.name} - {track.title}.mp3'
        os.rename(file, track_data)
