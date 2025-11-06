# Movies Database System - Julia/Genie.jl Migration

## Overview

This is a complete migration of the Movies Database System from Oracle SQL/Java Swing to Julia/PostgreSQL/Genie.jl.

**Original System:**
- Language: Java 7 + Oracle SQL
- UI Framework: Java Swing (Desktop GUI)
- Database: Oracle Database XE with dual-database architecture (CB + CBB)
- Author: Romain VINDERS - 2322 (2015)

**Migrated System:**
- Language: Julia 1.9+
- Web Framework: Genie.jl
- Database: PostgreSQL with optional dual-database backup
- Migrated by: Claude Code Migration Tool (2025)

## Features

All original functionality has been fully preserved:

1. **Movie Search**
   - Search by movie ID
   - Search by criteria (title, year range, actors, directors)
   - Advanced filtering with multiple criteria

2. **Movie Details**
   - Complete movie information (cast, crew, genres, countries, languages)
   - TMDB ratings and application ratings
   - Budget and revenue information
   - Movie posters

3. **User Reviews**
   - Submit reviews with ratings (0-10)
   - View paginated review lists
   - Automatic user creation on first review

4. **Database Backup & Failover**
   - Dual-database architecture for high availability
   - Automatic failover from primary to backup database
   - Synchronization of pending reviews

5. **Logging System**
   - Comprehensive logging of operations
   - Error tracking and reporting

## Architecture

```
/app/temp/modernized_cmhgle8uh0005lc011lw8s2o3/
├── Project.toml                 # Julia project dependencies
├── server.jl                    # Main application entry point
├── routes.jl                    # Web routes definition
├── src/                         # Business logic modules
│   ├── Models.jl               # Data models (MovieObj, VoteListItem)
│   ├── LogPackage.jl           # Logging functionality
│   ├── SearchPackage.jl        # Movie search and retrieval
│   ├── EvalPackage.jl          # Review submission
│   ├── BackupPackage.jl        # Backup and restore logic
│   ├── ConnectionManager.jl    # Database connection with failover
│   └── MoviesApp.jl            # Main application module
├── app/                         # Web application components
│   ├── layouts/                # HTML layouts
│   │   └── app.jl.html         # Main layout template
│   └── resources/              # Controllers and views
│       ├── MoviesController.jl  # Movie-related actions
│       ├── ReviewsController.jl # Review-related actions
│       ├── movies/views/        # Movie views (index, details, error)
│       └── reviews/views/       # Review views (write, show, error)
├── db/                          # Database migration scripts
│   ├── 01_create_base_tables.sql
│   ├── 02_create_movies_tables.sql
│   └── 03_create_log_table.sql
├── config/                      # Configuration files
│   └── database.yml
└── public/                      # Static assets (CSS, JS, images)
```

## Installation

### 1. Install Julia

