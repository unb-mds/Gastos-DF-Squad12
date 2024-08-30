from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re
import json
from datetime import datetime, timedelta
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def fetch_and_process_data(start_date, end_date):
    # Fazendo a solicitação GET para a API
    url = f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={start_date}&published_until={end_date}&querystring=%22cujo%20objeto%20%C3%A9%20a%20aquisi%C3%A7%C3%A3o%20do%20item%20identificado%20pelo%20C%C3%B3digo%22&excerpt_size=3000&number_of_excerpts=10000&pre_tags=&post_tags=&size=10000&sort_by=ascending_date'
    response = requests.get(url)

    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        dados = response.json()

        # Acessando a lista de gazettes dentro dos dados
        gazettes = dados['gazettes']

        # Dicionário para armazenar os dados organizados por data
        dados_por_data = {}

        # Iterando sobre cada gazette na lista
        for gazette in gazettes:
            # Acessando a data de cada gazette
            data = gazette['date']

            # Inicializa a lista de itens para a data, caso não exista
            if data not in dados_por_data:
                dados_por_data[data] = []

            # Acessando a lista de excertos de cada gazette
            excertos = gazette['excerpts']
            total_diario = 0
            excerto_relevante_encontrado = False

            # Iterando sobre cada excerto
            for excerto in excertos:
                # Remover quebras de linha no meio das palavras e espaços extras
                excerto = re.sub(r'(\w)-\n(\w)', r'\1\2', excerto)
                excerto = excerto.replace('\n', ' ').strip()

                # Usando expressão regular para encontrar a Empresa, Objeto e Valor
                empresa_match = re.search(r'empresa\s+([\w\s\-ÇçÉéÁáÍíÓóÚúÃãÕõâêîôûÂÊÎÔÛäëïöüÄËÏÖÜ]+)\s*-\s*CNPJ:\s*(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', excerto, re.DOTALL | re.IGNORECASE)
                objeto_match = re.search(r'cujo\s+objeto\s+é\s+a\s+aquisição\s+do\s+item\s+identificado\s+pelo\s+Código\s+SES\s+\d+\s*-\s*([^\n,]+)', excerto, re.DOTALL | re.IGNORECASE)
                valor_match = re.search(r'valor\s+global\s+de\s+R\$\s*([\d.,]+)', excerto, re.IGNORECASE)

                if empresa_match and objeto_match and valor_match:
                    excerto_relevante_encontrado = True
                    # Extraindo a empresa e o CNPJ encontrados
                    empresa = empresa_match.group(1).strip()
                    cnpj = empresa_match.group(2).strip()

                    # Extraindo o objeto encontrado e removendo parte desnecessária
                    objeto = objeto_match.group(1).strip()
                    objeto = re.sub(r',\s*para\s+atender\s+as\s+necessidades.*', '', objeto, flags=re.IGNORECASE)

                    # Extraindo o valor encontrado
                    valor = valor_match.group(1).strip()
                    # Removendo caracteres não numéricos, exceto vírgulas e pontos
                    valor_limpo = re.sub(r'[^\d,]', '', valor)
                    # Trocando a vírgula por ponto para ter o formato correto para float
                    valor_limpo = valor_limpo.replace(',', '.')
                    # Convertendo o valor para float
                    valor_float = float(valor_limpo)
                    total_diario += valor_float

                    # Adiciona os dados ao dicionário por data
                    dados_por_data[data].append({
                        "Empresa": empresa,
                        "CNPJ": cnpj,
                        "Objeto": objeto,
                        "Valor": f"R${valor_float:.2f}"
                    })

            if excerto_relevante_encontrado:
                print(f'Data: {data}, Dívidas totais = R${total_diario:.2f}')
            else:
                # Remove a data se não houver excertos relevantes
                dados_por_data.pop(data, None)

        return dados_por_data
    else:
        # Se a solicitação falhar, imprima o código de status
        print("Erro:", response.status_code)
        return None

# Caminho para o arquivo JSON
json_path = "../../resultado_compras.json"

# pega o dia de hoje e de 30 dias atras
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# captura nova informaçao
new_data = fetch_and_process_data(start_date, end_date)

if new_data:
    # Carrega os dados existentes, se houver
    try:
        with open(json_path, "r", encoding='utf-8') as arquivo_json:
            dados_existentes = json.load(arquivo_json)
    except FileNotFoundError:
        dados_existentes = {}

    # Adiciona os novos dados aos existentes
    for data, itens in new_data.items():
        if data in dados_existentes:
            dados_existentes[data].extend(itens)
        else:
            dados_existentes[data] = itens

    # Salva todos os dados coletados em um arquivo JSON
    with open(json_path, "w", encoding='utf-8') as arquivo_json:
        json.dump(dados_existentes, arquivo_json, ensure_ascii=False, indent=4)

    print(f"Dados atualizados salvos em '{json_path}'")
else:
    print("Nenhum dado novo para adicionar.")
