import requests
import re
import json
from collections import defaultdict
import os
from datetime import datetime, timedelta

# Set the correct paths
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'resultados_convenio.json')

def process_gazettes():
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # Fazendo a solicitação GET para a API
    url = f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={yesterday_str}&published_until={yesterday_str}&querystring=%22RECONHECIMENTO%20DE%20D%C3%8DVIDA%22&excerpt_size=500&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Erro na solicitação: {response.status_code}")
        return

    # Convertendo a resposta para JSON
    dados = response.json()
    gazettes = dados.get('gazettes', [])

    # Load existing data or create an empty dictionary
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    else:
        existing_data = {"resultados": []}

    # Estrutura para armazenar dados
    resultados = defaultdict(lambda: {"decretos": []})

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        data = gazette.get('date')
        if not data:
            continue

        excertos = gazette.get('excerpts', [])
        total_diario = 0

        for excerto in excertos:
            # Normalizando o texto para facilitar a extração
            excerto = excerto.replace('\n', ' ').replace('\r', ' ')

            # Ajustando regex para capturar corretamente o interessado e valor
            interessado_match = re.search(
                r'(?:Interessado:\s*|\bem\s+favor\s+da\s+empresa\s+)([^\.,\n]+(?:[^\.,\n]+)*)',
                excerto, re.IGNORECASE)
            valor_match = re.search(
                r'Valor:\s*R\$(.*?[\d,.]+)|(?:no\s+valor\s+total\s+de\s+R\$(.*?[\d,.]+))',
                excerto, re.IGNORECASE)

            if interessado_match and valor_match:
                interessado = interessado_match.group(1).strip()

                if valor_match.group(1):
                    valor = valor_match.group(1).strip()
                else:
                    valor = valor_match.group(2).strip()

                # Limpeza do valor
                valor_limpo = re.sub(r'[^\d,]', '', valor)
                valor_limpo = valor_limpo.replace('.', '', valor_limpo.count(',') - 1)
                valor_limpo = valor_limpo.replace(',', '.')

                try:
                    valor_float = float(valor_limpo)
                except ValueError:
                    print(f"Erro ao converter o valor '{valor_limpo}' para float.")
                    valor_float = 0.0

                # Adicionando ao resultado
                resultados[data]["decretos"].append({"interessado": interessado, "valor": valor_float})
                total_diario += valor_float

        if total_diario > 0:  # Ignorando datas com total 0
            resultados[data]["total_diario"] = total_diario

    # Convertendo o resultado para o formato JSON esperado, ignorando datas com total igual a 0
    new_results = [
        {
            "date": data,
            "total_gasto_dia": info["total_diario"],
            "decretos": info["decretos"]
        }
        for data, info in resultados.items()
        if "total_diario" in info and info["total_diario"] > 0
    ]

    # Merge new results with existing data
    existing_data["resultados"].extend(new_results)

    # Salvando o resultado atualizado em um arquivo JSON
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Arquivo JSON '{json_file_path}' atualizado com sucesso.")

if __name__ == "__main__":
    process_gazettes()