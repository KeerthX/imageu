import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

def load_stylesheet(file_path):
    # Determine the correct base path for accessing assets
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller bundle
        base_path = sys._MEIPASS  # Temporary extraction folder
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Script's directory

    stylesheet_path = os.path.join(base_path, file_path)

    try:
        with open(stylesheet_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Stylesheet file '{stylesheet_path}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load and apply QSS stylesheet
    qss = load_stylesheet("assets/styles.qss")
    app.setStyleSheet(qss)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
