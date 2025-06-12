import sys  # Importa o módulo para interagir com argumentos da linha de comando
from pathlib import Path  # Fornece funcionalidades para manipulação de caminhos de ficheiros

# Adiciona a pasta do script atual ao sys.path para que o Python encontre o ficheiro utils.py
sys.path.append(str(Path(__file__).resolve().parent))

# Importa funções utilitárias do ficheiro utils.py
from utils import (
    criar_pasta,         # Cria uma pasta se ela ainda não existir
    ler_csv,             # Lê um ficheiro CSV e devolve um DataFrame
    salvar_csv,          # Salva um DataFrame num ficheiro CSV
    clean_tracks,        # Função que limpa e trata os dados de músicas
    clean_artists,       # Função que limpa e trata os dados de artistas
    clean_genres         # Função que limpa e trata os dados de géneros
)

# Função principal que limpa os dados de um utilizador
def main(usuario):
    BASE_DIR = Path(__file__).resolve().parent.parent  # Define a pasta base do projeto
    raw_path = BASE_DIR / "data" / "raw" / usuario  # Caminho para os ficheiros brutos do utilizador
    processed_path = criar_pasta(BASE_DIR / "data" / "processed" / usuario)  # Cria e define o caminho para os ficheiros limpos

    # Carrega os dados brutos em DataFrames
    tracks = ler_csv(raw_path / "top_musicas.csv")  # Lê o ficheiro de músicas
    artists = ler_csv(raw_path / "top_artistas.csv")  # Lê o ficheiro de artistas
    genres = ler_csv(raw_path / "top_generos.csv")  # Lê o ficheiro de géneros

    # Aplica as funções de limpeza aos dados carregados
    tracks_clean = clean_tracks(tracks)  # Limpa o DataFrame de músicas
    artists_clean = clean_artists(artists)  # Limpa o DataFrame de artistas
    genres_clean = clean_genres(genres)  # Limpa o DataFrame de géneros

    # Salva os DataFrames limpos em novos ficheiros CSV
    salvar_csv(tracks_clean, processed_path / "top_tracks_clean.csv")  # Salva as músicas limpas
    salvar_csv(artists_clean, processed_path / "top_artists_clean.csv")  # Salva os artistas limpos
    salvar_csv(genres_clean, processed_path / "top_genres_clean.csv")  # Salva os géneros limpos

    # Mensagem de sucesso com o caminho onde os dados foram salvos
    print(f"Dados limpos salvos em: {processed_path}")

# Se o ficheiro for executado diretamente (não importado), esta parte corre
if __name__ == "__main__":
    # Verifica se o nome do utilizador foi fornecido como argumento
    if len(sys.argv) < 2:
        print("Uso: python 2_clean_data.py <nome_usuario>")  # Mostra mensagem de uso correto
        sys.exit(1)  # Sai do programa com erro
    main(sys.argv[1])  # Executa a função main com o nome do utilizador passado por argumento

