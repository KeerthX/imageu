from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QGridLayout
)
from gui.image_viewer import ImageViewer
from gui.dialogs import ConfigDialog, AddProcessDialog
from utils.tool_manager import ToolManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processing Tool")
        self.setGeometry(200, 100, 800, 600)

        # Initialize ToolManager
        self.tool_manager = ToolManager()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top: Image viewer
        self.image_viewer = ImageViewer()
        self.layout.addWidget(self.image_viewer)

        # Bottom: Controls
        bottom_layout = QHBoxLayout()

        # Left panel: Upload and Save buttons
        left_panel = QVBoxLayout()
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload_image)
        left_panel.addWidget(self.upload_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_image)
        left_panel.addWidget(self.save_button)
        bottom_layout.addLayout(left_panel)

        # Center panel: Process List
        self.process_list = QListWidget()
        self.process_list.itemDoubleClicked.connect(self.edit_process)
        bottom_layout.addWidget(self.process_list)

        # Right panel: Control buttons (Add, Move Up, Move Down, Remove)
        right_panel = QVBoxLayout()
        self.add_process_button = QPushButton("Add")
        self.add_process_button.clicked.connect(self.add_processing)
        right_panel.addWidget(self.add_process_button)

        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_up)
        right_panel.addWidget(self.move_up_button)

        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_down)
        right_panel.addWidget(self.move_down_button)

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_processing)
        right_panel.addWidget(self.remove_button)

        bottom_layout.addLayout(right_panel)

        # Add bottom layout to main layout
        self.layout.addLayout(bottom_layout)

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
        if dialog.exec_():
            process = dialog.selected_process
            if process:
                tool = self.tool_manager.get_tool(process)
                self.process_list.addItem(process)
                self.image_viewer.add_processing(tool)

    def edit_process(self, item):
        process_name = item.text()
        tool_index = self.process_list.row(item)
        process_tool = self.image_viewer.processing_stack[tool_index]

        dialog = ConfigDialog(process_tool)
        if dialog.exec_():
            self.image_viewer.apply_processing()

    def move_up(self):
        current_row = self.process_list.currentRow()
        if current_row > 0:
            self.process_list.insertItem(current_row - 1, self.process_list.takeItem(current_row))
            self.image_viewer.processing_stack.insert(
                current_row - 1, self.image_viewer.processing_stack.pop(current_row)
            )
            self.process_list.setCurrentRow(current_row - 1)
            self.image_viewer.apply_processing()

    def move_down(self):
        current_row = self.process_list.currentRow()
        if current_row < self.process_list.count() - 1:
            self.process_list.insertItem(current_row + 1, self.process_list.takeItem(current_row))
            self.image_viewer.processing_stack.insert(
                current_row + 1, self.image_viewer.processing_stack.pop(current_row)
            )
            self.process_list.setCurrentRow(current_row + 1)
            self.image_viewer.apply_processing()

    def remove_processing(self):
        current_row = self.process_list.currentRow()
        if current_row != -1:
            self.process_list.takeItem(current_row)
            del self.image_viewer.processing_stack[current_row]
            self.image_viewer.apply_processing()
