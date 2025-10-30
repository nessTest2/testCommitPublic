# Write Vote Dialog - Submit user review
# Source: movies_gui_app/src/sgbdrennequinepolis/DialogWriteVote.java

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QSlider, QMessageBox
)
from PyQt6.QtCore import Qt
from services.database_service import DatabaseService
from services.review_service import ReviewService

class WriteVoteDialog(QDialog):
    """Dialog for submitting a movie review

    Migrated from DialogWriteVote.java
    """

    def __init__(self, parent=None, movie_id: int = None, current_user: str = None):
        super().__init__(parent)
        self.movie_id = movie_id
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Écrire un avis")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # Rating slider
        rating_label = QLabel("Note (0-10):")
        layout.addWidget(rating_label)

        self.rating_slider = QSlider(Qt.Orientation.Horizontal)
        self.rating_slider.setMinimum(0)
        self.rating_slider.setMaximum(10)
        self.rating_slider.setValue(5)
        self.rating_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.rating_slider.setTickInterval(1)
        layout.addWidget(self.rating_slider)

        self.rating_value_label = QLabel("5")
        self.rating_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rating_slider.valueChanged.connect(
            lambda v: self.rating_value_label.setText(str(v))
        )
        layout.addWidget(self.rating_value_label)

        # Review text
        review_label = QLabel("Avis (max 200 caractères):")
        layout.addWidget(review_label)

        self.review_text = QTextEdit()
        self.review_text.setMaximumHeight(100)
        self.review_text.setPlaceholderText("Écrivez votre avis ici...")
        layout.addWidget(self.review_text)

        self.char_count_label = QLabel("0/200")
        self.review_text.textChanged.connect(self.update_char_count)
        layout.addWidget(self.char_count_label)

        # Buttons
        button_layout = QHBoxLayout()

        confirm_btn = QPushButton("Confirmer")
        confirm_btn.clicked.connect(self.on_confirm)
        button_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def update_char_count(self):
        """Update character count label"""
        text = self.review_text.toPlainText()
        count = len(text)
        self.char_count_label.setText(f"{count}/200")

        if count > 200:
            self.char_count_label.setStyleSheet("color: red;")
        else:
            self.char_count_label.setStyleSheet("")

    def on_confirm(self):
        """Submit the review"""
        review_text = self.review_text.toPlainText().strip()

        # Validate length
        if len(review_text) > 200:
            QMessageBox.warning(
                self,
                "Erreur",
                "L'avis ne peut pas dépasser 200 caractères."
            )
            return

        rating = self.rating_slider.value()

        try:
            # Get database session and submit review
            db_service = DatabaseService.get_instance()
            with db_service.get_session() as session:
                ReviewService.add_user_review(
                    session,
                    self.current_user,
                    self.movie_id,
                    rating,
                    review_text if review_text else None
                )

            QMessageBox.information(
                self,
                "Succès",
                "Votre avis a été enregistré avec succès!"
            )
            self.accept()

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'enregistrement de l'avis:\n{str(exc)}"
            )
