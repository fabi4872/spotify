from flask import Flask, request, jsonify, send_file
from psycopg2 import connect
import spotipy
import json
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials



app = Flask(__name__)    

#playlist_LINK = "https://open.spotify.com/playlist/29KoPj20uHyOknHNJnrXEk?si=ecfc9126881f4011" 
@app.post('/api/obtener_enlaces_youtube')
def obtener_enlaces_youtube():
    new_link = request.get_json()
    playlist_LINK = new_link['link']
    cid = "2fe4fd32de64419988cfd0e7fb6e812e"
    secret = "6675fc7579a24e688a71dbda483d768e"
    enlaces = []

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    playlist_URI = playlist_LINK.split("/")[-1].split("?")[0]
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    #Get playlist
    tracks = []
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
        print(artist_name + ' - ' + track_name)
        results_dict = json.loads(YoutubeSearch((artist_name + ' ' + track_name)).to_json())
        dic = results_dict['videos']
        if i == 1:
            file.write('https://www.youtube.com' + dic[0]['url_suffix'])
            i += 1
        else:
            file.write('\n' + 'https://www.youtube.com' + dic[0]['url_suffix'])
        url = 'https://www.youtube.com' + dic[0]['url_suffix']
        enlace = {
            "indice": indice,
            "enlace": url,
            "track_name": track_name,
            "artist_name": artist_name
        }
        enlaces.append(enlace)
        indice += 1
    file.close()   

    print("Archivo txt creado")
    return enlaces 
    
@app.get('/')
def home():
    return send_file('static/index.html')



if __name__ == '__main__':
    app.run()