from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re

# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2024-04-01&published_until=2024-06-01&querystring=%22Abre%20cr%C3%A9dito%20suplementar%22&excerpt_size=120&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date')

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
        # url para o pdf do diario oficial
        url = gazette['url']

        # Verificando se a data já foi impressa
        if data not in datas_vistas:
            print("\nData:", data)
            print("Diario oficial:", url)
            # Adicionando a data ao conjunto de datas vistas
            datas_vistas.add(data)

        # Acessando a lista de excertos de cada gazette
        excertos = gazette['excerpts']


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

                print(f"Decreto: {decreto}, Valor: R${valor_float:.2f}")

else:
    # Se a solicitação falhar, imprima o código de status
    print("Erro:", response.status_code)
