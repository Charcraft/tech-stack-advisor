#!/usr/bin/env python3
"""
Detector heurístico de stack tecnológico.
Escanea el repo y emite señales JSON para el análisis LLM.
Uso: python scripts/detect-stack.py [ruta_proyecto]
"""
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

signals: Dict[str, Any] = {
    "languages": [],
    "frameworks": [],
    "build_tools": [],
    "infra": [],
    "db": [],
    "ml": False,
    "testing": [],
    "ci_cd": [],
    "container": False,
    "k8s": False,
    "serverless": False,
    "monorepo": False,
    "config_files": [],
    "entry_points": [],
    "tree_summary": {},
}

# ---------- Helpers ----------
def add_unique(arr: List[str], val: str):
    if val not in arr:
        arr.append(val)

def scan_glob(pattern: str, callback):
    for f in ROOT.rglob(pattern):
        if not any(part.startswith('.') for part in f.relative_to(ROOT).parts):
            callback(f)

# ---------- Package Managers & Configs ----------
# Node / TypeScript / Bun / Deno
for f in ROOT.rglob("package.json"):
    data = read_json(f)
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    signals["config_files"].append(str(f.relative_to(ROOT)))
    if "typescript" in deps: add_unique(signals["languages"], "typescript")
    if "javascript" in data.get("engines", {}): add_unique(signals["languages"], "javascript")
    if "bun" in deps or (ROOT / "bun.lockb").exists(): add_unique(signals["build_tools"], "bun")
    if "deno" in deps: add_unique(signals["build_tools"], "deno")
    # Frameworks
    fw_map = {
        "next": "nextjs", "react": "react", "vue": "vue", "svelte": "svelte",
        "fastify": "fastify", "express": "express", "hono": "hono", "elysia": "elysia",
        "nestjs": "nestjs", "remix": "remix", "astro": "astro", "nuxt": "nuxt",
        "solid": "solid", "qwik": "qwik",
    }
    for dep, fw in fw_map.items():
        if dep in deps: add_unique(signals["frameworks"], fw)
    # Testing
    test_map = {"vitest": "vitest", "jest": "jest", "playwright": "playwright", "cypress": "cypress"}
    for dep, t in test_map.items():
        if dep in deps: add_unique(signals["testing"], t)
    # Monorepo
    if data.get("workspaces") or (ROOT / "turbo.json").exists() or (ROOT / "nx.json").exists():
        signals["monorepo"] = True

# Python
py_files = list(ROOT.rglob("pyproject.toml")) + list(ROOT.rglob("requirements*.txt")) + list(ROOT.rglob("setup.py"))
for f in py_files:
    txt = read_text(f)
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "python")
    fw_map = {
        "fastapi": "fastapi", "django": "django", "flask": "flask", "starlette": "starlette",
        "litestar": "litestar", "quart": "quart", "sanic": "sanic", "tornado": "tornado",
    }
    for kw, fw in fw_map.items():
        if kw in txt.lower(): add_unique(signals["frameworks"], fw)
    # ML/Data
    ml_kws = ["torch", "tensorflow", "jax", "langchain", "llamaindex", "transformers", "sklearn", "xgboost", "lightgbm"]
    if any(kw in txt.lower() for kw in ml_kws):
        signals["ml"] = True
    # Testing
    if "pytest" in txt: add_unique(signals["testing"], "pytest")
    # Tools
    if "ruff" in txt: add_unique(signals["build_tools"], "ruff")
    if "mypy" in txt: add_unique(signals["build_tools"], "mypy")
    if "poetry" in txt or (ROOT / "poetry.lock").exists(): add_unique(signals["build_tools"], "poetry")
    if "uv" in txt or (ROOT / "uv.lock").exists(): add_unique(signals["build_tools"], "uv")

# Go
if (ROOT / "go.mod").exists():
    mod = read_text(ROOT / "go.mod")
    signals["config_files"].append("go.mod")
    add_unique(signals["languages"], "go")
    fw_map = {"chi": "chi", "gin": "gin", "echo": "echo", "fiber": "fiber", "httprouter": "httprouter", "gorilla/mux": "gorilla-mux"}
    for kw, fw in fw_map.items():
        if kw in mod: add_unique(signals["frameworks"], fw)
    # Check go.mod for tools
    if "sqlc" in mod: add_unique(signals["build_tools"], "sqlc")
    if "wire" in mod: add_unique(signals["build_tools"], "wire")
    if "air" in mod: add_unique(signals["build_tools"], "air")
    # Also check for sqlc.yaml config file
    if (ROOT / "sqlc.yaml").exists() or (ROOT / "sqlc.json").exists():
        add_unique(signals["build_tools"], "sqlc")
        signals["config_files"].append("sqlc.yaml" if (ROOT / "sqlc.yaml").exists() else "sqlc.json")
    # Testing
    if "testify" in mod: add_unique(signals["testing"], "testify")
    if "ginkgo" in mod: add_unique(signals["testing"], "ginkgo")

