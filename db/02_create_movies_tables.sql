-- Movies Database System - Movie Tables Migration
-- @SOURCE: movies_sql_procedures/movies_tables/create_movies_tables.sql::CREATE TABLE COUNTRIES::IsoCountry  VARCHAR2(2)     CONSTRAINT COUNTRIES_PK      PRIMARY KEY
-- Migrated from Oracle SQL to PostgreSQL
-- Original: Romain VINDERS - 2322

-- Drop existing tables if they exist
DROP TABLE IF EXISTS movie_prod_comps CASCADE;
DROP TABLE IF EXISTS movie_directors CASCADE;
DROP TABLE IF EXISTS movie_actors CASCADE;
DROP TABLE IF EXISTS movie_genres CASCADE;
DROP TABLE IF EXISTS movie_languages CASCADE;
DROP TABLE IF EXISTS movie_countries CASCADE;
DROP TABLE IF EXISTS movies CASCADE;
DROP TABLE IF EXISTS prod_comps CASCADE;
DROP TABLE IF EXISTS directors CASCADE;
DROP TABLE IF EXISTS actors CASCADE;
DROP TABLE IF EXISTS movies_status CASCADE;
DROP TABLE IF EXISTS languages CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS certifications CASCADE;

-- Create reference tables (countries, languages, genres, certifications, status)
CREATE TABLE countries (
    iso_country VARCHAR(2) PRIMARY KEY,
    name VARCHAR(24) UNIQUE NOT NULL
);

CREATE TABLE languages (
    iso_lang VARCHAR(2) PRIMARY KEY,
    name VARCHAR(11) UNIQUE NOT NULL
);

CREATE TABLE genres (
    id_genre INTEGER PRIMARY KEY,
    name VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE certifications (
    id_certif SERIAL PRIMARY KEY,
    name VARCHAR(12) UNIQUE NOT NULL
);

CREATE TABLE movies_status (
    id_status SERIAL PRIMARY KEY,
    name VARCHAR(15) UNIQUE NOT NULL
);

-- Create entity tables (actors, directors, production companies)
CREATE TABLE actors (
    id_actor INTEGER PRIMARY KEY,
    name VARCHAR(36) UNIQUE NOT NULL
);

CREATE TABLE directors (
    id_director INTEGER PRIMARY KEY,
    name VARCHAR(23) UNIQUE NOT NULL
);

CREATE TABLE prod_comps (
    id_comp INTEGER PRIMARY KEY,
    name VARCHAR(44) UNIQUE NOT NULL
);

-- Create movies table
CREATE TABLE movies (
    id_movie INTEGER PRIMARY KEY,
    title VARCHAR(58) NOT NULL,
    title_orig VARCHAR(59) NOT NULL,
    release_date DATE,
    id_status INTEGER NOT NULL REFERENCES movies_status(id_status) ON DELETE CASCADE,
    vote_average NUMERIC(3,1) NOT NULL CHECK (vote_average >= 0 AND vote_average <= 10),
    vote_count INTEGER NOT NULL,
    runtime INTEGER,
    id_certif INTEGER REFERENCES certifications(id_certif) ON DELETE CASCADE,
    poster_path VARCHAR(32),
    budget BIGINT,
    revenue BIGINT,
    homepage VARCHAR(122),
    tagline VARCHAR(172),
    overview VARCHAR(949),
    sync_token CHAR(1) DEFAULT '0' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create association tables (junction tables)
CREATE TABLE movie_countries (
    id_movie INTEGER REFERENCES movies(id_movie) ON DELETE CASCADE,
    iso_country VARCHAR(2) REFERENCES countries(iso_country) ON DELETE CASCADE,
    PRIMARY KEY (id_movie, iso_country)
);

CREATE TABLE movie_languages (
    id_movie INTEGER REFERENCES movies(id_movie) ON DELETE CASCADE,
    iso_lang VARCHAR(2) REFERENCES languages(iso_lang) ON DELETE CASCADE,
    PRIMARY KEY (id_movie, iso_lang)
);

CREATE TABLE movie_genres (
    id_movie INTEGER REFERENCES movies(id_movie) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES genres(id_genre) ON DELETE CASCADE,
    PRIMARY KEY (id_movie, id_genre)
);

CREATE TABLE movie_actors (
    id_movie INTEGER NOT NULL REFERENCES movies(id_movie) ON DELETE CASCADE,
    id_actor INTEGER NOT NULL REFERENCES actors(id_actor) ON DELETE CASCADE,
    character_name VARCHAR(36) NOT NULL,
    PRIMARY KEY (id_movie, id_actor, character_name)
);

CREATE TABLE movie_directors (
    id_movie INTEGER REFERENCES movies(id_movie) ON DELETE CASCADE,
    id_director INTEGER REFERENCES directors(id_director) ON DELETE CASCADE,
    PRIMARY KEY (id_movie, id_director)
);

CREATE TABLE movie_prod_comps (
    id_movie INTEGER REFERENCES movies(id_movie) ON DELETE CASCADE,
    id_comp INTEGER REFERENCES prod_comps(id_comp) ON DELETE CASCADE,
    PRIMARY KEY (id_movie, id_comp)
);

-- Add foreign key from user_reviews to movies
ALTER TABLE user_reviews
ADD CONSTRAINT user_reviews_id_movie_fk
FOREIGN KEY (id_movie) REFERENCES movies(id_movie) ON DELETE CASCADE;

-- Create indexes for performance
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_release_date ON movies(release_date);
CREATE INDEX idx_movies_vote_average ON movies(vote_average);
CREATE INDEX idx_movies_status ON movies(id_status);

CREATE INDEX idx_movie_countries_country ON movie_countries(iso_country);
CREATE INDEX idx_movie_languages_lang ON movie_languages(iso_lang);
CREATE INDEX idx_movie_genres_genre ON movie_genres(id_genre);
CREATE INDEX idx_movie_actors_actor ON movie_actors(id_actor);
CREATE INDEX idx_movie_actors_character ON movie_actors(character_name);
CREATE INDEX idx_movie_directors_director ON movie_directors(id_director);
CREATE INDEX idx_movie_prod_comps_comp ON movie_prod_comps(id_comp);

CREATE INDEX idx_actors_name ON actors(name);
CREATE INDEX idx_directors_name ON directors(name);

-- Apply updated_at triggers
CREATE TRIGGER update_movies_updated_at BEFORE UPDATE ON movies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE movies IS 'Main movies table with metadata';
COMMENT ON TABLE movie_actors IS 'Junction table linking movies to actors with character names';
COMMENT ON TABLE movie_directors IS 'Junction table linking movies to directors';
COMMENT ON TABLE movie_genres IS 'Junction table linking movies to genres';
COMMENT ON TABLE movie_countries IS 'Junction table linking movies to production countries';
COMMENT ON TABLE movie_languages IS 'Junction table linking movies to languages';
COMMENT ON TABLE movie_prod_comps IS 'Junction table linking movies to production companies';
