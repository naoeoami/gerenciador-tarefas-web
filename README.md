# Gerenciador de Tarefas Web

Aplicação web para gerenciamento de tarefas em grupo, semelhante a um Trello simplificado. Desenvolvida em Python com Flask.

## Funcionalidades

- **Cadastro e autenticação de usuários**: registro, login e logout com sessão.
- **Gerenciamento de tarefas**: criar, visualizar, editar e excluir tarefas (título, descrição e status).
- **Atribuição de tarefas** a outros usuários cadastrados no sistema.
- **Status de tarefas**: Pendente, Em Andamento e Concluída, com filtro por status.
- **Dashboard do grupo**: visão geral de todas as tarefas de todos os usuários, com contadores por status.
- **Minhas Tarefas**: lista das tarefas criadas por ou atribuídas ao usuário logado.

## Tecnologias

- Python 3 + Flask
- Flask-SQLAlchemy (ORM) + SQLite
- Flask-Login (autenticação)
- Flask-WTF / WTForms (formulários e proteção CSRF)
- Bootstrap 5 (interface)
- Pytest (testes automatizados)

## Estrutura do projeto

```
gerenciador-tarefas-web/
├── app/
│   ├── auth/          # Blueprint de autenticação (login, registro, logout)
│   ├── tasks/          # Blueprint de tarefas (CRUD, status)
│   ├── main/           # Blueprint do dashboard
│   ├── templates/       # Templates Jinja2 (HTML)
│   ├── static/          # CSS
│   ├── models.py        # Modelos User e Task
│   └── forms.py         # Formulários (WTForms)
├── tests/               # Testes automatizados (pytest)
├── config.py             # Configurações da aplicação
├── run.py                # Ponto de entrada da aplicação
└── requirements.txt
```

## Instalação e uso

### 1. Pré-requisitos

- Python 3.10+ instalado

### 2. Clonar o repositório

```bash
git clone <url-do-seu-repositorio>
cd gerenciador-tarefas-web
```

### 3. Criar e ativar um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente (opcional)

Copie o arquivo de exemplo e ajuste se necessário:

```bash
cp .env.example .env
```

### 6. Executar a aplicação

```bash
python run.py
```

A aplicação ficará disponível em `http://127.0.0.1:5000`. O banco de dados SQLite (`instance/app.db`) é criado automaticamente na primeira execução.

### 7. Rodar os testes

```bash
pytest
```

## Como usar

1. Acesse a aplicação e clique em **Cadastrar** para criar uma conta.
2. Faça **login** com o e-mail e senha cadastrados.
3. Em **Nova Tarefa**, crie uma tarefa informando título, descrição, status e (opcionalmente) um usuário responsável.
4. Em **Minhas Tarefas**, acompanhe as tarefas que você criou ou que foram atribuídas a você, e filtre por status.
5. No **Dashboard**, veja todas as tarefas do grupo e os contadores por status.
6. Apenas o criador de uma tarefa pode editá-la ou excluí-la; o criador e o responsável podem atualizar o status diretamente pela lista.

## Licença

Projeto acadêmico, de uso livre.
