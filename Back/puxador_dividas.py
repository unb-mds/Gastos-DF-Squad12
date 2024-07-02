from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re

# Fazendo a solicitação GET para a API, neste caso de teste é de 29/05/2023 ate 29/05/2024
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2023-05-09&published_until=2024-05-29&querystring=RECONHECIMENTO%20DE%20D%C3%8DVIDA&excerpt_size=500&number_of_excerpts=100000&pre_tags=&post_tags=&size=1000&sort_by=descending_date')

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

        # Acessando a lista de excertos de cada gazette
        excertos = gazette['excerpts']
        total_diario = 0

        # Iterando sobre cada excerto
        for excerto in excertos:
            # Usando expressão regular para encontrar o Interessado e Valor
            interessado_match = re.search(r'Interessado:\s*([^,]+(?:\s*[^,]+)*)', excerto, re.DOTALL)
            valor_match = re.search(r'Valor:\s*R\$(.*?[\d,.]+)', excerto)

            if interessado_match and valor_match:
                # Extraindo o interessado encontrado
                interessado = interessado_match.group(1).strip().replace('\n', ' ')

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
                total_diario += float(valor_limpo)


                print(f"Interessado: {interessado}\nValor: R${valor_float:.2f}")
        print(f'Dívidas totais = R${total_diario:.2f}')
else:
    # Se a solicitação falhar, imprima o código de status
    print("Erro:", response.status_code)
