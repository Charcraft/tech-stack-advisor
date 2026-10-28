package main

import (
	"context"
	"flag"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/redis/go-redis/v9"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"

	"my-api/internal/config"
	"my-api/internal/handler"
	"my-api/internal/middleware/logging"
	"my-api/internal/middleware/metrics"
	"my-api/internal/middleware/tracing"
)

var (
	version   = "dev"
	buildTime = "unknown"
	gitCommit = "unknown"
)

func main() {
	// Flags
	configPath := flag.String("config", "", "Ruta al archivo de configuración (opcional, usa .env por defecto)")
	showVersion := flag.Bool("version", false, "Muestra versión y sale")
	flag.Parse()

	if *showVersion {
		printVersion()
		return
	}

	// Carga configuración
	cfg, err := config.Load(*configPath)
	if err != nil {
		panic("config load: " + err.Error())
	}

	// Logger estructurado (JSON en prod, console en dev)
	logger := newLogger(cfg.Env)
	defer logger.Sync()

	logger.Info("Iniciando aplicación",
		zap.String("version", version),
		zap.String("build_time", buildTime),
		zap.String("git_commit", gitCommit),
		zap.String("env", cfg.Env),
	)

	// Conexiones
	dbpool, err := newDBPool(cfg.DatabaseURL)
	if err != nil {
		logger.Fatal("DB connection failed", zap.Error(err))
	}
	defer dbpool.Close()

	redisClient := newRedisClient(cfg.RedisURL)
	defer redisClient.Close()

	// Router Chi
	r := chi.NewRouter()

	// Middlewares base
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(30 * time.Second))
	r.Use(logging.New(logger))
	r.Use(metrics.New())
	r.Use(tracing.New("my-api"))

	// Health checks (sin auth, sin rate limit)
	r.Get("/healthz", handler.Healthz(dbpool, redisClient))
	r.Get("/readyz", handler.Readyz(dbpool, redisClient))

	// Métricas Prometheus
	r.Handle("/metrics", metrics.Handler())

	// API v1
	r.Route("/api/v1", func(r chi.Router) {
		// r.Use(auth.Middleware(cfg.JWTSecret)) // Descomenta cuando implementes auth
		r.Get("/users", handler.ListUsers(dbpool))
		r.Post("/users", handler.CreateUser(dbpool))
		r.Get("/users/{id}", handler.GetUser(dbpool))
		r.Put("/users/{id}", handler.UpdateUser(dbpool))
		r.Delete("/users/{id}", handler.DeleteUser(dbpool))
	})

	// Servidor HTTP
	srv := &http.Server{
		Addr:         ":" + cfg.Port,
		Handler:      r,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Graceful shutdown
	go func() {
		logger.Info("Servidor escuchando", zap.String("addr", srv.Addr))
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatal("Server error", zap.Error(err))
		}
	}()

	// Espera señal de terminación
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	logger.Info("Apagando servidor...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Fatal("Server forced to shutdown", zap.Error(err))
	}

	logger.Info("Servidor detenido correctamente")
}

func printVersion() {
	println("Version:", version)
	println("Build Time:", buildTime)
	println("Git Commit:", gitCommit)
}

func newLogger(env string) *zap.Logger {
	var cfg zap.Config
	if env == "production" {
		cfg = zap.NewProductionConfig()
		cfg.EncoderConfig.TimeKey = "timestamp"
		cfg.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	} else {
		cfg = zap.NewDevelopmentConfig()
		cfg.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
	}
	logger, _ := cfg.Build()
	return logger
}

func newDBPool(dsn string) (*pgxpool.Pool, error) {
	cfg, err := pgxpool.ParseConfig(dsn)
	if err != nil {
		return nil, err
	}
	cfg.MaxConns = 25
	cfg.MinConns = 5
	cfg.MaxConnLifetime = time.Hour
	cfg.MaxConnIdleTime = 30 * time.Minute
	cfg.HealthCheckPeriod = 1 * time.Minute
	return pgxpool.NewWithConfig(context.Background(), cfg)
}

func newRedisClient(url string) *redis.Client {
	opt, err := redis.ParseURL(url)
	if err != nil {
		// Fallback a defaults si URL inválida
		opt = &redis.Options{
			Addr:     "localhost:6379",
			Password: "",
			DB:       0,
		}
	}
	opt.PoolSize = 20
	opt.MinIdleConns = 5
	opt.MaxRetries = 3
	opt.DialTimeout = 5 * time.Second
	opt.ReadTimeout = 3 * time.Second
	opt.WriteTimeout = 3 * time.Second
	return redis.NewClient(opt)
}