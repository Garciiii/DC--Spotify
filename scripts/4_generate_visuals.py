import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Estilo
sns.set(style="whitegrid")

# Lê os dados
csv_path = "../data/spotify_top_tracks.csv"
if not os.path.exists(csv_path):
    print("O arquivo 'spotify_top_tracks.csv' não foi encontrado.")
    exit(1)

df = pd.read_csv(csv_path)

# Cria pasta para relatórios
os.makedirs("../reports", exist_ok=True)

# --- Gráfico 1: Top 10 músicas por minutos ouvidos (estático e interativo)
top_played = df.sort_values("played_minutes", ascending=False).head(10)

# Estático
plt.figure(figsize=(12, 6))
sns.barplot(data=top_played, x="played_minutes", y="track_name", palette="mako")
plt.title("Top 10 Músicas por Minutos Ouvidos")
plt.xlabel("Minutos")
plt.ylabel("Música")
plt.tight_layout()
plt.savefig("../reports/top10_minutos_ouvidos.png")
plt.close()

# Interativo
fig1 = px.bar(top_played, x="played_minutes", y="track_name", orientation="h",
              title="Top 10 Músicas por Minutos Ouvidos (Interativo)", color="played_minutes")
fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
fig1.write_html("../reports/top10_minutos_ouvidos_interativo.html")

# --- Gráfico 2: Distribuição da popularidade
plt.figure(figsize=(10, 6))
sns.histplot(df["popularity"], bins=10, kde=True, color="skyblue")
plt.title("Distribuição da Popularidade das Faixas")
plt.xlabel("Popularidade")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig("../reports/distribuicao_popularidade.png")
plt.close()

fig2 = px.histogram(df, x="popularity", nbins=10, title="Distribuição Interativa da Popularidade")
fig2.write_html("../reports/distribuicao_popularidade_interativa.html")

# --- Gráfico 3: Top 10 artistas por número de faixas
top_artists = df["artist_name"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_artists.values, y=top_artists.index, palette="viridis")
plt.title("Top 10 Artistas por Número de Faixas")
plt.xlabel("Quantidade de Faixas")
plt.ylabel("Artista")
plt.tight_layout()
plt.savefig("../reports/top10_artistas.png")
plt.close()

fig3 = px.bar(x=top_artists.values, y=top_artists.index,
              labels={'x': 'Quantidade de Faixas', 'y': 'Artista'},
              title="Top 10 Artistas por Número de Faixas (Interativo)")
fig3.write_html("../reports/top10_artistas_interativo.html")

# --- Gráfico 4: Duração média por artista (Top 5)
avg_duration = df.groupby("artist_name")["played_minutes"].mean().sort_values(ascending=False).head(5)
plt.figure(figsize=(10, 6))
sns.barplot(x=avg_duration.values, y=avg_duration.index, palette="rocket")
plt.title("Duração Média das Faixas por Artista (Top 5)")
plt.xlabel("Minutos")
plt.ylabel("Artista")
plt.tight_layout()
plt.savefig("../reports/duracao_media_por_artista.png")
plt.close()

fig4 = px.bar(x=avg_duration.values, y=avg_duration.index,
              labels={'x': 'Minutos', 'y': 'Artista'},
              title="Duração Média por Artista (Top 5) - Interativo")
fig4.write_html("../reports/duracao_media_por_artista_interativo.html")

print("Visualizações salvas em '../reports'")
