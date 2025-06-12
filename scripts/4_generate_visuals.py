import os  # Biblioteca para operações com o sistema de ficheiros
import pandas as pd  # Biblioteca para análise e manipulação de dados
import matplotlib.pyplot as plt  # Biblioteca para criar gráficos estáticos
import seaborn as sns  # Biblioteca para visualização de dados baseada no matplotlib
from pathlib import Path  # Biblioteca para lidar com caminhos de ficheiros
import plotly.express as px  # Biblioteca para criar gráficos interativos

sns.set(style="whitegrid")  # Define o estilo dos gráficos do seaborn

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho para os dados brutos
RAW_DIR = BASE_DIR / "data" / "raw"

# Caminho para os relatórios (onde os gráficos serão salvos)
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)  # Cria o diretório se não existir

# Lista para armazenar tuplos com nome de utilizador e minutos totais
ranking = []

# Itera sobre cada pasta de utilizador na pasta de dados brutos
for user_dir in RAW_DIR.iterdir():
    if user_dir.is_dir():  # Garante que só pastas sejam processadas
        nome = user_dir.name  # Nome do utilizador (nome da pasta)
        print(f"Gerando gráficos para: {nome}")  # Mensagem de progresso

        # Tenta ler os ficheiros CSV
        try:
            df_musicas = pd.read_csv(user_dir / "top_musicas.csv")  # Músicas
            df_artistas = pd.read_csv(user_dir / "top_artistas.csv")  # Artistas
            df_generos = pd.read_csv(user_dir / "top_generos.csv")  # Géneros
            stats = pd.read_csv(user_dir / "spotify_stats.csv")  # Estatísticas
        except Exception as e:
            print(f"Erro ao ler arquivos de {nome}: {e}")  # Erro ao ler ficheiros
            continue  # Pula para o próximo utilizador

        # Cria diretório para os relatórios do utilizador
        user_report_dir = REPORTS_DIR / nome
        user_report_dir.mkdir(parents=True, exist_ok=True)

        # === GRÁFICO 1 ===
        # Seleciona as 10 músicas com maior duração
        top10_musicas = df_musicas.sort_values("duracao_min", ascending=False).head(10)
        plt.figure(figsize=(12, 6))  # Tamanho do gráfico
        sns.barplot(data=top10_musicas, x="duracao_min", y="musica", palette="Blues_d")  # Gráfico de barras
        plt.title(f"Top 10 Músicas - {nome}")  # Título
        plt.xlabel("Duração (min)")  # Rótulo do eixo X
        plt.tight_layout()  # Ajusta layout
        plt.savefig(user_report_dir / "top10_musicas.png")  # Salva imagem
        plt.close()  # Fecha a figura atual

        # === GRÁFICO 2 ===
        # Agrupa por artista e soma o tempo total
        duracoes_artistas = df_musicas.groupby("artista")["duracao_min"].sum().sort_values(ascending=False).head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=duracoes_artistas.values, y=duracoes_artistas.index, palette="Greens_d")
        plt.title(f"Top Artistas por Tempo - {nome}")
        plt.xlabel("Tempo Total (min)")
        plt.tight_layout()
        plt.savefig(user_report_dir / "top_artistas.png")
        plt.close()

        # === GRÁFICO 3 ===
        # Gêneros mais frequentes (top 10)
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_generos.head(10), x="contagem", y="genero", palette="Purples_d")
        plt.title(f"Top Gêneros - {nome}")
        plt.xlabel("Frequência")
        plt.tight_layout()
        plt.savefig(user_report_dir / "top_generos.png")
        plt.close()

        # Obtém o total de minutos ouvidos do ficheiro de estatísticas
        minutos_totais = stats["Total de minutos ouvidos"].iloc[0]
        ranking.append((nome, minutos_totais))  # Adiciona ao ranking

# === RANKING GERAL ===
# Cria DataFrame com ranking de todos os utilizadores
ranking_df = pd.DataFrame(ranking, columns=["Utilizador", "Minutos"])

# Ordena do maior para o menor
ranking_df = ranking_df.sort_values("Minutos", ascending=False)

# Gráfico estático do ranking
plt.figure(figsize=(10, 6))
sns.barplot(data=ranking_df, x="Minutos", y="Utilizador", palette="coolwarm")
plt.title("Ranking de Utilizadores por Minutos Ouvidos")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "ranking_utilizadores.png")
plt.close()

# Gráfico interativo com Plotly
fig = px.bar(ranking_df, x="Minutos", y="Utilizador", orientation="h", title="Ranking Interativo de Utilizadores")
fig.update_layout(yaxis={'categoryorder': 'total ascending'})  # Ordena os nomes pelo valor
fig.write_html(str(REPORTS_DIR / "ranking_utilizadores_interativo.html"))  # Salva como HTML interativo

# Mensagem final de sucesso
print("Todos os gráficos foram gerados em:", REPORTS_DIR.resolve())
