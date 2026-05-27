import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

# Utilização de API do Spotify para buscar informações de álbuns e artistas

auth_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
spot = spotipy.Spotify(auth_manager=auth_manager)

def buscar_cove(name : str):

    query = f"album:{name}"
    results = spot.search(query, type='album',limit=5)
    albuns = []

    for item in results['albums']['items']:
        albuns.append({
            "spotify_id": item['id'],
            "name": item['name'],
            "artist": item['artists'][0]['name'],
            "image_url": item['images'][0]['url'] if item['images'] else None
        })
    return albuns[:5]

