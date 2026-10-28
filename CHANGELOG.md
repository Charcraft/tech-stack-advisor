# Changelog

All notable changes to this project will be documented in this format.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-27

### Added
- Initial release of Tech Stack Advisor skill
- Complete workflow: detect → analyze → interview → recommend → report
- Heuristic stack detector (`scripts/detect-stack.py`) supporting 15+ languages/frameworks
- Senior architect analysis prompt (extracts project type, domain, scale, team, constraints)
- CTO-fractional interview prompt (7 key questions with "why" explanations)
- Decision engine with weighted matrix (Go/Python/Rust/Node recommendations)
- Professional report generator: ADR (`STACK_DECISION.md`) + Actionable checklist (`NEXT_STEPS.md`)
- Production-ready templates for 4 stacks:
  - **Go**: Chi, pgx, sqlc, Redis, Zap, Prometheus, Jaeger, Docker multi-stage, CI/CD, k6
  - **Python**: FastAPI, SQLAlchemy, Pydantic, Alembic, pytest, Docker, CI
  - **Rust**: Axum, Tokio, SQLx, Redis, tracing, Docker, CI
  - **Node/TypeScript**: Fastify/Hono, Prisma/Drizzle, Zod, Vitest, Docker, CI
- Comprehensive documentation (README, template READMEs, inline comments)
- MIT License

### Technical Details
- Skill entry: `workflows/evaluate.yaml`
- Prompts: `analyze-project.md`, `interview.md`, `recommend.md`, `report.md`
- Tools required: `read`, `glob`, `grep`, `question`, `write`, `bash`
- Minimum opencode version: 0.4.0

## [Unreleased]

### Planned
- [ ] Interactive TUI mode for interview (vs CLI questions)
- [ ] Support for monorepo detection (Nx, Turborepo, Bazel)
- [ ] Cost estimation calculator (cloud bill projection per stack)
- [ ] Team skill gap analysis (LinkedIn/GitHub integration)
- [ ] Architecture diagram generation (Mermaid/C4 from decision)
- [ ] VS Code extension for one-click evaluation
- [ ] More templates: Java/Spring, .NET, Elixir/Phoenix, Zig