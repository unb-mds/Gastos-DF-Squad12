# Arquitetura

## Visão Geral

A arquitetura do sistema é composta por "colocar aqui": o [backend](link das apis) e o [frontend](link do nosso site). O backend é responsável por fornecer uma API REST que apresenta as seguintes funcionalidades:

Explicar as funcionalidades da api

O frontend é responsável por consumir a API REST e apresentar as informações para o usuário final. O fluxo da aplicação se dá da seguinte forma:

1. O usuário acessa o site do [SaúdeDF](link do site)
2. a sequencia do usuario

## Design do Sistema

O design do sistema foi feito utilizando a ferramenta [Figma](https://www.figma.com) e comporta-se da seguinte forma:

1. O usuário acessa o site do [SaúdeDF](link do site) e é apresentado com a tela de login
2. explicar sequencia

### Lógica do WebScraping

Para nossa aplicação gerenciar as disciplinas e horários disponíveis, foi necessário fazer um _web scraping_ no site da [UnB](link do site caso necessário o scraping) para obter as informações necessárias e não gerar um overload de requisições no site da universidade.

Após a obtenção dos dados, foi feito um tratamento para que as informações ficassem mais legíveis e organizadas para o usuário final, cadastrando-as no Banco de Dados PostgreSQL que é gerenciado pela API colocar api.

As requisições de web scraping ainda não são feitas de forma automática, mas sim pela equipe de desenvolvimento, assim tentamos executar o _web scraping_ a cada 24h para manter as informações atualizadas.

- Para execução do _web scraping_ de forma total é necessário executar o comando `make updatedb-all` no servidor da Heroku.

<div style="text-align:center;">
  <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="link do figma da arquitetura" allowfullscreen></iframe>
</div>

### Lógica da criação dos gráficos

explicar aqui

## Tecnologias Utilizadas

### Backend

- [Python](https://www.python.org)

### Frontend

colocar aqui