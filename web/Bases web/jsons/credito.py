import requests
import re
import json
from collections import defaultdict

def process_gazettes():
    # Fazendo a solicitação GET para a API
    response = requests.get(
        'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2020-01-01&published_until=2024-08-21&querystring=%22Abre%20cr%C3%A9dito%20suplementar%22&excerpt_size=120&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    )

    if response.status_code != 200:
        print(f"Erro na solicitação: {response.status_code}")
        return

    # Convertendo a resposta para JSON
    dados = response.json()
    gazettes = dados.get('gazettes', [])

    # Estrutura para armazenar dados
    resultados = defaultdict(lambda: {"url": "", "total_gasto_dia": 0.0, "decretos": []})

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        data = gazette.get('date')
        url = gazette.get('url')
        excertos = gazette.get('excerpts', [])

        # Verificando se a data já foi registrada
        if resultados[data]["url"] == "":
            resultados[data]["url"] = url

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

                # Adicionando ao resultado
                resultados[data]["total_gasto_dia"] += valor_float
                resultados[data]["decretos"].append({"decreto": decreto, "valor": valor_float})

    # Convertendo o resultado para o formato JSON esperado
    resultado_final = [
        {
            "date": data,
            "url": info["url"],
            "total_gasto_dia": info["total_gasto_dia"],
            "decretos": info["decretos"]
        }
        for data, info in resultados.items()
    ]

    # Salvando o resultado em um arquivo JSON
    with open('gazettes_data.json', 'w', encoding='utf-8') as f:
        json.dump({"resultados": resultado_final}, f, ensure_ascii=False, indent=4)

    print("Arquivo JSON 'gazettes_data.json' gerado com sucesso.")

if __name__ == "__main__":
    process_gazettes()
