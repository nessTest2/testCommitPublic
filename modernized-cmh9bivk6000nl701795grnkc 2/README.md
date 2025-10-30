# Movies Database Application (Rennequinepolis)

## Overview
This is a Python/PyQt6 desktop application for managing and searching a movie database. Originally developed in Java with Oracle database, this version has been modernized to use Python, PyQt6 for the GUI, and SQLAlchemy with SQLite for database management.

**Original Author:** Romain Vinders
**Original Date:** 2015
**License:** GPLv2
**Migrated:** 2025

## Features

### Core Functionality
1. **Movie Search**
   - Search by movie ID (direct lookup)
   - Advanced search with multiple filters:
     - Title (partial match)
     - Year (exact, minimum, maximum)
     - Multiple actors
     - Multiple directors
   - Display up to 30 results

2. **Movie Details**
   - Complete movie information display
   - Title, original title, release year
   - TMDB ratings and app ratings
   - Runtime, budget, revenue
   - Status, certification
   - Full description/overview
   - Genres, cast, characters
   - Directors, production companies
   - Countries, languages
   - Poster reference

3. **User Reviews**
   - Submit reviews with 0-10 rating scale
   - Write review text (up to 200 characters)
   - View paginated reviews (5 per page)
   - Display user, date, rating, and review text

4. **Database Failover**
   - Dual-database architecture simulation
   - Automatic failover to backup database
   - Automatic restore when primary available
   - Transparent error handling

## Architecture

### Technology Stack
- **Language:** Python 3.11+
- **GUI Framework:** PyQt6
- **Database:** SQLite with SQLAlchemy 2.0 ORM
- **Migration Tools:** Alembic (for future schema changes)

### Project Structure
```
movies_app/
├── main.py                     # Application entry point
├── models/                     # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py
│   ├── movie.py
│   ├── review.py
│   ├── person.py             # Actors, Directors
│   ├── company.py            # Production companies
│   └── lookup.py             # Genres, Countries, etc.
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── database_service.py   # Connection management
│   ├── search_service.py     # Movie search
│   ├── movie_service.py      # Movie details
│   └── review_service.py     # Reviews management
├── ui/                        # PyQt6 GUI components
│   ├── __init__.py
│   ├── main_window.py        # Main application window
│   ├── login_dialog.py       # User login dialog
│   ├── movie_dialog.py       # Movie details dialog
│   ├── write_vote_dialog.py  # Review submission
│   └── show_votes_dialog.py  # Reviews display
├── database/                  # Database setup
│   ├── __init__.py
│   ├── init_db.py            # Schema initialization
│   └── sample_data.py        # Test data
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m database.init_db

# Run application
python main.py
```

## Usage

### First Launch
1. The application will create a SQLite database (`movies.db`) on first run
2. Sample movie data will be loaded automatically
3. A login dialog will appear - enter any username (no password required)

### Searching Movies
**By ID:**
1. Select "Rechercher identifiant" (Search by ID)
2. Enter movie ID in spinner
3. Click "Rechercher" (Search)
4. Movie details will appear immediately

**Advanced Search:**
1. Select "Recherche avancée" (Advanced Search)
2. Fill in any combination of:
   - Title (partial match supported)
   - Year (exact, or use checkboxes for min/max range)
   - Actors (add multiple using the text field and "Ajouter" button)
   - Directors (add multiple using the text field and "Ajouter" button)
3. Click "Rechercher" (Search)
4. Results appear in the list (click to view details)

### Viewing Movie Details
- Click on any movie in the search results
- A dialog will open showing all movie information
- From here you can:
  - Write a review (button at bottom)
  - View existing reviews (button at bottom)

### Writing Reviews
1. Open movie details dialog
2. Click the review button
3. Use slider to select rating (0-10)
4. Write review text (max 200 characters)
5. Click confirm to submit

### Viewing Reviews
1. Open movie details dialog
2. Click the show reviews button
3. Reviews displayed 5 per page
4. Use navigation buttons for pagination

## Database Schema

### Core Tables
- **users** - User accounts (IdUser, Login, SyncToken)
- **movies** - Main movie table (all movie details)
- **user_reviews** - User reviews (IdUser, IdMovie, Rating, Review, ReviewDate)
- **actors** - Actor/actress entities
- **directors** - Director entities
- **movie_actors** - Movie-Actor relationships with character names
- **movie_directors** - Movie-Director relationships
- **genres** - Movie genres
- **countries** - Production countries
- **languages** - Spoken languages
- **certifications** - Movie certifications/ratings
- **production_companies** - Production company entities
- **movie_genres** - Movie-Genre relationships
- **movie_countries** - Movie-Country relationships
- **movie_languages** - Movie-Language relationships
- **movie_companies** - Movie-Company relationships

## Migration Notes

### Changes from Original Java Version
1. **Database:**
   - Oracle DB → SQLite
   - PL/SQL packages → Python service layer
   - Custom Oracle types → Python dataclasses
   - DB Links → Simulated with dual database files

2. **GUI:**
   - Java Swing → PyQt6
   - NetBeans Form Designer → Programmatic PyQt6 layouts
   - Event handling adapted to PyQt signals/slots

3. **Architecture:**
   - JDBC → SQLAlchemy ORM
   - Singleton pattern maintained for database service
   - Business logic moved from stored procedures to Python

4. **Enhancements:**
   - Better type safety with Python type hints
   - Modern Python patterns (context managers, dataclasses)
   - Improved error handling
   - Cleaner separation of concerns

### Original Java Files Mapping
- `LoginSingleton.java` → `services/database_service.py`
- `Rennequinepolis.java` → `ui/main_window.py`
- `DialogLogin.java` → `ui/login_dialog.py`
- `DialogMovie.java` → `ui/movie_dialog.py`
- `DialogWriteVote.java` → `ui/write_vote_dialog.py`
- `DialogShowVotes.java` → `ui/show_votes_dialog.py`
- SQL procedures → `services/*.py`

## Development

### Running Tests
```bash
# Run search functionality test
python -m pytest tests/test_search.py

# Run all tests
python -m pytest
```

### Database Management
```bash
# Reset database
rm movies.db movies_backup.db
python -m database.init_db

# Add more sample data
python -m database.sample_data
```

## Known Limitations
1. No external data import (182MB file not included)
2. Background backup jobs not implemented (can be added with APScheduler)
3. Poster images not downloaded/displayed (paths stored only)
4. Simplified authentication (username only, no password)

## Future Enhancements
1. Add poster image display with web fetching
2. Implement full backup/restore automation
3. Add data import from CSV/text files
4. Enhance UI with modern styling
5. Add export functionality (CSV, PDF reports)
6. Multi-language support
7. Add movie recommendations
8. Implement full authentication system

## License
GPLv2 - Same as original application

## Credits
- Original Application: Romain Vinders (2015)
- Python Migration: 2025
- Framework: PyQt6, SQLAlchemy
