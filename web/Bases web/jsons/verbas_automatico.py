import re
import requests
import json
from datetime import datetime, timedelta
import os

# corrige os diretorios
script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(os.path.dirname(os.path.dirname(script_dir)), 'resultados_escola.json')


def get_month_name(date):
    months = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return months[date.month - 1]


# data de ontem
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")

# Fazendo a solicitação GET para a API
url = f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={yesterday_str}&published_until={yesterday_str}&querystring=%22N%C2%BA%20UE%20Custeio%20Total%22%20%22N%C2%BA%20CRE%2FUE%20Capital%20Custeio%20Total%22&excerpt_size=50000&number_of_excerpts=100&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
response = requests.get(url)

# carrega os dados existentes ou cria um novo
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        escolas_data = json.load(f)
else:
    escolas_data = []

# Create a dictionary for quick lookup
escolas_dict = {escola['escola']: escola for escola in escolas_data}

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Convertendo a resposta para JSON
    dados = response.json()

    # Acessando a lista de gazettes dentro dos dados
    gazettes = dados['gazettes']

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        # Acessando a data de cada gazette
        data = gazette['date']
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        data_formatada = data_obj.strftime("%d-%m-%Y")
        mes = get_month_name(data_obj)

        # Acessando a lista de excertos de cada gazette
        excertos = gazette['excerpts']

        # Iterando sobre cada excerto
        for excerto in excertos:
            # Função para processar os padrões
            def process_pattern(pattern, regex):
                if pattern in excerto:
                    linhas = excerto.strip().split('\n')
                    for linha in linhas[linhas.index(pattern) + 1:]:
                        matches = re.findall(regex, linha)
                        if matches:
                            for match in matches:
                                escola = match[0].strip()
                                total = match[-1].strip()
                                total_float = float(total.replace('.', '').replace(',', '.'))

                                if escola not in escolas_dict:
                                    escolas_dict[escola] = {"escola": escola, "dados": []}

                                escolas_dict[escola]["dados"].append({
                                    "data": data_formatada,
                                    "mes": mes,
                                    "valor": total_float
                                })


            # Processando os diferentes padrões
            process_pattern("Nº CRE/UE Capital Custeio Total",
                            r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)')
            process_pattern("Nº UE Custeio Total", r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)')
            process_pattern("Nº CRE / UE Capital Custeio Total",
                            r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)')

else:
    # Se a solicitação falhar, imprima o código de status
    print("Erro:", response.status_code)

# Converte o dicionario de volta para uma lista
output_data = list(escolas_dict.values())

# Salvando os dados em um arquivo JSON
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Arquivo JSON '{json_file_path}' foi atualizado com sucesso.")
