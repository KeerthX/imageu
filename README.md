# ImageU

**ImageU** is an simple image processing application that provides an intuitive UI for applying various image enhancement and transformation techniques. It includes real-time image processing, a modern full-screen UI, and dynamic parameter adjustments.

## 🚀 Features

- **Modern Full-Screen UI**: A sleek, responsive design with smooth animations.
- **Advanced Image Viewer**: Supports zoom, pan, reset, and fit-to-screen functionalities.
- **Processing Tools**: Apply enhancements like brightness, contrast, filters, rotation, sharpening, and resizing.
- **Dynamic Parameter Adjustment**: Modify tool settings in real-time using dialogs.
- **Processing Queue**: Add, remove, and reorder processing steps with an intuitive draggable list.
- **Dark Mode Styling**: Aesthetic and user-friendly interface with custom themes.

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/KeerthX/imageu
cd image-u
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎨 Usage

### Run the Application

```bash
python main.py
```

### UI Overview

- **Left Sidebar**: Upload, Save, and Processing Queue.
- **Center Panel**: Displays the image with interactive controls.
- **Right Panel**: Parameter adjustment dialogs for processing tools.

---

## 📦 Project Structure

```
image-u/
│── assets/                 # Stylesheets and assets
│   ├── styles.qss          # UI styling file
│
│── build/                  # Distribution build folder
│── config/                 # Configuration files
│   ├── tools_config.json   # Stores tool settings
│
│── dist/                   # Compiled executable (if built with PyInstaller)
│
│── gui/                    # UI components
│   ├── dialogs.py          # Configuration dialogs
│   ├── image_viewer.py     # Image display & manipulation
│   ├── main_window.py      # Main application window
│
│── styles/                 # UI styles
│── tools/                  # Image processing tools
│   ├── brightness.py
│   ├── contrast.py
│   ├── filter.py
│   ├── resize.py
│   ├── rotate.py
│   ├── sharpen.py
│
│── utils/                  # Helper functions
│   ├── tool_manager.py     # Manages available processing tools
│
│── LICENSE                 # License file
│── main.py                 # Entry point of the application
│── main.spec               # PyInstaller specification file
│── README.md               # Documentation
│── requirements.txt        # Dependencies
```

---

## 🏗 Building an Executable

To generate a standalone executable using **PyInstaller**:

```bash
pyinstaller --onefile --windowed main.py
```

The output executable will be located in the `dist/` folder.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🏆 Credits

Developed by **Prakeerth Jisha Madhu Prakash**.
