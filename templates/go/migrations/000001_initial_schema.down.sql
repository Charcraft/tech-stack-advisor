-- 000001_initial_schema.down.sql
-- Rollback de migración inicial

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS schema_migrations;