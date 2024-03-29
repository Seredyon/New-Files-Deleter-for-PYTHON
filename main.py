import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt

class FileManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.directory_path = ""
        self.file_list = []
        self.white_list = set()
        self.error_timer = QTimer(self)
        self.error_timer.timeout.connect(self.clear_error)

        self.init_ui()

    def init_ui(self):
        directory_label = QLabel("Directory Path:")
        self.directory_entry = QLineEdit(self)
        self.directory_entry.textChanged.connect(self.update_delete_button_state)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_directory)
        browse_button.setStyleSheet("color: white; background-color: #006699;")

        save_button = QPushButton("Save Files", self)
        save_button.clicked.connect(self.save_files)
        save_button.setStyleSheet("color: white; background-color: #006699;")

        self.delete_button = QPushButton("Delete New Files", self)
        self.delete_button.clicked.connect(self.delete_new_files)
        self.delete_button.setStyleSheet("color: white; background-color: #A9A9A9;")  # Initial grayed out
        self.delete_button.setEnabled(False)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.message_label = QLabel("")
        self.message_label.hide()

        layout = QVBoxLayout()
        layout.addWidget(directory_label)
        layout.addWidget(self.directory_entry)
        layout.addWidget(browse_button)
        layout.addWidget(save_button)
        layout.addWidget(self.delete_button)
        layout.addItem(spacer)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        self.set_dark_theme()

        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(400, 200)

    def browse_directory(self):
        directory_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory_path:
            self.directory_entry.setText(directory_path)
            self.load_file_list()
            self.update_delete_button_state()

    def load_file_list(self):
        try:
            path = Path(self.directory_entry.text())
            self.file_list = [f.name for f in path.iterdir() if f.is_file()]
        except FileNotFoundError:
            self.display_error("ERROR: THIS ROUTE DOESN'T EXIST")
            return

    def save_files(self):
        directory_path = self.directory_entry.text().strip()
        if not directory_path or not Path(directory_path).exists():
            self.display_error("ERROR: INVALID DIRECTORY PATH")
            return

        self.load_file_list()
        self.white_list = set(self.file_list)
        self.display_success("Files have been successfully saved to the whitelist!")

        self.delete_button.setEnabled(True)
        self.delete_button.setStyleSheet("color: white; background-color: #006699;")

    def delete_new_files(self):
        directory_path = self.directory_entry.text()
        if not directory_path:
            self.display_error("ERROR: EMPTY ROUTE")
            return

        self.load_file_list()
        files_to_delete = set(self.file_list) - self.white_list

        for file_name in files_to_delete:
            file_path = Path(directory_path) / file_name
            try:
                file_path.unlink()
            except PermissionError:
                self.display_error(f"ERROR: Permission denied for {file_path}")

        self.display_success("New files have been successfully DELETED.")

    def update_delete_button_state(self):
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("color: white; background-color: #A9A9A9;")

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)

        font = QFont("Roboto", 10)
        self.setFont(font)

    def display_error(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: red")
        self.message_label.show()
        self.error_timer.start(3000)

    def display_success(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: green")
        self.message_label.show()
        self.error_timer.start(3000)

    def clear_error(self):
        self.message_label.clear()
        self.message_label.hide()

if __name__ == "__main__":
    app = QApplication([], applicationName="New Files Deleter")

    app_icon_path = r"path/to/your/icon"
    app_icon = QIcon(app_icon_path)
    app.setWindowIcon(app_icon)

    window = FileManagementApp()
    window.show()
    app.exec_()
