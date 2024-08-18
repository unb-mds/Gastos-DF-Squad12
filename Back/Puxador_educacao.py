import re
import requests
from typing import List, Dict, Union
from pydantic import BaseModel
from datetime import date

class DateRange(BaseModel):
    published_since: date
    published_until: date

async def puxador_educacao(date_range: DateRange) -> Union[List[Dict[str, Union[str, float]]], int]:
    # Formatando as datas no formato americano
    published_since_str = date_range.published_since.strftime('%Y-%m-%d')
    published_until_str = date_range.published_until.strftime('%Y-%m-%d')

    # Fazendo a solicitação GET para a API
    response = requests.get(
        f'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since={published_since_str}&published_until={published_until_str}&querystring=%22N%C2%BA%20UE%20Custeio%20Total%22%20%22N%C2%BA%20CRE%2FUE%20Capital%20Custeio%20Total%22&excerpt_size=50000&number_of_excerpts=100&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    )

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

            # Variável para armazenar o total gasto no dia
            total_gasto_dia = 0.0

            # Verificando se a data já foi impressa
            if data not in datas_vistas:
                # Adicionando a data ao conjunto de datas vistas
                datas_vistas.add(data)

            # Acessando a lista de excertos de cada gazette
            excertos = gazette['excerpts']

            # Iterando sobre cada excerto
            for excerto in excertos:
                # Verificando se o padrão específico "Nº CRE/UE Capital Custeio Total" está presente no excerto
                if "Nº CRE/UE Capital Custeio Total" in excerto:
                    # Dividindo o excerto por linhas
                    linhas = excerto.strip().split('\n')

                    # Iterando sobre as linhas a partir da linha do cabeçalho
                    for linha in linhas[linhas.index("Nº CRE/UE Capital Custeio Total") + 1:]:
                        # Aplicando a expressão regular para capturar os valores
                        matches = re.findall(r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)', linha)

                        if matches:
                            for match in matches:
                                escola = match[0].strip()
                                total = match[3].strip()

                                # Convertendo o valor total de texto para float
                                total = total.replace('.', '').replace(',', '.')
                                total_float = float(total)
                                
                                # Extraindo o nome do município do campo escola
                                municipio = escola.split('CRE')[-1].strip()

                                # Adicionando o valor total ao total gasto no dia
                                total_gasto_dia += total_float

                                # Adicionando o resultado à lista
                                results.append({
                                    "escola": escola,
                                    "municipio": municipio,
                                    "data": data,
                                    "total": total_float
                                })

                # Verificando se o padrão específico "Nº UE Custeio Total" está presente no excerto
                if "Nº UE Custeio Total" in excerto:
                    # Dividindo o excerto por linhas
                    linhas = excerto.strip().split('\n')

                    # Iterando sobre as linhas a partir da linha do cabeçalho
                    for linha in linhas[linhas.index("Nº UE Custeio Total") + 1:]:
                        # Aplicando a expressão regular para capturar os valores
                        matches = re.findall(r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)', linha)

                        if matches:
                            for match in matches:
                                escola = match[0].strip()
                                total = match[2].strip()

                                # Convertendo o valor total de texto para float
                                total = total.replace('.', '').replace(',', '.')
                                total_float = float(total)
                                
                                # Extraindo o nome do município do campo escola
                                municipio = escola.split('CRE')[-1].strip()

                                # Adicionando o valor total ao total gasto no dia
                                total_gasto_dia += total_float

                                # Adicionando o resultado à lista
                                results.append({
                                    "escola": escola,
                                    "municipio": municipio,
                                    "data": data,
                                    "total": total_float
                                })

                # Verificando o padrão específico "Nº CRE / UE Capital Custeio Total" no segundo formato
                if "Nº CRE / UE Capital Custeio Total" in excerto:
                    # Dividindo o excerto por linhas
                    linhas = excerto.strip().split('\n')

                    # Iterando sobre as linhas a partir da linha do cabeçalho
                    for linha in linhas[linhas.index("Nº CRE / UE Capital Custeio Total") + 1:]:
                        # Aplicando a expressão regular para capturar os valores
                        matches = re.findall(r'\d+\s+([\w\s]+?)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)\s+R\$\s*([\d,.]+)', linha)

                        if matches:
                            for match in matches:
                                escola = match[0].strip()
                                total = match[3].strip()

                                # Convertendo o valor total de texto para float
                                total = total.replace('.', '').replace(',', '.')
                                total_float = float(total)
                                
                                # Extraindo o nome do município do campo escola
                                municipio = escola.split('CRE')[-1].strip()

                                # Adicionando o valor total ao total gasto no dia
                                total_gasto_dia += total_float

                                # Adicionando o resultado à lista
                                results.append({
                                    "escola": escola,
                                    "municipio": municipio,
                                    "data": data,
                                    "total": total_float
                                })

        return results
    else:
        # Se a solicitação falhar, retorne o código de status
        return response.status_code
