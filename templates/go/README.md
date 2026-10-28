# Go Production Template

Plantilla lista para producción para APIs en Go. Incluye: router Chi, PostgreSQL (pgx + sqlc), Redis, observabilidad completa (logs JSON, métricas Prometheus, tracing Jaeger), migraciones, Docker multi-stage, CI/CD, y load testing.

## 🚀 Inicio Rápido

```bash
# 1. Clona y entra
git clone https://github.com/Charcraft/tech-stack-advisor/templates/go my-api
cd my-api

# 2. Configura entorno
cp .env.example .env
# Edita .env con tus valores (JWT_SECRET mínimo 32 chars!)

# 3. Levanta infra local (Postgres + Redis + Observabilidad)
make docker-up

# 4. Ejecuta migraciones
make migrate

# 5. Desarrollo con hot-reload
make dev
# → Servidor en http://localhost:8080
# → Health: curl localhost:8080/healthz
# → Métricas: curl localhost:8080/metrics
# → Jaeger UI: http://localhost:16686
# → Grafana: http://localhost:3000 (admin/admin)
# → Prometheus: http://localhost:9090
```

## ✅ Validación Rápida (30 seg)

```bash
make validate
# Ejecuta: fmt → lint → test → build
# Si todo pasa → stack validado
```

## 📁 Estructura

```
.
├── cmd/server/           # Entry point (main.go)
├── internal/
│   ├── config/           # Configuración (env + validación)
│   ├── database/         # Código generado por sqlc (NO editar a mano)
│   ├── handler/          # Handlers HTTP (Chi)
│   └── middleware/       # Logging, metrics, tracing
├── migrations/           # Migraciones SQL (golang-migrate)
├── sql/queries.sql       # Queries para sqlc (type-safe)
├── observability/        # Prometheus + Grafana dashboards
├── scripts/              # k6 load test
├── docker-compose.yml    # Postgres + Redis
├── docker-compose.observability.yml  # Jaeger + Prometheus + Grafana
├── Dockerfile            # Multi-stage (builder → runtime ~15MB)
├── Makefile              # Comandos unificados
├── sqlc.yaml             # Config sqlc
├── .air.toml             # Hot-reload config
├── go.mod / go.sum
└── .github/workflows/    # CI/CD (lint, test, build, docker, security)
```

## 🛠 Comandos Principales (Makefile)

| Comando | Qué hace |
|---------|----------|
| `make dev` | Hot-reload con air |
| `make build` | Binario estático en `bin/` |
| `make build-all` | Cross-compile Linux/macOS/Windows |
| `make test` | Tests unit + integración + coverage |
| `make lint` | golangci-lint completo |
| `make fmt` | gofmt + goimports |
| `make generate` | sqlc + wire + mocks |
| `make migrate` | Ejecuta migraciones UP |
| `make migrate-create NAME=xxx` | Crea nueva migración |
| `make docker-up` | Levanta Postgres + Redis |
| `make docker-build` | Build imagen Docker multi-arch |
| `make validate` | fmt + lint + test + build (CI local) |

## 🔧 Stack Tecnológico

| Capa | Tecnología | Por qué |
|------|------------|---------|
| Router | **Chi v5** | Rápido, compatible `net/http`, middleware chain |
| DB Driver | **pgx/v5** | Nativo, pool nativo, prepared statements, performance |
| Query Builder | **sqlc** | SQL → Go type-safe, zero runtime overhead |
| Migrations | **golang-migrate** | Versionado, up/down, CI-friendly |
| Cache | **Redis (go-redis/v9)** | Pool, cluster, pipelines, Lua scripts |
| Config | **godotenv + validación** | 12-factor, fail-fast en startup |
| Logging | **Zap (JSON)** | Estructurado, leveled, sampling, performance |
| Metrics | **Prometheus client** | Histograms, counters, gauges, `/metrics` endpoint |
| Tracing | **OpenTelemetry + Jaeger** | W3C TraceContext, sampling, spans automáticos |
| DI | **Wire** | Compile-time DI, zero reflection |
| Testing | **Testify + httptest** | Unit + integration con DB real |
| Linting | **golangci-lint** | 50+ linters, fast, configurable |
| Container | **Docker multi-stage** | Builder → distroless (~15MB final) |
| CI/CD | **GitHub Actions** | Lint, test, build, docker, security, release |

