import os
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Verificar se as variáveis de ambiente estão sendo carregadas
print(f"CLIENT_ID: {os.getenv('SPOTIPY_CLIENT_ID')}")
print(f"CLIENT_SECRET: {os.getenv('SPOTIPY_CLIENT_SECRET')}")
print(f"REDIRECT_URI: {os.getenv('SPOTIPY_REDIRECT_URI')}")

# Configurações do Spotify
SCOPE = "user-top-read"
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

def authenticate_spotify():
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

# ... resto do código
