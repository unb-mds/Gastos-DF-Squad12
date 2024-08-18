from fastapi import FastAPI
import requests
import re
from typing import List, Dict, Union
from pydantic import BaseModel
from datetime import date

class DateRange(BaseModel):
    published_since: date
    published_until: date

async def puxador_credito(date_range: DateRange) -> Union[List[Dict[str, Union[str, float]]], int]:
    # Formatando as datas no formato americano
    published_since_str = date_range.published_since.strftime('%Y-%m-%d')
    published_until_str = date_range.published_until.strftime('%Y-%m-%d')

    # Fazendo a solicitação GET para a API
    response = requests.get(
        f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={published_since_str}&published_until={published_until_str}&querystring=%22Abre%20cr%C3%A9dito%20suplementar%22&excerpt_size=120&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date')

    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        dados = response.json()

        # Acessando a lista de gazettes dentro dos dados
        gazettes = dados['gazettes']
        
        # Lista para armazenar os dicionários com as informações extraídas
        results = []

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
                    
                    results.append({
                        "data": data,
                        "decreto": decreto,
                        "valor": valor_float
                    })
                    
                    
        return results
    else:
        # Se a solicitação falhar, retorne o código de status
        return response.status_code
