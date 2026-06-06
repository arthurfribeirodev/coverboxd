# CoverBoxd

Plataforma web para descobrir, salvar e avaliar capas de álbuns musicais. O projeto foi desenvolvido como Trabalho Prático Semestral da disciplina **Arquitetura de Aplicações Web (2026.1)** e demonstra a construção de uma API REST, persistência de dados, documentação OpenAPI e consumo assíncrono no frontend.

---

## Sobre o projeto

O **CoverBoxd** é inspirado em plataformas de avaliação cultural (como o Letterboxd), mas focado em **capas de álbuns**. O usuário pode:

- Buscar álbuns na API do Spotify;
- Salvar álbuns no banco de dados da aplicação;
- Publicar reviews com nota (1 a 5) e comentário;
- Gerenciar sua conta (cadastro, login, atualização de perfil e exclusão).

O domínio possui **três entidades relacionadas**:

| Entidade | Descrição | Relacionamentos |
|----------|-----------|-----------------|
| **Users** | Usuários da plataforma | Autor das reviews |
| **Covers** | Álbuns/capas salvos | Recebem reviews |
| **Rates** | Reviews (nota + comentário) | Pertencem a um usuário e a uma capa |

---

## Stack tecnológica

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.10 + [FastAPI](https://fastapi.tiangolo.com/) |
| Banco de dados | SQLite com [SQLAlchemy](https://www.sqlalchemy.org/) |
| Migrações | [Alembic](https://alembic.sqlalchemy.org/) |
| Autenticação | JWT ([python-jose](https://python-jose.readthedocs.io/)) + hash Argon2 ([passlib](https://passlib.readthedocs.io/)) |
| Integração externa | [Spotipy](https://spotipy.readthedocs.io/) (API do Spotify) |
| Frontend | HTML + CSS + JavaScript (`fetch`) |
| Documentação da API | Swagger UI e ReDoc (gerados automaticamente pelo FastAPI) |

---

## Estrutura do repositório

```
coverboxd/
├── main.py              # Aplicação FastAPI, CORS e configuração global
├── models.py            # Modelos SQLAlchemy (Users, Covers, Rates)
├── schemas.py           # Schemas Pydantic para validação de entrada/saída
├── dependencies.py      # Sessão do banco e verificação de JWT
├── auth_routes.py       # Rotas de autenticação e usuário
├── albuns_routes.py     # Rotas de álbuns/capas
├── reviews_routes.py    # Rotas de reviews
├── spotify_service.py   # Integração com a API do Spotify
├── alembic/             # Migrações do banco de dados
├── alembic.ini
├── front/
│   └── index.html       # Interface web (SPA simples com navegação assíncrona)
├── requirements.txt     # Arquivo de Dependências
├── .env                 # Variáveis de ambiente (não versionar)
└── database.db          # Banco SQLite (gerado após migração)
```

---

## Pré-requisitos

Antes de executar o projeto, instale:

- **Python 3.10** ou superior
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório e manter histórico de commits)
- Conta no [Spotify for Developers](https://developer.spotify.com/) para obter credenciais da API

Opcional:

- **Live Server** (extensão do VS Code) ou outro servidor HTTP local para servir o frontend

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd coverboxd
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

O projeto possui `requirements.txt` na raiz.

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte formato (substitua pelos seus valores):

```env
# Autenticação JWT
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACESS_TOKEN_EXPIRE_MINUTES=30

# API do Spotify
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
```

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `SECRET_KEY` | Chave secreta para assinar tokens JWT | `minha-chave-super-secreta-123` |
| `ALGORITHM` | Algoritmo de assinatura do JWT | `HS256` |
| `ACESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do access token (minutos) | `30` |
| `SPOTIFY_CLIENT_ID` | Client ID do app no Spotify Developer | `abc123...` |
| `SPOTIFY_CLIENT_SECRET` | Client Secret do app no Spotify Developer | `xyz789...` |


### 5. Criar o banco de dados

Execute as migrações com o Alembic:

```bash
alembic upgrade head
```

Isso cria o arquivo `database.db` com as tabelas `users`, `covers` e `rates`.

---

## Como executar

### Backend (API)

Com o ambiente virtual ativado, na raiz do projeto:

```bash
uvicorn main:app --reload
```

A API ficará disponível em: **http://localhost:8000**

### Frontend

Abra o arquivo `front/index.html` em um navegador. Para evitar problemas de CORS em alguns cenários, recomenda-se servir a pasta `front/` com um servidor local:

```bash
# Exemplo com Python
cd front
python -m http.server 5500
```

Acesse: **http://localhost:5500**

> O frontend está configurado para consumir a API em `http://localhost:8000`. Certifique-se de que o backend esteja rodando antes de usar a interface.

---

## Documentação Swagger (OpenAPI)

O FastAPI gera a documentação automaticamente. Com o servidor em execução, acesse:

| Interface | URL |
|-----------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Schema OpenAPI (JSON)** | http://localhost:8000/openapi.json |

Na interface Swagger é possível testar todos os endpoints, visualizar parâmetros, corpos de requisição e exemplos de resposta. Para rotas protegidas, use o botão **Authorize** e informe o token no formato `Bearer <seu_token>`.

---

## API REST — Endpoints

### Autenticação (`/auth`)

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| `POST` | `/auth/register` | Cadastro de novo usuário | Não |
| `POST` | `/auth/login` | Login (retorna JWT) | Não |
| `POST` | `/auth/login-form` | Login via OAuth2 (compatível com Swagger) | Não |
| `GET` | `/auth/auth` | Valida token e retorna dados do usuário | Sim |
| `GET` | `/auth/refresh` | Renova o access token | Sim |
| `PATCH` | `/auth/` | Atualiza perfil do usuário logado | Sim |
| `DELETE` | `/auth/` | Remove conta do usuário logado | Sim |

**Exemplo de resposta do login:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "usuario",
  "pfp": null
}
```

### Álbuns (`/albuns`)

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| `GET` | `/albuns/` | Lista todos os álbuns salvos | Não |
| `GET` | `/albuns/search/{query}` | Busca álbuns no Spotify | Não |
| `POST` | `/albuns/` | Cadastra um álbum | Não |
| `PATCH` | `/albuns/{album_id}` | Atualiza um álbum | Não |
| `DELETE` | `/albuns/{album_id}` | Remove um álbum | Não |

### Reviews (`/reviews`)

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| `POST` | `/reviews/review` | Cria uma review | Sim |
| `GET` | `/reviews/review/{review_id}` | Busca review por ID | Não |
| `GET` | `/reviews/album/{cover_id}` | Lista reviews de um álbum | Não |
| `PATCH` | `/reviews/review/{review_id}` | Atualiza review (apenas o autor) | Sim |
| `DELETE` | `/reviews/review/{review_id}` | Remove review (apenas o autor) | Sim |

### Códigos de status HTTP utilizados

| Código | Situação |
|--------|----------|
| `200` | Requisição bem-sucedida |
| `201` | Recurso criado (quando aplicável) |
| `400` | Dados inválidos (ex.: email já cadastrado) |
| `401` | Token ausente ou inválido |
| `403` | Acesso negado (ex.: editar review de outro usuário) |
| `404` | Recurso não encontrado |
| `500` | Erro interno do servidor |

---

## Frontend — Navegação assíncrona

A interface em `front/index.html` consome a API via `fetch`, **sem recarregar a página**. As principais visões são:

1. **Home** — área inicial limpa;
2. **Busca** — digite no campo de pesquisa para buscar álbuns no Spotify e salvá-los;
3. **Álbuns** — lista os álbuns salvos no banco; ao clicar, abre o modal de reviews;
4. **Reviews** — exibe todas as reviews dos álbuns salvos, com opção de editar/apagar as próprias;
5. **Login / Sign Up** — modais para autenticação;
6. **Perfil** — atualização de nome, foto e exclusão de conta.

O token JWT é armazenado em `localStorage` e enviado no header `Authorization: Bearer <token>` nas requisições protegidas.

---

## Atendimento aos requisitos do trabalho prático

### Requisitos obrigatórios

| Requisito | Status | Observação |
|-----------|--------|------------|
| REST API com CRUD (2+ entidades) | Atendido | Entidades **Álbuns** e **Reviews**, com operações completas |
| Banco NoSQL | Exceção | Utiliza **SQLite** (SQL). Permitido pelo Professor |
| Documentação OpenAPI/Swagger | Atendido | Disponível em `/docs` e `/redoc` |
| README com instruções | Atendido | Este documento |
| Página web com navegação assíncrona | Atendido | `front/index.html` com `fetch` e atualização dinâmica do DOM |

## Fluxo de uso sugerido

1. Inicie o backend (`uvicorn main:app --reload`).
2. Acesse o frontend (`front/index.html`).
3. Crie uma conta em **Sign Up**.
4. Faça **Login** — o token será salvo automaticamente.
5. Use a **busca** para encontrar álbuns no Spotify.
6. Clique em um álbum para **salvá-lo** no banco.
7. Acesse **Álbuns** e clique em **Faça uma Review!** para avaliar.
8. Consulte **Reviews** para ver todas as avaliações publicadas.

---

## Segurança

- Senhas são armazenadas com hash **Argon2** (via `passlib`).
- Tokens JWT possuem tempo de expiração configurável via `.env`.
- Reviews só podem ser editadas ou excluídas pelo usuário que as criou.
- A `SECRET_KEY` e as credenciais do Spotify devem permanecer apenas no `.env`.

---

---

## Autores

Projeto desenvolvido para a disciplina **Arquitetura de Aplicações Web — 2026.1**.