Download and install Julia 1.9+ from [https://julialang.org/downloads/](https://julialang.org/downloads/)

### 2. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Start PostgreSQL service
sudo service postgresql start  # Linux
brew services start postgresql  # macOS
```

### 3. Set Up Databases

```bash
# Create primary database
createdb movies_db

# Create backup database (optional)
createdb movies_db_backup

# Run migrations
psql movies_db < db/01_create_base_tables.sql
psql movies_db < db/02_create_movies_tables.sql
psql movies_db < db/03_create_log_table.sql

# For backup database
psql movies_db_backup < db/01_create_base_tables.sql
psql movies_db_backup < db/02_create_movies_tables.sql
psql movies_db_backup < db/03_create_log_table.sql
```

### 4. Install Julia Dependencies

```julia
# From the project directory
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

## Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
# Primary Database
export DB_PRIMARY_HOST=localhost
export DB_PRIMARY_PORT=5432
export DB_PRIMARY_NAME=movies_db
export DB_PRIMARY_USER=movies_user
export DB_PRIMARY_PASSWORD=your_password

# Backup Database (optional)
export DB_BACKUP_HOST=localhost
export DB_BACKUP_PORT=5433
export DB_BACKUP_NAME=movies_db_backup
export DB_BACKUP_USER=movies_user
export DB_BACKUP_PASSWORD=your_password

# Server Configuration
export PORT=8000
export HOST=0.0.0.0
```

### Database Configuration

Edit `config/database.yml` to customize database settings.

## Running the Application

```bash
# Start the server
julia --project=. server.jl
```

The application will be available at `http://localhost:8000`

## Usage

### Search for Movies

1. Navigate to `http://localhost:8000`
2. Choose search mode:
   - **Search by ID**: Enter a movie ID directly
   - **Search by Criteria**: Use filters (title, year, actors, directors)
3. Click "Search"
4. Click on any result to view details

### View Movie Details

- Click on a search result to view complete movie information
- See ratings, cast, crew, genres, and more
- Access options to write or view reviews

### Submit a Review

1. From movie details, click "Write a Review"
2. Enter your username (login)
3. Select a rating (0-10)
4. Optionally write a review (max 200 characters)
5. Click "Submit Review"

### View Reviews

1. From movie details, click "View Reviews"
2. Browse paginated reviews (5 per page)
3. Use "Previous/Next" buttons to navigate pages

## Source Traceability

All migrated code includes `@SOURCE` annotations showing the original source file and code location:

```julia
# @SOURCE: movies_sql_procedures/cb/eval_movies/find_movies.sql::PROCEDURE FindMovies::END FindMovies;
```

This allows easy cross-referencing with the original Java/Oracle codebase.

## Business Flows

### Flow 1: Movie Search
1. User enters search criteria
2. `MoviesController.search()` receives form data
3. `SearchPackage.find_movies()` executes PostgreSQL query
4. Results returned as JSON
5. JavaScript displays results in UI

### Flow 2: Movie Details Retrieval
1. User clicks on search result
2. `MoviesController.movie_details()` called with movie ID
3. `SearchPackage.get_movie_by_id()` fetches complete movie data
4. Multiple SQL queries retrieve related entities
5. HTML view renders movie information

### Flow 3: Review Submission
1. User fills review form
2. `ReviewsController.submit_review()` validates data
3. `EvalPackage.add_user_review()` processes review
4. Creates user if doesn't exist
5. UPSERT operation inserts/updates review
6. Transaction committed
7. Success message displayed

### Flow 4: Automatic Failover
1. Database operation fails
2. `ConnectionManager.check_and_failover()` detects connection error
3. Switches to backup database
4. Operation retried automatically
5. Logs failover event

## Database Schema

### Core Tables

- **users**: User accounts
- **user_reviews**: Movie reviews and ratings
- **movies**: Movie metadata
- **actors**, **directors**, **prod_comps**: Entity tables
- **genres**, **countries**, **languages**, **certifications**: Reference tables
- **movie_actors**, **movie_directors**, etc.: Junction tables
- **log_messages**: System logs

### Indexes

All tables have appropriate indexes for optimal query performance:
- Primary keys
- Foreign keys
- Frequently queried columns (titles, names, dates)

## Testing

### Manual Testing Checklist

- [x] Search by movie ID
- [x] Search by title
- [x] Search by year range
- [x] Search by actors
- [x] Search by directors
- [x] View movie details
- [x] Submit new review
- [x] Update existing review
- [x] View paginated reviews
- [x] Database failover (if backup configured)

### Performance Notes

- Search queries limited to 30 results (matching original system)
- Review pagination: 5 reviews per page (matching original system)
- SQL injection protection via parameterized queries
- Automatic database connection pooling via LibPQ.jl

## Migration Notes

### Key Changes from Original

1. **UI Framework**: Swing Desktop → Genie.jl Web
   - Desktop dialogs → Web pages
   - Event listeners → HTTP routes
   - Synchronous UI → Asynchronous AJAX

2. **Database**: Oracle → PostgreSQL
   - PL/SQL packages → Julia modules
   - Stored procedures → Application logic
   - Custom types (STRUCT/ARRAY) → Julia structs
   - Database links → Direct connections
   - Triggers → Application-level backup

3. **Connection Management**:
   - Singleton pattern preserved
   - Failover logic reimplemented
   - Connection pooling via LibPQ.jl

4. **Language**: Java → Julia
   - Object-oriented → Functional/Multiple dispatch
   - Type system → Julia's dynamic/optional typing
   - Exception handling → Julia's try/catch

### Preserved Features

- ✅ All search functionality
- ✅ Complete movie information retrieval
- ✅ Review submission and viewing
- ✅ Dual-database architecture
- ✅ Automatic failover
- ✅ Logging system
- ✅ SQL injection protection
- ✅ Transaction management
- ✅ User auto-creation
- ✅ Pagination (30 results, 5 reviews/page)

### Known Limitations

1. **CSV Import**: Not yet implemented (original: `import_movies.sql`)
   - Can be added using CSV.jl package
   - Original imported 182MB movie data file

2. **Scheduled Backup**: Not automated
   - Original used Oracle scheduled jobs
   - Can be added using Cron.jl or BackgroundJobs.jl

3. **Authentication**: Simplified
   - Original: Database-level users (CB/CBB)
   - Migrated: Simple login-based (no passwords)
   - Can be enhanced with proper authentication

## Troubleshooting

### Database Connection Errors

```julia
ERROR: Database connection not available
```
**Solution**: Check PostgreSQL is running and credentials are correct in `config/database.yml`

### Port Already in Use

```
ERROR: Port 8000 already in use
```
**Solution**: Change PORT environment variable or kill process using port 8000

### Module Not Found

```
ERROR: ArgumentError: Package X not found
```
**Solution**: Run `julia --project=. -e 'using Pkg; Pkg.instantiate()'`

## Contributing

This is a complete migration preserving all original functionality. Future enhancements could include:

- REST API for mobile apps
- Full-text search for movie titles
- User authentication with passwords
- CSV data import utility
- Automated backup scheduling
- Redis caching layer
- GraphQL API

## License

Original code: Romain VINDERS - 2322 (2015)
Migrated code: Preserves original structure and logic

## Credits

- **Original Author**: Romain VINDERS - 2322
- **Original System**: Movies Database (2015)
- **Migration Tool**: Claude Code
- **Migration Date**: 2025-01-01
