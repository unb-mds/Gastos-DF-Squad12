import requests
import re

from typing import List, Dict, Union
from pydantic import BaseModel
from datetime import date

class DateRange(BaseModel):
    published_since: date
    published_until: date

async def puxador_bens1(date_range: DateRange) -> Union[List[Dict[str, Union[str, float]]], int]:
    # Formatando as datas no formato americano
    published_since_str = date_range.published_since.strftime('%Y-%m-%d')
    published_until_str = date_range.published_until.strftime('%Y-%m-%d')

    # Fazendo a solicitação GET para a API
    response = requests.get(
        F'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2023-06-26&published_until=2023-06-30&querystring=%22RECONHECIMENTO%20DE%20D%C3%8DVIDA%22&excerpt_size=500&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    )

    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        dados = response.json()
        gazettes = dados.get('gazettes', [])
        
        # Lista para armazenar os dicionários com as informações extraídas
        results = []

        datas_vistas = set()

        for gazette in gazettes:
            data = gazette.get('date')

            # Verifica se a data está presente e não é uma string vazia
            if data and data not in datas_vistas:
                datas_vistas.add(data)

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
                        valor_limpo = re.sub(r'[^\d,]', '',
                                             valor)  # Remove todos os caracteres não numéricos, exceto vírgula
                        valor_limpo = valor_limpo.replace('.', '', valor_limpo.count(
                            ',') - 1)  # Remove pontos de milhar, mantém apenas o último
                        valor_limpo = valor_limpo.replace(',', '.')  # Substitui vírgula por ponto decimal
                            
                        try:
                            valor_float = float(valor_limpo)
                            total_diario += valor_float
                            erro = False
                        except ValueError:
                            valor_float = None
                            erro = True
                        
                        # Adiciona os dados à lista de resultados e agora ele informa se hove erro e passa o valor_limpo sem conversão de float.
                        results.append({
                            'data': data,
                            'interessado': interessado,
                            'valor': valor_float,
                            'valor_limpo': valor_limpo,
                            'erro': erro
                        })
                        # não adicionei o total diario mas ele pode ser facilmente implementado aqui ou no front.
                        
        return results
    else:
        # Se a solicitação falhar, retorne o código de status
        return response.status_code
