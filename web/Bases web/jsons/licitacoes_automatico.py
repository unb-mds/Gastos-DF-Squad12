import requests
import json
from datetime import datetime, timedelta
import os

# Set the working directory to the script's location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# URL base da API
base_url = "https://dadosabertos.compras.gov.br/modulo-legado/1_consultarLicitacao"

# Get today's date and the date 30 days ago
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

params = {
    "tamanhoPagina": 500,
    "data_publicacao_inicial": start_date,
    "data_publicacao_final": end_date
}

# Inicializa a variável para armazenar todos os dados
todos_os_dados = []

# Página inicial
pagina_atual = 1

while True:
    # Atualiza o parâmetro de página
    params["pagina"] = pagina_atual

    # Faz a requisição à API
    response = requests.get(base_url, params=params)
    response.encoding = 'utf-8'  # Garante que a resposta esteja codificada em UTF-8
    dados = response.json()

    # Adiciona os resultados à lista principal
    todos_os_dados.extend(dados["resultado"])

    # Mostra em qual página o programa está
    print(f"Coletando dados da página {pagina_atual} de {dados['totalPaginas']}")

    # Verifica se há mais páginas para buscar
    if pagina_atual >= dados["totalPaginas"]:
        break

    # Incrementa a página
    pagina_atual += 1

# Caminho para o arquivo JSON
json_path = "../../dados_licitacoes.json"

# Carrega os dados existentes, se houver
try:
    with open(json_path, "r", encoding='utf-8') as arquivo_json:
        dados_existentes = json.load(arquivo_json)
except FileNotFoundError:
    dados_existentes = []

# Adiciona os novos dados aos existentes
dados_existentes.extend(todos_os_dados)

# Remove duplicatas baseadas no ID da licitação
dados_unicos = {item['id_licitacao']: item for item in dados_existentes}.values()

# Salva todos os dados coletados em um arquivo JSON
with open(json_path, "w", encoding='utf-8') as arquivo_json:
    json.dump(list(dados_unicos), arquivo_json, ensure_ascii=False, indent=4)

print(f"Coleta concluída. Dados salvos em '{json_path}'")