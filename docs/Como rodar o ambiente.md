# Como rodar os ambientes



## Como rodar o Front-end

ainda será adicionado

## Como rodar o API

ainda será adicionado

## Como rodar o Back-end

<h1>Como utilizar o WebScrapper com a API do Querido diário</h1>


Os WebScrapper são progamas em python que filtram os dados recebidos através da API do Querido diário



### Requisitos:
+ Python 3.10 ou superior
+ Requests
+ Re

A API pode ser acessada por este [link](https://queridodiario.ok.org.br/api/docs#/)

### Configurando a API
Primeiro é nescessario ditar os parâmetros na opção de gazetas:
+ ID do município que deseja realizar a busca
+ Intervalo de tempo em que deseja buscar
+ String que deseja
+ o numero de caractéres que irá retornar
+ Numero maximo de resultados
+ Numero maximo de resultaods por gazeta retornada
+ Ordenar a Data
![image](https://github.com/user-attachments/assets/74b48bc4-5ba7-49fd-97c3-1593f1bf837f)


Ao executar a APi ela retornará o seguinte link
![image](https://github.com/user-attachments/assets/ebde8164-2ee5-4fb0-8aa6-14b82f64397b)

Este link retorna um ou varios Json de acordo com os parâmetros buscados
Temos:
+ O total de gazetas
+ Id do territorio
+ Data
+ Data em que foi processado
+ URL do diario em PDF
+ Nome do territorio
+ Sigla do estado
+ A string que foi buscada dentro de um excerpt
+ verifica se o diario é uma versão extra-oficial
+ link para o diario oficial em txt
![image](https://github.com/user-attachments/assets/bfbb22ea-9022-4aa9-a624-abbf30eeeffc)


### Utilizando o progama em python

usarei de exemplo o codigo do puxador de verbas de escola

Como parametro de query coloquei "Nº CRE/UE Capital Total" pois é assim que aparecem as verbas de escola no arquivo .txt
![image](https://github.com/user-attachments/assets/517990ca-08ec-49fb-a65a-836e708e3e53)


Utilizando a biblioteca Requests, colocando o link com o comando Request.get(link)
~~~Python
# Fazendo a solicitação GET para a API
response = requests.get(
    'https://queridodiario.ok.org.br/api/gazettes?territory_ids=5300108&published_since=2024-01-01&published_until=2024-06-28&querystring=%22N%C2%BA%20UE%20Custeio%20Total%22%20%22N%C2%BA%20CRE%2FUE%20Capital%20Custeio%20Total%22&excerpt_size=5000&number_of_excerpts=1000&pre_tags=&post_tags=&size=10000&sort_by=descending_date')
~~~

Apos isso o resultado é tratado e reorganizado para que valores moneterios utilizem "." ao invez de "," para que sejam tratados em python

~~~Python
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
~~~~
Por fim, e esta parte difere de outros puxadores, esta em especifico serve para verificar a grafia dos textos, ignorar coisas como "\n" e conferir a expressão regular pesquisada para em fim printar o resultado

~~~python
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
~~~

Exemplo de Resultado obtido:


![image](https://github.com/user-attachments/assets/c5d30a91-3853-439c-b8ed-a58ba6ca18c9)
