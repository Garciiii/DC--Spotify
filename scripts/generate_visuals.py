"""Este ficheiro gera graficos com as estatisticas de cada utilizador e um geral."""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.express as px

sns.set(style="whitegrid")

"""Define os diretórios base"""
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

"""Lista com (utilizador, minutos ouvidos)"""
ranking = []

"""Itera sobre as pastas de cada utilizador"""
for user_dir in RAW_DIR.iterdir():
    if user_dir.is_dir():
        nome = user_dir.name
        print(f"Gerando gráficos para: {nome}")

        try:
            df_musicas = pd.read_csv(user_dir / "top_musicas.csv")
            df_artistas = pd.read_csv(user_dir / "top_artistas.csv")
            df_generos = pd.read_csv(user_dir / "top_generos.csv")
            stats = pd.read_csv(user_dir / "spotify_stats.csv")
        except Exception as e:
            print(f"Erro ao ler arquivos de {nome}: {e}")
            continue

        """Cria pasta de relatórios para o utilizador"""
        user_report_dir = REPORTS_DIR / nome
        user_report_dir.mkdir(parents=True, exist_ok=True)

        """GRÁFICO 1: Top 10 músicas por duração"""
        top10_musicas = df_musicas.sort_values("duracao_min", ascending=False).head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(data=top10_musicas, x="duracao_min", y="musica", palette="Blues_d")
        plt.title(f"Top 10 Músicas - {nome}")
        plt.xlabel("Duração (min)")
        plt.tight_layout()
        plt.savefig(user_report_dir / "top10_musicas.png")
        plt.close()

        """GRÁFICO 2: Top artistas por tempo total"""
        duracoes_artistas = df_musicas.groupby("artista")["duracao_min"].sum().sort_values(ascending=False).head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=duracoes_artistas.values, y=duracoes_artistas.index, palette="Greens_d")
        plt.title(f"Top Artistas por Tempo - {nome}")
        plt.xlabel("Tempo Total (min)")
        plt.tight_layout()
        plt.savefig(user_report_dir / "top_artistas.png")
        plt.close()

        """GRÁFICO 3: Gêneros mais frequentes"""
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_generos.head(10), x="contagem", y="genero", palette="Purples_d")
        plt.title(f"Top Gêneros - {nome}")
        plt.xlabel("Frequência")
        plt.tight_layout()
        plt.savefig(user_report_dir / "top_generos.png")
        plt.close()

        """Coleta estatística para o ranking"""
        minutos_totais = stats["Total de minutos ouvidos"].iloc[0]
        ranking.append((nome, minutos_totais))

"""RANKING GERAL de todos os utilizadores"""
ranking_df = pd.DataFrame(ranking, columns=["Utilizador", "Minutos"])
ranking_df = ranking_df.sort_values("Minutos", ascending=False)

"""Gráfico estático do ranking"""
plt.figure(figsize=(10, 6))
sns.barplot(data=ranking_df, x="Minutos", y="Utilizador", palette="coolwarm")
plt.title("Ranking de Utilizadores por Minutos Ouvidos")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "ranking_utilizadores.png")
plt.close()

"""Gráfico interativo com Plotly"""
fig = px.bar(ranking_df, x="Minutos", y="Utilizador", orientation="h", title="Ranking Interativo de Utilizadores")
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
fig.write_html(str(REPORTS_DIR / "ranking_utilizadores_interativo.html"))

print("Todos os gráficos foram gerados em:", REPORTS_DIR.resolve())
