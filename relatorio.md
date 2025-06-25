# Projeto Final – DC-Spotify 🎧

## Curso: Licenciatura em Engenharia Informática  
## Unidade Curricular: Projeto de Integração Vertical (PIV)  
## Ano letivo: 2024/2025  
## Grupo: [Nome do Aluno 1], [Nome do Aluno 2]  
## Docente: Miguel Rodrigues  

---

## 1. Objetivo do Projeto

O objetivo deste projeto é desenvolver uma aplicação em Python que permita recolher, tratar, analisar e visualizar dados musicais provenientes da plataforma Spotify.  
A aplicação tem como finalidade explorar os hábitos de escuta dos utilizadores, artistas e géneros musicais mais populares, com base em dados reais extraídos através da API do Spotify ou ficheiros CSV.

---

## 2. Estrutura do Projeto

A aplicação está organizada em várias fases:

1. **Extração de Dados (`scripts/1_extract_data.py`)**  
   - Ligação à API do Spotify ou leitura de ficheiros `.csv`.
   - Simulação de uma base de dados com informações de faixas, artistas e géneros.

2. **Limpeza e Preparação (`scripts/2_clean_data.py`)**  
   - Tratamento de dados em falta, normalização de formatos e estruturação da informação.

3. **Geração de Estatísticas (`scripts/3_generate_stats.py`)**  
   - Cálculo de totais, médias e rankings com base em artistas, géneros, popularidade, etc.

4. **Visualização de Dados (`scripts/4_generate_visuals.py`)**  
   - Criação de gráficos com `matplotlib` e `seaborn`.
   - Exportação em `.json`, `.csv`, `.xlsx` e imagens.

5. **Dashboard Interativo (`ui/dashboard.py`)**  
   - Visualização pública dos resultados com `streamlit`.

---

## 3. Tecnologias e Ferramentas Utilizadas

- **Linguagem de Programação:** Python 3.11  
- **Bibliotecas Principais:**  
  - `spotipy`, `pandas`, `matplotlib`, `seaborn`, `streamlit`, `openpyxl`, `dotenv`  
- **Ferramentas de Qualidade de Código:**  
  - `pylint` para análise estática  
  - `pytest` para testes  
  - `coverage` para cobertura de testes  
- **Controlo de Versão:** Git / GitHub  

---

## 4. Divisão de Tarefas

| Tarefa                     | Helder Garcia    | Diogo santos     |
|----------------------------|------------------|------------------|
| Configuração do projeto    | ✅               |                 
| Extração de dados          | ✅               |     ✅                
| Limpeza de dados           | ✅               |      ✅                
| Estatísticas e análise     | ✅               |     ✅
| Visualização e dashboard   |                  |       ✅                
| Testes e validação         | ✅               |      ✅            
| Relatório e documentação   | ✅               |      ✅                

---

## 5. Resultados Exportados

- Ficheiros `.json` com metadados de faixas, artistas e géneros  
- `.csv` com dados tratados  
- `.xlsx` com estatísticas agregadas  
- Gráficos de barras, dispersão, mapas de calor (em `.png`)  
- Dashboard em `streamlit` com filtros interativos

---

## 6. Possíveis Melhorias Futuras

- Integração com mais APIs externas (ex: YouTube, Last.fm)  
- Comparação entre diferentes playlists ou anos  
- Geração de mapas geográficos com dados regionais (se aplicável)  
- Recomendação musical com base em análise preditiva

---

## 7. Como Executar o Projeto

1. Criar um ficheiro `.env` com as credenciais da API do Spotify:
