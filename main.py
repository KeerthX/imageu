import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def load_stylesheet(app):
    """Loads the QSS stylesheet from 'assets/styles.qss' and applies it to the application."""
    stylesheet_path = os.path.join(os.path.dirname(__file__), "assets", "styles.qss")

    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r") as file:
            app.setStyleSheet(file.read())
    else:
        print(f"Warning: Stylesheet file not found at {stylesheet_path}")

def main():
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Load and apply the stylesheet
    load_stylesheet(app)

    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
