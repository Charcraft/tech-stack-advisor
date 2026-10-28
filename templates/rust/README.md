# Rust Axum Production Template

Plantilla lista para producción para APIs en Rust. Incluye: Axum, Tokio, SQLx, Redis, tracing, Docker, CI/CD.

## 🚀 Inicio Rápido

```bash
git clone https://github.com/Charcraft/tech-stack-advisor/templates/rust my-api
cd my-api

cp .env.example .env
# Edita .env (DATABASE_URL, REDIS_URL, JWT_SECRET)

make docker-up          # Postgres + Redis
make migrate            # SQLx migrations
make dev                # cargo watch (hot-reload)
# → http://localhost:3000/healthz
```

## ✅ Validación

```bash
make validate
# fmt (rustfmt) → lint (clippy) → test (cargo test) → build (release)
```

## 📁 Estructura

```
.
├── src/
│   ├── main.rs              # Entry point + router
│   ├── config.rs            # Config (figment + serde)
│   ├── db.rs                # SQLx pool + migrations
│   ├── handlers/            # Axum handlers
│   ├── models/              # Domain models
│   ├── services/            # Business logic
│   ├── middleware/          # Logging, auth, metrics
│   └── error.rs             # Error handling
├── migrations/              # SQLx migrations
├── tests/                   # Integration tests
├── docker-compose.yml
├── Dockerfile               # Multi-stage (rust:1.79 → distroless)
├── Makefile
├── Cargo.toml
├── sqlx-data.json           # Offline compile cache
└── .github/workflows/ci.yml
```

## 🛠 Stack

| Capa | Tecnología |
|------|------------|
| Framework | **Axum** (tower + hyper) |
| Runtime | **Tokio** (multi-threaded) |
| DB | **SQLx** (compile-time checked, async) |
| Migrations | **SQLx migrate** |
| Cache | **redis-rs** (async, cluster support) |
| Config | **figment** (env + file + defaults) |
| Serialization | **serde** + **serde_json** |
| Logging/Tracing | **tracing** + **tracing-subscriber** (JSON) |
| Metrics | **prometheus-client** |
| Testing | **cargo test** + **axum-test** + **sqlx-test** |
| Linting | **clippy** + **rustfmt** |
| Container | **Docker multi-stage** (rust:1.79 → gcr.io/distroless/cc) |
| CI/CD | **GitHub Actions** (clippy, test, build, docker, audit) |

## 📦 Dependencias Principales

```toml
# Cargo.toml
[dependencies]
axum = { version = "0.7", features = ["macros"] }
tokio = { version = "1.38", features = ["full", "macros"] }
sqlx = { version = "0.8", features = ["runtime-tokio-rustls", "postgres", "uuid", "chrono", "migrate", "offline"] }
redis = { version = "0.24", features = ["tokio-comp", "connection-manager"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
figment = { version = "0.11", features = ["env", "toml"] }
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["json", "env-filter"] }
prometheus-client = "0.3"
uuid = { version = "1.7", features = ["v4", "serde", "sqlx-postgres"] }
chrono = { version = "0.4", features = ["serde"] }
anyhow = "1.0"
thiserror = "1.0"
jsonwebtoken = "9.2"
argon2 = "0.5"
```

## 🐳 Docker

```bash
make docker-build   # Multi-stage, ~20MB final (distroless)
make docker-run
```

## 🚀 Deploy

```bash
# GitHub Actions en push a main:
# 1. clippy + test + cargo audit
# 2. docker buildx multi-arch push a ghcr.io
# 3. Release automático con binarios + SBOM
```

## 📚 Recursos

- [Axum](https://github.com/tokio-rs/axum)
- [SQLx](https://github.com/launchbadge/sqlx)
- [Tokio](https://tokio.rs/)
- [Tracing](https://docs.rs/tracing/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)