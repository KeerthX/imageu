

# gui/main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QListWidget, QFileDialog, QFrame, QLabel, QGraphicsOpacityEffect,
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PyQt5.QtGui import QIcon, QFont
from gui.image_viewer import ImageViewer
from gui.dialogs import ConfigDialog, AddProcessDialog
from utils.tool_manager import ToolManager

class SidebarButton(QPushButton):
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setStyleSheet("""
            QPushButton {
                padding: 15px;
                border: none;
                border-radius: 8px;
                background: #34495E;
                color: #ECF0F1;
                font-size: 14px;
                text-align: left;
                margin: 5px;
            }
            QPushButton:hover {
                background: #2980B9;
            }
            QPushButton:pressed {
                background: #2574A9;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Image Processing Tool")
        self.setStyleSheet("""
            QMainWindow {
                background: #2C3E50;
            }
        """)
        
        # Initialize ToolManager
        self.tool_manager = ToolManager()
        
        # Main layout setup
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create sidebar
        self.setup_sidebar()
        
        # Create main content area
        self.setup_main_content()
        
        # Setup animations
        self.setup_animations()

    def setup_sidebar(self):
        # Sidebar container
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("""
            QFrame#sidebar {
                background: #2C3E50;
                border-right: 1px solid #34495E;
                min-width: 250px;
                max-width: 250px;
            }
        """)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo/Title
        title_label = QLabel("Image Processor")
        title_label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        sidebar_layout.addWidget(title_label)
        
        # Action buttons
        self.upload_button = SidebarButton("Upload Image", "assets/upload.png")
        self.upload_button.clicked.connect(self.upload_image)
        sidebar_layout.addWidget(self.upload_button)
        
        self.save_button = SidebarButton("Save Image", "assets/save.png")
        self.save_button.clicked.connect(self.save_image)
        sidebar_layout.addWidget(self.save_button)
        
        # Process list
        list_label = QLabel("Processing Stack")
        list_label.setStyleSheet("color: #ECF0F1; font-size: 16px; margin: 10px 0;")
        sidebar_layout.addWidget(list_label)
        
        self.process_list = QListWidget()
        self.process_list.setStyleSheet("""
            QListWidget {
                background: #34495E;
                border-radius: 8px;
                color: #ECF0F1;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #2980B9;
            }
            QListWidget::item:hover {
                background: #3498DB;
            }
        """)
        self.process_list.itemDoubleClicked.connect(self.edit_process)
        sidebar_layout.addWidget(self.process_list)
        
        # Process control buttons
        control_layout = QVBoxLayout()
        
        self.add_process_button = SidebarButton("Add Process", "assets/add.png")
        self.add_process_button.clicked.connect(self.add_processing)
        control_layout.addWidget(self.add_process_button)
        
        self.move_up_button = SidebarButton("Move Up", "assets/up.png")
        self.move_up_button.clicked.connect(self.move_up)
        control_layout.addWidget(self.move_up_button)
        
        self.move_down_button = SidebarButton("Move Down", "assets/down.png")
        self.move_down_button.clicked.connect(self.move_down)
        control_layout.addWidget(self.move_down_button)
        
        self.remove_button = SidebarButton("Remove", "assets/remove.png")
        self.remove_button.clicked.connect(self.remove_processing)
        control_layout.addWidget(self.remove_button)
        
        sidebar_layout.addLayout(control_layout)
        
        # Add spacer at the bottom
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.layout.addWidget(self.sidebar)

    def setup_main_content(self):
        # Main content container
        main_content = QFrame()
        main_content.setStyleSheet("""
            QFrame {
                background: #1A242F;
            }
        """)
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Image viewer
        self.image_viewer = ImageViewer()
        self.image_viewer.setStyleSheet("""
            QGraphicsView {
                border: 2px solid #34495E;
                border-radius: 10px;
                background: #2C3E50;
            }
        """)
        main_layout.addWidget(self.image_viewer)
        
        self.layout.addWidget(main_content)

    def setup_animations(self):
        # Create opacity effect for main content
        self.opacity_effect = QGraphicsOpacityEffect(self.central_widget)
        self.central_widget.setGraphicsEffect(self.opacity_effect)
        
        # Setup fade-in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Start animation when window is shown
        self.fade_in.start()

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
    )
        if file_path:
            if self.image_viewer.load_image(file_path):  # Changed from set_image to load_image
                print(f"Successfully loaded image: {file_path}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load the image.")

    def save_image(self):
        if self.image_viewer.processed_image is None:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", 
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if file_path:
            self.image_viewer.save_image(file_path)

    def add_processing(self):
        try:
            dialog = AddProcessDialog(self.tool_manager.get_available_tools())
            if dialog.exec_():
                process = dialog.selected_process
                if process:
                    tool = self.tool_manager.get_tool(process)
                    self.process_list.addItem(process)
                    self.image_viewer.add_processing(tool)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add processing tool: {str(e)}")

    def remove_processing(self):
        current_row = self.process_list.currentRow()
        if current_row != -1:
            try:
                self.process_list.takeItem(current_row)
                self.image_viewer.remove_processing(current_row)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove processing tool: {str(e)}")

    def move_up(self):
        current_row = self.process_list.currentRow()
        if current_row > 0:
            try:
                # Move item in list widget
                self.process_list.insertItem(current_row - 1, self.process_list.takeItem(current_row))
                
                # Update processing stack
                stack = self.image_viewer.processing_stack
                stack.insert(current_row - 1, stack.pop(current_row))
                self.image_viewer.update_processing_order(stack)
                
                # Update selection
                self.process_list.setCurrentRow(current_row - 1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to move processing tool: {str(e)}")

    def move_down(self):
        current_row = self.process_list.currentRow()
        if current_row < self.process_list.count() - 1:
            try:
                # Move item in list widget
                self.process_list.insertItem(current_row + 1, self.process_list.takeItem(current_row))
                
                # Update processing stack
                stack = self.image_viewer.processing_stack
                stack.insert(current_row + 1, stack.pop(current_row))
                self.image_viewer.update_processing_order(stack)
                
                # Update selection
                self.process_list.setCurrentRow(current_row + 1)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to move processing tool: {str(e)}")

    def edit_process(self, item):
        try:
            process_name = item.text()
            tool_index = self.process_list.row(item)
            process_tool = self.image_viewer.processing_stack[tool_index]
            
            dialog = ConfigDialog(process_tool)
            if dialog.exec_():
                self.image_viewer.apply_processing()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit processing tool: {str(e)}")