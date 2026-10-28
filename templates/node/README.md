# Node/TypeScript Production Template

Plantilla lista para producción para APIs en Node/TypeScript. Incluye: Fastify/Hono, Prisma/Drizzle, Zod, Vitest, Docker, CI/CD.

## 🚀 Inicio Rápido

```bash
git clone https://github.com/Charcraft/tech-stack-advisor/templates/node my-api
cd my-api

cp .env.example .env
# Edita .env (DATABASE_URL, REDIS_URL, JWT_SECRET)

make docker-up          # Postgres + Redis
make migrate            # Prisma/Drizzle migrations
make dev                # tsx watch (hot-reload)
# → http://localhost:3000/healthz
# → http://localhost:3000/docs (Scalar/OpenAPI)
```

## ✅ Validación

```bash
make validate
# fmt (prettier) → lint (eslint) → typecheck (tsc) → test (vitest + coverage) → build
```

## 📁 Estructura

```
.
├── src/
│   ├── main.ts              # Entry point (Fastify/Hono)
│   ├── config.ts            # Config (zod-validated env)
│   ├── db.ts                # Prisma/Drizzle client
│   ├── routes/              # Route handlers
│   ├── schemas/             # Zod schemas (request/response)
│   ├── services/            # Business logic
│   ├── middleware/          # Auth, logging, metrics, error handling
│   └── utils/               # Helpers
├── prisma/                  # Prisma schema + migrations
│   └── schema.prisma
├── tests/                   # Vitest (unit + integration)
├── docker-compose.yml
├── Dockerfile               # Multi-stage (node:22-alpine → distroless)
├── Makefile
├── package.json
├── tsconfig.json
├── .eslintrc.cjs
├── .prettierrc
├── vitest.config.ts
└── .github/workflows/ci.yml
```

## 🛠 Stack (Dos Sabores)

### Opción A: Fastify + Prisma (Recomendado para equipos)

| Capa | Tecnología |
|------|------------|
| Framework | **Fastify** (rápido, schema-based, plugin ecosystem) |
| ORM | **Prisma** (type-safe, migrations, studio) |
| Validation | **Zod** (runtime + TypeScript inference) |
| DB Driver | **@prisma/client** (PostgreSQL) |
| Cache | **ioredis** (cluster, sentinel) |
| Config | **zod** + **dotenv** |
| Logging | **pino** (JSON, fast, child loggers) |
| Metrics | **prom-client** |
| Testing | **Vitest** + **@fastify/vite** |
| Linting | **ESLint** (typescript-eslint) + **Prettier** |
| Container | **Docker multi-stage** (node:22-alpine → distroless) |
| CI/CD | **GitHub Actions** (lint, typecheck, test, build, security) |

### Opción B: Hono + Drizzle (Edge/Serverless First)

| Capa | Tecnología |
|------|------------|
| Framework | **Hono** (ultra-light, edge-compatible, std web APIs) |
| ORM | **Drizzle ORM** (SQL-like, type-safe, zero-runtime) |
| Validation | **Zod** + **@hono/zod-validator** |
| DB Driver | **postgres.js** / **node-postgres** |
| Cache | **ioredis** / **@hono/redis** |
| Config | **zod** + **dotenv** |
| Logging | **pino** / **hono-pino** |
| Testing | **Vitest** + **hono-test** |
| Container | **Docker multi-stage** (node:22-alpine → distroless) |

## 📦 Dependencias Principales (Fastify + Prisma)

```json
// package.json
{
  "dependencies": {
    "fastify": "^4.28",
    "@fastify/swagger": "^8.14",
    "@fastify/swagger-ui": "^4.0",
    "@fastify/cors": "^9.0",
    "@fastify/helmet": "^11.1",
    "@fastify/rate-limit": "^9.1",
    "@fastify/sensible": "^5.6",
    "prisma": "^5.18",
    "@prisma/client": "^5.18",
    "zod": "^3.23",
    "ioredis": "^5.4",
    "pino": "^9.2",
    "pino-pretty": "^11.2",
    "prom-client": "^15.1",
    "jsonwebtoken": "^9.0",
    "bcryptjs": "^2.4",
    "dotenv": "^16.4"
  },
  "devDependencies": {
    "typescript": "^5.5",
    "tsx": "^4.16",
    "vitest": "^2.0",
    "@vitest/coverage-v8": "^2.0",
    "eslint": "^9.9",
    "@typescript-eslint/eslint-plugin": "^8.0",
    "@typescript-eslint/parser": "^8.0",
    "prettier": "^3.3",
    "@types/node": "^22.0",
    "@types/jsonwebtoken": "^9.0",
    "@types/bcryptjs": "^2.4"
  }
}
```

## 🐳 Docker

```bash
make docker-build   # Multi-stage, ~80MB final
make docker-run
```

## 🚀 Deploy

```bash
# GitHub Actions en push a main:
# 1. lint + typecheck + test + build
# 2. docker buildx multi-arch push a ghcr.io
# 3. Release automático
```

## 📚 Recursos

- [Fastify](https://fastify.io/)
- [Prisma](https://www.prisma.io/)
- [Drizzle ORM](https://orm.drizzle.team/)
- [Hono](https://hono.dev/)
- [Zod](https://zod.dev/)
- [Vitest](https://vitest.dev/)
- [TypeScript ESLint](https://typescript-eslint.io/)