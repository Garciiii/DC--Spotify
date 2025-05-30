import sys
import pandas as pd
from pathlib import Path

def clean_tracks(df):
    df = df.copy()
    df["musica"] = df["musica"].str.strip()
    df["artista"] = df["artista"].str.strip()
    return df

def clean_artists(df):
    df = df.copy()
    df["artista"] = df["artista"].str.strip()
    df["generos"] = df["generos"].str.lower()
    return df

def clean_genres(df):
    df = df.copy()
    df["genero"] = df["genero"].str.lower()
    return df

def main(usuario):
    raw_path = Path("data/raw") / usuario
    processed_path = Path("data/processed") / usuario
    processed_path.mkdir(parents=True, exist_ok=True)

    # Carregar arquivos com nomes corretos
    tracks = pd.read_csv(raw_path / "top_musicas.csv")
    artists = pd.read_csv(raw_path / "top_artistas.csv")
    genres = pd.read_csv(raw_path / "top_generos.csv")

    # Limpar dados
    tracks_clean = clean_tracks(tracks)
    artists_clean = clean_artists(artists)
    genres_clean = clean_genres(genres)

    # Salvar arquivos limpos
    tracks_clean.to_csv(processed_path / "top_tracks_clean.csv", index=False, encoding="utf-8-sig")
    artists_clean.to_csv(processed_path / "top_artists_clean.csv", index=False, encoding="utf-8-sig")
    genres_clean.to_csv(processed_path / "top_genres_clean.csv", index=False, encoding="utf-8-sig")

    print(f"Dados limpos salvos em: {processed_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python 2_clean_data.py <nome_usuario>")
        sys.exit(1)
    main(sys.argv[1])
