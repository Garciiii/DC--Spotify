"""Funções utilitárias para manipulação de arquivos e dados."""
import os
from pathlib import Path
import pandas as pd

def criar_pasta(pasta_path):
    """Cria uma pasta se ela não existir"""
    Path(pasta_path).mkdir(parents=True, exist_ok=True)
    return pasta_path  # Retorna o caminho para uso posterior

def salvar_csv(df, caminho_csv):
    """Salva um DataFrame como CSV com codificação UTF-8"""
    df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

def ler_csv(caminho_csv):
    """Lê um arquivo CSV para um DataFrame"""
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")
    return pd.read_csv(caminho_csv)

def limpar_colunas_espaco(df, colunas):
    """Remove espaços em branco das colunas especificadas"""
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.strip()
    return df

def padronizar_minusculas(df, colunas):
    """Converte o conteúdo das colunas especificadas para minúsculas"""
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.lower()
    return df

# ---------- Funções para limpeza específica ----------
def clean_tracks(df):
    """Limpa e padroniza dados de músicas"""
    df = limpar_colunas_espaco(df, ["musica", "artista", "album"])
    df = padronizar_minusculas(df, ["musica", "artista", "album"])
    return df

def clean_artists(df):
    """Limpa e padroniza dados de artistas"""
    df = limpar_colunas_espaco(df, ["artista", "generos"])
    df = padronizar_minusculas(df, ["artista", "generos"])
    return df

def clean_genres(df):
    """Limpa e padroniza dados de gêneros"""
    df = limpar_colunas_espaco(df, ["genero"])
    df = padronizar_minusculas(df, ["genero"])
    return df
