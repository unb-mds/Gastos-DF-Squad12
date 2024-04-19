from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re

# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5208707&published_since=2023-01-01&published_until=2023-12-31&querystring=%22valor%20de%20R%24%20%22&excerpt_size=50&number_of_excerpts=500&pre_tags=&post_tags=&size=1100&sort_by=ascending_date')

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Convertendo a resposta para JSON
    dados = response.json()

    # Acessando a lista de gazettes dentro dos dados
    gazettes = dados['gazettes']

    # Conjunto para armazenar as datas já vistas
    datas_vistas = set()

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        # Acessando a data de cada gazette
        data = gazette['date']

        # Verificando se a data já foi impressa
        if data not in datas_vistas:
            print("\nData:", data)
            # Adicionando a data ao conjunto de datas vistas
            datas_vistas.add(data)

            # Inicializando o total do dia
            total_do_dia = 0

        # Acessando a lista de excertos de cada gazette
        excertos = gazette['excerpts']

        # Iterando sobre cada excerto
        for excerto in excertos:
            # Usando expressão regular para encontrar o trecho desejado
            match = re.search(r'no valor de (.*?,.{2})', excerto)
            if match:
                # Extraindo o valor encontrado e limpando o formato
                valor = match.group(1)
                # Removendo caracteres não numéricos e substituindo vírgulas por ponto
                valor_limpo = re.sub(r'[^\d,]', '', valor).replace(',', '.')
                # Removendo pontos extras como separadores de milhar
                valor_limpo = valor_limpo.replace('.', '')
                # Convertendo o valor para float e incrementando o total do dia
                total_do_dia += float(valor_limpo)
                print("Valor:", valor)

        # Imprimindo o total dos valores para esta data
        if len(excertos) > 0:
            print("Total:", total_do_dia/100)
else:
    # Se a solicitação falhar, imprima o código de status
    print("Erro:", response.status_code)
