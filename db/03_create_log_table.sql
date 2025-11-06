-- Movies Database System - Logging Table Migration
-- @SOURCE: movies_sql_procedures/create_log.sql::CREATE TABLE LOG_MESSAGES::IdLog       INTEGER        CONSTRAINT ERROR_LOGS_PK           PRIMARY KEY
-- Migrated from Oracle SQL to PostgreSQL
-- Original: Romain VINDERS - 2322

-- Drop existing table if it exists
DROP TABLE IF EXISTS log_messages CASCADE;

-- Create log_messages table
CREATE TABLE log_messages (
    id_log SERIAL PRIMARY KEY,
    username VARCHAR(5) DEFAULT CURRENT_USER NOT NULL,
    origin VARCHAR(48) NOT NULL,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    code INTEGER NOT NULL,
    message VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_log_messages_origin ON log_messages(origin);
CREATE INDEX idx_log_messages_date ON log_messages(review_date);
CREATE INDEX idx_log_messages_code ON log_messages(code);

-- Comments for documentation
COMMENT ON TABLE log_messages IS 'System log messages for information and errors';
COMMENT ON COLUMN log_messages.code IS 'Error code (0 for informational messages)';
COMMENT ON COLUMN log_messages.origin IS 'Origin of the log message (module.function)';
