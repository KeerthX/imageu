from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QLineEdit, QMessageBox


class AddProcessDialog(QDialog):
    def __init__(self, available_tools):
        super().__init__()
        self.setWindowTitle("Add Processing Tool")
        self.setGeometry(400, 200, 300, 150)
        self.selected_process = None

        # Main layout
        layout = QVBoxLayout(self)

        # Label and ComboBox for selecting tools
        self.label = QLabel("Select a processing tool:")
        layout.addWidget(self.label)

        self.tool_selector = QComboBox()
        self.tool_selector.addItems(available_tools)
        layout.addWidget(self.tool_selector)

        # Add and Cancel buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_tool)
        layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

    def add_tool(self):
        self.selected_process = self.tool_selector.currentText()
        self.accept()


class ConfigDialog(QDialog):
    def __init__(self, tool):
        super().__init__()
        self.tool = tool
        self.setWindowTitle(f"Configure {tool.__class__.__name__}")
        self.setGeometry(400, 200, 300, 150)
        self.layout = QVBoxLayout(self)

        self.config_inputs = {}
        for param, value in tool.get_parameters().items():
            self.layout.addWidget(QLabel(param))
            input_field = QLineEdit(str(value))
            self.layout.addWidget(input_field)
            self.config_inputs[param] = input_field

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        self.layout.addWidget(save_button)

    def save_config(self):
        try:
            for param, input_field in self.config_inputs.items():
                new_value = eval(input_field.text().strip())
                setattr(self.tool, param, new_value)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Invalid Parameter", str(e))
