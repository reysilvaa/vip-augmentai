# Augment VIP - MVC Architecture

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Architecture](https://img.shields.io/badge/architecture-MVC-orange.svg)

A modern, well-structured utility toolkit for Augment VIP users following **Model-View-Controller (MVC)** architecture. Provides tools to manage and clean VS Code databases with a professional GUI interface.

## 🏗️ Architecture Overview

This project follows the **MVC (Model-View-Controller)** pattern for better code organization, maintainability, and testability:

```
src/
├── models/           # Data structures and business logic
│   ├── vscode_model.py      # VS Code installation management
│   ├── database_model.py    # Database operations
│   └── telemetry_model.py   # Telemetry ID operations
├── views/            # User interface components
│   ├── main_window.py       # Primary GUI window
│   └── style_manager.py     # Centralized styling
├── controllers/      # Application logic coordination  
│   └── main_controller.py   # Main application controller
├── services/         # External integrations & utilities
│   ├── file_service.py      # File operations service
│   └── vscode_service.py    # High-level VS Code service
└── core/             # Application foundation
    └── application.py       # Application entry point
```

### 🔧 MVC Benefits
- **Separation of Concerns**: Clear separation between data, UI, and logic
- **Maintainability**: Easy to modify individual components 
- **Testability**: Each layer can be tested independently
- **Scalability**: Easy to add new features and components
- **Reusability**: Components can be reused across the application

## 🚀 Features

- **Modern GUI Interface**: Clean, professional PySide6-based interface with sidebar layout
- **Database Cleaning**: Remove Augment-related entries from VS Code databases
- **Telemetry ID Modification**: Generate random telemetry IDs for enhanced privacy
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Safe Operations**: Automatic backups before making changes
- **Real-time Progress**: Live operation tracking with detailed logs
- **MVC Architecture**: Well-structured, maintainable codebase

## 📋 Requirements

- Python 3.6 or higher
- PySide6 (Qt for Python)
- VS Code installation

## 💻 Installation & Usage

### Quick Start - GUI Application

```bash
# Clone repository
git clone https://github.com/azrilaiman2003/augment-vip.git
cd augment-vip

# Install dependencies
pip install -r requirements.txt

# Run MVC application
python main_mvc.py
```

### Building Executable

```bash
# Build standalone executable
pyinstaller augment_vip_mvc.spec

# Run executable
dist/AugmentVIP_MVC.exe  # Windows
dist/AugmentVIP_MVC      # macOS/Linux
```

### Legacy CLI Support

The original CLI interface is still available:

```bash
# Install as package
pip install -e .

# Run CLI commands
augment-vip gui     # Launch GUI
augment-vip clean   # Clean databases
augment-vip modify-ids  # Modify telemetry IDs
augment-vip all     # Run all operations
```

## 🗂️ Project Structure (Clean MVC)

```
augment-vip/
├── src/                      # Source code (MVC architecture)
│   ├── models/               # Business logic & data structures
│   ├── views/                # UI components & styling  
│   ├── controllers/          # Application logic coordination
│   ├── services/             # External service integrations
│   └── core/                 # Application foundation
├── config/                   # Configuration files
├── assets/                   # Static resources
├── tests/                    # Unit tests
├── scripts/                  # Build & installation scripts
├── augment_vip/             # Legacy package (backward compatibility)
├── main_mvc.py              # MVC application entry point
├── main_gui.py              # Legacy GUI entry point
└── augment_vip_mvc.spec     # PyInstaller spec for MVC build
```

## 🎨 GUI Features

### Sidebar Layout
- **No scrolling** - Everything fits in the window
- **Persistent controls** - Sidebar always visible
- **Large output area** - Better log visibility
- **Resizable** - User can adjust splitter

### Modern Styling
- **Dark theme** with professional gradients
- **Color-coded buttons** for different operations
- **Status indicators** with dynamic colors
- **Real-time timestamps** in logs
- **Custom message boxes** with consistent styling

### User Experience
- **Threaded operations** - UI never freezes
- **Progress tracking** - Real-time operation status
- **Detailed logging** - Complete operation history
- **Safe operations** - Automatic backups
- **Error handling** - Graceful failure management

## 🔍 How It Works

### Models (Data Layer)
- **VSCodeModel**: Detects and manages VS Code installation
- **DatabaseModel**: Handles SQLite database operations
- **TelemetryModel**: Manages telemetry ID generation and updates

### Views (Presentation Layer)  
- **MainWindow**: Primary GUI interface with sidebar layout
- **StyleManager**: Centralized styling and theme management

### Controllers (Logic Layer)
- **MainController**: Coordinates between models and views
- **OperationWorker**: Background thread for non-blocking operations

### Services (Integration Layer)
- **VSCodeService**: High-level VS Code operations
- **FileService**: File system operations and utilities

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Structure Guidelines
- **Models**: Pure business logic, no UI dependencies
- **Views**: UI components, minimal business logic
- **Controllers**: Coordinate between models and views
- **Services**: External integrations and utilities

### Adding Features
1. Create model for data structure
2. Add service methods for operations  
3. Update controller for coordination
4. Modify view for UI changes
5. Add tests for new functionality

## 📜 Migration from Legacy

The MVC version coexists with the legacy structure:

- **New users**: Use `main_mvc.py` for modern architecture
- **Existing users**: Legacy `main_gui.py` still works
- **CLI users**: `augment-vip` commands unchanged
- **Build scripts**: Updated to support both versions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Follow MVC patterns for new code
4. Add tests for new functionality
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open Pull Request

## 📞 Contact

Azril Aiman - me@azrilaiman.my

Project Link: [https://github.com/azrilaiman2003/augment-vip](https://github.com/azrilaiman2003/augment-vip)

---

Made with ❤️ and proper software architecture by [Azril Aiman](https://github.com/azrilaiman2003)
