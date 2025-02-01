# gui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QListWidget, QFileDialog, QFrame, QLabel, QMessageBox,
    QSizePolicy, QSpacerItem, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from .image_viewer import ImageViewer 
from .dialogs import AddProcessDialog, ConfigDialog
from utils.tool_manager import ToolManager

import cv2
import google.generativeai as genai
from PIL import Image
import markdown

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("Image Processing Tool")
        self.setStyleSheet("""
            QMainWindow {
                background: #2C3E50;
            }
        """)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebars and main content
        self.setup_left_sidebar(main_layout)
        self.setup_main_content(main_layout)
        self.setup_right_sidebar(main_layout)

        # Initialize tool manager
        self.tool_manager = ToolManager()

    def setup_left_sidebar(self, main_layout):
        # Sidebar container
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background: #2C3E50;
                border-right: 1px solid #34495E;
                min-width: 250px;
                max-width: 250px;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Title
        title = QLabel("Image Processor")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        sidebar_layout.addWidget(title)

        # Action buttons
        self.create_action_buttons(sidebar_layout)

        # Processing stack list
        self.create_processing_list(sidebar_layout)

        # Add to main layout
        main_layout.addWidget(sidebar)

    def create_action_buttons(self, layout):
        # File operations
        self.upload_button = self.create_button("Upload Image", "upload.png")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button)

        self.save_button = self.create_button("Save Image", "save.png")
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        # Process controls
        layout.addWidget(QLabel("Processing Stack"))
        
        self.add_process_button = self.create_button("Add Process", "add.png")
        self.add_process_button.clicked.connect(self.add_processing)
        layout.addWidget(self.add_process_button)

        self.remove_button = self.create_button("Remove Selected", "remove.png")
        self.remove_button.clicked.connect(self.remove_processing)
        layout.addWidget(self.remove_button)

        # Process movement buttons
        move_layout = QHBoxLayout()
        
        self.move_up_button = self.create_button("Move Up", "arrow-up.png")
        self.move_up_button.clicked.connect(self.move_process_up)
        move_layout.addWidget(self.move_up_button)
        
        self.move_down_button = self.create_button("Move Down", "arrow-down.png")
        self.move_down_button.clicked.connect(self.move_process_down)
        move_layout.addWidget(self.move_down_button)
        
        layout.addLayout(move_layout)

    def create_button(self, text, icon_path=None):
        button = QPushButton(text)
        if icon_path:
            button.setIcon(QIcon(f"assets/{icon_path}"))
        button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #34495E;
                border: none;
                border-radius: 5px;
                color: white;
                text-align: left;
                margin: 2px 0;
            }
            QPushButton:hover { background: #2980B9; }
        """)
        return button

    def create_processing_list(self, layout):
        self.process_list = QListWidget()
        self.process_list.setStyleSheet("""
            QListWidget {
                background: #34495E;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected { background: #2980B9; }
            QListWidget::item:hover { background: #3498DB; }
        """)
        self.process_list.itemDoubleClicked.connect(self.edit_process)
        layout.addWidget(self.process_list)

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

    def setup_right_sidebar(self, main_layout):
        # Right sidebar container
        right_sidebar = QFrame()
        right_sidebar.setObjectName("rightSidebar")
        right_sidebar.setStyleSheet("""
            QFrame#rightSidebar {
                background: #2C3E50;
                border-left: 1px solid #34495E;
                min-width: 300px;
                max-width: 300px;
            }
        """)
        
        sidebar_layout = QVBoxLayout(right_sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Title
        title = QLabel("Gemini Image Analysis")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        sidebar_layout.addWidget(title)

        # API Key input
        api_key_label = QLabel("Gemini API Key:")
        api_key_label.setStyleSheet("color: white;")
        sidebar_layout.addWidget(api_key_label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #34495E;
                color: white;
                border: 1px solid #456789;
                border-radius: 5px;
            }
        """)
        sidebar_layout.addWidget(self.api_key_input)

        # Analyze button
        self.analyze_button = QPushButton("Analyze with Gemini")
        self.analyze_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #2ECC71;
                border: none;
                border-radius: 5px;
                color: white;
                margin: 10px 0;
            }
            QPushButton:hover { background: #27AE60; }
            QPushButton:disabled { background: #95A5A6; }
        """)
        self.analyze_button.clicked.connect(self.analyze_image)
        sidebar_layout.addWidget(self.analyze_button)

        # Results area
        self.analysis_results = QTextEdit()
        self.analysis_results.setReadOnly(True)
        self.analysis_results.setPlaceholderText("Upload an image and click Analyze to get Gemini's analysis")
        self.analysis_results.setStyleSheet("""
            QTextEdit {
                color: white;
                background: #34495E;
                padding: 10px;
                border-radius: 5px;
                min-height: 200px;
                border: none;
            }
            QTextEdit:focus {
                border: none;
                outline: none;
            }
        """)
        sidebar_layout.addWidget(self.analysis_results)

        # Add stretch to push everything to the top
        sidebar_layout.addStretch()

        # Add to main layout
        main_layout.addWidget(right_sidebar)

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

    def analyze_image(self):
        # Check if image exists
        if self.image_viewer.original_image is None:
            QMessageBox.warning(self, "Warning", "Please upload an image first")
            return

        # Get API key
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter your Gemini API key")
            return

        try:
            self.analyze_button.setEnabled(False)
            self.analysis_results.setText("Analyzing image with Gemini...")
            
            # Get the appropriate image (processed if exists, otherwise original)
            image_to_analyze = self.image_viewer.processed_image if self.image_viewer.processed_image is not None else self.image_viewer.original_image
            
            # Convert OpenCV BGR to RGB
            rgb_image = cv2.cvtColor(image_to_analyze, cv2.COLOR_BGR2RGB)
            
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(rgb_image)
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate content
            response = model.generate_content([
                "Analyze this image in detail. Describe what you see, including any notable objects, patterns, colors, or interesting features. If there's text in the image, include that as well. Format your response in markdown with appropriate headers, lists, and emphasis where relevant.",
                pil_image
            ])
            
            # Convert markdown to HTML and display
            html_content = markdown.markdown(response.text)
            self.analysis_results.setHtml(html_content)

        except Exception as e:
            error_msg = f"Failed to analyze image: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg)
            self.analysis_results.setPlainText("Analysis failed. Please try again.")
        
        finally:
            self.analyze_button.setEnabled(True)