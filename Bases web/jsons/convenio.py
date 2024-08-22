import requests
import re
import json
from collections import defaultdict


def process_gazettes():
    # Fazendo a solicitação GET para a API
    response = requests.get(
        'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2020-01-01&published_until=2024-08-21&querystring=%22RECONHECIMENTO%20DE%20D%C3%8DVIDA%22&excerpt_size=500&number_of_excerpts=100000&pre_tags=&post_tags=&size=10000&sort_by=descending_date'
    )

    if response.status_code != 200:
        print(f"Erro na solicitação: {response.status_code}")
        return

    # Convertendo a resposta para JSON
    dados = response.json()
    gazettes = dados.get('gazettes', [])

    # Estrutura para armazenar dados
    resultados = defaultdict(lambda: {"decretos": []})

    # Iterando sobre cada gazette na lista
    for gazette in gazettes:
        data = gazette.get('date')
        if not data:
            continue

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

                # Adicionando ao resultado
                resultados[data]["decretos"].append({"interessado": interessado, "valor": valor_float})
                total_diario += valor_float

        if total_diario > 0:  # Ignorando datas com total 0
            resultados[data]["total_diario"] = total_diario

    # Convertendo o resultado para o formato JSON esperado, ignorando datas com total igual a 0
    resultado_final = [
        {
            "date": data,
            "total_gasto_dia": info["total_diario"],
            "decretos": info["decretos"]
        }
        for data, info in resultados.items()
        if "total_diario" in info and info["total_diario"] > 0
    ]

    # Salvando o resultado em um arquivo JSON
    with open('gazettes_data.json', 'w', encoding='utf-8') as f:
        json.dump({"resultados": resultado_final}, f, ensure_ascii=False, indent=4)

    print("Arquivo JSON 'gazettes_data.json' gerado com sucesso.")


if __name__ == "__main__":
    process_gazettes()
