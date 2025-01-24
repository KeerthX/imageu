from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget, QFileDialog, QHBoxLayout, QInputDialog
)
from gui.image_viewer import ImageViewer
from utils.tool_manager import ToolManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Tool")
        self.setGeometry(200, 100, 1000, 600)

        # Initialize variables
        self.current_image = None
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
            self.current_image = file_path
            self.image_viewer.set_image(file_path)

    def save_image(self):
        if self.image_viewer.processed_image is None:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_viewer.save_image(file_path)

    def add_processing(self):
        processes = self.tool_manager.get_available_tools()
        process, ok = QInputDialog.getItem(self, "Select Processing", "Choose a processing:", processes, 0, False)
        if ok and process:
            self.process_list.addItem(process)
            self.image_viewer.add_processing(self.tool_manager.get_tool(process))

    def edit_process(self, item):
        process_name = item.text()
        process_tool = self.tool_manager.get_tool(process_name)
        process_tool.configure()
        self.image_viewer.update_image()
