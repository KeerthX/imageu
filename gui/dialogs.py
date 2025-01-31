# gui/dialogs.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QFrame, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPalette

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
                background: #2C3E50;
                border-radius: 10px;
                border: 1px solid #34495E;
            }
        """)
        
        self.frame_layout = QVBoxLayout(self.frame)
        self.main_layout.addWidget(self.frame)

class AddProcessDialog(BaseDialog):
    def __init__(self, available_tools, parent=None):
        self.available_tools = available_tools
        super().__init__(parent)
        self.selected_process = None
        self.setup_content()

    def setup_content(self):
        # Title
        title = QLabel("Add Processing Tool")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.frame_layout.addWidget(title)

        # Tool selector
        self.tool_selector = QComboBox()
        self.tool_selector.addItems(self.available_tools)
        self.tool_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                background: #34495E;
                color: white;
                border: 1px solid #456789;
                border-radius: 5px;
            }
        """)
        self.frame_layout.addWidget(self.tool_selector)

        # Buttons
        button_layout = QVBoxLayout()
        
        add_button = QPushButton("Add")
        add_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #2ECC71;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover { background: #27AE60; }
        """)
        add_button.clicked.connect(self.accept_tool)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #E74C3C;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover { background: #C0392B; }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        self.frame_layout.addLayout(button_layout)

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
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.frame_layout.addWidget(title)

        # Parameter inputs
        self.param_inputs = {}
        for param, value in self.tool.get_parameters().items():
            param_label = QLabel(param)
            param_label.setStyleSheet("color: white;")
            self.frame_layout.addWidget(param_label)
            
            input_field = QLineEdit(str(value))
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    background: #34495E;
                    color: white;
                    border: 1px solid #456789;
                    border-radius: 5px;
                }
            """)
            self.frame_layout.addWidget(input_field)
            self.param_inputs[param] = input_field

        # Buttons
        button_layout = QVBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #2ECC71;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover { background: #27AE60; }
        """)
        save_button.clicked.connect(self.save_config)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #E74C3C;
                border: none;
                border-radius: 5px;
                color: white;
            }
            QPushButton:hover { background: #C0392B; }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        self.frame_layout.addLayout(button_layout)

    def save_config(self):
        try:
            new_params = {}
            for param, input_field in self.param_inputs.items():
                try:
                    new_value = eval(input_field.text().strip())
                    new_params[param] = new_value
                except Exception as e:
                    raise ValueError(f"Invalid value for {param}: {str(e)}")

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