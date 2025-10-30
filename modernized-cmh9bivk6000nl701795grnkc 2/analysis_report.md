# Codebase Analysis Report: Movies Database System

**Analysis Date:** 2025-10-27
**Project Name:** Movies Database SQL Management (Rennequinepolis)
**Source Location:** `/app/temp/job_mod_cmh9bivk6000nl701795grnkc_1761580462_prog_movies_database_2015`
**Target Language:** Python
**Original Author:** Romain Vinders
**Original Date:** 2015
**Original License:** GPLv2

---

## 1. Source Language and Version Identification

### Primary Languages
- **Java SE 7** (source/target version 1.7)
- **Oracle SQL** and **PL/SQL**

### Key Indicators
- **Java Version:** Java 1.7 (specified in `nbproject/project.properties`: `javac.source=1.7`, `javac.target=1.7`)
- **Database:** Oracle Database XE (Express Edition) with Oracle JDBC driver (`ojdbc6.jar`)
- **GUI Framework:** Java Swing (Javax Swing components)
- **IDE:** NetBeans (indicated by nbproject structure and build.xml)
- **Build System:** Apache Ant (build.xml)

### Dependencies
- Oracle JDBC Driver 6 (`ojdbc6.jar`) - for Oracle database connectivity
- Java Swing - for GUI components
- Oracle SQL types and custom PL/SQL types

---

## 2. File Count and Categorization

### Total Files: 49 (excluding .git directory)

### File Breakdown by Type

| File Type | Count | Category | Description |
|-----------|-------|----------|-------------|
| SQL | 28 | Core Database | PL/SQL procedures, schemas, triggers, jobs |
| Java | 6 | Core Application | GUI application and database access layer |
| Form | 5 | UI Assets | NetBeans GUI form definitions (.form files) |
| XML | 4 | Configuration | NetBeans project and build configurations |
| Properties | 3 | Configuration | NetBeans and build properties |
| JAR | 1 | Vendor Dependency | Oracle JDBC driver (ojdbc6.jar) |
| Manifest | 1 | Configuration | JAR manifest file |
| Markdown | 1 | Documentation | README.md |

### Detailed Categorization

#### **Core Database Files (28 SQL files)**
- **Base Tables** (3 files): User management, reviews, logging
- **Movie Tables** (4 files): Movie entities, import, external tables, statistics
- **CB Database Procedures** (4 files): Main database backup, search, evaluation packages
- **CBB Database Procedures** (4 files): Backup database restore, search, evaluation packages
- **Schema Setup** (2 files): Role/user creation, logging setup
- **Command Scripts** (11 files): Setup and testing commands

#### **Core Application Files (6 Java files)**
- `Rennequinepolis.java` - Main application frame and entry point
- `LoginSingleton.java` - Database connection management and SQL execution
- `DialogLogin.java` - Login dialog
- `DialogMovie.java` - Movie details display dialog
- `DialogWriteVote.java` - User review submission dialog
- `DialogShowVotes.java` - User reviews display dialog

#### **Configuration Files (9 files)**
- NetBeans project files (4 XML, 3 properties)
- Build configuration (build.xml, manifest.mf)

#### **Vendor Dependencies (1 file)**
- `ojdbc6.jar` - Oracle JDBC driver (cannot be migrated, needs Python equivalent)

---

## 3. Folder Structure Analysis

