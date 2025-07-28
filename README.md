Sistema de Gestão da Federação de Futebol (CBF)

Este projeto é um sistema de gestão completo para uma federação de futebol, construído com um backend Flask (Python), um frontend Vue.js e um banco de dados MySQL, tudo orquestrado com Docker.

Funcionalidades

    Gestão de Entidades: CRUD completo para as principais entidades de uma federação:

        Jogadores

        Equipas

        Contratos

        Competições

        Árbitros

        Partidas

    Recursos Avançados de Banco de Dados: Utilização de Stored Procedures, Views, Triggers e Funções para garantir a integridade e a eficiência dos dados.

    Ambiente Containerizado: A aplicação é totalmente executada em contentores Docker, garantindo um ambiente de desenvolvimento e teste consistente e fácil de configurar.

Tecnologias Utilizadas

Backend

    Framework: Flask

    ORM: SQLAlchemy

    Banco de Dados: MySQL 8.0

    Linguagem: Python 3.9

Frontend

    Framework: Vue.js 2

    UI Framework: Vuetify

    Servidor Web: Nginx

Ambiente

    Orquestração: Docker Compose

Pré-requisitos

Para executar este projeto, precisa de ter instalados na sua máquina:

    Docker

    Docker Compose

Como Executar

Siga os passos abaixo para colocar toda a aplicação a funcionar.

1. Clone o Repositório
Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>

2. Inicie a Aplicação com Docker Compose

No terminal, a partir da raiz do projeto (onde o ficheiro docker-compose.yml se encontra), execute o seguinte comando:
Bash

docker-compose up --build

    O comando irá construir as imagens Docker para o frontend e o backend, descarregar a imagem do MySQL e iniciar os três contentores.

    Na primeira vez, este processo pode demorar alguns minutos.

3. Aceda à Aplicação

Após os contentores estarem a ser executados, os serviços estarão disponíveis nos seguintes endereços:

    Frontend (Aplicação Web): http://localhost:8080

    Backend (API): http://localhost:5000

4. Acesso ao Banco de Dados

Se precisar de aceder diretamente ao banco de dados MySQL (por exemplo, com o DBeaver, MySQL Workbench ou outro cliente SQL), utilize as seguintes credenciais:

    Host: localhost

    Porta: 3307

    Utilizador: root

    Senha: root

    Base de Dados: cbf

Estrutura do Projeto

.
├── app/                  # Contém toda a lógica do backend Flask (models, routes)
├── database/             # Scripts SQL para inicialização do banco de dados
├── frontend/cbf-front/   # Código-fonte da aplicação Vue.js
├── .gitignore            # Ficheiros e pastas a serem ignorados pelo Git
├── docker-compose.yml    # Ficheiro de orquestração dos contentores
├── Dockerfile            # Define a imagem Docker para o backend
├── requirements.txt      # Dependências Python do backend
└── run.py                # Ponto de entrada para iniciar a aplicação Flask

Endpoints da API

A API expõe os seguintes endpoints principais para gestão das entidades:

    /jogadores

    /equipes

    /contratos

    /competicoes

    /arbitros

    /partidas

    /escalacoes

    /arbitragem

    /eventos