import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from utils import (
    criar_pasta,
    ler_csv,
    salvar_csv,
    clean_tracks,
    clean_artists,
    clean_genres
)

def main(usuario):
    """
    Limpa os dados brutos de um utilizador e salva os resultados processados.

    Parâmetros:
        usuario (str): Nome do utilizador cuja pasta de dados será processada.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    raw_path = BASE_DIR / "data" / "raw" / usuario
    processed_path = criar_pasta(BASE_DIR / "data" / "processed" / usuario)

    tracks = ler_csv(raw_path / "top_musicas.csv")
    artists = ler_csv(raw_path / "top_artistas.csv")
    genres = ler_csv(raw_path / "top_generos.csv")

    tracks_clean = clean_tracks(tracks)
    artists_clean = clean_artists(artists)
    genres_clean = clean_genres(genres)

    salvar_csv(tracks_clean, processed_path / "top_tracks_clean.csv")
    salvar_csv(artists_clean, processed_path / "top_artists_clean.csv")
    salvar_csv(genres_clean, processed_path / "top_genres_clean.csv")

    print(f"Dados limpos salvos em: {processed_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python 2_clean_data.py <nome_usuario>")
        sys.exit(1)
    main(sys.argv[1])
