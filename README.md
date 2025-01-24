 
image_processor_tool/
├── assets/
│   ├── icons/
│   └── sample_images/
├── build/                # Contains build/executable files (if any)
├── config/
│   └── tools_config.json # Tool-specific configurations
├── dist/                 # Distribution files for sharing
├── gui/                  # All GUI-related files
│   ├── __init__.py
│   ├── main_window.py
│   ├── dialogs.py
│   └── image_viewer.py
├── utils/                # Utilities like tool manager
│   ├── __init__.py
│   └── tool_manager.py
├── tools/                # Image processing tools
│   ├── __init__.py
│   ├── resize.py
│   ├── filter.py
│   └── rotate.py
├── tests/                # Test files
│   ├── test_main.py
│   └── test_tools.py
├── LICENSE
├── main.py               # Main entry point of the application
├── main.spec             # For packaging with PyInstaller
├── README.md
└── requirements.txt      # Python dependencies
