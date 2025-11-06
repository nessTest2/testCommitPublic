-- Movies Database System - Base Tables Migration
-- @SOURCE: movies_sql_procedures/base_tables/create_base_tables.sql::CREATE TABLE USERS::SyncToken   CHAR(1) DEFAULT 0 CONSTRAINT USERS_SYNCTOKEN_NN NOT NULL
-- Migrated from Oracle SQL to PostgreSQL
-- Original: Romain VINDERS - 2322

-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_reviews CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_seq;

-- Create users table
CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    login VARCHAR(30) UNIQUE NOT NULL,
    sync_token CHAR(1) DEFAULT '0' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_reviews table
CREATE TABLE user_reviews (
    id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
    id_movie INTEGER NOT NULL,  -- Foreign key added later after movies table creation
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 10),
    review VARCHAR(200),
    sync_token CHAR(1) DEFAULT '0' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user, id_movie)
);

-- Create indexes for performance
CREATE INDEX idx_users_login ON users(login);
CREATE INDEX idx_user_reviews_movie ON user_reviews(id_movie);
CREATE INDEX idx_user_reviews_date ON user_reviews(review_date);
CREATE INDEX idx_user_reviews_rating ON user_reviews(rating);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_reviews_updated_at BEFORE UPDATE ON user_reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE users IS 'User accounts for movie reviews and ratings';
COMMENT ON TABLE user_reviews IS 'User reviews and ratings for movies';
COMMENT ON COLUMN user_reviews.sync_token IS 'Token for backup synchronization (0=synced, 1=pending)';
