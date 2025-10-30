# Show Votes Dialog - Display user reviews
# Source: movies_gui_app/src/sgbdrennequinepolis/DialogShowVotes.java

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from services.database_service import DatabaseService
from services.review_service import ReviewService

class ShowVotesDialog(QDialog):
    """Dialog for displaying movie reviews with pagination

    Migrated from DialogShowVotes.java
    """

    ITEMS_PER_PAGE = 5  # Show 5 reviews per page

    def __init__(self, parent=None, movie_id: int = None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.current_page = 0
        self.total_count = 0
        self.setup_ui()
        self.load_reviews()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Avis des utilisateurs")
        self.setMinimumSize(500, 600)

        layout = QVBoxLayout()

        # Scroll area for reviews
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll.setWidget(self.content_widget)

        layout.addWidget(self.scroll)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        self.prev_btn = QPushButton("← Précédent")
        self.prev_btn.clicked.connect(self.on_prev_page)
        nav_layout.addWidget(self.prev_btn)

        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_layout.addWidget(self.page_label)

        self.next_btn = QPushButton("Suivant →")
        self.next_btn.clicked.connect(self.on_next_page)
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)

        # Close button
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def load_reviews(self):
        """Load and display reviews for current page"""
        try:
            # Clear existing content
            while self.content_layout.count():
                child = self.content_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Get database session and fetch reviews
            db_service = DatabaseService.get_instance()
            with db_service.get_session() as session:
                # Get total count
                self.total_count = ReviewService.get_review_count(session, self.movie_id)

                # Get reviews for current page
                reviews = ReviewService.get_votes_paginated(
                    session,
                    self.movie_id,
                    self.current_page,
                    self.ITEMS_PER_PAGE
                )

            if not reviews:
                no_reviews_label = QLabel("Aucun avis pour ce film.")
                no_reviews_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.content_layout.addWidget(no_reviews_label)
            else:
                # Display each review
                for review in reviews:
                    review_widget = self.create_review_widget(review)
                    self.content_layout.addWidget(review_widget)

            self.content_layout.addStretch()

            # Update navigation
            self.update_navigation()

        except Exception as exc:
            error_label = QLabel(f"Erreur lors du chargement des avis:\n{str(exc)}")
            error_label.setStyleSheet("color: red;")
            self.content_layout.addWidget(error_label)

    def create_review_widget(self, review):
        """Create a widget for a single review"""
        widget = QWidget()
        widget.setStyleSheet("QWidget { background-color: #f0f0f0; border-radius: 5px; padding: 10px; }")

        layout = QVBoxLayout(widget)

        # Header: user and date
        header_text = f"<b>{review.login}</b> - {review.review_date.strftime('%d/%m/%Y %H:%M')}"
        header_label = QLabel(header_text)
        layout.addWidget(header_label)

        # Rating
        rating_text = f"Note: {review.rating}/10 " + "★" * review.rating
        rating_label = QLabel(rating_text)
        rating_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        layout.addWidget(rating_label)

        # Review text
        if review.review:
            review_text = QTextEdit()
            review_text.setPlainText(review.review)
            review_text.setReadOnly(True)
            review_text.setMaximumHeight(80)
            layout.addWidget(review_text)

        return widget

    def update_navigation(self):
        """Update navigation buttons and page label"""
        total_pages = (self.total_count + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE
        if total_pages == 0:
            total_pages = 1

        self.page_label.setText(f"Page {self.current_page + 1} / {total_pages}")

        # Enable/disable navigation buttons
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)

    def on_prev_page(self):
        """Navigate to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_reviews()

    def on_next_page(self):
        """Navigate to next page"""
        total_pages = (self.total_count + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_reviews()
