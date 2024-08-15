import requests
import re

# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2023-06-26&published_until=2023-06-30&querystring=%22RECONHECIMENTO%20DE%20D%C3%8DVIDA%22&excerpt_size=500&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    dados = response.json()
    gazettes = dados.get('gazettes', [])

    datas_vistas = set()

    for gazette in gazettes:
        data = gazette.get('date')

        # Verifica se a data está presente e não é uma string vazia
        if data and data not in datas_vistas:
            print("\nData:", data)
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
                    except ValueError:
                        print(f"Erro ao converter o valor '{valor_limpo}' para float.")
                        valor_float = 0.0

                    total_diario += valor_float

                    print(f"Interessado: {interessado}\nValor: R${valor_float:.2f}")

            print(f'Dívidas totais = R${total_diario:.2f}')
else:
    print("Erro:", response.status_code)
