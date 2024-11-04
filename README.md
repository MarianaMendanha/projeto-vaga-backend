# ACMEVita API

Este projeto é uma API desenvolvida em Python utilizando Flask para gerenciar departamentos e colaboradores da ACMEVita. O projeto inclui funcionalidades para consulta e registro de dados, além de documentação em Swagger e testes unitários Pytest.

## Funcionalidades

- **GET /departamentos:** Consulta todos os departamentos da ACMEVita.
- **GET /departamentos/{id}/colaboradores:** Consulta todos os colaboradores de um departamento específico.
- **POST /departamentos:** Adiciona um novo departamento à ACMEVita.
- **POST /departamentos/{id}/colaboradores:** Adiciona um novo colaborador a um departamento específico.

## Documentação

A documentação da API está disponível no Swagger. Para acessar, inicie a aplicação e acesse a URL `http://127.0.0.1:5000/apidocs` no seu navegador.

## Testes Unitários

O projeto inclui testes unitários utilizando pytest. Os testes realizados são:

1. **test_conf.py**
   - Verifica a configuração da aplicação e se o banco de dados está acessível.
2. **test_routes.py**
   - Testa as rotas da API para garantir que os endpoints estão retornando as respostas corretas e no formato esperado.
   - Inclui testes para as funcionalidades GET e POST.

Para executar os testes, siga as instruções abaixo:

1. **Instale as dependências necessárias:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Execute os testes na raíz do projeto:**
   ```bash
   pytest -v
   ```

Os resultados dos testes serão exibidos no terminal.

## Setup

Para rodar a API localmente, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/MarianaMendanha/projeto-vaga-backend.git
   cd seu_repositorio
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie a aplicação:**
   ```bash
   python run.py
   ```

A API estará disponível em `http://127.0.0.1:5000`.

## Organização do Diretório

```
C:.
│   README.md                 # Documentação do projeto
│   requirements.txt          # Dependências do projeto
│   run.py                    # Arquivo principal para iniciar a aplicação
│
├───app
│   │   config.py             # Configurações da aplicação
│   │   models.py             # Modelos de dados e definições do banco de dados
│   │   routes.py             # Definição das rotas da API
│   │   schemas.py            # Definições de esquemas para validação de dados
│   │   __init__.py           # Inicializa o pacote da aplicação
│   │
│   ├───docs                  # Documentação das rotas em formato YAML
│   │       get_collaborators.yml  # Documentação para a rota GET colaboradores
│   │       get_departments.yml     # Documentação para a rota GET departamentos
│   │       post_collaborator.yml    # Documentação para a rota POST colaborador
│   │       post_department.yml      # Documentação para a rota POST departamento
│   │
│   └───templates             # Arquivos de template HTML
│           index.html         # Template principal da aplicação
│
├───instance                  # Arquivos específicos da instância
│       app.db                # Banco de dados SQLite
│       config.py             # Configuração específica da instância
│
├───migrations                # Scripts de migração de banco de dados
└───tests                     # Testes unitários
        conftest.py           # Configurações e fixtures para os testes
        test_conf.py          # Testes de configuração da aplicação
        test_routes.py         # Testes das rotas da API
        __init__.py           # Inicializa o pacote de testes

```
