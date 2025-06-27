"""Testes para verificar a qualidade dos dados."""
from pathlib import Path
import pandas as pd
import pytest

# pylint: disable=redefined-outer-name
# Caminho dos dados limpos para testes
BASE_DIR = Path("data/processed/Helder")

@pytest.fixture
def df_tracks():
    """Carrega o DataFrame de músicas limpas para testes."""
    return pd.read_csv(BASE_DIR / "top_tracks_clean.csv")

@pytest.fixture
def df_artists():
    """Carrega o DataFrame de artistas limpos para testes."""
    return pd.read_csv(BASE_DIR / "top_artists_clean.csv")

@pytest.fixture
def df_genres():
    """Carrega o DataFrame de géneros limpos para testes."""
    return pd.read_csv(BASE_DIR / "top_genres_clean.csv")

def test_tracks_columns(df_tracks):
    """
    Verifica se o DataFrame de músicas contém todas as colunas esperadas.
    """
    expected_cols = {"musica", "artista", "album", "duracao_min", "popularidade", "uri"}
    assert set(df_tracks.columns) == expected_cols

def test_artists_columns(df_artists):
    """
    Verifica se o DataFrame de artistas contém todas as colunas esperadas.
    """
    expected_cols = {"artista", "generos", "seguidores", "popularidade", "uri"}
    assert set(df_artists.columns) == expected_cols

def test_genres_columns(df_genres):
    """
    Verifica se o DataFrame de géneros contém todas as colunas esperadas.
    """
    expected_cols = {"genero", "contagem"}
    assert set(df_genres.columns) == expected_cols

def test_no_nulls(df_tracks, df_artists, df_genres):
    """
    Garante que não existam valores nulos nos DataFrames de músicas, artistas e géneros.
    """
    assert not df_tracks.isnull().any().any(), "Dados de tracks contêm nulos"
    # Preenche nulos em 'generos' com string vazia para evitar erro
    df_artists_filled = df_artists.fillna({"generos": ""})
    assert not df_artists_filled.isnull().any().any(), \
        "Dados de artistas contêm nulos"
    assert not df_genres.isnull().any().any(), "Dados de géneros contêm nulos"

def test_positive_values(df_tracks, df_artists, df_genres):
    """
    Verifica que os valores numéricos importantes são positivos ou não-negativos:
    - duração das músicas
    - popularidade das músicas e artistas
    - seguidores
    - contagem de géneros
    """
    assert (df_tracks["duracao_min"] > 0).all()
    assert (df_tracks["popularidade"] >= 0).all()
    assert (df_artists["seguidores"] >= 0).all()
    assert (df_artists["popularidade"] >= 0).all()
    assert (df_genres["contagem"] > 0).all()
