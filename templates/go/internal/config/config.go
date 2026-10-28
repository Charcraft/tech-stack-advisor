package config

import (
	"fmt"
	"os"
	"strconv"
	"time"

	"github.com/joho/godotenv"
)

type Config struct {
	Env          string
	Port         string
	DatabaseURL  string
	RedisURL     string
	JWTSecret    string
	JWTExpiry    time.Duration
	RateLimitRPS int
	RateLimitBurst int
}

func Load(configPath string) (*Config, error) {
	// Carga .env si existe
	if configPath != "" {
		_ = godotenv.Load(configPath)
	} else {
		_ = godotenv.Load(".env.local")
		_ = godotenv.Load(".env")
	}

	cfg := &Config{
		Env:           getEnv("ENV", "development"),
		Port:          getEnv("PORT", "8080"),
		DatabaseURL:   getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/myapi?sslmode=disable"),
		RedisURL:      getEnv("REDIS_URL", "redis://localhost:6379/0"),
		JWTSecret:     getEnv("JWT_SECRET", "change-me-in-production-32-chars-min"),
		JWTExpiry:     getDurationEnv("JWT_EXPIRY", 24*time.Hour),
		RateLimitRPS:  getIntEnv("RATE_LIMIT_RPS", 100),
		RateLimitBurst: getIntEnv("RATE_LIMIT_BURST", 200),
	}

	if err := cfg.Validate(); err != nil {
		return nil, err
	}

	return cfg, nil
}

func (c *Config) Validate() error {
	if len(c.JWTSecret) < 32 {
		return fmt.Errorf("JWT_SECRET debe tener al menos 32 caracteres")
	}
	if c.Port == "" {
		return fmt.Errorf("PORT es requerido")
	}
	return nil
}

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func getIntEnv(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if i, err := strconv.Atoi(v); err == nil {
			return i
		}
	}
	return fallback
}

func getDurationEnv(key string, fallback time.Duration) time.Duration {
	if v := os.Getenv(key); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			return d
		}
	}
	return fallback
}