import requests
import json

# URL base da API
base_url = "https://dadosabertos.compras.gov.br/modulo-legado/1_consultarLicitacao"
params = {
    "tamanhoPagina": 500,
    "data_publicacao_inicial": "2024-01-01",
    "data_publicacao_final": "2024-08-01"
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

# Salva todos os dados coletados em um arquivo JSON
with open("dados_licitacoes.json", "w", encoding='utf-8') as arquivo_json:
    json.dump(todos_os_dados, arquivo_json, ensure_ascii=False, indent=4)

print("Coleta concluída. Dados salvos em 'dados_licitacoes.json'")
