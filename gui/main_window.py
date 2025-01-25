from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QHBoxLayout, QDialog, QVBoxLayout, QComboBox
)
from gui.image_viewer import ImageViewer
from gui.dialogs import ConfigDialog
from utils.tool_manager import ToolManager


class AddProcessDialog(QDialog):
    def __init__(self, processes):
        super().__init__()
        self.setWindowTitle("Select Processing")
        self.selected_process = None

        layout = QVBoxLayout(self)

        # Dropdown menu for selecting processes
        self.combo_box = QComboBox()
        self.combo_box.addItems(processes)
        layout.addWidget(self.combo_box)

        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.confirm_selection)
        layout.addWidget(ok_button)

    def confirm_selection(self):
        self.selected_process = self.combo_box.currentText()
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Tool")
        self.setGeometry(200, 100, 1000, 600)

        # Initialize variables
        self.tool_manager = ToolManager()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Image viewer
        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)

        # Controls layout
        controls_layout = QHBoxLayout()

        # Upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        controls_layout.addWidget(self.upload_button)

        # Save button
        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        controls_layout.addWidget(self.save_button)

        # Processing list
        self.process_list = QListWidget()
        self.process_list.itemDoubleClicked.connect(self.edit_process)
        controls_layout.addWidget(self.process_list)

        # Add processing button
        self.add_process_button = QPushButton("Add Processing")
        self.add_process_button.clicked.connect(self.add_processing)
        controls_layout.addWidget(self.add_process_button)

        self.layout.addLayout(controls_layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_viewer.set_image(file_path)

    def save_image(self):
        if self.image_viewer.processed_image is None:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_viewer.save_image(file_path)

    def add_processing(self):
        dialog = AddProcessDialog(self.tool_manager.get_available_tools())
        if dialog.exec_():  # Dialog accepted
            process = dialog.selected_process
            if process:
                tool = self.tool_manager.get_tool(process)
                self.process_list.addItem(process)
                self.image_viewer.add_processing(tool)

    def edit_process(self, item):
        process_name = item.text()
        process_tool = self.tool_manager.get_tool(process_name)
        dialog = ConfigDialog(process_tool)
        if dialog.exec_():
            self.image_viewer.apply_processing()
