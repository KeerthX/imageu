from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


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
        try:
            for param, input_field in self.config_inputs.items():
                new_value = input_field.text().strip()

                # Validate and set new values for specific parameters
                if param == "kernel_size":  # Example: FilterTool
                    new_value = int(new_value)
                    if new_value <= 0 or new_value % 2 == 0:
                        raise ValueError("Kernel size must be a positive odd integer.")
                elif param in ["width", "height"]:  # Example: ResizeTool
                    new_value = int(new_value)
                    if new_value <= 0:
                        raise ValueError(f"{param} must be a positive integer.")
                else:
                    # For generic string, float, or int parameters
                    try:
                        new_value = eval(new_value)  # Use eval carefully, or avoid it.
                    except:
                        pass

                # Set the validated new value to the tool
                setattr(self.tool, param, new_value)

            self.accept()  # Close the dialog after successful save

        except Exception as e:
        # Show an error message if the input is invalid
            QMessageBox.critical(self, "Invalid Parameter", str(e))
