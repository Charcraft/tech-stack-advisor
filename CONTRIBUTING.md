# Contributing to Tech Stack Advisor

Gracias por contribuir. Este proyecto sigue principios de **calidad sobre cantidad** y **decisiones documentadas**.

## 🎯 Principios

1. **Senior-first**: El output debe ser usable por un CTO/founder sin jerga innecesaria
2. **Actionable**: Cada recomendación termina en comando copy-paste verificable
3. **Honest trade-offs**: No vendas humo; documenta costes reales
4. **Versionable**: Artefactos listos para `git add` (Markdown puro, sin HTML)
5. **Testeable**: `make validate` en plantillas debe pasar en CI limpio

## 🛠 Desarrollo Local

```bash
# 1. Clona
git clone https://github.com/Charcraft/tech-stack-advisor
cd tech-stack-advisor

# 2. Instala opencode (si no lo tienes)
# https://opencode.ai/docs/installation

# 3. Registra skill local en opencode.json
# "skills": { "tech_stack_advisor": "./tech-stack-advisor" }

# 4. Prueba en un proyecto de ejemplo
mkdir /tmp/test-project && cd /tmp/test-project
git init
echo '{"name":"test","dependencies":{"fastapi":"^0.110"}}' > package.json
# ... o crea go.mod, Cargo.toml, pyproject.toml según stack a testear

# 5. Ejecuta skill
opencode run --skill tech_stack_advisor
```

## 📝 Estructura de Cambios

### Prompts (`prompts/`)
- Modifica con cuidado: son el "cerebro" del skill
- Mantén `temperature` baja (0.1-0.3) para consistencia
- Añade ejemplos de entrada/salida en comentarios
- Prueba con `opencode run --prompt prompts/analyze-project.md --input '{"languages":["python"]}'`

### Workflow (`workflows/evaluate.yaml`)
- Cambios aquí afectan el flujo completo
- Añade `timeout` a steps que usan `bash`
- Usa `loop.until` para entrevista iterativa
- Documenta `output` schema en comentarios

### Detector (`scripts/detect-stack.py`)
- Heurísticas, no LLM → rápido y determinista
- Añade tests en `tests/test_detect_stack.py`
- No rompas JSON de salida (downstream lo parsea)

### Plantillas (`templates/<stack>/`)
- Cada plantilla debe pasar `make validate` (o equivalente)
- Incluye `README.md` con inicio rápido
- Docker multi-stage + usuario no-root
- CI/CD con lint + test + build + security
- Observabilidad básica (logs, métricas, health)

## ✅ Checklist de PR

Antes de abrir PR, verifica:

- [ ] `make validate` pasa en **todas** las plantillas modificadas
- [ ] Skill ejecuta end-to-end en proyecto vacío + proyecto con código
- [ ] `STACK_DECISION.md` y `NEXT_STEPS.md` generados son Markdown válido
- [ ] No hay secrets, tokens, ni URLs privadas en código
- [ ] CHANGELOG.md actualizado (formato Keep a Changelog)
- [ ] Tests nuevos en `tests/` si añades lógica
- [ ] Documentación actualizada (README, template READMEs, inline)

## 🧪 Tests

```bash
# Tests del detector
python -m pytest tests/test_detect_stack.py -v

# Tests de integración skill (requiere opencode)
opencode test skill/tech_stack_advisor

# Smoke test plantillas
cd templates/go && make validate
cd templates/python && make validate
cd templates/rust && cargo test && cargo clippy
cd templates/node && npm test && npm run lint
```

## 📋 Convenciones

### Commits (Conventional Commits)
```
feat: add Java/Spring Boot template
fix: detect-stack false positive on monorepo
docs: update Go template README with observability section
refactor: simplify interview prompt logic
test: add detector tests for pnpm workspaces
chore: update golangci-lint to v1.60
```

### Code Style
- **Python**: `ruff` + `mypy` (config en `pyproject.toml`)
- **Go**: `gofmt` + `golangci-lint` (config en `.golangci.yml`)
- **Rust**: `rustfmt` + `clippy`
- **TypeScript**: `prettier` + `eslint` (config en `package.json`)
- **YAML/Markdown**: `prettier` (2 spaces, no tabs)

## 🐛 Reportar Bugs

Usa [GitHub Issues](https://github.com/Charcraft/tech-stack-advisor/issues/new/choose) con plantilla:

1. **Entorno**: opencode version, OS, skill version
2. **Proyecto analizado**: tipo, stack detectado, archivos clave
3. **Comportamiento esperado vs real**
4. **Logs relevantes** (sin secrets)
5. **Pasos para reproducir**

## 💡 Request Features

Abre [Discussion](https://github.com/Charcraft/tech-stack-advisor/discussions/new) con:
- Problema que resuelve
- Alternativas consideradas
- Impacto en usuarios (founders, vibecoders, teams)
- Complejidad estimada

## 🏷 Versionado

- **SemVer estricto**: MAJOR.MINOR.PATCH
- **MAJOR**: Cambios breaking en output (`STACK_DECISION.md` schema, workflow steps)
- **MINOR**: Nuevos stacks, plantillas, preguntas, mejoras no-breaking
- **PATCH**: Bug fixes, typos, docs, CI tweaks

## 📞 Contacto

- **Maintainer**: Carlos Martinez Pineda (@Charcraft)
- **Email**: charcraftycarlos@gmail.com
- **Discord**: (próximamente)

---

> **Regla de oro**: Si no estás seguro, abre un Discussion primero. Prefiero 1 PR bien pensado a 10 PRs rápidos que rompan cosas.