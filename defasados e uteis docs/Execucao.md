---
hide:
  - navigation
---

# Como executar o projeto?

## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/Saude-DF-Squad12.git
```

### 📋 Pré-requisitos

Para rodar o projeto, você precisa instalar as dependências globais, que são:

- GNU Make 4.3 (ou superior)
- Python v3.11.6 e Pip v22.0.2 (ou superior)

### 💻 Ambiente

Para configurar o ambiente, você pode rodar o seguinte script:

```bash
make config
```

### 📁 Dependências do projeto

Para instalar as dependências do projeto, você pode rodar os seguintes comando:

```bash
# Crie um ambiente virtual Python
python3 -m venv api/env

# Ative o ambiente virtual
source api/env/bin/activate

# Instale os pacotes do Python
make install
```

### 💾 Execução

Para executar o projeto, você pode rodar o seguinte comando:

```bash
docker compose up
```

#### Observações do Docker

```bash
# Se você quiser rodar em segundo plano
docker compose up -d

# Se alterações foram feitas no Dockerfile ou no docker-compose.yml
docker compose up --build

# Se for necessário deletar os volumes
docker compose down -v
```

### 🖱️ Acesso aos serviços

| Serviço  |                      URL                       |
| :------- | :--------------------------------------------: |
| Frontend | [http://localhost:3000](http://localhost:3000) |
| Backend  | [http://localhost:8000](http://localhost:8000) |

### 📍 Migrations

Migration é um recurso do Django que permite que você altere o modelo de dados do seu projeto. Portanto, sempre que você alterar o modelo de dados, você deve criar uma nova migration.

Para criar possíveis novas migrations, você pode rodar o seguinte comando:

```bash
# Crie as migrations
make makemigrations

# Execute as migrations
make migrate
```
