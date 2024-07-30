# Gerenciador de tarefas (to do)

Nessa aplicação fiz implementações, simples, com fastapi, docker, etc para cria uma api rest full que tem o intuito de gerenciar tarefas. 
As tecnologias usadas foram todas listadas no arquivo **pyproject.toml**, mas irei lista-las a baixo:
- python = "^3.11"
- fastapi-utils = "^0.7.0"
- factory-boy = "^3.3.0"
- freezegun = "^1.5.1"
- testcontainers = "^4.7.2"
- fastapi = "^0.111.1"
- pydantic = "^2.8.2"
- sqlalchemy = "^2.0.31"
- pwdlib = {extras = ["argon2"], version = "^0.2.0"}
- pytest = "^8.3.2"
- pytest-cov = "^5.0.0"
- ruff = "^0.5.5"
- pyjwt = "^2.8.0"
- pydantic-settings = "^2.3.4"
- alembic = "^1.13.2"
- fastapi-utils = "^0.7.0"
- psycopg = "^3.2.1"
- fastapi-redis-cache = "^0.2.5"

## Preparo da maquina
A api foi pensada justamente para ser escalonável, de fácil entendimento e utilizade.
Segue a baixo as orientações para rodar em maquina:
- Ao obter os códigos ative a venv já embutida;
- Verifique se na sua maquina já tem o database **postgresql**
- Execute o comando `fastapi dev gnc_todo/main.py`

## Como consulmir a api
A Api tem 3 rotas nas quais voçê podera usufruir:
- */auth* rota competete pela autenticação e entrega do token na qual o usuario usará para fazer os outros requests;
- */users* rota para requerimentos que compete ao usuario;
- */todo* rota responsavel pelas requests das tarefas do usuario

Vale lembrar tambem que o usuario terá mais acessibilidade e flexibilidade usando as rotas tradicionais do fastapi: */docs* e */redoc*

### Algumas ressalvas sobre a api
A api usa da tecnologia de implementação de test com a ajuda da biblioteca Pytest, para utilizar dos testes use o comando `pytest -vv`
A aplicação também usa de memoria cache, com o **Redis**, para entregar com mais agilidade a resposta para o usuário.
