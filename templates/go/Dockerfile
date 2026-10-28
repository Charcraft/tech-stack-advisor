# Dockerfile multi-stage para binario estático mínimo
# Build: docker build -t my-api .
# Run: docker run -p 8080:8080 --env-file .env my-api

# =============================================================================
# STAGE 1: Builder (compila con cache de módulos)
# =============================================================================
FROM golang:1.23-alpine AS builder

# Instala dependencias de build (git, make, gcc para CGO si se necesita)
RUN apk add --no-cache git make gcc musl-dev

WORKDIR /app

# Cache de go.mod/go.sum
COPY go.mod go.sum ./
RUN go mod download

# Copia código y compila
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=${VERSION:-dev} -X main.buildTime=${BUILD_TIME:-unknown} -X main.gitCommit=${GIT_COMMIT:-unknown}" \
    -o /app/bin/server ./cmd/server

# =============================================================================
# STAGE 2: Runtime (imagen mínima ~15MB)
# =============================================================================
FROM alpine:3.20 AS runtime

# Certificados CA + timezone + usuario no-root
RUN apk add --no-cache ca-certificates tzdata && \
    adduser -D -H -u 10001 appuser

WORKDIR /app

# Copia binario desde builder
COPY --from=builder /app/bin/server /app/server

# Copia migraciones (para migrate CLI si se usa en contenedor)
COPY --from=builder /app/migrations /app/migrations

# Usuario no-root
USER appuser

# Puerto expuesto
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/healthz || exit 1

# Entry point
ENTRYPOINT ["/app/server"]