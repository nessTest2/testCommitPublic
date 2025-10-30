# Login Dialog - User authentication
# Source: movies_gui_app/src/sgbdrennequinepolis/DialogLogin.java

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from typing import Optional

class LoginDialog(QDialog):
    """Login dialog for user authentication

    Migrated from DialogLogin.java (lines 12-125)
    Simple login dialog - asks for username only (no password)
    """

    def __init__(self, parent=None):
        """Initialize the login dialog

        Source: DialogLogin constructor (lines 19-23)
        """
        super().__init__(parent)
        self._login: Optional[str] = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface

        Source: initComponents() (lines 36-96)
        """
        self.setWindowTitle("Identification...")  # Line 45
        self.setModal(True)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(43, 21, 43, 30)
        layout.setSpacing(10)

        # Label - Source: line 56
        label = QLabel("Veuillez entrer votre login")
        layout.addWidget(label)

        # Login input box - Source: line 40
        self.login_box = QLineEdit()
        layout.addWidget(self.login_box)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Validate button - Source: lines 47-54
        self.login_btn = QPushButton("Valider")
        self.login_btn.setFixedWidth(75)
        self.login_btn.clicked.connect(self.on_login_clicked)
        button_layout.addWidget(self.login_btn)

        # Cancel button - Source: lines 58-65
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setFixedWidth(75)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Allow Enter key to submit
        self.login_box.returnPressed.connect(self.on_login_clicked)

    def on_login_clicked(self):
        """Handle login button click

        Source: jLoginBtnActionPerformed() (lines 100-111)
        """
        login_text = self.login_box.text().strip()

        # Validate non-empty - Source: line 102
        if not login_text:
            QMessageBox.warning(
                self,
                "Erreur",
                "Vous ne pouvez pas choisir un login vide."  # Line 104
            )
        else:
            # Accept login - Source: lines 108-109
            self._login = login_text
            self.accept()

    def on_cancel_clicked(self):
        """Handle cancel button click

        Source: jCancelBtnActionPerformed() (lines 113-116)
        """
        self.reject()

    def get_login(self) -> Optional[str]:
        """Get the entered login

        Source: getLogin() (lines 24-27)

        Returns:
            The entered login string, or None if cancelled
        """
        return self._login

    @staticmethod
    def get_user_login(parent=None) -> Optional[str]:
        """Show login dialog and return the entered login

        Convenience method for showing the dialog and getting the result.

        Args:
            parent: Parent widget

        Returns:
            Login string if accepted, None if cancelled
        """
        dialog = LoginDialog(parent)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return dialog.get_login()
        return None
