import re
import requests
import json
from datetime import datetime


# Function to get month name in Portuguese
def get_month_name(date):
    months = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return months[date.month - 1]


# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2024-01-01&published_until=2024-06-28&querystring=%22N%C2%BA%20UE%20Custeio%20Total%22%20%22N%C2%BA%20CRE%2FUE%20Capital%20Custeio%20Total%22&excerpt_size=50000&number_of_excerpts=100&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
)

# Dicionário para armazenar os dados das escolas
escolas_data = {}

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

                                if escola not in escolas_data:
                                    escolas_data[escola] = []

                                escolas_data[escola].append({
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

# Convertendo o dicionário para o formato de lista desejado
output_data = [{"escola": escola, "dados": dados} for escola, dados in escolas_data.items()]

# Salvando os dados em um arquivo JSON
with open('escolas_dados.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("Arquivo JSON 'escolas_dados.json' foi criado com sucesso.")