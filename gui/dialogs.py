# gui/dialogs.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QFrame, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtGui import QPalette, QFont

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

class AddProcessDialog(BaseDialog):
    def __init__(self, available_tools, parent=None):
        self.available_tools = available_tools
        super().__init__(parent)
        self.selected_process = None
        self.setup_content()

    def setup_content(self):
        # Title
        title = QLabel("Add Processing Tool")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #E0E0E0; margin-bottom: 8px;")
        self.frame_layout.addWidget(title)

        # Tool selector
        self.tool_selector = QComboBox()
        self.tool_selector.addItems(self.available_tools)
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

        # Buttons
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
            
            input_field = QLineEdit(str(value))
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 12px;
                    background: #3E3E42;
                    color: #E0E0E0;
                    border: none;
                    border-radius: 6px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 1px solid #007ACC;
                }
                QLineEdit:hover {
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