from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QListWidget, QFileDialog, QFrame, QLabel, QMessageBox,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from .image_viewer import ImageViewer 
from .dialogs import AddProcessDialog, ConfigDialog
from utils.tool_manager import ToolManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("Image Processing Tool")
        self.setStyleSheet("""
            QMainWindow {
                background: #1E1E1E;
            }
            QLabel {
                color: #E0E0E0;
            }
            QMessageBox {
                background-color: #2D2D2D;
                color: #E0E0E0;
            }
            QMessageBox QLabel {
                color: #E0E0E0;
            }
            QMessageBox QPushButton {
                background-color: #3D3D3D;
                color: #E0E0E0;
                border: 1px solid #555555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4D4D4D;
            }
        """)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar and main content
        self.setup_sidebar(main_layout)
        self.setup_main_content(main_layout)

        # Initialize tool manager
        self.tool_manager = ToolManager()

    def setup_sidebar(self, main_layout):
        # Sidebar container
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background: #252526;
                border-right: 1px solid #3E3E42;
                min-width: 280px;
                max-width: 350px;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(12)

        # Title
        title = QLabel("ImageU V0.6")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                margin-bottom: 10px;
                font-size: 45px;
            }
        """)
        sidebar_layout.addWidget(title)

        # Section labels style
        section_label_style = """
            QLabel {
                color: #969696;
                font-size: 13px;
                font-weight: bold;
                margin-top: 16px;
                margin-bottom: 8px;
            }
        """

        # File operations section
        file_label = QLabel("FILE OPERATIONS")
        file_label.setStyleSheet(section_label_style)
        sidebar_layout.addWidget(file_label)

        # Action buttons
        self.create_action_buttons(sidebar_layout)

        # Processing section
        process_label = QLabel("PROCESSING STACK")
        process_label.setStyleSheet(section_label_style)
        sidebar_layout.addWidget(process_label)

        # Processing stack list
        self.create_processing_list(sidebar_layout)

        # Add to main layout
        main_layout.addWidget(sidebar)

    def create_button(self, text, icon_path=None):
        button = QPushButton(text)
        if icon_path:
            button.setIcon(QIcon(f"assets/{icon_path}"))
        button.setStyleSheet("""
            QPushButton {
                padding: 12px 16px;
                background: #3E3E42;
                border: none;
                border-radius: 6px;
                color: #E0E0E0;
                font-size: 13px;
                font-weight: 500;
                text-align: left;
                margin: 2px 0;
            }
            QPushButton:hover {
                background: #4E4E52;
            }
            QPushButton:pressed {
                background: #2E2E32;
            }
            QPushButton:disabled {
                background: #2D2D30;
                color: #6D6D6D;
            }
        """)
        return button

    def create_action_buttons(self, layout):
        # File operations
        self.upload_button = self.create_button("Upload Image", "upload.png")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button)

        self.save_button = self.create_button("Save Image", "save.png")
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        # Process controls
        self.add_process_button = self.create_button("Add Process", "add.png")
        self.add_process_button.clicked.connect(self.add_processing)
        layout.addWidget(self.add_process_button)

        self.remove_button = self.create_button("Remove Selected", "remove.png")
        self.remove_button.clicked.connect(self.remove_processing)
        layout.addWidget(self.remove_button)

        # Process movement buttons
        move_layout = QHBoxLayout()
        move_layout.setSpacing(8)
        
        self.move_up_button = self.create_button("↑ Move Up", "arrow-up.png")
        self.move_up_button.clicked.connect(self.move_process_up)
        move_layout.addWidget(self.move_up_button)
        
        self.move_down_button = self.create_button("↓ Move Down", "arrow-down.png")
        self.move_down_button.clicked.connect(self.move_process_down)
        move_layout.addWidget(self.move_down_button)
        
        layout.addLayout(move_layout)

    def create_processing_list(self, layout):
        self.process_list = QListWidget()
        self.process_list.setStyleSheet("""
            QListWidget {
                background: #1E1E1E;
                border: 1px solid #3E3E42;
                border-radius: 6px;
                color: #E0E0E0;
                padding: 8px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 4px;
                margin-bottom: 4px;
            }
            QListWidget::item:selected {
                background: #264F78;
            }
            QListWidget::item:hover {
                background: #2D2D30;
            }
            QListWidget:focus {
                border: 1px solid #007ACC;
            }
        """)
        self.process_list.itemDoubleClicked.connect(self.edit_process)
        layout.addWidget(self.process_list)

    def setup_main_content(self, main_layout):
        # Main content container
        content = QFrame()
        content.setStyleSheet("""
            QFrame {
                background: #1E1E1E;
            }
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 24, 24, 24)

        # Image viewer
        self.image_viewer = ImageViewer()
        self.image_viewer.setStyleSheet("""
            QLabel {
                background: #2D2D30;
                border: 1px solid #3E3E42;
                border-radius: 6px;
            }
        """)
        content_layout.addWidget(self.image_viewer)

        main_layout.addWidget(content)

    def setup_main_content(self, main_layout):
        # Main content container
        content = QFrame()
        content.setStyleSheet("background: #1A242F;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Image viewer
        self.image_viewer = ImageViewer()
        content_layout.addWidget(self.image_viewer)

        main_layout.addWidget(content)

    def setup_connections(self):
        self.process_list.itemSelectionChanged.connect(self.update_button_states)
        self.update_button_states()

    def update_button_states(self):
        has_selection = bool(self.process_list.selectedItems())
        current_row = self.process_list.currentRow()
        self.remove_button.setEnabled(has_selection)
        self.move_up_button.setEnabled(has_selection and current_row > 0)
        self.move_down_button.setEnabled(has_selection and current_row < self.process_list.count() - 1)

    def upload_image(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open Image", "",
                "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
            )
            if file_path and self.image_viewer.load_image(file_path):
                self.process_list.clear()
                self.statusBar().showMessage("Image loaded successfully", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")

    def save_image(self):
        try:
            if self.image_viewer.processed_image is None:
                raise ValueError("No image to save")

            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "",
                "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
            )
            if file_path and self.image_viewer.save_image(file_path):
                self.statusBar().showMessage("Image saved successfully", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def add_processing(self):
        try:
            if self.image_viewer.original_image is None:
                raise ValueError("Please load an image first")

            dialog = AddProcessDialog(self.tool_manager.get_available_tools(), self)
            if dialog.exec_():
                process_name = dialog.selected_process
                if process_name:
                    tool = self.tool_manager.get_tool(process_name)
                    if self.image_viewer.add_processing(tool):
                        self.process_list.addItem(process_name)
                        self.statusBar().showMessage("Processing tool added", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def remove_processing(self):
        try:
            current_row = self.process_list.currentRow()
            if current_row == -1:
                raise ValueError("No processing tool selected")

            if self.image_viewer.remove_processing(current_row):
                self.process_list.takeItem(current_row)
                self.statusBar().showMessage("Processing tool removed", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def move_process_up(self):
        current_row = self.process_list.currentRow()
        if current_row > 0:
            try:
                if self.image_viewer.move_processing(current_row, current_row - 1):
                    # Swap items in the list widget
                    item = self.process_list.takeItem(current_row)
                    self.process_list.insertItem(current_row - 1, item)
                    self.process_list.setCurrentRow(current_row - 1)
                    self.statusBar().showMessage("Process moved up", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def move_process_down(self):
        current_row = self.process_list.currentRow()
        if current_row < self.process_list.count() - 1:
            try:
                if self.image_viewer.move_processing(current_row, current_row + 1):
                    # Swap items in the list widget
                    item = self.process_list.takeItem(current_row)
                    self.process_list.insertItem(current_row + 1, item)
                    self.process_list.setCurrentRow(current_row + 1)
                    self.statusBar().showMessage("Process moved down", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def edit_process(self, item):
        try:
            process_name = item.text()
            tool_index = self.process_list.row(item)
            process_tool = self.image_viewer.processing_stack[tool_index]

            dialog = ConfigDialog(process_tool, self)
            if dialog.exec_():
                self.image_viewer.apply_processing()
                self.statusBar().showMessage("Processing tool updated", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))