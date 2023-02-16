import spotipy
import json
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials
from flask import current_app as app
from flask import render_template ,request, redirect, url_for, flash, make_response, Response

def obtener_enlaces_youtube():
    cid = "2fe4fd32de64419988cfd0e7fb6e812e"
    secret = "6675fc7579a24e688a71dbda483d768e"
    playlist_LINK = "https://open.spotify.com/playlist/29KoPj20uHyOknHNJnrXEk?si=ecfc9126881f4011"
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

    urlJsonList = []

    file = open("canciones.txt", 'w')
    i = 1
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
            "enlace": enlace,
            "track_name": track_name,
            "artist_name": artist_name
        }
        enlaces.append(enlace)
    file.close()   

    print("Archivo txt creado")
    input()
    return render_template("index.html", enlaces = enlaces) 



    # dic_mes={ "Enero":1, "Febrero":2, "Marzo":3, "Abril":4, "Mayo":5, "Junio":6,
    #          "Julio":7, "Agosto":8, "Septiembre":9, "Octubre":10, "Noviembre":11, "Diciembre":12}
    # cuo = Cuota.get_cuota_by_id(id_c)
    # cuo.estado = Cuota.get_estado_paga()
    # fecha_hoy = datetime.now()
    # recargo_cuota = Config.get_valor_porcentaje()
    # dia_actual=int(fecha_hoy.strftime('%d'))
    # mes_actual=int(fecha_hoy.strftime('%m'))
    # if dia_actual >= 1 and dia_actual <= 10:
    #     cuo.register_cuota_database()
    #     register_pago_database(id_c, monto, cuo.periodo)
    #     flash("Se realizo el pago correctamente")
    # else:
    #     recargo = (cuo.monto * recargo_cuota)/100
    #     monto_recargo = cuo.monto + recargo
    #     msg= f"Al realizar el pago con vencimiento aplicandose el %{recargo_cuota} de interes quedando su valor en: {monto_recargo}"
    #     flash(msg)
    #     cuo.monto = monto_recargo
    #     cuo.register_cuota_database()
    #     register_pago_database(id_c, monto_recargo, cuo.periodo)
    # cuotas = Cuota.get_cuotas_by_disciplina_asociado(id_d, id_a)
    # return render_template("pago_de_una_couta/realizar_pago.html", cuotas = cuotas) 