```
movies_database_2015/
├── README.md                          # Project documentation
├── movies_gui_app/                    # Java Swing GUI application
│   ├── build.xml                      # Ant build script
│   ├── manifest.mf                    # JAR manifest
│   ├── ojdbc6.jar                     # Oracle JDBC driver (VENDOR)
│   ├── nbproject/                     # NetBeans project files (IDE-specific)
│   │   ├── build-impl.xml
│   │   ├── genfiles.properties
│   │   ├── project.xml
│   │   ├── project.properties
│   │   └── private/
│   │       ├── private.properties
│   │       └── private.xml
│   └── src/sgbdrennequinepolis/      # Source code
│       ├── Rennequinepolis.java      # Main frame (ENTRYPOINT)
│       ├── Rennequinepolis.form
│       ├── LoginSingleton.java        # DB connection (SERVICE)
│       ├── DialogLogin.java           # Login dialog
│       ├── DialogLogin.form
│       ├── DialogMovie.java           # Movie details dialog
│       ├── DialogMovie.form
│       ├── DialogWriteVote.java       # Write review dialog
│       ├── DialogWriteVote.form
│       ├── DialogShowVotes.java       # Show reviews dialog
│       └── DialogShowVotes.form
│
├── movies_sql_add_cmd/                # SQL command scripts (SETUP)
│   ├── CMD1_START_BACKUP_RESTORE.sql  # Initial setup
│   ├── CMD2_START_CREA.sql            # Create tables
│   ├── CMD3_START_ALIM.sql            # Data population
│   ├── CMD4_START_RECH.sql            # Search setup
│   ├── CMD5_START_BACKUP.sql          # Backup setup
│   ├── CMD5_TESTS_BACKUP.sql          # Backup tests
│   ├── CMD6_CRASH_OFF.sql             # Disable crash simulation
│   ├── CMD6_CRASH_ON.sql              # Enable crash simulation
│   ├── CMD6_START_EVAL.sql            # Evaluation setup
│   └── CMD6_START_RECH.sql            # Search setup
│
└── movies_sql_procedures/             # SQL procedures and schemas
    ├── base_tables/                   # User and review tables
    │   ├── create_base_tables.sql
    │   ├── create_base_tables_triggers.sql
    │   └── alter_base_tables_for_movies.sql
    ├── movies_tables/                 # Movie entity tables
    │   ├── create_movies_tables.sql
    │   ├── movies_external_table.sql
    │   ├── import_movies.sql
    │   └── movies_stats.sql
    ├── cb/                            # Main database (CB)
    │   ├── cb_dblink.sql              # DB link to CBB
    │   ├── cb_backup.sql              # Backup procedures
    │   ├── cb_backup_full.sql         # Full backup
    │   └── eval_movies/
    │       ├── find_movies.sql        # Search package
    │       └── eval_movies.sql        # Evaluation package
    ├── cbb/                           # Backup database (CBB)
    │   ├── cbb_dblink.sql             # DB link to CB
    │   ├── cbb_restore.sql            # Restore procedures
    │   └── eval_movies/
    │       ├── find_movies.sql        # Search package
    │       └── eval_movies.sql        # Evaluation package
    ├── create_log.sql                 # Logging tables/procedures
    └── create_role_user.sql           # User roles setup
```

---

## 4. Main Business Flows

### Overview
The application is a **movie database management system** with features for searching movies, viewing details, and submitting/viewing user reviews. It implements a **dual-database architecture** with automatic failover for high availability.

