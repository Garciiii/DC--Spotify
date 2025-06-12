import os  # Importa o módulo para interagir com o sistema operativo
import sys  # Permite o acesso a argumentos da linha de comando e controlo do sistema
from pathlib import Path  # Fornece classes para manipulação de caminhos de ficheiros
from dotenv import load_dotenv  # Permite carregar variáveis de ambiente de um ficheiro .env
import spotipy  # Biblioteca para interagir com a API do Spotify
from spotipy.oauth2 import SpotifyOAuth  # Classe de autenticação OAuth do Spotipy

import pandas as pd  # Biblioteca para manipulação de dados em tabelas (DataFrames)
from collections import Counter  # Permite contar ocorrências de elementos (ex: géneros musicais)

from utils import criar_pasta, salvar_csv  # Importa funções auxiliares do ficheiro utils.py

# Define a pasta base do projeto (dois níveis acima do ficheiro atual)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do ficheiro .env localizado em /secrets
load_dotenv(dotenv_path=BASE_DIR / "secrets" / ".env")

# Lê as variáveis do .env necessárias para a autenticação com o Spotify
CLIENT_ID = os.getenv("CLIENT_ID")  # ID da aplicação no Spotify
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Segredo da aplicação
REDIRECT_URI = os.getenv("REDIRECT_URI")  # URL para redirecionamento após login no Spotify
SCOPE = "user-top-read"  # Permissão para ler as músicas e artistas mais ouvidos pelo utilizador

# Função para pedir o nome do utilizador e criar uma pasta para armazenar os dados dele
def criar_pasta_usuario():
    nome_usuario = input("Digite o nome do usuário para salvar os dados: ").strip()  # Solicita o nome do utilizador
    if not nome_usuario:  # Verifica se o nome é válido
        print("Nome inválido. Saindo...")  # Mostra erro e sai
        sys.exit(1)

    pasta_raw = BASE_DIR / "data" / "raw" / nome_usuario  # Define o caminho onde os dados serão salvos
    criar_pasta(pasta_raw)  # Cria a pasta, se ainda não existir
    return pasta_raw  # Retorna o caminho da pasta criada

# Função para autenticar o utilizador com a API do Spotify
def autenticar_spotify():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,  # Usa o CLIENT_ID do .env
            client_secret=CLIENT_SECRET,  # Usa o CLIENT_SECRET do .env
            redirect_uri=REDIRECT_URI,  # Usa o REDIRECT_URI do .env
            scope=SCOPE,  # Define o scope de permissões
            cache_path=".spotify_cache"  # Guarda token em cache para evitar múltiplos logins
        ))
        print("Autenticação com Spotify realizada com sucesso")  # Mensagem de sucesso
        return sp  # Retorna o objeto autenticado do Spotify
    except Exception as e:  # Em caso de erro na autenticação
        print(f"Falha na autenticação: {e}")  # Mostra o erro
        sys.exit(1)  # Encerra o programa

# Função que extrai os dados do Spotify
def extrair_dados(sp, limite=50):
    print(f"Extraindo top {limite} músicas e artistas...")  # Mostra mensagem de início

    # Extrai as top músicas do utilizador
    top_musicas = sp.current_user_top_tracks(limit=limite, time_range="medium_term")

    # Cria um DataFrame com dados das músicas
    df_musicas = pd.DataFrame([{
        "musica": item["name"],  # Nome da música
        "artista": item["artists"][0]["name"],  # Nome do primeiro artista
        "album": item["album"]["name"],  # Nome do álbum
        "duracao_min": round(item["duration_ms"] / 60000, 2),  # Duração em minutos
        "popularidade": item["popularity"],  # Popularidade (0 a 100)
        "uri": item["uri"]  # URI do Spotify
    } for item in top_musicas["items"]])  # Percorre todas as faixas extraídas

    # Extrai os top artistas do utilizador
    top_artistas = sp.current_user_top_artists(limit=limite, time_range="medium_term")

    # Cria um DataFrame com dados dos artistas
    df_artistas = pd.DataFrame([{
        "artista": item["name"],  # Nome do artista
        "generos": "|".join(item["genres"]),  # Lista de géneros, separados por '|'
        "seguidores": item["followers"]["total"],  # Total de seguidores
        "popularidade": item["popularity"],  # Popularidade do artista
        "uri": item["uri"]  # URI do Spotify
    } for item in top_artistas["items"]])  # Percorre todos os artistas extraídos

    # Extrai e conta todos os géneros musicais dos artistas
    generos = [g for item in top_artistas["items"] for g in item["genres"]]  # Junta todos os géneros
    df_generos = pd.DataFrame(Counter(generos).items(), columns=["genero", "contagem"])  # Conta quantos há de cada género
    df_generos = df_generos.sort_values("contagem", ascending=False)  # Ordena do mais comum para o menos

    return df_musicas, df_artistas, df_generos  # Retorna os 3 DataFrames criados

# Função que salva os DataFrames como ficheiros CSV
def salvar_arquivos(df_musicas, df_artistas, df_generos, pasta):
    salvar_csv(df_musicas, pasta / "top_musicas.csv")  # Salva o DataFrame de músicas
    salvar_csv(df_artistas, pasta / "top_artistas.csv")  # Salva o DataFrame de artistas
    salvar_csv(df_generos, pasta / "top_generos.csv")  # Salva o DataFrame de géneros
    print(f"Dados salvos em: {pasta.resolve()}")  # Mostra onde os ficheiros foram salvos

# Função principal que orquestra todo o processo
def main():
    pasta_usuario = criar_pasta_usuario()  # Pede nome do utilizador e cria pasta para ele

    try:
        limite = int(sys.argv[1]) if len(sys.argv) > 1 else 50  # Usa argumento opcional do terminal para definir limite
        if limite not in [10, 50]:  # Valida se o limite é permitido
            raise ValueError  # Lança erro se valor inválido
    except ValueError:  # Captura erro de valor
        print("Uso: python 1_extract_data.py [10|50]")  # Mostra instrução de uso
        sys.exit(1)  # Sai do programa

    sp = autenticar_spotify()  # Faz login na API do Spotify

    try:
        df_musicas, df_artistas, df_generos = extrair_dados(sp, limite)  # Extrai dados
        salvar_arquivos(df_musicas, df_artistas, df_generos, pasta_usuario)  # Salva os dados em CSV
    except Exception as e:  # Captura erros durante extração
        print(f"Erro durante a extração: {e}")  # Mostra o erro

# Executa o programa se este ficheiro for chamado diretamente
if __name__ == "__main__":
    main()
