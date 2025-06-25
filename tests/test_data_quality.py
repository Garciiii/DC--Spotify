"""Testes para verificar a qualidade dos dados."""
from pathlib import Path
import pandas as pd
import pytest

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

def test_tracks_columns(tracks):
    """
    Verifica se o DataFrame de músicas contém todas as colunas esperadas.
    """
    expected_cols = {"musica", "artista", "album", "duracao_min", "popularidade", "uri"}
    assert set(tracks.columns) == expected_cols

def test_artists_columns(artists):
    """
    Verifica se o DataFrame de artistas contém todas as colunas esperadas.
    """
    expected_cols = {"artista", "generos", "seguidores", "popularidade", "uri"}
    assert set(artists.columns) == expected_cols

def test_genres_columns(genres):
    """
    Verifica se o DataFrame de géneros contém todas as colunas esperadas.
    """
    expected_cols = {"genero", "contagem"}
    assert set(genres.columns) == expected_cols

def test_no_nulls(tracks, artists, genres):
    """
    Garante que não existam valores nulos nos DataFrames de músicas, artistas e géneros.
    """
    assert not tracks.isnull().any().any(), "Dados de tracks contêm nulos"
    assert not artists.isnull().any().any(), "Dados de artistas contêm nulos"
    assert not genres.isnull().any().any(), "Dados de géneros contêm nulos"

def test_positive_values(tracks, artists, genres):
    """
    Verifica que os valores numéricos importantes são positivos ou não-negativos:
    - duração das músicas
    - popularidade das músicas e artistas
    - seguidores
    - contagem de géneros
    """
    assert (tracks["duracao_min"] > 0).all()
    assert (tracks["popularidade"] >= 0).all()
    assert (artists["seguidores"] >= 0).all()
    assert (artists["popularidade"] >= 0).all()
    assert (genres["contagem"] > 0).all()
