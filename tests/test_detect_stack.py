#!/usr/bin/env python3
"""Tests para scripts/detect-stack.py"""
import json
import tempfile
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "detect-stack.py"

def run_detect(project_dir: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(project_dir)],
        capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, f"Detector failed: {result.stderr}"
    return json.loads(result.stdout)

def test_go_project():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "go.mod").write_text("module test\n\ngo 1.23\n\nrequire github.com/go-chi/chi/v5 v5.2.0\n")
        (root / "main.go").write_text("package main\n\nfunc main() {}\n")
        (root / "sqlc.yaml").write_text("version: '2'\n")
        
        signals = run_detect(root)
        
        assert "go" in signals["languages"]
        assert "chi" in signals["frameworks"]
        assert "sqlc" in signals["build_tools"]
        assert any("main.go" in ep for ep in signals["entry_points"])

def test_python_fastapi():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pyproject.toml").write_text("""
[project]
name = "test"
dependencies = ["fastapi", "uvicorn", "sqlalchemy", "asyncpg"]
""")
        (root / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n")
        
        signals = run_detect(root)
        
        assert "python" in signals["languages"]
        assert "fastapi" in signals["frameworks"]
        assert any("main.py" in ep for ep in signals["entry_points"])

def test_node_typescript():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text(json.dumps({
            "name": "test",
            "dependencies": {"fastify": "^4.28", "zod": "^3.23"},
            "devDependencies": {"typescript": "^5.5", "vitest": "^2.0"}
        }))
        (root / "index.ts").write_text("import Fastify from 'fastify';\nconst app = Fastify();\n")
        
        signals = run_detect(root)
        
        assert "typescript" in signals["languages"]
        assert "fastify" in signals["frameworks"]
        assert "vitest" in signals["testing"]
        assert any("index.ts" in ep for ep in signals["entry_points"])

def test_rust_axum():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "Cargo.toml").write_text("""
[package]
name = "test"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["postgres", "runtime-tokio"] }
""")
        (root / "src" / "main.rs").write_text("fn main() {}\n")
        (root / "src" / "main.rs").parent.mkdir(exist_ok=True)
        
        signals = run_detect(root)
        
        assert "rust" in signals["languages"]
        assert "axum" in signals["frameworks"]
        assert "tokio" in signals["frameworks"]

def test_docker_compose():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docker-compose.yml").write_text("version: '3.9'\nservices:\n  db:\n    image: postgres:16\n")
        
        signals = run_detect(root)
        
        assert signals["container"] is True
        assert "docker" in signals["infra"]

def test_monorepo_detection():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text(json.dumps({
            "name": "monorepo",
            "workspaces": ["packages/*"],
            "devDependencies": {"turbo": "^2.0"}
        }))
        (root / "turbo.json").write_text('{"pipeline": {"build": {}}}')
        
        signals = run_detect(root)
        
        assert signals["monorepo"] is True

def test_ml_detection():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "requirements.txt").write_text("torch\ntensorflow\nlangchain\n")
        
        signals = run_detect(root)
        
        assert signals["ml"] is True

if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))