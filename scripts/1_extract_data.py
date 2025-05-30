import os
import sys
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Configuração da API Spotify
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-top-read"

def criar_pasta_usuario():
    """Pede o nome do usuário e cria a pasta em data/raw/nome_usuario"""
    nome_usuario = input("Digite o nome do usuário para salvar os dados: ").strip()
    if not nome_usuario:
        print("Nome inválido. Saindo...")
        sys.exit(1)

    pasta_raw = os.path.join("data", "raw", nome_usuario)
    Path(pasta_raw).mkdir(parents=True, exist_ok=True)
    return pasta_raw

def autenticar_spotify():
    """Autentica com a API do Spotify"""
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
    """Extrai top músicas, artistas e gêneros"""
    print(f"Extraindo top {limite} músicas e artistas...")

    # Extrair músicas
    resultados_musicas = sp.current_user_top_tracks(limit=limite, time_range='medium_term')
    df_musicas = pd.DataFrame([{
        "musica": item["name"],
        "artista": item["artists"][0]["name"],
        "album": item["album"]["name"],
        "duracao_min": round(item["duration_ms"] / 60000, 2),
        "popularidade": item["popularity"],
        "uri": item["uri"]
    } for item in resultados_musicas["items"]])

    # Extrair artistas e gêneros
    resultados_artistas = sp.current_user_top_artists(limit=limite, time_range='medium_term')
    generos = []
    df_artistas = pd.DataFrame([{
        "artista": item["name"],
        "generos": "|".join(item["genres"]),
        "seguidores": item["followers"]["total"],
        "popularidade": item["popularity"],
        "uri": item["uri"]
    } for item in resultados_artistas["items"]])

    # Contar gêneros
    generos = [genero for item in resultados_artistas["items"] for genero in item["genres"]]
    df_generos = pd.DataFrame(Counter(generos).items(), columns=["genero", "contagem"])
    df_generos = df_generos.sort_values("contagem", ascending=False)

    return df_musicas, df_artistas, df_generos

def salvar_arquivos(df_musicas, df_artistas, df_generos, pasta_usuario):
    """Salva os DataFrames em CSV na pasta do usuário"""
    df_musicas.to_csv(os.path.join(pasta_usuario, "top_musicas.csv"), index=False, encoding="utf-8-sig")
    df_artistas.to_csv(os.path.join(pasta_usuario, "top_artistas.csv"), index=False, encoding="utf-8-sig")
    df_generos.to_csv(os.path.join(pasta_usuario, "top_generos.csv"), index=False, encoding="utf-8-sig")
    print(f"Dados salvos em: {os.path.abspath(pasta_usuario)}")

def main():
    # Pede o nome do usuário e cria a pasta
    pasta_usuario = criar_pasta_usuario()

    # Verifica se o argumento (10 ou 50) foi passado
    try:
        limite = int(sys.argv[1]) if len(sys.argv) > 1 else 50
        if limite not in [10, 50]:
            raise ValueError
    except ValueError:
        print("Uso: python spotify_extract.py [10|50]")
        sys.exit(1)

    # Autentica no Spotify
    sp = autenticar_spotify()

    # Extrai e salva os dados
    try:
        df_musicas, df_artistas, df_generos = extrair_dados(sp, limite)
        salvar_arquivos(df_musicas, df_artistas, df_generos, pasta_usuario)
    except Exception as e:
        print(f"Erro durante a extração: {e}")

if __name__ == "__main__":
    main()