## 📊 Observabilidad Incluida

### Logs (Zap JSON)
```json
{"level":"info","timestamp":"2026-10-27T10:30:00.123Z","method":"GET","path":"/api/v1/users","status":200,"duration_ms":12.3,"request_id":"abc123"}
```

### Métricas Prometheus (`/metrics`)
- `http_requests_total{method,path,status}` – Counter
- `http_request_duration_seconds{method,path}` – Histogram (p50/p95/p99)
- `http_requests_in_flight` – Gauge

### Tracing (Jaeger)
- Spans automáticos por request (middleware)
- Propagación W3C TraceContext
- Atributos: http.method, url, status_code, error

### Dashboards Grafana (pre-cargados)
- HTTP Request Rate
- Latency p50/p95/p99
- In-flight requests
- Error rates 4xx/5xx

## 🧪 Testing

```bash
# Tests unitarios (rápidos, sin DB)
make test-unit

# Tests integración (requiere docker-up)
make test-integration

# Benchmarks
make bench

# Coverage report
go tool cover -html=coverage.out
```

## 🐳 Docker

```bash
# Build local
make docker-build

# Run contenedor
make docker-run

# Producción: imagen multi-arch en ghcr.io
# docker pull ghcr.io/tu-user/my-api:latest
```

## 🚀 Deploy Producción

```bash
# 1. Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. GitHub Actions hace:
#    - lint + test + build
#    - docker buildx multi-arch push a ghcr.io
#    - Crea Release en GitHub con artifacts

# 3. En servidor:
#    docker pull ghcr.io/tu-user/my-api:v1.0.0
#    docker run -d --env-file .env.prod -p 8080:8080 ghcr.io/tu-user/my-api:v1.0.0
#    # O systemd service + binario estático (sin Docker)
```

## 📈 Load Testing

```bash
# Instala k6: https://k6.io/docs/getting-started/installation/
k6 run scripts/load-test.js

# Con URL custom
BASE_URL=https://api.midominio.com k6 run scripts/load-test.js
```

**Objetivos baseline** (ajusta a tu caso):
- p99 < 50ms @ 1k RPS en local
- p99 < 100ms @ 5k RPS en 2 vCPU / 2GB RAM
- Error rate < 0.1%

## 🔐 Seguridad

- `govulncheck` en CI (vulnerabilidades Go)
- `gosec` en CI (static analysis seguridad)
- Binario estático sin CGO (superficie ataque mínima)
- Usuario no-root en contenedor
- Health/Ready checks para k8s/Docker
- Rate limiting configurable (middleware ready)

## 📝 Próximos Pasos (personaliza)

1. **Auth**: Implementa JWT middleware en `internal/middleware/auth/`
2. **Rate limiting**: Añade token bucket/redis en middleware
3. **CORS**: Configura en Chi middleware
4. **Swagger**: `make doc` genera OpenAPI 3.0
5. **Domain logic**: Añade services en `internal/service/`
6. **Events**: Integra message broker (Kafka, NATS, RabbitMQ)

## 📚 Recursos

- [Chi Router](https://github.com/go-chi/chi)
- [sqlc](https://sqlc.dev/)
- [pgx](https://github.com/jackc/pgx)
- [OpenTelemetry Go](https://opentelemetry.io/docs/instrumentation/go/)
- [golangci-lint](https://golangci-lint.run/)
- [k6](https://k6.io/)

## 📄 Licencia

MIT – Úsalo libremente en proyectos propios o comerciales.