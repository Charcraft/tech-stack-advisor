# Makefile – Go Production Template
# Uso: make <target>
# Variables configurables via .env o línea de comandos

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
BINARY_NAME        ?= my-api
VERSION            ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
BUILD_TIME         ?= $(shell date -u '+%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT         ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GO_VERSION         ?= 1.23
GOOS               ?= $(shell go env GOOS)
GOARCH             ?= $(shell go env GOARCH)
CGO_ENABLED        ?= 0
LDFLAGS            ?= -s -w -X main.version=$(VERSION) -X main.buildTime=$(BUILD_TIME) -X main.gitCommit=$(GIT_COMMIT)

# Directorios
BUILD_DIR          ?= ./bin
DIST_DIR           ?= ./dist
SQLC_DIR           ?= ./internal/database
MIGRATIONS_DIR     ?= ./migrations

# Docker
DOCKER_REGISTRY    ?= ghcr.io
DOCKER_IMAGE       ?= $(DOCKER_REGISTRY)/$(shell git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/$(BINARY_NAME)
DOCKER_TAG         ?= $(VERSION)

# =============================================================================
# TARGETS PRINCIPALES
# =============================================================================
.PHONY: help dev build test lint fmt generate migrate docker-up docker-down clean

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Desarrollo con hot-reload (requiere 'air')
	@which air > /dev/null || (echo "Instalando air..." && go install github.com/air-verse/air@latest)
	@air -c .air.toml

build: ## Compila binario estático para producción
	@mkdir -p $(BUILD_DIR)
	CGO_ENABLED=$(CGO_ENABLED) GOOS=$(GOOS) GOARCH=$(GOARCH) go build \
		-ldflags="$(LDFLAGS)" \
		-o $(BUILD_DIR)/$(BINARY_NAME) \
		./cmd/server

build-all: ## Compila para linux/amd64, linux/arm64, darwin/amd64, darwin/arm64, windows/amd64
	@mkdir -p $(DIST_DIR)
	@for os in linux darwin windows; do \
		for arch in amd64 arm64; do \
			if [ "$$os" = "windows" ] && [ "$$arch" = "arm64" ]; then continue; fi; \
			ext=""; [ "$$os" = "windows" ] && ext=".exe"; \
			echo "Building $$os/$$arch..."; \
			CGO_ENABLED=0 GOOS=$$os GOARCH=$$arch go build \
				-ldflags="$(LDFLAGS)" \
				-o $(DIST_DIR)/$(BINARY_NAME)-$$os-$$arch$$ext \
				./cmd/server; \
		done; \
	done

test: ## Ejecuta tests unitarios + integración con coverage
	go test -v -race -coverprofile=coverage.out -covermode=atomic ./...
	go tool cover -func=coverage.out | grep total

test-unit: ## Solo tests unitarios (rápido)
	go test -short -v ./internal/...

test-integration: ## Tests de integración (requiere docker-compose up -d)
	go test -v -tags=integration ./tests/integration/...

bench: ## Benchmarks
	go test -bench=. -benchmem -run=^$$ ./...

lint: ## Lint completo (golangci-lint)
	@which golangci-lint > /dev/null || (echo "Instalando golangci-lint..." && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest)
	golangci-lint run --timeout=5m

fmt: ## Formatea código (gofmt + goimports)
	@which goimports > /dev/null || go install golang.org/x/tools/cmd/goimports@latest
	goimports -w .
	gofmt -w .

generate: ## Genera código (sqlc, wire, mocks)
	@which sqlc > /dev/null || (echo "Instalando sqlc..." && go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest)
	@which wire > /dev/null || (echo "Instalando wire..." && go install github.com/google/wire/cmd/wire@latest)
	@which mockgen > /dev/null || (echo "Instalando mockgen..." && go install go.uber.org/mock/mockgen@latest)
	sqlc generate
	wire ./cmd/server
	go generate ./...

migrate: ## Ejecuta migraciones DB (requiere migrate CLI)
	@which migrate > /dev/null || (echo "Instalando migrate..." && go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest)
	migrate -path $(MIGRATIONS_DIR) -database "$$DATABASE_URL" up

migrate-down: ## Revierte última migración
	migrate -path $(MIGRATIONS_DIR) -database "$$DATABASE_URL" down 1

migrate-create: ## Crea nueva migración (uso: make migrate-create NAME=add_users_table)
	migrate create -ext sql -dir $(MIGRATIONS_DIR) -seq $(NAME)

# =============================================================================
# DOCKER & INFRA LOCAL
# =============================================================================
docker-up: ## Levanta Postgres + Redis + Jaeger + Prometheus + Grafana
	docker compose -f docker-compose.yml -f docker-compose.observability.yml up -d
	@echo "Esperando a que Postgres esté listo..."
	@until docker compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do sleep 1; done
	@echo "✅ Infra lista"

docker-down: ## Para y limpia contenedores
	docker compose -f docker-compose.yml -f docker-compose.observability.yml down -v

docker-logs: ## Logs de la infra
	docker compose -f docker-compose.yml -f docker-compose.observability.yml logs -f

docker-build: ## Build imagen Docker multi-arch
	docker buildx build --platform linux/amd64,linux/arm64 \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) \
		-t $(DOCKER_IMAGE):latest \
		--push .

docker-run: ## Corre la imagen built localmente
	docker run --rm -p 8080:8080 --env-file .env $(DOCKER_IMAGE):$(DOCKER_TAG)

# =============================================================================
# RELEASE & DEPLOY
# =============================================================================
release: ## Crea release (tag + build + docker push)
	@git tag -a v$(VERSION) -m "Release v$(VERSION)"
	@git push origin v$(VERSION)
	@make build-all docker-build

# =============================================================================
# UTILIDADES
# =============================================================================
clean: ## Limpia artifacts
	rm -rf $(BUILD_DIR) $(DIST_DIR) coverage.out

deps: ## Descarga y verifica dependencias
	go mod download
	go mod verify
	go mod tidy

deps-upgrade: ## Actualiza dependencias a versiones menores/patch
	go get -u ./...
	go mod tidy

security: ## Escaneo de vulnerabilidades (govulncheck)
	@which govulncheck > /dev/null || go install golang.org/x/vuln/cmd/govulncheck@latest
	govulncheck ./...

doc: ## Genera docs API (swagger via swag)
	@which swag > /dev/null || go install github.com/swaggo/swag/cmd/swag@latest
	swag init -g cmd/server/main.go -o ./docs

# =============================================================================
# VALIDACIÓN RÁPIDA (para NEXT_STEPS.md)
# =============================================================================
validate: ## Validación completa: fmt + lint + test + build
	@make fmt
	@make lint
	@make test
	@make build
	@echo "✅ Validación completa OK"

quick-check: ## Check rápido para CI (sin race detector)
	go build -ldflags="$(LDFLAGS)" ./cmd/server
	go test -short ./...
	go vet ./...