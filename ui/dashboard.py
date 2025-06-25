"""Interface do dashboard para visualização dos dados do usuário."""
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

def carregar_dados(utilizador):
    """
    Carrega e valida os dados do utilizador a partir de ficheiros CSV.
    
    Args:
        utilizador (str): Nome do utilizador para carregar os dados
        
    Returns:
        tuple: DataFrames contendo dados de músicas, artistas e géneros
        
    Raises:
        FileNotFoundError: Se algum ficheiro de dados não for encontrado
        ValueError: Se colunas obrigatórias estiverem em falta
    """
    caminho = Path("data/processed") / utilizador
    try:
        df_musicas = pd.read_csv(caminho / "top_tracks_clean.csv")
        df_artistas = pd.read_csv(caminho / "top_artists_clean.csv")
        df_generos = pd.read_csv(caminho / "top_genres_clean.csv")
        # Validar colunas obrigatórias
        colunas_obrigatorias = {"musica", "artista", "duracao_min", "popularidade"}
        if not colunas_obrigatorias.issubset(df_musicas.columns):
            raise ValueError("Colunas obrigatórias em falta nos dados de músicas")
        return df_musicas, df_artistas, df_generos
    except FileNotFoundError as e:
        st.error(f"Ficheiro de dados não encontrado: {e.filename}")
        st.stop()
    except ValueError as e:
        st.error(f"Formato de dados inválido: {str(e)}")
        st.stop()

def criar_grafico_barras(df, x, y, titulo, coluna_cor=None):
    """
    Cria um gráfico de barras horizontal padronizado.
    
    Args:
        df (DataFrame): Dados para visualização
        x (str): Nome da coluna para valores do eixo x
        y (str): Nome da coluna para categorias do eixo y
        titulo (str): Título do gráfico
        coluna_cor (str, optional): Coluna para usar na escala de cores 
    Returns:
        plotly.graph_objects.Figure: Figura Plotly configurada
    """
    fig = px.bar(df.head(10), x=x, y=y, orientation="h",
                 title=titulo, color=coluna_cor)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

# Configuração da página
st.set_page_config(page_title="Dashboard Spotify", layout="wide")

# Input do utilizador na barra lateral
st.sidebar.title("Dashboard de Dados Spotify")
nome_utilizador = st.sidebar.text_input("Introduza o nome do utilizador:").strip()

if nome_utilizador:
    musicas, artistas, generos = carregar_dados(nome_utilizador)

    st.title(f"Análise Musical para {nome_utilizador.capitalize()}")

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    col1.metric("Músicas Únicas", musicas["musica"].nunique())
    col2.metric("Artistas Únicos", musicas["artista"].nunique())
    col3.metric("Duração Total (min)", round(musicas["duracao_min"].sum(), 1))

    st.markdown("---")

    # Gráficos
    st.plotly_chart(
        criar_grafico_barras(
            musicas.sort_values("popularidade", ascending=False),
            x="popularidade", y="musica",
            titulo="Top 10 Músicas Mais Populares",
            coluna_cor="popularidade"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        criar_grafico_barras(
            generos.sort_values("contagem", ascending=False),
            x="contagem", y="genero",
            titulo="Top 10 Géneros Mais Frequentes",
            coluna_cor="contagem"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        criar_grafico_barras(
            artistas.sort_values("popularidade", ascending=False),
            x="popularidade", y="artista",
            titulo="Top 10 Artistas por Popularidade",
            coluna_cor="popularidade"
        ),
        use_container_width=True
    )
else:
    st.info("Por favor, introduza um nome de utilizador na barra lateral para visualizar os dados.")
