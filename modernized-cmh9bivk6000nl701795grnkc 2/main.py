# Main entry point for the Movies Database Application
# Source: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java main() (lines 587-600)

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow
from database.init_db import init_database, populate_lookup_tables, get_database_path
from database.sample_data import add_sample_movies
from sqlalchemy import create_engine

def initialize_database_if_needed():
    """Initialize database if it doesn't exist"""
    db_file = Path(__file__).parent / "movies.db"

    if not db_file.exists():
        print("Database not found. Initializing...")

        try:
            # Create database schema
            engine = init_database()

            # Populate lookup tables
            populate_lookup_tables(engine)

            # Add sample movies
            add_sample_movies(engine)

            print("\nDatabase initialized successfully!")
            return True

        except Exception as exc:
            print(f"Error initializing database: {exc}")
            return False
    else:
        print("Database found. Using existing database.")
        return True

def main():
    """Main application entry point

    Source: Rennequinepolis.main() (lines 587-600)
    """
    # Initialize database if needed
    if not initialize_database_if_needed():
        print("Failed to initialize database. Exiting.")
        sys.exit(1)

    # Create application
    # Source: Line 588 - sets Nimbus Look and Feel
    app = QApplication(sys.argv)
    app.setApplicationName("Rennequinepolis")

    # Set application style (equivalent to Nimbus Look and Feel)
    app.setStyle("Fusion")

    try:
        # Create and show main window
        # Source: Lines 593-599
        window = MainWindow()
        window.show()

        # Start event loop
        sys.exit(app.exec())

    except Exception as exc:
        QMessageBox.critical(
            None,
            "Erreur",
            f"Erreur lors du démarrage de l'application:\n{str(exc)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
