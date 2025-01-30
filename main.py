# main.py

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

# Set attributes before QApplication creation
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def load_stylesheet(file_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    stylesheet_path = os.path.join(base_path, file_path)

    try:
        with open(stylesheet_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Stylesheet file '{stylesheet_path}' not found.")
        return ""

def main():
    app = QApplication(sys.argv)
    
    # Load and apply QSS stylesheet
    qss = load_stylesheet("assets/styles.qss")
    if qss:
        app.setStyleSheet(qss)

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()