"""
Main entry point for Augment VIP GUI (MVC Version)
Universal launcher with dependency management
Works on Windows, macOS, and Linux
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def get_python_command():
    """Get the appropriate Python command for this system"""
    python_commands = ['python3', 'python', 'py']
    
    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0 and 'Python 3' in result.stdout:
                return cmd
        except FileNotFoundError:
            continue
    
    return None

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PySide6
        import psutil
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    python_cmd = get_python_command()
    if not python_cmd:
        print("❌ Python 3 not found. Please install Python 3.6 or later.")
        return False
    
    print("📦 Installing dependencies...")
    try:
        subprocess.run([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please run manually:")
        print(f"   {python_cmd} -m pip install -r requirements.txt")
        return False

def main():
    """Main entry point with auto-setup"""
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    system = platform.system()
    print(f"🚀 Augment VIP - VS Code Privacy Tools")
    print(f"📱 Platform: {system}")
    print(f"📁 Directory: {current_dir}")
    print()
    
    # Check dependencies first
    if not check_dependencies():
        print("📦 Setting up dependencies for first run...")
        if not install_dependencies():
            print("\n❌ Setup failed. Please install manually:")
            print("   pip install -r requirements.txt")
            input("Press Enter to exit...")
            sys.exit(1)
        print("✅ Setup completed successfully!")
        print()
    
    # Add src directory to Python path
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        # Import and run GUI application
        from src.core.application import run_gui_application
        print("🎯 Starting GUI application...")
        return run_gui_application()
        
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("Please ensure all dependencies are installed correctly.")
        input("Press Enter to exit...")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
