# Como rodar o ambiente da documentação

## Pré-requisitos

Tentei. Não roda, ativa o WSL ou instala um ubuntu e segue os passos do linux 👍

### No linux (ubuntu)

Para ativar o ambiente virtual do python execute:
```
source venv/bin/activate
```

Em seguida para abrir um servidor local e visualizar no seu navegador execute:
```
mkdocs serve
```

Será aberto no endereço http://localhost:8000/

Caso tenha problemas para subir o servidor local execute:
```
pip3 install --upgrade mkdocs mkdocs-material
```

Mais informações sobre o ambiente virtal python podem ser encontrado em https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/


