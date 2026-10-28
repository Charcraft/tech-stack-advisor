# Python FastAPI Production Template

Plantilla lista para producción para APIs en Python. Incluye: FastAPI, SQLAlchemy 2.0, Pydantic v2, Alembic, pytest, Docker, CI/CD.

## 🚀 Inicio Rápido

```bash
git clone https://github.com/Charcraft/tech-stack-advisor/templates/python my-api
cd my-api

cp .env.example .env
# Edita .env (DATABASE_URL, SECRET_KEY, etc.)

make docker-up          # Postgres + Redis
make migrate            # Alembic migrations
make dev                # uvicorn con hot-reload (watchfiles)
# → http://localhost:8000/docs (Swagger UI)
# → http://localhost:8000/healthz
```

## ✅ Validación

```bash
make validate
# fmt (ruff) → lint (ruff + mypy) → test (pytest + coverage) → build (docker)
```

## 📁 Estructura

```
.
├── app/
│   ├── main.py              # FastAPI app + lifespan
│   ├── core/                # Config, security, database
│   ├── api/v1/              # Routers, dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas (request/response)
│   ├── services/            # Business logic
│   └── repositories/        # Data access
├── migrations/              # Alembic
├── tests/                   # pytest (unit + integration)
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml           # ruff, mypy, pytest, coverage config
├── requirements.txt         # Locked deps (uv pip compile)
└── .github/workflows/ci.yml
```

## 🛠 Stack

| Capa | Tecnología |
|------|------------|
| Framework | **FastAPI** (Starlette + Pydantic) |
| ORM | **SQLAlchemy 2.0** (async) + Alembic |
| Validation | **Pydantic v2** |
| DB Driver | **asyncpg** (PostgreSQL) |
| Cache | **redis-py** (async) |
| Config | **pydantic-settings** (.env) |
| Logging | **structlog** (JSON) |
| Testing | **pytest** + **pytest-asyncio** + **httpx** |
| Linting | **ruff** (fast, replaces flake8/black/isort) + **mypy** |
| Container | **Docker multi-stage** (python:3.12-slim → distroless) |
| CI/CD | **GitHub Actions** (lint, test, build, security) |

## 📦 Dependencias Principales

```toml
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.110",
    "uvicorn[standard]>=0.29",
    "sqlalchemy>=2.0",
    "alembic>=1.13",
    "asyncpg>=0.29",
    "redis>=5.0",
    "pydantic>=2.7",
    "pydantic-settings>=2.3",
    "python-jose[cryptography]>=3.3",
    "passlib[bcrypt]>=1.7",
    "structlog>=24.1",
    "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "httpx>=0.27",
    "ruff>=0.5",
    "mypy>=1.10",
    "watchfiles>=0.22",
]
```

## 🐳 Docker

```bash
make docker-build   # Multi-stage, ~100MB final
make docker-run
```

## 🚀 Deploy

```bash
# GitHub Actions en push a main:
# 1. lint + test + build
# 2. docker buildx push a ghcr.io
# 3. Release automático
```

## 📚 Recursos

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [ruff](https://docs.astral.sh/ruff/)