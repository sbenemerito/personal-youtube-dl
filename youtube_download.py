from pytube import YouTube

import urllib.request
import urllib.parse
import bs4
import re


def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    filesize = stream.filesize
    finished = filesize - bytes_remaining
    progress = float(finished)/filesize * 100
    print('{0} / {1} bytes ({2: .2f}% complete)'.format(finished, filesize, progress)) 
    print('--------')


def askForPath():
    path = input('Save to (uses relative path, leave blank for current directory): ')
    path = None if len(path.strip()) == 0 else path
    return path

query_string = urllib.parse.urlencode({"search_query" : input('Search YouTube: ')})
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
soup = bs4.BeautifulSoup(html_content.read().decode(), 'html.parser')
results = soup.find_all("a", href=re.compile(r'^/watch'))
results = [result for result in results if result.get('title')]

for i, result in enumerate(results):
    print('[{0}] {1} (http://youtube.com{2})'.format(i+1, result.get('title'), result.get('href')))

selected_video = int(input('Select video number: '))
if selected_video in range(1, len(results)+1):
    video_url = 'http://youtube.com' + results[selected_video-1].get('href')
    selected_video = YouTube(video_url)
    selected_video.register_on_progress_callback(show_progress_bar)
    print(selected_video.title)
    print('[1] Download video + audio')
    print('[2] Download audio')
    ch = input('Option: ')
    save_path = askForPath()
    print('Downloading...')
    if ch == '1':
        selected_video.streams.filter(subtype='mp4').filter(progressive=True).all()[1].download(save_path)
        print('Download complete')
    elif ch == '2':
        selected_video.streams.filter(only_audio=True).filter(subtype='mp4').all()[0].download(save_path)
        print('Download complete')


# import requests


# response = requests.get('https://github.com/EbookFoundation/free-programming-books/blob/master/free-programming-books.md')

# print(soup.prettify())
# linkElems = soup.select('a')
# i = 0
# for linkElem in linkElems:
#   if i == 5:
#       break
#   if linkElem.get('href').endswith('.pdf'):
#           print('Downloading ' + linkElem.get('href'))

#           pdfUrl = linkElem.get('href')
#           pdfFilename = pdfUrl[pdfUrl.rfind('/') + 1:]
#           pdfFile = open(pdfFilename, 'wb')

#           pdfResponse = requests.get(pdfUrl)
#           for chunk in pdfResponse.iter_content(100000):
#               pdfFile.write(chunk)
#           pdfFile.close()
#           i = i + 1
