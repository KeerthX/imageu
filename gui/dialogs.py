 
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ConfigDialog(QDialog):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.setWindowTitle(f"Configure {tool.__class__.__name__}")
        self.layout = QVBoxLayout(self)

        # Display configuration options
        self.config_inputs = {}
        for attr, value in vars(tool).items():
            if isinstance(value, (int, float, str)):
                self.layout.addWidget(QLabel(attr))
                input_field = QLineEdit(str(value))
                self.layout.addWidget(input_field)
                self.config_inputs[attr] = input_field

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        self.layout.addWidget(save_button)

    def save_config(self):
        for attr, input_field in self.config_inputs.items():
            new_value = input_field.text()
            try:
                setattr(self.tool, attr, eval(new_value))
            except:
                setattr(self.tool, attr, new_value)
        self.accept()
