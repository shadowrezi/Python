from sys import argv
from youtubesearchpython import VideosSearch
from pytube import YouTube

if len(argv) == 1:
    print('Enter query!')
    exit()

args = ' '.join(argv[1:])

video = VideosSearch(args, limit=3)


videos = video.result()['result']

video1 = videos[0]
video2 = videos[1]
video3 = videos[2]


print(
    f"1) {video1['title']} - {video1['duration']}"
) if video1['duration'] else None  # if video isnt stream

print(
    f"2) {video2['title']} - {video2['duration']}"
) if video2['duration'] else None
print(
    f"3) {video3['title']} - {video3['duration']}"
) if video3['duration'] else None
while True:
    try:
        select = int(input())
    except ValueError:
        continue
    else:
        break

print(select-1)

link = 'https://www.youtube.com/watch?v=' + videos[select-1]['id']

yt = YouTube(link)

yt.streams.\
        filter(progressive=True, file_extension='mp4')\
        .order_by('resolution')\
        .desc()\
        .first()\
        .download()

