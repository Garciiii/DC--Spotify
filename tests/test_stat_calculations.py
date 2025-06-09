# tests/test_stat_calculations.py

import pandas as pd

def test_basic_statistics():
    # Dados simulados
    data = {
        "track_name": ["Song A", "Song B", "Song C", "Song D"],
        "artist_name": ["Artist 1", "Artist 2", "Artist 1", "Artist 3"],
        "played_minutes": [3.5, 4.0, 2.5, 5.0],
        "popularity": [80, 65, 70, 90],
        "duration_ms": [210000, 240000, 180000, 300000]
    }
    df = pd.DataFrame(data)

    # Testa total de minutos
    assert df["played_minutes"].sum() == 15.0

    # Testa média de popularidade
    assert round(df["popularity"].mean(), 1) == 76.3

    # Testa faixa mais popular
    most_popular = df.loc[df["popularity"].idxmax()]
    assert most_popular["track_name"] == "Song D"

    # Testa artista mais comum
    assert df["artist_name"].value_counts().idxmax() == "Artist 1"

def test_track_durations():
    data = {
        "track_name": ["A", "B"],
        "duration_ms": [180000, 240000]
    }
    df = pd.DataFrame(data)
    durations = df["duration_ms"] / 60000  # Convertido para minutos
    assert list(durations.round(1)) == [3.0, 4.0]