# Rust
if (ROOT / "Cargo.toml").exists():
    cargo = read_text(ROOT / "Cargo.toml")
    signals["config_files"].append("Cargo.toml")
    add_unique(signals["languages"], "rust")
    fw_map = {"axum": "axum", "actix-web": "actix-web", "warp": "warp", "rocket": "rocket", "poem": "poem", "salvo": "salvo"}
    for kw, fw in fw_map.items():
        if kw in cargo: add_unique(signals["frameworks"], fw)
    if "tokio" in cargo: add_unique(signals["frameworks"], "tokio")
    if "sqlx" in cargo: add_unique(signals["build_tools"], "sqlx")
    if "sea-orm" in cargo: add_unique(signals["build_tools"], "sea-orm")
    # Testing
    if "test" in cargo: add_unique(signals["testing"], "cargo-test")

# Java / Kotlin / Scala
for f in ROOT.rglob("pom.xml"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "java")
for f in ROOT.rglob("build.gradle*"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    txt = read_text(f)
    if "kotlin" in txt: add_unique(signals["languages"], "kotlin")
    else: add_unique(signals["languages"], "java")

# .NET
for f in ROOT.rglob("*.csproj"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "csharp")

# PHP
for f in ROOT.rglob("composer.json"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "php")
    data = read_json(f)
    if "laravel/framework" in data.get("require", {}): add_unique(signals["frameworks"], "laravel")
    if "symfony" in str(data): add_unique(signals["frameworks"], "symfony")

# Ruby
for f in ROOT.rglob("Gemfile"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "ruby")
    txt = read_text(f)
    if "rails" in txt: add_unique(signals["frameworks"], "rails")

# Elixir
for f in ROOT.rglob("mix.exs"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["languages"], "elixir")
    txt = read_text(f)
    if "phoenix" in txt: add_unique(signals["frameworks"], "phoenix")

# ---------- Infra & Deploy ----------
# Docker
docker_files = list(ROOT.rglob("Dockerfile*")) + list(ROOT.rglob("docker-compose*.y*ml")) + list(ROOT.rglob("docker-bake*.hcl"))
if docker_files:
    signals["container"] = True
    for f in docker_files:
        signals["config_files"].append(str(f.relative_to(ROOT)))
        add_unique(signals["infra"], "docker")

# Kubernetes
k8s_files = list(ROOT.rglob("k8s/**/*.y*ml")) + list(ROOT.rglob("kustomization.y*ml")) + list(ROOT.rglob("helm/**/*.y*ml"))
if k8s_files:
    signals["k8s"] = True
    add_unique(signals["infra"], "kubernetes")

# Serverless
serverless_files = list(ROOT.rglob("serverless.y*ml")) + list(ROOT.rglob("samconfig.toml")) + list(ROOT.rglob("template.y*ml"))
if serverless_files:
    signals["serverless"] = True
    add_unique(signals["infra"], "serverless")

# Terraform / Pulumi / Crossplane
for f in ROOT.rglob("*.tf"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["infra"], "terraform")
for f in ROOT.rglob("Pulumi.y*ml"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["infra"], "pulumi")

# CI/CD
for f in ROOT.rglob(".github/workflows/*.y*ml"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["ci_cd"], "github-actions")
for f in ROOT.rglob(".gitlab-ci.y*ml"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["ci_cd"], "gitlab-ci")
for f in ROOT.rglob("Jenkinsfile*"):
    signals["config_files"].append(str(f.relative_to(ROOT)))
    add_unique(signals["ci_cd"], "jenkins")

# ---------- Database ----------
db_patterns = ["*.sql", "migrations/**/*.sql", "prisma/**", "ent/**", "sqlc.yaml", "sqlc.json", "dbmate.yaml", "goose.yaml"]
for pattern in db_patterns:
    if list(ROOT.rglob(pattern)):
        add_unique(signals["db"], "sql")
        break

# ---------- Entry Points ----------
for f in ROOT.rglob("main.go"):
    signals["entry_points"].append(str(f.relative_to(ROOT)))
for f in ROOT.rglob("main.py"):
    signals["entry_points"].append(str(f.relative_to(ROOT)))
for f in ROOT.rglob("src/main.rs"):
    signals["entry_points"].append(str(f.relative_to(ROOT)))
for f in ROOT.rglob("index.ts"):
    signals["entry_points"].append(str(f.relative_to(ROOT)))
for f in ROOT.rglob("app.py"):
    signals["entry_points"].append(str(f.relative_to(ROOT)))

# ---------- Tree Summary (top 3 levels) ----------
def tree_summary(path: Path, max_depth: int = 3, current_depth: int = 0) -> dict:
    if current_depth >= max_depth:
        return {}
    result = {"dirs": [], "files": []}
    try:
        for item in sorted(path.iterdir()):
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                result["dirs"].append({"name": item.name, "children": tree_summary(item, max_depth, current_depth + 1)})
            else:
                result["files"].append(item.name)
    except PermissionError:
        pass
    return result

signals["tree_summary"] = tree_summary(ROOT)

# ---------- Git Info ----------
try:
    git_root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True, text=True, timeout=5)
    if git_root.returncode == 0:
        signals["git_root"] = git_root.stdout.strip()
        # Branch
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, timeout=5)
        signals["git_branch"] = branch.stdout.strip()
        # Last commit
        log = subprocess.run(["git", "log", "-1", "--pretty=format:%h %s (%an, %ar)"], cwd=ROOT, capture_output=True, text=True, timeout=5)
        signals["last_commit"] = log.stdout.strip()
except Exception:
    pass

# ---------- Output ----------
print(json.dumps(signals, indent=2, ensure_ascii=False))