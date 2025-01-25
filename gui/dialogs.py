from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class ConfigDialog(QDialog):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.setWindowTitle(f"Configure {tool.__class__.__name__}")
        self.layout = QVBoxLayout(self)

        # Display tool parameters as editable fields
        self.config_inputs = {}
        for param, value in tool.get_parameters().items():
            self.layout.addWidget(QLabel(param))
            input_field = QLineEdit(str(value))
            self.layout.addWidget(input_field)
            self.config_inputs[param] = input_field

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        self.layout.addWidget(save_button)

    def save_config(self):
        for param, input_field in self.config_inputs.items():
            new_value = input_field.text()
            try:
                setattr(self.tool, param, eval(new_value))
            except:
                setattr(self.tool, param, new_value)
        self.accept()
