# Main Window - Application main interface
# Source: movies_gui_app/src/sgbdrennequinepolis/Rennequinepolis.java

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QRadioButton, QPushButton, QSpinBox, QLineEdit, QListWidget,
    QCheckBox, QMessageBox, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt
from services.database_service import DatabaseService
from services.search_service import SearchService
from services.movie_service import MovieService
from ui.movie_dialog import MovieDialog
from ui.login_dialog import LoginDialog

class MainWindow(QMainWindow):
    """Main application window for movie search

    Migrated from Rennequinepolis.java (lines 36-587)
    """

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.actor_list = []
        self.director_list = []
        self.results = {}  # Maps display string to movie ID
        self.setup_ui()

        # Show login dialog
        self.show_login()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Rennequinepolis")  # Line 186
        self.setMinimumSize(800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("<h2>Rechercher un film</h2>")  # Line 192
        main_layout.addWidget(title_label)

        # Error label
        self.error_label = QLabel("-")  # Line 189
        self.error_label.setStyleSheet("color: #CC0033;")  # Line 188
        main_layout.addWidget(self.error_label)

        # Search mode selection
        mode_layout = QHBoxLayout()
        self.radio_seek_id = QRadioButton("Rechercher identifiant")  # Line 207
        self.radio_seek_id.setChecked(True)  # Line 53
        self.radio_seek_id.toggled.connect(self.on_search_mode_changed)
        mode_layout.addWidget(self.radio_seek_id)

        self.radio_seek_advanced = QRadioButton("Recherche avancée")  # Line 217
        self.radio_seek_advanced.toggled.connect(self.on_search_mode_changed)
        mode_layout.addWidget(self.radio_seek_advanced)

        main_layout.addLayout(mode_layout)

        # ID search section
        self.id_search_widget = QWidget()
        id_layout = QHBoxLayout(self.id_search_widget)
        id_layout.addWidget(QLabel("ID du film:"))
        self.spin_id = QSpinBox()  # Line 235
        self.spin_id.setMinimum(1)
        self.spin_id.setMaximum(999999)
        id_layout.addWidget(self.spin_id)
        id_layout.addStretch()
        main_layout.addWidget(self.id_search_widget)

        # Advanced search section
        self.advanced_search_widget = QWidget()
        advanced_layout = QVBoxLayout(self.advanced_search_widget)

        # Title search
        title_group = QGroupBox("Titre")
        title_layout = QHBoxLayout(title_group)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titre du film...")
        title_layout.addWidget(self.title_input)
        advanced_layout.addWidget(title_group)

        # Year search
        year_group = QGroupBox("Année")
        year_layout = QVBoxLayout(year_group)

        # Exact year
        exact_year_layout = QHBoxLayout()
        self.check_year_val = QCheckBox("Année exacte")
        exact_year_layout.addWidget(self.check_year_val)
        self.spin_year = QSpinBox()
        self.spin_year.setMinimum(1880)
        self.spin_year.setMaximum(2030)
        self.spin_year.setValue(2000)
        exact_year_layout.addWidget(self.spin_year)
        year_layout.addLayout(exact_year_layout)

        # Year range
        range_layout = QHBoxLayout()
        self.check_min = QCheckBox("Supérieure à")
        range_layout.addWidget(self.check_min)
        self.spin_year_min = QSpinBox()
        self.spin_year_min.setMinimum(1880)
        self.spin_year_min.setMaximum(2030)
        self.spin_year_min.setValue(1880)
        range_layout.addWidget(self.spin_year_min)
        year_layout.addLayout(range_layout)

        range_layout2 = QHBoxLayout()
        self.check_max = QCheckBox("Inférieure à")
        range_layout2.addWidget(self.check_max)
        self.spin_year_max = QSpinBox()
        self.spin_year_max.setMinimum(1880)
        self.spin_year_max.setMaximum(2030)
        self.spin_year_max.setValue(2030)
        range_layout2.addWidget(self.spin_year_max)
        year_layout.addLayout(range_layout2)

        year_group.setLayout(year_layout)
        advanced_layout.addWidget(year_group)

        # Actors
        actor_group = QGroupBox("Acteur(s)")
        actor_layout = QVBoxLayout(actor_group)
        actor_input_layout = QHBoxLayout()
        self.actor_input = QLineEdit()
        self.actor_input.setPlaceholderText("Nom de l'acteur...")
        actor_input_layout.addWidget(self.actor_input)
        btn_add_actor = QPushButton("Ajouter")
        btn_add_actor.clicked.connect(self.on_add_actor)
        actor_input_layout.addWidget(btn_add_actor)
        btn_remove_actor = QPushButton("Retirer")
        btn_remove_actor.clicked.connect(self.on_remove_actor)
        actor_input_layout.addWidget(btn_remove_actor)
        actor_layout.addLayout(actor_input_layout)
        self.actor_list_widget = QListWidget()
        self.actor_list_widget.setMaximumHeight(100)
        actor_layout.addWidget(self.actor_list_widget)
        advanced_layout.addWidget(actor_group)

        # Directors
        director_group = QGroupBox("Réalisateur(s)")
        director_layout = QVBoxLayout(director_group)
        director_input_layout = QHBoxLayout()
        self.director_input = QLineEdit()
        self.director_input.setPlaceholderText("Nom du réalisateur...")
        director_input_layout.addWidget(self.director_input)
        btn_add_director = QPushButton("Ajouter")
        btn_add_director.clicked.connect(self.on_add_director)
        director_input_layout.addWidget(btn_add_director)
        btn_remove_director = QPushButton("Retirer")
        btn_remove_director.clicked.connect(self.on_remove_director)
        director_input_layout.addWidget(btn_remove_director)
        director_layout.addLayout(director_input_layout)
        self.director_list_widget = QListWidget()
        self.director_list_widget.setMaximumHeight(100)
        director_layout.addWidget(self.director_list_widget)
        advanced_layout.addWidget(director_group)

        main_layout.addWidget(self.advanced_search_widget)
        self.advanced_search_widget.setVisible(False)

        # Search button
        self.btn_search = QPushButton("Rechercher")  # Line 226
        self.btn_search.clicked.connect(self.on_search)
        main_layout.addWidget(self.btn_search)

        # Results list
        results_label = QLabel("<b>Résultats:</b>")
        main_layout.addWidget(results_label)
        self.results_list = QListWidget()  # Line 158
        self.results_list.itemDoubleClicked.connect(self.on_result_selected)
        main_layout.addWidget(self.results_list)

    def show_login(self):
        """Show login dialog"""
        login = LoginDialog.get_user_login(self)
        if login:
            self.current_user = login
            DatabaseService.get_instance().set_login(login)
            self.statusBar().showMessage(f"Connecté en tant que: {login}")
        else:
            self.close()

    def on_search_mode_changed(self):
        """Handle search mode radio button toggle"""
        is_id_search = self.radio_seek_id.isChecked()
        self.id_search_widget.setVisible(is_id_search)
        self.advanced_search_widget.setVisible(not is_id_search)

    def on_add_actor(self):
        """Add actor to search filters"""
        actor_name = self.actor_input.text().strip()
        if actor_name:
            self.actor_list.append(actor_name)
            self.actor_list_widget.addItem(actor_name)
            self.actor_input.clear()

    def on_remove_actor(self):
        """Remove selected actor from filters"""
        current_item = self.actor_list_widget.currentItem()
        if current_item:
            index = self.actor_list_widget.row(current_item)
            self.actor_list.pop(index)
            self.actor_list_widget.takeItem(index)

    def on_add_director(self):
        """Add director to search filters"""
        director_name = self.director_input.text().strip()
        if director_name:
            self.director_list.append(director_name)
            self.director_list_widget.addItem(director_name)
            self.director_input.clear()

    def on_remove_director(self):
        """Remove selected director from filters"""
        current_item = self.director_list_widget.currentItem()
        if current_item:
            index = self.director_list_widget.row(current_item)
            self.director_list.pop(index)
            self.director_list_widget.takeItem(index)

    def on_search(self):
        """Handle search button click"""
        self.error_label.setText("-")
        self.results_list.clear()
        self.results.clear()

        if self.radio_seek_id.isChecked():
            # Search by ID
            movie_id = self.spin_id.value()
            self.get_movie(movie_id)
        else:
            # Advanced search
            title = self.title_input.text().strip() or None
            year = self.spin_year.value() if self.check_year_val.isChecked() else None
            year_min = self.spin_year_min.value() if self.check_min.isChecked() else None
            year_max = self.spin_year_max.value() if self.check_max.isChecked() else None

            self.find_movies(title, year, year_min, year_max)

    def find_movies(self, title, year, year_min, year_max):
        """Search for movies with filters (Source: lines 63-109)"""
        try:
            db_service = DatabaseService.get_instance()
            db_service.start_connection()

            with db_service.get_session() as session:
                self.results = SearchService.find_movies_dict(
                    session, title, year, year_min, year_max,
                    self.actor_list, self.director_list
                )

            if not self.results:
                self.error_label.setText("Aucun film trouvé selon ces critères...")
            else:
                for display_text in self.results.keys():
                    self.results_list.addItem(display_text)

        except Exception as exc:
            self.error_label.setText(str(exc))

    def get_movie(self, movie_id):
        """Get movie by ID and display details (Source: lines 112-143)"""
        try:
            db_service = DatabaseService.get_instance()
            db_service.start_connection()

            with db_service.get_session() as session:
                movie_details = MovieService.get_movie_by_id(session, movie_id)

            if movie_details:
                dialog = MovieDialog(self, movie_details, self.current_user)
                dialog.exec()
            else:
                self.error_label.setText("Aucun film trouvé avec cet identifiant...")

        except Exception as exc:
            self.error_label.setText(str(exc))

    def on_result_selected(self, item):
        """Handle double-click on search result"""
        display_text = item.text()
        movie_id = self.results.get(display_text)
        if movie_id:
            self.get_movie(movie_id)
