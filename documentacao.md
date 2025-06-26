# Documentação do Projeto DC--Spotify

## 1. Requisitos do Sistema

Antes de começar, garante que tens os seguintes componentes instalados:

- Python 3.10 ou superior
- Git
- Visual Studio Code (VS Code)

---

## 2. Instalação do Python (Passo a Passo)

1. Acede a [https://www.python.org/downloads](https://www.python.org/downloads)
2. Clica em **Download Python 3.x.x**
3. Executa o instalador
4. Marca a opção **"Add Python to PATH"**
5. Clica em **Install Now**
6. Verifica a instalação com:

```bash
python --version
```

---

## 3. Instalação do Git

1. Acede a [https://git-scm.com/](https://git-scm.com/)
2. Faz download e instala (mantém as opções por defeito)
3. Verifica a instalação com:

```bash
git --version
```

---

## 4. Clonar o Repositório GitHub

```bash
git clone https://github.com/Garciiii/DC--Spotify
cd DC--Spotify
```

---

## 5. Criar uma Dashboard, Recolher a Credenciais do Utilizador e criar um ficheiro .env

1. Aceder ao site https://developer.spotify.com
2. Fazer login com a conta
3. Selecionar Documentation e depois Web API
4. Carregar no sublinhado "dashboard"
5. Carregar em Create app
6. Meter estes dados 
    App name : Trackily
    App description : web app que gera recibo com as musicas mais ouvidos Top 10 a 50, com as músicas, artistas, álbuns e minutos também gera uma playlists para o seu spotify com musicas mais ouvidas
    Website : Trackily
    Redirect URIs : http://127.0.0.1:8888/callback
    APIs used : selecionar WEB API e Android
7. Por fim Save
8. Após criação abrir o "Trackily"
9. Guardar o Client ID e visualizar o "View client secret" e guardar também esse codigo
10. Agora criamos na nossa pasta geral um ficheiro .env
11. Conteudo dentro do ficheiro:
    SPOTIPY_CLIENT_ID= "nossa credencial"
    SPOTIPY_CLIENT_SECRET= "nossa credencial"
    SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
---

## 6. Instalar a requiments.txt e pacotes para o Projeto

```bash
pip install -r requirements.txt
```

Caso não exista um ficheiro `requirements.txt`, instalamos manualmente os pacotes:

```bash
pip install spotipy pandas numpy matplotlib seaborn plotly streamlit
```

---

## 7. Executar os Scripts

```bash
python scripts/extract_data.py
python scripts/clean_data.py
python scripts/generate_stats.py
python scripts/generate_visuals.py
```

---

## 8. Executar os Testes com Pytest

```bash
python -m pytest
```

---

## 9. Verificar a Cobertura com Coverage

```bash
python install coverage
python -m coverage run -m pytest
python -m coverage html
start htmlcov/index.html
```

---

## 10. Verificar Qualidade com Pylint

```bash
python install pytest
pylint --version
python -m pylint scripts/ tests/ ui/
```

---

## 11. Git - Guardar e Enviar Alterações

```bash
git status
git add .
git commit -m "mensagem do commit"
git push origin main
```

Se quiseres remover ficheiros desnecessários antes:

```bash
del .coverage
```

---

## 12. Instruções Finais

- Os relatórios HTML de testes estarão na pasta `htmlcov`
- A cache dos testes é guardada em `.pytest_cache`
- A estrutura típica da pasta:
  - `scripts/` – scripts de processamento
  - `tests/` – testes com Pytest
  - `data/` – dados brutos e processados
  - `ui/` – interface 

---


