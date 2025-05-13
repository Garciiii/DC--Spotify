import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Configurações do app Spotify
CLIENT_ID = "39f54a08c7c543debd7ec305f12df078"
CLIENT_SECRET = "6034a0a72f0845b0914fbedda8cc1f71"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-top-read playlist-modify-public"

# Autenticação
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache"
))

# Entrada do usuário
while True:
    choice = input("Deseja ver o Top 10 ou Top 50 músicas mais ouvidas? (10/50): ").strip()
    if choice in ['10', '50']:
        limit = int(choice)
        break
    else:
        print("Opção inválida. Digite 10 ou 50.")


user = sp.current_user()
user_id = user['id']


top_tracks = sp.current_user_top_tracks(limit=limit, time_range='medium_term')

print(f"\nSuas {limit} músicas mais ouvidas:\n")

track_uris = []

for i, item in enumerate(top_tracks['items'], start=1):
    name = item['name']
    artist = item['artists'][0]['name']
    album = item['album']['name']
    duration_ms = item['duration_ms']
    minutes = round(duration_ms / 60000, 2)
    
    print(f"{i}. {name} - {artist} | Álbum: {album} | Duração: {minutes} min")
    
    track_uris.append(item['uri'])


playlist_name = f"Top {limit} mais ouvidas (Trackily)"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description="Suas músicas mais ouvidas")

sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

print(f"\nPlaylist '{playlist_name}' criada com sucesso: {playlist['external_urls']['spotify']}")
