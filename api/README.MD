# Como rodar o ambiente do Web Scrapig

## Algumas informações

O Web Scraping é feita em `python` usando `fastapi` e esta rodando em um ambiente virtual python com suas dependências já instaladas.

## Como o Web Sracping funciona

Primeiro o nosso Web Scraping começa com o envio de uma requisição HTTP ao servidor onde o site está hospedado, no nosso caso é o (http://localhost:8001/).

Segundo, servidor responde com o código HTML da página. Esse código contém todo o conteúdo da página, como texto, links, imagens, e estrutura dos dados.

Terceiro, no momento que os elementos são identificados, os dados são extraídos e processados. Isso pode incluir a coleta de tabelas, listas, parágrafos ou qualquer outro elemento presente no HTML, sendo posteriormente processados para serem mostrados no nosso gráfico com os dados extraídos.

Quarto, nosso script poderá ser executado periodicamente para coletar dados novos ou atualizados automaticamente do Querido Diário.



O repositório principal do Gastos DF pode ser visualizado clicando <a href="https://github.com/unb-mds/Gastos-DF-Squad12">aqui</a>.

A documentação do projeto pode ser visualizada clicando <a href="https://unb-mds.github.io/2024-1-Gastos-DF-Doc-Squad12/">aqui</a>.

## Pré-requisitos

Ter o Python 3.12.3 ou superior instalado.

Ter o pip 24.0 ou superior instalado.

### No Windows

Tentei. Não roda, ativa o WSL ou instala um ubuntu e segue os passos do linux 👍

### No linux (ubuntu)

Dentro da pasta raiz do projeto `Gastos-DF-Squad12` execulte os seguintes comandos:

Para ativar o ambiente virtual do python execute:
```
source venv/bin/activate
```

Em seguida para abrir um servidor local e visualizar no seu navegador execute:
```
python3 api/main.py
```

Será aberto no endereço http://localhost:8001/

O seu docs estará no endereço http://localhost:8001/docs

Mais informações sobre o ambiente virtal python podem ser encontrado em https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

