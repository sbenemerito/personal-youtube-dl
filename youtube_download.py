from pytube import YouTube

import urllib.request
import urllib.parse
import bs4
import re
import os
import sys
from subprocess import run


def convert_to_mp3(filename, path):
    run(['mplayer', '-novideo', '-ao', 'pcm:waveheader', filename + '.mp4'])
    run(['lame', '-h', 'audiodump.wav', filename + '.mp3'])
    os.remove('audiodump.wav')
    os.remove(filename + '.mp4')


def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    filesize = stream.filesize
    finished = filesize - bytes_remaining
    progress = int(finished/filesize * 100)
    complete = int(progress/10)
    remaining = 10-complete
    bar = '{}{}'.format('#'*complete, '-'*remaining)
    sys.stdout.write('[{3}] {0} / {1} bytes ({2}% complete)\r'.format(finished, filesize, progress, bar))
    sys.stdout.flush()


def askForPath():
    path = input('Save to (uses relative path, leave blank for current directory): ')
    path = os.getcwd() if len(path.strip()) == 0 else path
    return path


query_string = urllib.parse.urlencode({"search_query" : input('Search YouTube: ')})
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
soup = bs4.BeautifulSoup(html_content.read().decode(), 'html.parser')
results = soup.find_all("a", href=re.compile(r'^/watch'))
results = [result for result in results if result.get('title')]

for i, result in enumerate(results):
    print('[{0}] {1}'.format(i+1, result.get('title')))

selected_video = int(input('Select video number: '))
if selected_video in range(1, len(results)+1):
    video_url = 'http://youtube.com' + results[selected_video-1].get('href')
    selected_video = YouTube(video_url)
    selected_video.register_on_progress_callback(show_progress_bar)

    print('[1] Download video (.mp4)')
    print('[2] Download audio only (.mp3)')
    ch = input('Option: ')
    save_path = askForPath()
    print('Downloading...')
    if ch == '1':
        selected_video.streams.filter(subtype='mp4').filter(progressive=True).all()[1].download(save_path)
        print('\nDownload complete')
    elif ch == '2':
        selected_video.streams.filter(only_audio=True).filter(subtype='mp4').all()[0].download(save_path)
        print('\nProcessing...')
        convert_to_mp3(selected_video.title, save_path)
        print('\nDownload complete')
