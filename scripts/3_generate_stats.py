import pandas as pd
import os

# Caminho do CSV
csv_path = "../data/spotify_top_tracks.csv"

# Verifica se o arquivo existe
if not os.path.exists(csv_path):
    print("O arquivo 'spotify_top_tracks.csv' não foi encontrado. Execute primeiro o script de extração.")
    exit(1)

# Lê os dados
df = pd.read_csv(csv_path)

# Estatísticas básicas
total_minutes = df["played_minutes"].sum()
avg_minutes = df["played_minutes"].mean()
max_minutes = df["played_minutes"].max()
min_minutes = df["played_minutes"].min()

avg_popularity = df["popularity"].mean()
max_popularity = df["popularity"].max()
min_popularity = df["popularity"].min()

most_popular_track = df.loc[df["popularity"].idxmax()]
least_popular_track = df.loc[df["popularity"].idxmin()]

longest_track = df.loc[df["duration_ms"].idxmax()]
shortest_track = df.loc[df["duration_ms"].idxmin()]

most_common_artist = df["artist_name"].value_counts().idxmax()
most_common_artist_count = df["artist_name"].value_counts().max()

# Gêneros ainda não disponíveis no CSV, então é ignorado

# Novas estatísticas (extras)
unique_tracks = df["track_name"].nunique()
unique_artists = df["artist_name"].nunique()
average_track_name_length = df["track_name"].apply(len).mean()
average_album_name_length = df["album_name"].apply(len).mean()
average_tracks_per_artist = round(df.shape[0] / unique_artists, 2)

# Compila as 15 estatísticas principais
stats = {
    "Total de minutos ouvidos": round(total_minutes, 1),
    "Média de minutos por faixa": round(avg_minutes, 1),
    "Faixa mais longa (minutos)": round(longest_track["duration_ms"] / 60000, 1),
    "Faixa mais curta (minutos)": round(shortest_track["duration_ms"] / 60000, 1),
    "Faixa mais popular": most_popular_track["track_name"],
    "Popularidade da faixa mais popular": most_popular_track["popularity"],
    "Faixa menos popular": least_popular_track["track_name"],
    "Popularidade da faixa menos popular": least_popular_track["popularity"],
    "Popularidade média": round(avg_popularity, 1),
    "Artista mais frequente": most_common_artist,
    "Quantidade de faixas desse artista": most_common_artist_count,
    "Número de faixas únicas": unique_tracks,
    "Número de artistas únicos": unique_artists,
    "Média de faixas por artista": average_tracks_per_artist,
    "Comprimento médio do nome das faixas": round(average_track_name_length, 1),
}

# Exibe no terminal
print("Top 15 Estatísticas:")
for k, v in stats.items():
    print(f"- {k}: {v}")

# Salva como CSV
stats_df = pd.DataFrame([stats])
stats_df.to_csv("../data/spotify_stats.csv", index=False, encoding="utf-8-sig")
print("\nEstatísticas salvas em '../data/spotify_stats.csv'")

