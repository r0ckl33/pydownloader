import pytube
import moviepy.editor as mp
import eyed3
import re
import os


def title_scrubber(video_name):
    video_name = re.sub(r',|"|\.|\\|\/|\:|\*|\<|\>|\||\'', '', video_name)
    # video_name = re.sub(r' +\[Official Music Video\]', '', video_name, re.I)
    video_name = re.sub(r' +(\[|\()Official Music Video(\]|\))', '', video_name, re.I)
    video_name = re.sub(r' +\(?Official Video\)?', '', video_name, re.I)
    video_name = re.sub(r' +\+ Lyrics', '', video_name, re.I)
    return video_name


def set_mp3_tags(mp3_name):
    # Create eye3d instance
    mp3 = eyed3.load(mp3_name)
    if ' - ' in mp3_name:
        artist, title = mp3_name.replace('.mp3', '').split(' - ')
        print(f'setting artist: {artist}\nsetting title: {title}')

        mp3.tag.artist = artist
        mp3.tag.title = title
    else:
        title = mp3_name.replace('.mp3', '')
        print(f'setting title: {title}')
        mp3.tag.title = title
    mp3.tag.save()


url = r'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

youtube = pytube.YouTube(url)

title = youtube.title

title = title_scrubber(title)

print(title)

# Downloading
youtube.streams.filter(only_audio=True).first().download(filename=title)

# Converting
mp4 = f'{title}.mp4'
mp3 = f'{title}.mp3'

clip = mp.AudioFileClip(mp4)
clip.write_audiofile(mp3)

set_mp3_tags(mp3)

print('deleting mp4')

os.remove(mp4)

print('complete')
