"""Este ficheiro gera as estatisticas de cada utilizador."""
from pathlib import Path
import sys
import pandas as pd

nome_usuario = input("Digite o nome do utilizador para gerar estatísticas: ").strip()

base_dir = Path(__file__).resolve().parent.parent
csv_path = base_dir / "data" / "raw" / nome_usuario / "top_musicas.csv"

if not csv_path.exists():
    print(f"\n[Erro] O ficheiro '{csv_path}' não foi encontrado.")
    print("Certifique-se de que já executou o script de extração " \
    "e de que o nome do utilizador está correto.")
    sys.exit(1)

df = pd.read_csv(csv_path)

"""
Estatísticas de duração das faixas
"""
total_minutes = df["duracao_min"].sum()
avg_minutes = df["duracao_min"].mean()
max_minutes = df["duracao_min"].max()
min_minutes = df["duracao_min"].min()

"""
Estatísticas de popularidade das faixas
"""
avg_popularity = df["popularidade"].mean()
max_popularity = df["popularidade"].max()
min_popularity = df["popularidade"].min()

most_popular_track = df.loc[df["popularidade"].idxmax()]
least_popular_track = df.loc[df["popularidade"].idxmin()]

longest_track = df.loc[df["duracao_min"].idxmax()]
shortest_track = df.loc[df["duracao_min"].idxmin()]

"""
Artista mais frequente e contagens diversas
"""
most_common_artist = df["artista"].value_counts().idxmax()
most_common_artist_count = df["artista"].value_counts().max()

unique_tracks = df["musica"].nunique()
unique_artists = df["artista"].nunique()
average_track_name_length = df["musica"].apply(len).mean()
average_album_name_length = df["album"].apply(len).mean()
average_tracks_per_artist = round(df.shape[0] / unique_artists, 2)

"""
Dicionário com todas as estatísticas geradas
"""
stats = {
    "Total de minutos ouvidos": round(total_minutes, 1),
    "Média de minutos por faixa": round(avg_minutes, 1),
    "Faixa mais longa (minutos)": round(longest_track["duracao_min"], 1),
    "Faixa mais curta (minutos)": round(shortest_track["duracao_min"], 1),
    "Faixa mais popular": most_popular_track["musica"],
    "Popularidade da faixa mais popular": most_popular_track["popularidade"],
    "Faixa menos popular": least_popular_track["musica"],
    "Popularidade da faixa menos popular": least_popular_track["popularidade"],
    "Popularidade média": round(avg_popularity, 1),
    "Artista mais frequente": most_common_artist,
    "Quantidade de faixas desse artista": most_common_artist_count,
    "Número de faixas únicas": unique_tracks,
    "Número de artistas únicos": unique_artists,
    "Média de faixas por artista": average_tracks_per_artist,
    "Comprimento médio do nome das faixas": round(average_track_name_length, 1),
}

print("\n Estatísticas do utilizador:")
for k, v in stats.items():
    print(f"- {k}: {v}")

stats_df = pd.DataFrame([stats])
output_path = csv_path.parent / "spotify_stats.csv"
stats_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n Estatísticas salvas em: {output_path.resolve()}")