### Business Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTIONS                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. LOGIN FLOW                                               │
│     • User enters login via DialogLogin                      │
│     • Login stored in LoginSingleton                         │
│     • No password validation (simplified authentication)     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SEARCH FLOW                                              │
│     ┌─────────────────────────────────────────┐             │
│     │ A. Search by Movie ID                   │             │
│     │    • Direct ID lookup                   │             │
│     │    • Calls: GetMovieById stored proc    │             │
│     │    • Returns single movie details       │             │
│     └─────────────────────────────────────────┘             │
│     ┌─────────────────────────────────────────┐             │
│     │ B. Advanced Search                      │             │
│     │    • Title (partial match)              │             │
│     │    • Year (exact, min, max)             │             │
│     │    • Actors (multiple)                  │             │
│     │    • Directors (multiple)               │             │
│     │    • Calls: FindMovies stored proc      │             │
│     │    • Returns list of matching movies    │             │
│     │    • Max 30 results displayed           │             │
│     └─────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. MOVIE DETAILS FLOW                                       │
│     • Display movie information (DialogMovie)                │
│     • Title, original title, release year                    │
│     • TMDB ratings (vote average, count)                     │
│     • App ratings (RQS - Rennequinepolis votes)             │
│     • Runtime, budget, revenue                               │
│     • Status, certification                                  │
│     • Overview/description                                   │
│     • Genres, actors, characters                             │
│     • Directors, production companies                        │
│     • Countries, languages                                   │
│     • Poster path (image reference)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. USER REVIEW FLOW                                         │
│     ┌─────────────────────────────────────────┐             │
│     │ A. Write Review (DialogWriteVote)       │             │
│     │    • Rating slider (0-10)               │             │
│     │    • Review text (max 200 chars)        │             │
│     │    • Calls: AddUserReview stored proc   │             │
│     │    • Stored with timestamp              │             │
│     └─────────────────────────────────────────┘             │
│     ┌─────────────────────────────────────────┐             │
│     │ B. View Reviews (DialogShowVotes)       │             │
│     │    • Paginated display (5 per page)     │             │
│     │    • Shows: user, date, rating, review  │             │
│     │    • Calls: GetVotes stored proc        │             │
│     └─────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. DATABASE FAILOVER FLOW                                   │
│     • Primary: CB database (Cinema Base)                     │
│     • Backup: CBB database (Cinema Base Backup)              │
│     ┌─────────────────────────────────────────┐             │
│     │ Crash Detection Logic:                  │             │
│     │  • SQLException 28000 on CB = crash     │             │
│     │  • SQLException 20400 on CBB = CB ready │             │
│     │  • Automatic switch to backup DB        │             │
│     │  • Automatic restore when CB available  │             │
│     │  • Retry failed operation on new DB     │             │
│     └─────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  6. BACKGROUND PROCESSES                                     │
│     • Backup triggers (on data insert/update)                │
│     • Scheduled backup jobs (periodic)                       │
│     • Scheduled restore jobs (when CB available)             │
│     • DB link synchronization (CB <-> CBB)                   │
│     • Data import from external files (182 MB text file)     │
└─────────────────────────────────────────────────────────────┘
```

### Key Business Operations

1. **Movie Search**
   - Entry: `Rennequinepolis.jBtnSearchActionPerformed()`
   - Service: `LoginSingleton.findMoviesRequest()`
   - DB Procedure: `SEARCH_PACKAGE.FindMovies`
   - Returns: ResultSet with movie list

2. **Movie Details Retrieval**
   - Entry: `Rennequinepolis.getMovie()`
   - Service: `LoginSingleton.getMovieRequest()`
   - DB Procedure: `SEARCH_PACKAGE.GetMovieById`
   - Returns: Struct (MovieObj_t)

3. **Review Submission**
   - Entry: `DialogWriteVote.jConfirmBtnActionPerformed()`
   - Service: `LoginSingleton.writeVoteRequest()`
   - DB Procedure: `EVAL_PACKAGE.AddUserReview`
   - Effect: Inserts review, triggers backup

4. **Review Listing**
   - Entry: `DialogShowVotes.getVotes()`
   - Service: `LoginSingleton.showVotesRequest()`
   - DB Procedure: `SEARCH_PACKAGE.GetVotes`
   - Returns: Array of Struct (VoteListItem_t)

---

## 5. Entrypoints, Routes, Services, and Models

### Application Architecture

#### **Entrypoint**
- **Main Class:** `sgbdrennequinepolis.Rennequinepolis`
- **Main Method:** `Rennequinepolis.main()` at line 587
- **Launch:** Creates main JFrame window with event-driven Swing GUI

#### **Routes/Navigation** (GUI-based, not web routes)
```
Main Window (Rennequinepolis)
├── Search by ID → DialogMovie
├── Advanced Search → Results List → DialogMovie
└── DialogMovie
    ├── Write Review → DialogWriteVote → (requires DialogLogin)
    └── View Reviews → DialogShowVotes
