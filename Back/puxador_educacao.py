import re
import requests

# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2024-01-01&published_until=2024-06-28&querystring=%22N%C2%BA%20UE%20Custeio%20Total%22%20%22N%C2%BA%20CRE%2FUE%20Capital%20Custeio%20Total%22&excerpt_size=5000&number_of_excerpts=1000&pre_tags=&post_tags=&size=10000&sort_by=descending_date')

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

        # Variável para armazenar o total gasto no dia
        total_gasto_dia = 0.0

        # Verificando se a data já foi impressa
        if data not in datas_vistas:
            print("\nData:", data)
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

                            # Adicionando o valor total ao total gasto no dia
                            total_gasto_dia += total_float

                            print(f"{escola}\nTotal: R${total_float:.2f}")

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

                            # Adicionando o valor total ao total gasto no dia
                            total_gasto_dia += total_float

                            print(f"{escola}\nTotal: R${total_float:.2f}")

        # Imprimindo o total gasto no dia
        print(f"\nTotal gasto no dia {data}: R${total_gasto_dia:.2f}")

else:
    # Se a solicitação falhar, imprima o código de status
    print("Erro:", response.status_code)
