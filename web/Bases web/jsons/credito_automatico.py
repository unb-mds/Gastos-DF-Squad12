import requests
import re
import json
from collections import defaultdict
import os
from datetime import datetime, timedelta

# seta os diretorios
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'resultados_credito.json')

def process_gazettes():
    # pega a data de ontem
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # Fazendo a solicitação GET para a API
    url = f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={yesterday_str}&published_until={yesterday_str}&querystring=%22Abre%20cr%C3%A9dito%20suplementar%22&excerpt_size=120&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro na solicitação: {response.status_code}")
        return

    # Convertendo a resposta para JSON
    dados = response.json()
    gazettes = dados.get('gazettes', [])

    # carrega os dados existentes ou cria um novo
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {"resultados": []}

    # Estrutura para armazenar dados
    resultados = defaultdict(lambda: {"url": "", "total_gasto_dia": 0.0, "decretos": []})

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        data = gazette.get('date')
        url = gazette.get('url')
        excertos = gazette.get('excerpts', [])

        # Verificando se a data já foi registrada
        if resultados[data]["url"] == "":
            resultados[data]["url"] = url

        # Iterando sobre cada excerto
        for excerto in excertos:
            # Substituindo quebras de linha múltiplas por um único espaço
            excerto = re.sub(r'\s+', ' ', excerto)

            # Usando expressão regular para encontrar o Decreto e Valor
            decreto_match = re.search(r'DECRETO\s*N[ºo]\s*([\d.]+)', excerto, re.IGNORECASE)
            valor_match = re.search(r'valor\s*de\s*R\$\s*([\d,.]+)', excerto, re.IGNORECASE)

            if decreto_match and valor_match:
                # Extraindo o decreto encontrado
                decreto = decreto_match.group(1).strip()

                # Extraindo o valor encontrado
                valor = valor_match.group(1)
                # Removendo caracteres não numéricos, exceto vírgulas e pontos
                valor_limpo = re.sub(r'[^\d,.]', '', valor)
                # Removendo pontos extras como separadores de milhar
                valor_limpo = valor_limpo.replace('.', '')
                # Trocando a vírgula por ponto para ter o formato correto para float
                valor_limpo = valor_limpo.replace(',', '.')
                # Convertendo o valor para float
                valor_float = float(valor_limpo)

                # Adicionando ao resultado
                resultados[data]["total_gasto_dia"] += valor_float
                resultados[data]["decretos"].append({"decreto": decreto, "valor": valor_float})

    # Convertendo o resultado para o formato JSON esperado
    new_results = [
        {
            "date": data,
            "url": info["url"],
            "total_gasto_dia": info["total_gasto_dia"],
            "decretos": info["decretos"]
        }
        for data, info in resultados.items()
    ]

    # Junta resultado com os existentes
    existing_data["resultados"].extend(new_results)

    # Salvando o resultado atualizado em um arquivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Arquivo JSON '{json_file_path}' atualizado com sucesso.")

if __name__ == "__main__":
    process_gazettes()
