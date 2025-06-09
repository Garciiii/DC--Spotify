# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Dashboard Spotify", layout="wide")

# Sidebar: selecionar usuário
st.sidebar.title(" Dashboard Spotify")
usuario = st.sidebar.text_input("Digite o nome do usuário:")

if usuario:
    path = Path("data/processed") / usuario
    try:
        df_tracks = pd.read_csv(path / "top_tracks_clean.csv")
        df_artists = pd.read_csv(path / "top_artists_clean.csv")
        df_genres = pd.read_csv(path / "top_genres_clean.csv")
    except FileNotFoundError:
        st.error("Arquivos CSV não encontrados. Certifique-se de que os dados foram processados corretamente.")
        st.stop()

    st.title(f"🎵 Análise Musical de {usuario.capitalize()}")

    # Estatísticas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Faixas únicas", df_tracks["musica"].nunique())
    col2.metric("Artistas únicos", df_tracks["artista"].nunique())
    col3.metric("Duração total (min)", round(df_tracks["duracao_min"].sum(), 1))

    st.markdown("---")

    # Gráfico: Top 10 músicas por popularidade
    top_musics = df_tracks.sort_values("popularidade", ascending=False).head(10)
    fig1 = px.bar(top_musics, x="popularidade", y="musica", orientation="h",
                  title="Top 10 Músicas Mais Populares", color="popularidade")
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico: Gêneros mais ouvidos
    fig2 = px.bar(df_genres.head(10), x="contagem", y="genero", orientation="h",
                  title="Top 10 Gêneros Mais Frequentes", color="contagem")
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico: Artistas mais frequentes
    fig3 = px.bar(df_artists.head(10), x="popularidade", y="artista", orientation="h",
                  title="Top 10 Artistas por Popularidade", color="popularidade")
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Digite um nome de usuário à esquerda para visualizar os dados.")
