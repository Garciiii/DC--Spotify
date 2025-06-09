import pandas as pd
import pytest
from pathlib import Path

# Caminho dos dados limpos para testes
BASE_DIR = Path("data/processed/Helder")

@pytest.fixture
def df_tracks():
    return pd.read_csv(BASE_DIR / "top_tracks_clean.csv")

@pytest.fixture
def df_artists():
    return pd.read_csv(BASE_DIR / "top_artists_clean.csv")

@pytest.fixture
def df_genres():
    return pd.read_csv(BASE_DIR / "top_genres_clean.csv")

def test_tracks_columns(df_tracks):
    expected_cols = {"musica", "artista", "album", "duracao_min", "popularidade", "uri"}
    assert set(df_tracks.columns) == expected_cols

def test_artists_columns(df_artists):
    expected_cols = {"artista", "generos", "seguidores", "popularidade", "uri"}
    assert set(df_artists.columns) == expected_cols

def test_genres_columns(df_genres):
    expected_cols = {"genero", "contagem"}
    assert set(df_genres.columns) == expected_cols

def test_no_nulls(df_tracks, df_artists, df_genres):
    assert not df_tracks.isnull().any().any(), "Dados de tracks contêm nulos"
    assert not df_artists.isnull().any().any(), "Dados de artistas contêm nulos"
    assert not df_genres.isnull().any().any(), "Dados de gêneros contêm nulos"

def test_positive_values(df_tracks, df_artists, df_genres):
    assert (df_tracks["duracao_min"] > 0).all()
    assert (df_tracks["popularidade"] >= 0).all()
    assert (df_artists["seguidores"] >= 0).all()
    assert (df_artists["popularidade"] >= 0).all()
    assert (df_genres["contagem"] > 0).all()
