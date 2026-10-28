# Tech Stack Advisor

> **Evalúa tu proyecto y recomienda el stack tecnológico óptimo con justificación senior, accesible a founders y vibecoders.**

Convierte incertidumbre técnica en **decisiones documentadas y accionables** en 10-20 minutos.

---

## 🎯 ¿Qué hace?

1. **Analiza tu codebase** (heurísticas rápidas: `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, Docker, CI/CD, etc.)
2. **Entrevista ligera** (5-7 preguntas clave en lenguaje llano, cada una con *por qué importa*)
3. **Recomienda stack principal + 2 alternativas** con trade-offs honestos, métricas concretas y próximo paso copy-paste
4. **Genera artefactos versionables**:
   - `STACK_DECISION.md` – ADR ligero (contexto, decisión, consecuencias, follow-up a 90 días)
   - `NEXT_STEPS.md` – Checklist accionable con criterios de "hecho"

---

## 🚀 Instalación

```bash
# Opción 1: Desde GitHub (recomendado)
npx skills add Charcraft/tech-stack-advisor

# Opción 2: Local (desarrollo)
git clone https://github.com/Charcraft/tech-stack-advisor
# En opencode.json:
# "skills": { "tech_stack_advisor": "./tech-stack-advisor" }
```

---

## 💡 Uso

```bash
# En cualquier proyecto (nuevo o existente)
/skill tech_stack_advisor
```

**Flujo interactivo**:
```
🔍 Analizando codebase... (detecta: Go + Chi + PostgreSQL + Docker + GitHub Actions)
🤔 Pregunta 1/7: ¿Cuántos usuarios concurrentes esperas en el primer mes?
   └─ Why: Define si necesitamos concurrencia nativa (Go/Rust) o nos vale async Python/Node.
   Options: [<100, 100-1k, 1k-10k, >10k, no sé]
> 1k-10k
🤔 Pregunta 2/7: ¿Cuál es la latencia máxima aceptable en p99?
   ...
✅ Generando recomendación...
📝 Escrito: STACK_DECISION.md, NEXT_STEPS.md
```

---

## 📋 Ejemplo de Salida

### `STACK_DECISION.md` (extracto)
```markdown
# ADR: Elección de Stack Tecnológico

**Fecha**: 2026-10-27
**Estado**: Aceptado

## Contexto
- Proyecto: API SaaS B2B, 5k RPS objetivo, latencia p99 < 50ms
- Equipo: 3 devs (2 Python, 1 Go), bootstrap, deadline 8 semanas
- Hosting: VPS único, sin Kubernetes

## Decisión
**Stack Principal**: **Go 1.23** (chi, sqlc, zerolog, wire)

## Consecuencias
| Positivas | Negativas (Mitigadas) |
|-----------|----------------------|
| 5k+ RPS en 2 vCPU / 2 GB RAM | Curva 2-3 sem → Plantilla + primer PR guiado |
| Deploy: `scp binary && systemctl restart` | ML futuro → Sidecar Python gRPC |
| Contratación: pool grande Go devs | Boilerplate → Plantilla genera todo |
</markdown>

### `NEXT_STEPS.md` (extracto)
```markdown
# Próximos Pasos – Stack Validado: Go

## 0. Validación Rápida (5 min)
- [ ] `git clone https://github.com/Charcraft/tech-stack-advisor/templates/go my-project`
- [ ] `cd my-project && make dev` → compila y responde `/healthz` en <30 seg

## 1. Fundamentos (30 min)
- [ ] Configura `.env` desde `.env.example`
- [ ] `make migrate` → crea tablas
- [ ] `make test` → >80% coverage

## 2. Primer Feature Real (2-4h)
- [ ] Define 1 endpoint CRUD real
- [ ] Usa `sqlc` para queries type-safe
- [ ] Añade test de integración
...
```

---

## 🧠 Matriz de Decisión (Interna)

| Señal Fuerte | Empuja Hacia |
|--------------|--------------|
| RPS > 5k, latencia p99 < 50ms | Go / Rust |
| Equipo solo Python, deadline "ayer" | Python (FastAPI) |
| ML training / data science core | Python |
| CLI / tool / edge / WASM / embedded | Go / Rust |
| Serverless + cold-starts críticos | Node / Go (no Rust) |
| Compliance estricto (PCI, HIPAA) | Go / Rust |
| Bootstrap, solo founder, MVP semanas | Python / Node |
| Equipo 5+, contratar senior fácil | Go |
| Cloud bill > $5k/mes proyectado | Go / Rust |

---

## 📦 Plantillas Incluidas (Listas para Producción)

| Stack | Template | Características |
|-------|----------|-----------------|
| **Go** | `templates/go/` | Chi, pgx, sqlc, Redis, Zap, Prometheus, Jaeger, Docker multi-stage, CI/CD, k6 |
| **Python** | `templates/python/` | FastAPI, SQLAlchemy, Pydantic, Alembic, pytest, Docker, CI |
| **Rust** | `templates/rust/` | Axum, Tokio, SQLx, Redis, tracing, Docker, CI |
| **Node/TypeScript** | `templates/node/` | Fastify/Hono, Prisma/Drizzle, Zod, Vitest, Docker, CI |

> Cada plantilla incluye: `README.md`, `Makefile`/`justfile`, `docker-compose`, `Dockerfile`, `.github/workflows/ci.yml`, observabilidad básica, y validación `make validate`.

---

## 🛠 Requisitos

- **opencode** ≥ 0.4.0
- **Python 3.10+** (para `scripts/detect-stack.py`)
- **Git** (para metadatos de repo)

---

## 🤝 Contribuir

1. Fork → branch → PR
2. Añade tests en `tests/`
3. Actualiza `CHANGELOG.md`
4. Sigue `CONTRIBUTING.md`

---

## 📄 Licencia

MIT – Carlos Martinez Pineda (Charcraft)

---

## 🙋 Soporte

- **Issues**: [GitHub Issues](https://github.com/Charcraft/tech-stack-advisor/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/Charcraft/tech-stack-advisor/discussions)
- **Email**: charcraftycarlos@gmail.com

---

> **Hecho para founders, CTOs fraccionales, y vibecoders que quieren decidir bien desde el día 1.**