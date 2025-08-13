"""
Core Application - Main application entry point with MVC architecture
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ..views.main_window import MainWindow


class Application:
    """Main application class following MVC pattern"""
    
    def __init__(self):
        self.qt_app = None
        self.main_window = None
    
    def initialize(self) -> bool:
        """Initialize the application"""
        try:
            # Create QApplication
            self.qt_app = QApplication(sys.argv)
            
            # Set application properties
            self.qt_app.setApplicationName("Augment VIP")
            self.qt_app.setApplicationVersion("1.0.0")
            self.qt_app.setOrganizationName("Azril Aiman")
            self.qt_app.setOrganizationDomain("azrilaiman.my")
            
            # Set application attributes
            self.qt_app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
            self.qt_app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
            
            # Create main window
            self.main_window = MainWindow()
            
            return True
            
        except Exception as e:
            print(f"Failed to initialize application: {e}")
            return False
    
    def run(self) -> int:
        """Run the application"""
        if not self.initialize():
            return 1
        
        try:
            # Show main window
            self.main_window.show()
            
            # Run event loop
            return self.qt_app.exec()
            
        except Exception as e:
            print(f"Application runtime error: {e}")
            return 1
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup application resources"""
        if self.main_window:
            # Main window cleanup is handled in its closeEvent
            pass
        
        if self.qt_app:
            # Qt cleanup is automatic
            pass


def run_gui_application() -> int:
    """Entry point for GUI application"""
    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(run_gui_application())
