import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd
from collections import Counter

from utils import criar_pasta, salvar_csv

# Define a pasta base do projeto (dois níveis acima do ficheiro atual)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do ficheiro .env localizado em /secrets
load_dotenv(dotenv_path=BASE_DIR / "secrets" / ".env")

# Lê as variáveis do .env necessárias para a autenticação com o Spotify
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-top-read"

def criar_pasta_usuario():
    """
    Solicita o nome do usuário, cria uma pasta para armazenar os dados
    e retorna o caminho da pasta criada.
    """
    nome_usuario = input("Digite o nome do usuário para salvar os dados: ").strip()
    if not nome_usuario:
        print("Nome inválido. Saindo...")
        sys.exit(1)

    pasta_raw = BASE_DIR / "data" / "raw" / nome_usuario
    criar_pasta(pasta_raw)
    return pasta_raw

def autenticar_spotify():
    """
    Autentica o usuário com a API do Spotify usando OAuth.

    Retorna:
        Objeto autenticado do Spotify.
    """
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=".spotify_cache"
        ))
        print("Autenticação com Spotify realizada com sucesso")
        return sp
    except Exception as e:
        print(f"Falha na autenticação: {e}")
        sys.exit(1)

def extrair_dados(sp, limite=50):
    """
    Extrai os dados de músicas, artistas e géneros favoritos do usuário.

    Parâmetros:
        sp: objeto autenticado do Spotify.
        limite: número de itens a extrair (default = 50).

    Retorna:
        Tupla de três DataFrames: músicas, artistas, géneros.
    """
    print(f"Extraindo top {limite} músicas e artistas...")

    top_musicas = sp.current_user_top_tracks(limit=limite, time_range="medium_term")
    df_musicas = pd.DataFrame([{
        "musica": item["name"],
        "artista": item["artists"][0]["name"],
        "album": item["album"]["name"],
        "duracao_min": round(item["duration_ms"] / 60000, 2),
        "popularidade": item["popularity"],
        "uri": item["uri"]
    } for item in top_musicas["items"]])

    top_artistas = sp.current_user_top_artists(limit=limite, time_range="medium_term")
    df_artistas = pd.DataFrame([{
        "artista": item["name"],
        "generos": "|".join(item["genres"]),
        "seguidores": item["followers"]["total"],
        "popularidade": item["popularity"],
        "uri": item["uri"]
    } for item in top_artistas["items"]])

    generos = [g for item in top_artistas["items"] for g in item["genres"]]
    df_generos = pd.DataFrame(Counter(generos).items(), columns=["genero", "contagem"])
    df_generos = df_generos.sort_values("contagem", ascending=False)

    return df_musicas, df_artistas, df_generos

def salvar_arquivos(df_musicas, df_artistas, df_generos, pasta):
    """
    Salva os DataFrames como arquivos CSV na pasta especificada.
    """
    salvar_csv(df_musicas, pasta / "top_musicas.csv")
    salvar_csv(df_artistas, pasta / "top_artistas.csv")
    salvar_csv(df_generos, pasta / "top_generos.csv")
    print(f"Dados salvos em: {pasta.resolve()}")

def main():
    """
    Função principal: executa o fluxo completo de extração e salvamento dos dados.
    """
    pasta_usuario = criar_pasta_usuario()

    try:
        limite = int(sys.argv[1]) if len(sys.argv) > 1 else 50
        if limite not in [10, 50]:
            raise ValueError
    except ValueError:
        print("Uso: python 1_extract_data.py [10|50]")
        sys.exit(1)

    sp = autenticar_spotify()

    try:
        df_musicas, df_artistas, df_generos = extrair_dados(sp, limite)
        salvar_arquivos(df_musicas, df_artistas, df_generos, pasta_usuario)
    except Exception as e:
        print(f"Erro durante a extração: {e}")

if __name__ == "__main__":
    main()
