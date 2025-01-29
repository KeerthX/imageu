

# gui/dialogs.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QFrame, QGraphicsOpacityEffect
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QPoint
from PyQt5.QtGui import QColor, QPalette

class AnimatedDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create main frame
        self.frame = QFrame(self)
        self.frame.setObjectName("dialogFrame")
        self.frame.setStyleSheet("""
            QFrame#dialogFrame {
                background: #2C3E50;
                border-radius: 10px;
                border: 1px solid #34495E;
            }
        """)
        
        # Setup opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.frame.setGraphicsEffect(self.opacity_effect)
        
        # Setup animations
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)

    def showEvent(self, event):
        super().showEvent(event)
        self.fade_in.start()

class AddProcessDialog(AnimatedDialog):
    def __init__(self, available_tools):
        super().__init__()
        self.setWindowTitle("Add Processing Tool")
        self.setFixedSize(400, 250)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        layout = QVBoxLayout(self.frame)
        
        # Stylish label
        self.label = QLabel("Select a processing tool")
        self.label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(self.label)

        # Styled ComboBox
        self.tool_selector = QComboBox()
        self.tool_selector.addItems(available_tools)
        self.tool_selector.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border-radius: 5px;
                background: #34495E;
                color: #ECF0F1;
                border: 1px solid #456789;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(assets/down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        layout.addWidget(self.tool_selector)

        # Buttons
        button_layout = QVBoxLayout()
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #2ECC71;
                border: none;
                border-radius: 5px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #27AE60;
            }
        """)
        self.add_button.clicked.connect(self.add_tool)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #E74C3C;
                border: none;
                border-radius: 5px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #C0392B;
            }
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        main_layout.addWidget(self.frame)

    def add_tool(self):
        self.selected_process = self.tool_selector.currentText()
        self.accept()

class ConfigDialog(AnimatedDialog):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.setWindowTitle(f"Configure {tool.__class__.__name__}")
        self.setFixedSize(400, 300)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        self.layout = QVBoxLayout(self.frame)

        # Parameter inputs with styling
        self.config_inputs = {}
        for param, value in tool.get_parameters().items():
            param_label = QLabel(param)
            param_label.setStyleSheet("""
                QLabel {
                    color: #ECF0F1;
                    font-size: 14px;
                    margin-top: 5px;
                }
            """)
            self.layout.addWidget(param_label)
            
            input_field = QLineEdit(str(value))
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border-radius: 5px;
                    background: #34495E;
                    color: #ECF0F1;
                    border: 1px solid #456789;
                }
                QLineEdit:focus {
                    border: 1px solid #3498DB;
                }
            """)
            self.layout.addWidget(input_field)
            self.config_inputs[param] = input_field

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #2ECC71;
                border: none;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                margin-top: 15px;
            }
            QPushButton:hover {
                background: #27AE60;
            }
        """)
        save_button.clicked.connect(self.save_config)
        self.layout.addWidget(save_button)
        
        main_layout.addWidget(self.frame)

    def save_config(self):
        try:
            for param, input_field in self.config_inputs.items():
                new_value = eval(input_field.text().strip())
                setattr(self.tool, param, new_value)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Invalid Parameter", str(e))