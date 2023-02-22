from flask import Flask, request, jsonify, send_file
from psycopg2 import connect
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from moviepy.editor import *
from jinja2 import Template
import os, json, spotipy
from datetime import datetime
import shutil

app = Flask(__name__)    

@app.post('/api/obtener_enlaces_youtube')
def obtener_enlaces_youtube():
    dir = './static/music/'
    for file in os.scandir(dir):
        os.remove(file.path)
    new_link = request.get_json()
    playlist_LINK = new_link['link']
    cid = "2fe4fd32de64419988cfd0e7fb6e812e"
    secret = "6675fc7579a24e688a71dbda483d768e"
    enlaces = []
    tracks = []
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    playlist_URI = playlist_LINK.split("/")[-1].split("?")[0]
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    next_pages = 10
    results = sp.playlist_tracks(playlist_URI)
    tracks = results['items']
    while results['next']: 
        results = sp.next(results)
        tracks.extend(results['items'])
    file = open("canciones.txt", 'w')
    i = 1
    indice = 1
    for track in tracks:
        track_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        results_dict = json.loads(YoutubeSearch((artist_name + ' ' + track_name)).to_json())
        dic = results_dict['videos']
        if i == 1:
            file.write('https://www.youtube.com' + dic[0]['url_suffix'])
            i += 1
        else:
            file.write('\n' + 'https://www.youtube.com' + dic[0]['url_suffix'])
        url = 'https://www.youtube.com' + dic[0]['url_suffix']
        title = YouTube(url).title
        duration = YouTube(url).length
        enlace = {
            "id": indice,
            "link": url,
            "title": title,
            "artist": artist_name,
            "track": track_name,
            "duration": duration
        }
        enlaces.append(enlace)
        indice += 1
    file.close()   
    return enlaces 

@app.post('/api/convertir_a_mp3')
def get_mp3():
    url_video = request.get_json()
    url = url_video['url']
    output = "mp3"
    mp4 = YouTube(url).streams.get_highest_resolution().download()
    mp3 = mp4.split(".mp4", 1)[0] + f".{output}"
    video_clip = VideoFileClip(mp4)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3)
    shutil.copy(mp3, r'./static/music/')
    audio_clip.close()
    video_clip.close()
    os.remove(mp4)
    os.remove(mp3)
    cancion = {
        "fecha_descarga": datetime.now(),
        "conversion_realizada": True
    }
    return cancion
    
@app.get('/')
def home():
    return send_file('index.html')

if __name__ == '__main__':
    app.run()
