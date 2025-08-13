# Augment VIP - Cross-Platform MVC Architecture

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg)
![Architecture](https://img.shields.io/badge/architecture-MVC-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)

A modern, cross-platform utility toolkit for VS Code privacy management following **Model-View-Controller (MVC)** architecture. Provides tools to manage and clean VS Code databases with a professional GUI interface.

**🌟 Now supports Windows, macOS, and Linux!**

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

- **🖥️ Cross-Platform**: Native support for Windows, macOS, and Linux
- **🎨 Modern GUI Interface**: Clean, professional PySide6-based interface with sidebar layout
- **🧹 Database Cleaning**: Remove Augment-related entries from VS Code databases
- **🔐 Telemetry ID Modification**: Generate random telemetry IDs for enhanced privacy
- **🔄 VS Code Restart**: Automatically restart VS Code after operations
- **🛡️ Safe Operations**: Automatic backups before making changes
- **📊 Real-time Progress**: Live operation tracking with detailed logs
- **🏗️ MVC Architecture**: Well-structured, maintainable codebase
- **🚀 Process Management**: Smart VS Code process detection and management

## 📋 Requirements

- **Python 3.6+** (any platform)
- **PySide6** (Qt for Python) - GUI framework  
- **psutil** - Cross-platform process management
- **VS Code installation** (Windows/macOS/Linux)

## 💻 Installation & Usage

### 🚀 Super Simple - One Entry Point

**Just run this on any platform:**
```bash
python main.py
```

### 🏗️ Build Executables

**Windows/Mac/Linux (Local Build):**
```cmd
# Windows
build.bat

# Mac/Linux  
./build.sh
```

**ALL PLATFORMS (GitHub Actions):**
```bash
git tag v1.0.0
git push origin v1.0.0
```
✅ Automatically builds Windows `.exe`, macOS `.app`, Linux binary  
✅ Download from GitHub Releases  
✅ Zero setup needed!

### 📦 Building Executables

**Windows:**
```cmd
build_gui.bat
```

**macOS/Linux:**
```bash
chmod +x build_gui.sh
./build_gui.sh
```

The executable will be created in the `dist/` folder:
- **Windows**: `dist/AugmentVIP.exe`
- **macOS**: `dist/AugmentVIP.app` (double-click to run)
- **Linux**: `dist/AugmentVIP` (executable binary)

## 🖥️ Platform Support

### ✅ Supported Platforms

| Platform | Architecture | VS Code Detection | Process Management | Build Support |
|----------|-------------|-------------------|-------------------|---------------|
| **Windows 10/11** | x64, x86 | ✅ AppData paths | ✅ Process control | ✅ .exe |
| **macOS 10.14+** | Intel, Apple Silicon | ✅ Library paths | ✅ Process control | ✅ .app bundle |
| **Ubuntu 18.04+** | x64, ARM64 | ✅ .config paths | ✅ Process control | ✅ Binary |
| **Debian 10+** | x64, ARM64 | ✅ .config paths | ✅ Process control | ✅ Binary |
| **CentOS/RHEL 7+** | x64 | ✅ .config paths | ✅ Process control | ✅ Binary |
| **Arch Linux** | x64 | ✅ .config paths | ✅ Process control | ✅ Binary |

### 🔍 VS Code Variants Supported
- **VS Code** (Microsoft)
- **VS Code Insiders**
- **VSCodium** (Open Source)
- **Code - OSS**

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