```

#### **Services Layer** (Database Access)
- **Service Class:** `LoginSingleton` (Singleton pattern)
- **Methods:**
  - `startConnection()` - Establishes Oracle DB connection
  - `checkCrash()` - Detects and handles database failures
  - `findMoviesRequest()` - Search movies with filters
  - `getMovieRequest()` - Retrieve movie by ID
  - `writeVoteRequest()` - Submit user review
  - `showVotesRequest()` - Retrieve reviews with pagination

#### **Models/Data Structures**

**Java Models:**
- HashMap<String, String> for actors/directors filters
- HashMap<String, Integer> for search results
- DefaultListModel for UI lists
- Oracle Struct types for complex data transfer

**Database Models (Oracle Custom Types):**
```sql
StringArray_t        - VARCHAR2(4000) array
MovieObj_t           - Complex movie object with nested arrays
VoteListItem_t       - Single review/vote item
VotesList_t          - Array of vote items
```

**Database Tables:**

*Base Tables (CB and CBB):*
- `USERS` - User accounts (IdUser, Login, SyncToken)
- `USER_REVIEWS` - User reviews (IdUser, IdMovie, Rating, Review, ReviewDate)
- `LOG_MESSAGES` - System logs

*Movie Tables (CB only):*
- `MOVIES` - Main movie table
- `ACTORS`, `DIRECTORS`, `PROD_COMPS` - Person/company entities
- `GENRES`, `COUNTRIES`, `LANGUAGES`, `CERTIFICATIONS`, `MOVIES_STATUS` - Lookup tables
- `MOVIE_ACTORS`, `MOVIE_DIRECTORS`, `MOVIE_GENRES`, etc. - Junction tables

#### **State Management**
- **Connection State:** Managed in `LoginSingleton`
  - `_connex` - Active database connection
  - `_callStatement` - Active callable statement
  - `_login` - Current user login
  - `_secondaryServer` - Boolean flag (CB vs CBB)

- **UI State:** Managed in individual JFrame/JDialog instances
  - Form field values
  - List models for dynamic content
  - Error labels for user feedback

---

## 6. Database Architecture

### Dual-Database System

**CB (Cinema Base)** - Primary Database
- Holds all movie data
- Handles user operations
- Automatic backup to CBB via triggers
- DB Link to CBB: `DBLINK_CBB`

**CBB (Cinema Base Backup)** - Backup Database
- Mirrors user data from CB
- Used during CB failures (crash simulation)
- Automatic restore from CB when available
- DB Link to CB: `DBLINK_CB`

### PL/SQL Packages

**SEARCH_PACKAGE** (CB and CBB)
- `FindMovies()` - Complex search with multiple filters
- `GetMovieById()` - Retrieve single movie details
- `GetVotes()` - Paginated review retrieval

**EVAL_PACKAGE** (CB and CBB)
- `AddUserReview()` - Insert user review/rating

**BACKUP_PACKAGE** (CB)
- Backup procedures for user data
- Triggers on INSERT/UPDATE to USER_REVIEWS

**RESTORE_PACKAGE** (CBB)
- Restoration procedures from CB
- Scheduled jobs to sync data

**LOG_PACKAGE** (CB and CBB)
- Logging utilities for system operations

---

## 7. Assets and Directly Copyable Files

### Files That Can Be Copied Without Changes

#### **Documentation**
- `README.md` - Can be adapted for Python project (needs content update)

### Files That Need Python Equivalents (Cannot Be Directly Copied)

#### **SQL Files (28 files)** - **REQUIRE MIGRATION TO PYTHON-COMPATIBLE DATABASE**
- Oracle-specific syntax (PL/SQL, custom types, DB links)
- Needs migration to PostgreSQL, MySQL, or SQLite with SQLAlchemy
- **Priority:** High - Core business logic resides here

#### **Java Files (6 files)** - **REQUIRE COMPLETE REWRITE**
- Java Swing GUI → Python GUI framework (Tkinter, PyQt, or Web-based with Flask/Django)
- Oracle JDBC → Python DB driver (cx_Oracle, psycopg2, or mysql-connector-python)
- **Priority:** High - Application logic

#### **Form Files (5 files)** - **NOT COPYABLE**
- NetBeans-specific GUI designer files
- Need manual recreation in Python GUI framework
- **Priority:** Medium - UI can be redesigned

#### **Configuration Files (9 files)** - **NOT COPYABLE**
- NetBeans and Ant-specific
- Python equivalents: requirements.txt, setup.py, pyproject.toml
- **Priority:** Medium - New build system needed

#### **JAR File (1 file)** - **NOT COPYABLE**
- Oracle JDBC driver
- Python equivalent: cx_Oracle, oracledb, or migrate to PostgreSQL with psycopg2
- **Priority:** High - Database connectivity

---

## 8. Migration Complexity Assessment

### Complexity Rating: **HIGH**

#### Factors Contributing to High Complexity

1. **Database Technology**
   - Heavy use of Oracle-specific features (PL/SQL packages, custom types, DB links)
   - Dual-database architecture with automatic failover
   - Triggers and scheduled jobs
   - External tables for data import

2. **GUI Framework**
   - Extensive Java Swing GUI (5 dialog/frame classes)
   - Event-driven architecture
   - Complex layouts (GroupLayout)
   - NetBeans Form Designer dependencies

3. **Business Logic Distribution**
   - Significant logic in PL/SQL stored procedures
   - Java acts as thin client layer
   - Need to decide: keep in DB or move to Python?

4. **Data Types**
   - Custom Oracle STRUCT and ARRAY types
   - Conversion to Python equivalents needed

### Estimated Migration Effort

| Component | Lines of Code | Complexity | Effort (Days) |
|-----------|--------------|------------|---------------|
| SQL → Python ORM/SQL | ~2000 lines | High | 10-15 |
| Java GUI → Python GUI | ~1500 lines | High | 15-20 |
| Database Schema Migration | ~500 lines | Medium | 5-7 |
| Testing & Debugging | N/A | High | 10-15 |
| **Total** | **~4000 lines** | **High** | **40-57 days** |

---

## 9. Recommended Migration Strategy

### Phase 1: Database Migration (Week 1-3)

**Option A: Keep Oracle Database**
- Migrate Java to Python with cx_Oracle/oracledb
- Minimal SQL changes needed
- Preserve existing PL/SQL packages
- **Pros:** Faster, preserves business logic
- **Cons:** Oracle dependency, licensing costs

**Option B: Migrate to PostgreSQL** (Recommended)
- Convert PL/SQL packages to Python + SQLAlchemy
- Use PostgreSQL for open-source solution
- Migrate custom types to JSON or composite types
- **Pros:** Open-source, Python-native, portable
- **Cons:** More effort, logic redistribution

**Recommended:** Option B with PostgreSQL + SQLAlchemy

### Phase 2: Application Layer Migration (Week 4-6)

**GUI Options:**

1. **Desktop GUI - Tkinter** (Easiest)
   - Built-in with Python
   - Direct Swing equivalent
   - Good for quick migration

2. **Desktop GUI - PyQt5/6** (Better UX)
   - More modern look
   - Better widgets
   - Commercial licensing considerations

3. **Web Application - Flask/Django** (Modern)
   - Modern architecture
   - Better maintainability
   - Multi-user support
   - **Recommended for new development**

**Recommended:** Flask/Django web application with REST API

### Phase 3: Testing & Validation (Week 7-8)

- Unit tests for database operations
- Integration tests for business flows
- UI/UX testing
- Performance testing
- Failover testing (dual-database)

---

## 10. Technology Recommendations for Python Migration

### Core Stack Recommendation

```yaml
Language: Python 3.11+
Database: PostgreSQL 15+
ORM: SQLAlchemy 2.0+
Web Framework: Flask 3.0+ or Django 4.2+
Frontend: Bootstrap 5 + Jinja2 templates (Flask) or Django templates
Authentication: Flask-Login or Django Auth
Database Driver: psycopg2 or psycopg3
Testing: pytest + pytest-flask/pytest-django
```

### Alternative Stack (Desktop Application)

```yaml
Language: Python 3.11+
GUI Framework: PyQt6 or Tkinter
Database: PostgreSQL 15+ or SQLite 3
ORM: SQLAlchemy 2.0+
Database Driver: psycopg2 (PostgreSQL) or sqlite3 (SQLite)
Testing: pytest + pytest-qt
```

### Package Structure (Web Application)

```
movies_app/
├── app/
│   ├── __init__.py
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── movie.py
│   │   └── review.py
│   ├── services/            # Business logic (from PL/SQL)
│   │   ├── __init__.py
│   │   ├── search_service.py
│   │   ├── movie_service.py
│   │   └── review_service.py
│   ├── routes/              # Flask blueprints/Django views
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── movies.py
│   │   └── reviews.py
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── search.html
│   │   ├── movie_detail.html
│   │   └── reviews.html
│   └── static/              # CSS, JS, images
│       ├── css/
│       └── js/
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_routes.py
├── migrations/              # Alembic migrations
├── config.py
├── requirements.txt
└── run.py
```

---

## 11. Key Migration Considerations

### Critical Issues to Address

1. **Database Failover Mechanism**
   - Current: SQLException-based detection
   - Python: Implement connection pooling with automatic retry
   - Consider: PostgreSQL streaming replication or pgpool-II

2. **Data Import (182 MB File)**
   - Current: Oracle external tables
   - Python: Pandas for CSV/text parsing, bulk insert with SQLAlchemy

3. **Custom Type Handling**
   - Oracle STRUCT → Python dataclasses or Pydantic models
   - Oracle ARRAY → Python lists
   - Oracle CURSOR → SQLAlchemy result proxies

4. **Stored Procedures**
   - Option A: Migrate to Python service layer (recommended)
   - Option B: Use PostgreSQL functions (if staying close to original)

5. **Character Encoding**
   - Current SQL files contain French text with special characters
   - Ensure UTF-8 encoding throughout Python application

6. **Pagination**
   - Current: Manual page-based queries
   - Python: Flask-SQLAlchemy pagination or Django Paginator

### Security Considerations

**Current Issues:**
- No password authentication (login only)
- SQL injection risks (minimized by CallableStatement)
- Hardcoded database credentials in code

**Python Best Practices:**
- Implement proper authentication (Flask-Login, Django Auth)
- Use environment variables for credentials
- CSRF protection (built-in with Flask-WTF/Django)
- SQL injection prevention (SQLAlchemy parameterization)
- Input validation (WTForms, Django Forms, or Pydantic)

---

## 12. Migration Prioritization

### High Priority (Must Migrate)

1. **Core Database Schema** - Foundation for everything
2. **Movie Search Functionality** - Primary use case
3. **Movie Details Display** - Core feature
4. **Database Connection Management** - Critical infrastructure
5. **User Review System** - Key business feature

### Medium Priority (Should Migrate)

6. **User Authentication** - Improve existing simple login
7. **Pagination** - Better UX for large result sets
8. **Database Failover** - High availability feature
9. **Data Import** - Initial data loading

### Low Priority (Nice to Have)

10. **Backup/Restore Jobs** - Can be implemented later with cron/celery
11. **Logging System** - Python has built-in logging
12. **Advanced Search Filters** - Can be enhanced iteratively

---

## 13. Risk Assessment

### High Risks

1. **Data Loss During Migration**
   - Mitigation: Backup all data, test migration on copy first

2. **Functional Gaps**
   - Mitigation: Comprehensive test suite, feature parity checklist

3. **Performance Degradation**
   - Mitigation: Database indexing, query optimization, caching

### Medium Risks

4. **Learning Curve for New Stack**
   - Mitigation: Training, documentation, code reviews

5. **UI/UX Changes**
   - Mitigation: User testing, iterative design

### Low Risks

6. **Deployment Issues**
   - Mitigation: Docker containerization, CI/CD pipeline

---

## 14. Success Criteria

### Functional Requirements
- [ ] All 5 main business flows working
- [ ] Search by ID returns correct movie
- [ ] Advanced search with all filters working
- [ ] Movie details display all fields correctly
- [ ] User can submit reviews
- [ ] User can view paginated reviews
- [ ] User authentication working

### Non-Functional Requirements
- [ ] Response time < 2 seconds for searches
- [ ] Support 100+ concurrent users (web version)
- [ ] 99.9% uptime (with failover)
- [ ] All data migrated with 100% accuracy
- [ ] Code coverage > 80%

### Technical Requirements
- [ ] Python 3.11+ compatible
- [ ] PostgreSQL database fully functional
- [ ] RESTful API design (if web-based)
- [ ] Docker deployment ready
- [ ] Comprehensive documentation

---

## 15. Next Steps

### Immediate Actions

1. **Set up development environment**
   - Install Python 3.11+
   - Install PostgreSQL 15+
   - Set up virtual environment
   - Install base packages (Flask/Django, SQLAlchemy, psycopg2)

2. **Create database schema**
   - Design PostgreSQL schema based on Oracle tables
   - Create SQLAlchemy models
   - Set up Alembic migrations
   - Import sample data

3. **Implement core services**
   - Movie search service
   - Movie details service
   - User authentication service
   - Review management service

4. **Build MVP (Minimum Viable Product)**
   - Basic web interface
   - Search functionality
   - Movie details view
   - Review submission

5. **Iterative development**
   - Add advanced search filters
   - Implement pagination
   - Add user authentication
   - Implement database failover
   - Add data import functionality

---

## Appendix A: File Mapping (Java → Python)

| Original Java File | Target Python Module | Responsibility |
|-------------------|---------------------|----------------|
| Rennequinepolis.java | routes/search.py | Search routes/views |
| LoginSingleton.java | services/db_service.py | DB connection management |
| DialogMovie.java | routes/movies.py + templates/movie_detail.html | Movie display |
| DialogWriteVote.java | routes/reviews.py + templates/write_review.html | Review submission |
| DialogShowVotes.java | routes/reviews.py + templates/show_reviews.html | Review display |
| DialogLogin.java | routes/auth.py + templates/login.html | Authentication |

## Appendix B: SQL Procedure Mapping

| Oracle Procedure | Target Python Function | Location |
|-----------------|------------------------|----------|
| SEARCH_PACKAGE.FindMovies | search_movies() | services/search_service.py |
| SEARCH_PACKAGE.GetMovieById | get_movie_by_id() | services/movie_service.py |
| SEARCH_PACKAGE.GetVotes | get_reviews_paginated() | services/review_service.py |
| EVAL_PACKAGE.AddUserReview | add_user_review() | services/review_service.py |
| BACKUP_PACKAGE.* | Background tasks with Celery | tasks/backup_tasks.py |
| RESTORE_PACKAGE.* | Background tasks with Celery | tasks/restore_tasks.py |

---

**End of Analysis Report**
