import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
from pathlib import Path  # Biblioteca para manipulação de caminhos de ficheiros de forma robusta

# Pede o nome do utilizador via input
nome_usuario = input("Digite o nome do utilizador para gerar estatísticas: ").strip()

# Define a pasta base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Define o caminho do ficheiro CSV com as músicas do utilizador
csv_path = BASE_DIR / "data" / "raw" / nome_usuario / "top_musicas.csv"

# Verifica se o ficheiro existe; se não, mostra erro e termina o script
if not csv_path.exists():
    print(f"\n[Erro] O ficheiro '{csv_path}' não foi encontrado.")
    print("Certifique-se de que já executou o script de extração e de que o nome do utilizador está correto.")
    exit(1)

# Lê o ficheiro CSV para um DataFrame do pandas
df = pd.read_csv(csv_path)

# Calcula estatísticas de duração
total_minutes = df["duracao_min"].sum()  # Soma total de minutos ouvidos
avg_minutes = df["duracao_min"].mean()  # Duração média por faixa
max_minutes = df["duracao_min"].max()  # Faixa mais longa
min_minutes = df["duracao_min"].min()  # Faixa mais curta

# Calcula estatísticas de popularidade
avg_popularity = df["popularidade"].mean()  # Popularidade média
max_popularity = df["popularidade"].max()  # Maior popularidade
min_popularity = df["popularidade"].min()  # Menor popularidade

# Identifica a faixa mais e menos popular
most_popular_track = df.loc[df["popularidade"].idxmax()]  # Linha com a maior popularidade
least_popular_track = df.loc[df["popularidade"].idxmin()]  # Linha com a menor popularidade

# Identifica a faixa mais longa e mais curta
longest_track = df.loc[df["duracao_min"].idxmax()]  # Linha com maior duração
shortest_track = df.loc[df["duracao_min"].idxmin()]  # Linha com menor duração

# Artista mais frequente e sua contagem
most_common_artist = df["artista"].value_counts().idxmax()  # Nome do artista que aparece mais vezes
most_common_artist_count = df["artista"].value_counts().max()  # Quantidade de faixas desse artista

# Estatísticas adicionais
unique_tracks = df["musica"].nunique()  # Número de faixas únicas
unique_artists = df["artista"].nunique()  # Número de artistas únicos
average_track_name_length = df["musica"].apply(len).mean()  # Tamanho médio dos nomes das músicas
average_album_name_length = df["album"].apply(len).mean()  # Tamanho médio dos nomes dos álbuns
average_tracks_per_artist = round(df.shape[0] / unique_artists, 2)  # Média de faixas por artista

# Guarda todas as estatísticas num dicionário para facilitar uso e exportação
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

# Mostra as estatísticas no terminal de forma organizada
print("\n📊 Estatísticas do utilizador:")
for k, v in stats.items():
    print(f"- {k}: {v}")

# Cria um DataFrame com as estatísticas (só uma linha) para guardar como CSV
stats_df = pd.DataFrame([stats])

# Define o caminho de saída para o ficheiro com estatísticas
output_path = csv_path.parent / "spotify_stats.csv"

# Salva o ficheiro CSV com codificação compatível com Excel
stats_df.to_csv(output_path, index=False, encoding="utf-8-sig")

# Confirma que as estatísticas foram salvas
print(f"\n✅ Estatísticas salvas em: {output_path.resolve()}")
