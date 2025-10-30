# Movie Details Dialog
# Source: movies_gui_app/src/sgbdrennequinepolis/DialogMovie.java

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QScrollArea, QWidget, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt
from services.movie_service import MovieDetails

class MovieDialog(QDialog):
    """Dialog for displaying complete movie details

    Migrated from DialogMovie.java
    """

    def __init__(self, parent=None, movie_details: MovieDetails = None, current_user: str = None):
        super().__init__(parent)
        self.movie_details = movie_details
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        if not self.movie_details:
            return

        self.setWindowTitle(f"Détails: {self.movie_details.title}")
        self.setMinimumSize(600, 700)

        # Main layout
        main_layout = QVBoxLayout()

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Title section
        title_label = QLabel(f"<h1>{self.movie_details.title}</h1>")
        content_layout.addWidget(title_label)

        if self.movie_details.title_orig != self.movie_details.title:
            orig_label = QLabel(f"<i>Titre original: {self.movie_details.title_orig}</i>")
            content_layout.addWidget(orig_label)

        # Basic info grid
        info_grid = QGridLayout()
        row = 0

        # Year
        if self.movie_details.release_year:
            info_grid.addWidget(QLabel("<b>Année:</b>"), row, 0)
            info_grid.addWidget(QLabel(str(self.movie_details.release_year)), row, 1)
            row += 1

        # Status
        info_grid.addWidget(QLabel("<b>Statut:</b>"), row, 0)
        info_grid.addWidget(QLabel(self.movie_details.status), row, 1)
        row += 1

        # Certification
        if self.movie_details.certification:
            info_grid.addWidget(QLabel("<b>Classification:</b>"), row, 0)
            info_grid.addWidget(QLabel(self.movie_details.certification), row, 1)
            row += 1

        # Runtime
        if self.movie_details.runtime:
            info_grid.addWidget(QLabel("<b>Durée:</b>"), row, 0)
            info_grid.addWidget(QLabel(f"{self.movie_details.runtime} min"), row, 1)
            row += 1

        # TMDB Ratings
        info_grid.addWidget(QLabel("<b>Note TMDB:</b>"), row, 0)
        info_grid.addWidget(QLabel(f"{self.movie_details.vote_average_tmdb:.1f}/10 ({self.movie_details.vote_count_tmdb} votes)"), row, 1)
        row += 1

        # App Ratings
        info_grid.addWidget(QLabel("<b>Note RQS:</b>"), row, 0)
        info_grid.addWidget(QLabel(f"{self.movie_details.vote_average_app:.1f}/10 ({self.movie_details.vote_count_app} votes)"), row, 1)
        row += 1

        # Budget/Revenue
        if self.movie_details.budget:
            info_grid.addWidget(QLabel("<b>Budget:</b>"), row, 0)
            info_grid.addWidget(QLabel(f"${self.movie_details.budget:,}"), row, 1)
            row += 1

        if self.movie_details.revenue:
            info_grid.addWidget(QLabel("<b>Recettes:</b>"), row, 0)
            info_grid.addWidget(QLabel(f"${self.movie_details.revenue:,}"), row, 1)
            row += 1

        content_layout.addLayout(info_grid)

        # Overview
        if self.movie_details.overview:
            overview_group = QGroupBox("Synopsis")
            overview_layout = QVBoxLayout()
            overview_text = QTextEdit()
            overview_text.setPlainText(self.movie_details.overview)
            overview_text.setReadOnly(True)
            overview_text.setMaximumHeight(150)
            overview_layout.addWidget(overview_text)
            overview_group.setLayout(overview_layout)
            content_layout.addWidget(overview_group)

        # Genres
        if self.movie_details.genres:
            genres_label = QLabel(f"<b>Genres:</b> {', '.join(self.movie_details.genres)}")
            genres_label.setWordWrap(True)
            content_layout.addWidget(genres_label)

        # Cast
        if self.movie_details.actors:
            cast_text = []
            for i, (actor, character) in enumerate(zip(self.movie_details.actors, self.movie_details.characters)):
                cast_text.append(f"{actor} ({character})")
                if i >= 9:  # Limit to 10 actors
                    break
            cast_label = QLabel(f"<b>Acteurs:</b><br>{'<br>'.join(cast_text)}")
            cast_label.setWordWrap(True)
            content_layout.addWidget(cast_label)

        # Directors
        if self.movie_details.directors:
            directors_label = QLabel(f"<b>Réalisateurs:</b> {', '.join(self.movie_details.directors)}")
            directors_label.setWordWrap(True)
            content_layout.addWidget(directors_label)

        # Production companies
        if self.movie_details.prod_comps:
            comps_label = QLabel(f"<b>Sociétés de production:</b> {', '.join(self.movie_details.prod_comps)}")
            comps_label.setWordWrap(True)
            content_layout.addWidget(comps_label)

        # Countries
        if self.movie_details.countries:
            countries_label = QLabel(f"<b>Pays:</b> {', '.join(self.movie_details.countries)}")
            content_layout.addWidget(countries_label)

        # Languages
        if self.movie_details.languages:
            languages_label = QLabel(f"<b>Langues:</b> {', '.join(self.movie_details.languages)}")
            content_layout.addWidget(languages_label)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Buttons
        button_layout = QHBoxLayout()

        if self.current_user:
            write_review_btn = QPushButton("Écrire un avis")
            write_review_btn.clicked.connect(self.on_write_review)
            button_layout.addWidget(write_review_btn)

        show_reviews_btn = QPushButton("Voir les avis")
        show_reviews_btn.clicked.connect(self.on_show_reviews)
        button_layout.addWidget(show_reviews_btn)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def on_write_review(self):
        """Open write review dialog"""
        from ui.write_vote_dialog import WriteVoteDialog
        dialog = WriteVoteDialog(self, self.movie_details.id_movie, self.current_user)
        dialog.exec()

    def on_show_reviews(self):
        """Open show reviews dialog"""
        from ui.show_votes_dialog import ShowVotesDialog
        dialog = ShowVotesDialog(self, self.movie_details.id_movie)
        dialog.exec()
