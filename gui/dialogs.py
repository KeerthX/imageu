from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class BaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Content frame
        self.frame = QFrame(self)
        self.frame.setObjectName("dialogFrame")
        self.frame.setStyleSheet("""
            QFrame#dialogFrame {
                background: #252526;
                border-radius: 8px;
                border: 1px solid #3E3E42;
            }
        """)
        
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(24, 24, 24, 24)
        self.frame_layout.setSpacing(16)
        self.main_layout.addWidget(self.frame)

# In dialogs.py, modify the AddProcessDialog class
class AddProcessDialog(BaseDialog):
    def __init__(self, available_tools, tool_manager, parent=None):  # Updated parameter list
        self.available_tools = available_tools
        self.tool_manager = tool_manager  # Store the tool manager
        self.filtered_tools = available_tools.copy()  # Add this line
        super().__init__(parent)
        self.selected_process = None
        self.setup_content()

    def setup_content(self):
        # Title
        title = QLabel("Add Processing Tool")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #E0E0E0; margin-bottom: 8px;")
        self.frame_layout.addWidget(title)
        
        # Add this section for Category filter
        category_label = QLabel("Filter by Category")
        category_label.setStyleSheet("""
            QLabel {
                color: #969696;
                font-size: 13px;
                font-weight: bold;
                margin-top: 8px;
            }
        """)
        self.frame_layout.addWidget(category_label)
        
        # Get all categories from tool manager
        self.category_selector = QComboBox()
        categories = ["All Categories"] + [category.value for category in self.tool_manager.get_all_categories()]
        self.category_selector.addItems(categories)
        self.category_selector.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: #3E3E42;
                color: #E0E0E0;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox:hover {
                background: #4E4E52;
            }
            QComboBox QAbstractItemView {
                background: #2D2D30;
                color: #E0E0E0;
                selection-background-color: #264F78;
                border: 1px solid #3E3E42;
            }
        """)
        self.category_selector.currentIndexChanged.connect(self.filter_tools)
        self.frame_layout.addWidget(self.category_selector)

        # Tool selector (existing code)
        self.tool_selector = QComboBox()
        self.tool_selector.addItems(self.filtered_tools)  # Use filtered_tools instead of available_tools
        self.tool_selector.setStyleSheet("""
            QComboBox {
                padding: 12px;
                background: #3E3E42;
                color: #E0E0E0;
                border: none;
                border-radius: 6px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox:hover {
                background: #4E4E52;
            }
            QComboBox QAbstractItemView {
                background: #2D2D30;
                color: #E0E0E0;
                selection-background-color: #264F78;
                border: 1px solid #3E3E42;
            }
        """)
        self.frame_layout.addWidget(self.tool_selector)

        # Rest of your existing code for buttons
        button_layout = QVBoxLayout()
        
        add_button = QPushButton("Add")
        add_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #007ACC;
                border: none;
                border-radius: 6px;
                color: #E0E0E0;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #1C97EA;
            }
            QPushButton:pressed {
                background: #005B99;
            }
        """)
        add_button.clicked.connect(self.accept_tool)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #3E3E42;
                border: none;
                border-radius: 6px;
                color: #E0E0E0;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #4E4E52;
            }
            QPushButton:pressed {
                background: #2E2E32;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        self.frame_layout.addLayout(button_layout)

    # Add this new method for filtering tools
    def filter_tools(self):
        selected_category = self.category_selector.currentText()
        
        if selected_category == "All Categories":
            self.filtered_tools = self.available_tools.copy()
        else:
            # Filter tools based on the selected category
            self.filtered_tools = []
            for tool_name in self.available_tools:
                # Get the class name by removing spaces
                class_name = "".join(tool_name.split())
                
                # Try to find the tool in the tool categories dictionary
                # We need to check if the class name exists or if a similar name exists
                matching_tool = None
                for key in self.tool_manager.tool_categories:
                    if key.lower() in class_name.lower() or class_name.lower() in key.lower():
                        matching_tool = key
                        break
                
                if matching_tool and self.tool_manager.tool_categories[matching_tool].value == selected_category:
                    self.filtered_tools.append(tool_name)
        
        # Update the tool selector
        self.tool_selector.clear()
        self.tool_selector.addItems(self.filtered_tools)

    def accept_tool(self):
        self.selected_process = self.tool_selector.currentText()
        self.accept()

class ConfigDialog(BaseDialog):
    def __init__(self, tool, parent=None):
        self.tool = tool
        self.original_parameters = tool.get_parameters().copy()
        super().__init__(parent)
        self.setup_content()

    def setup_content(self):
        # Title
        title = QLabel(f"Configure {self.tool.__class__.__name__}")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #E0E0E0; margin-bottom: 8px;")
        self.frame_layout.addWidget(title)

        # Parameter inputs
        self.param_inputs = {}
        has_valid_options = hasattr(self.tool, 'get_valid_options') and callable(getattr(self.tool, 'get_valid_options', None))
        valid_options = self.tool.get_valid_options() if has_valid_options else {}

        for param, value in self.tool.get_parameters().items():
            param_label = QLabel(param)
            param_label.setStyleSheet("""
                QLabel {
                    color: #969696;
                    font-size: 13px;
                    font-weight: bold;
                    margin-top: 8px;
                }
            """)
            self.frame_layout.addWidget(param_label)
            
            if has_valid_options and param in valid_options:
                input_field = QComboBox()
                input_field.addItems(valid_options[param])
                input_field.setCurrentText(str(value))
            else:
                input_field = QLineEdit(str(value))
            
            input_field.setStyleSheet("""
                QLineEdit, QComboBox {
                    padding: 12px;
                    background: #3E3E42;
                    color: #E0E0E0;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                }
                QLineEdit:focus, QComboBox:focus {
                    border: 1px solid #007ACC;
                }
                QLineEdit:hover, QComboBox:hover {
                    background: #4E4E52;
                }
            """)
            self.frame_layout.addWidget(input_field)
            self.param_inputs[param] = input_field

        # Buttons
        button_layout = QVBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #007ACC;
                border: none;
                border-radius: 6px;
                color: #E0E0E0;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #1C97EA;
            }
            QPushButton:pressed {
                background: #005B99;
            }
        """)
        save_button.clicked.connect(self.save_config)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #3E3E42;
                border: none;
                border-radius: 6px;
                color: #E0E0E0;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #4E4E52;
            }
            QPushButton:pressed {
                background: #2E2E32;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        self.frame_layout.addLayout(button_layout)

    def save_config(self):
        try:
            new_params = {}
            for param, input_field in self.param_inputs.items():
                if isinstance(input_field, QLineEdit):
                    try:
                        new_value = eval(input_field.text().strip())
                        new_params[param] = new_value
                    except Exception as e:
                        raise ValueError(f"Invalid value for {param}: {str(e)}")
                elif isinstance(input_field, QComboBox):
                    new_params[param] = input_field.currentText()

            # Test parameters on a copy of the tool
            test_tool = self.tool.__class__()
            test_tool.update_parameters(new_params)
            
            # If successful, update the actual tool
            self.tool.update_parameters(new_params)
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            # Restore original parameters
            self.tool.update_parameters(self.original_parameters)