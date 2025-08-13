"""
Main Window - Primary application view using MVC pattern
"""

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTextEdit, QLabel, QProgressBar,
    QGroupBox, QMessageBox, QFrame, QSizePolicy,
    QGridLayout, QSpacerItem, QSplitter
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QTextCursor, QIcon
import os

from .style_manager import StyleManager
from ..controllers.main_controller import MainController


class MainWindow(QMainWindow):
    """Main application window following MVC pattern"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize controller
        self.controller = MainController(self)
        
        # UI components
        self.status_label = None
        self.clean_btn = None
        self.modify_ids_btn = None
        self.run_all_btn = None
        self.restart_btn = None
        self.output_text = None
        self.progress_bar = None
        
        # Initialize UI
        self.init_ui()
        
        # Connect to controller
        self.controller.initialize()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🚀 Augment VIP - VS Code Privacy & Database Tools")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'app_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Apply styling
        self.setStyleSheet(StyleManager.get_complete_stylesheet())
        
        # Create main splitter layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(350)
        splitter.addWidget(sidebar)
        
        # Create main content area
        main_content = self.create_main_content()
        main_content.setObjectName("mainContent")
        splitter.addWidget(main_content)
        
        # Set splitter proportions
        splitter.setStretchFactor(0, 0)  # Sidebar doesn't stretch
        splitter.setStretchFactor(1, 1)  # Main content stretches
    
    def create_sidebar(self) -> QWidget:
        """Create the sidebar with controls"""
        sidebar = QWidget()
        layout = QVBoxLayout()
        sidebar.setLayout(layout)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        self.create_header_section(layout)
        
        # VS Code Status
        self.create_status_section(layout)
        
        # Action buttons
        self.create_action_section(layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Processing... %p%")
        layout.addWidget(self.progress_bar)
        
        # Footer spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        return sidebar
    
    def create_main_content(self) -> QWidget:
        """Create the main content area with output log"""
        main_content = QWidget()
        layout = QVBoxLayout()
        main_content.setLayout(layout)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Output area (takes full main content)
        self.create_output_section(layout)
        
        return main_content
    
    def create_header_section(self, layout: QVBoxLayout):
        """Create header with title and description"""
        header_widget = QWidget()
        header_layout = QVBoxLayout()
        header_widget.setLayout(header_layout)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("🚀 Augment VIP")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("VS Code Privacy Tools")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #cccccc; font-size: 12px; font-style: italic; margin-bottom: 5px;")
        header_layout.addWidget(subtitle_label)
        
        # Separator
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        header_layout.addWidget(separator)
        
        layout.addWidget(header_widget)
    
    def create_status_section(self, layout: QVBoxLayout):
        """Create status information section"""
        status_group = QGroupBox("📊 VS Code Status")
        status_layout = QVBoxLayout()
        status_group.setLayout(status_layout)
        status_layout.setSpacing(15)
        status_layout.setContentsMargins(10, 15, 10, 15)
        
        # Status container
        status_container = QWidget()
        status_container_layout = QVBoxLayout()
        status_container.setLayout(status_container_layout)
        status_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Status icon and text
        self.status_label = QLabel("🔍 Checking...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        status_container_layout.addWidget(self.status_label)
        
        status_layout.addWidget(status_container)
        
        # Info text
        info_label = QLabel("ℹ️ VS Code installation required")
        info_label.setObjectName("descLabel")
        info_label.setWordWrap(True)
        status_layout.addWidget(info_label)
        
        layout.addWidget(status_group)
    
    def create_action_section(self, layout: QVBoxLayout):
        """Create action buttons section"""
        action_group = QGroupBox("🛠️ Actions")
        action_layout = QVBoxLayout()
        action_group.setLayout(action_layout)
        action_layout.setSpacing(15)
        action_layout.setContentsMargins(10, 15, 10, 15)
        
        # Clean Database button
        self.clean_btn = QPushButton("🧹 Clean DB")
        self.clean_btn.setObjectName("cleanBtn")
        self.clean_btn.setToolTip("Remove Augment-related entries from VS Code databases")
        self.clean_btn.clicked.connect(lambda: self.controller.clean_database())
        self.clean_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        action_layout.addWidget(self.clean_btn)
        
        # Modify IDs button  
        self.modify_ids_btn = QPushButton("🔐 Modify IDs")
        self.modify_ids_btn.setObjectName("modifyBtn")
        self.modify_ids_btn.setToolTip("Generate new random telemetry IDs for enhanced privacy")
        self.modify_ids_btn.clicked.connect(lambda: self.controller.modify_telemetry_ids())
        self.modify_ids_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        action_layout.addWidget(self.modify_ids_btn)
        
        # Run All button
        self.run_all_btn = QPushButton("🚀 Run All")
        self.run_all_btn.setObjectName("runAllBtn")
        self.run_all_btn.setToolTip("Execute both database cleaning and ID modification")
        self.run_all_btn.clicked.connect(lambda: self.controller.run_all_operations())
        self.run_all_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        action_layout.addWidget(self.run_all_btn)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #444444; margin: 10px 0;")
        action_layout.addWidget(separator)
        
        # Restart VS Code button
        self.restart_btn = QPushButton("🔄 Restart VS Code")
        self.restart_btn.setObjectName("restartBtn")
        self.restart_btn.setToolTip("Close and restart VS Code to apply changes")
        self.restart_btn.clicked.connect(lambda: self.controller.restart_vscode())
        self.restart_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        action_layout.addWidget(self.restart_btn)
        
        layout.addWidget(action_group)
    
    def create_output_section(self, layout: QVBoxLayout):
        """Create output text area"""
        output_group = QGroupBox("📋 Operation Log")
        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)
        output_layout.setSpacing(15)
        output_layout.setContentsMargins(15, 20, 15, 20)
        
        # Log header
        log_header = QWidget()
        log_header_layout = QHBoxLayout()
        log_header.setLayout(log_header_layout)
        log_header_layout.setContentsMargins(0, 0, 0, 0)
        
        log_info = QLabel("📝 Real-time operation status and detailed logs")
        log_info.setObjectName("descLabel")
        log_header_layout.addWidget(log_info)
        
        log_header_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setObjectName("clearBtn")
        clear_btn.setFixedWidth(100)
        clear_btn.clicked.connect(self.clear_output)
        log_header_layout.addWidget(clear_btn)
        
        output_layout.addWidget(log_header)
        
        # Output text area - takes full height
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        
        # Add welcome message
        self.show_welcome_message()
        
        output_layout.addWidget(self.output_text)
        
        layout.addWidget(output_group)
    
    def show_welcome_message(self):
        """Show welcome message in output"""
        welcome_msg = """
🚀 <b>Welcome to Augment VIP!</b>

This tool helps you maintain privacy and clean VS Code databases.
Select an operation from the sidebar to get started.

<b>Features:</b>
• Safe database cleaning with automatic backups
• Privacy-focused telemetry ID modification  
• Real-time progress tracking
• Detailed operation logs

Ready to enhance your VS Code privacy! 🔐
        """.strip()
        
        self.output_text.setHtml(f'<div style="color: #4a9eff; font-family: Consolas, Monaco, monospace; padding: 15px; line-height: 1.5;">{welcome_msg}</div>')
    
    def clear_output(self):
        """Clear output and show welcome message"""
        self.show_welcome_message()
    
    # View interface methods (called by controller)
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status label with message and styling"""
        self.status_label.setText(message)
        
        # Apply status-specific styling
        status_style = StyleManager.get_status_style(status_type)
        if status_style:
            self.status_label.setStyleSheet(status_style)
    
    def set_buttons_enabled(self, enabled: bool):
        """Enable or disable action buttons"""
        self.clean_btn.setEnabled(enabled)
        self.modify_ids_btn.setEnabled(enabled)
        self.run_all_btn.setEnabled(enabled)
        self.restart_btn.setEnabled(enabled)
    
    def set_specific_button_enabled(self, button_name: str, enabled: bool):
        """Enable/disable specific button"""
        if button_name == "clean":
            self.clean_btn.setEnabled(enabled)
        elif button_name == "modify":
            self.modify_ids_btn.setEnabled(enabled)
        elif button_name == "run_all":
            self.run_all_btn.setEnabled(enabled)
        elif button_name == "restart":
            self.restart_btn.setEnabled(enabled)
    
    def show_progress(self, show: bool = True):
        """Show or hide progress bar"""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
    
    def add_log_message(self, message: str, msg_type: str = "info"):
        """Add message to output log"""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        
        color_map = {
            "info": "#4a9eff",
            "success": "#28a745",
            "error": "#dc3545",
            "warning": "#ffc107"
        }
        
        color = color_map.get(msg_type, "#4a9eff")
        type_label = msg_type.upper()
        
        html_message = f'<div style="color: {color}; margin: 5px 0;"><b>[{timestamp}] {type_label}:</b> {message}</div>'
        self.output_text.append(html_message)
        
        # Scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.output_text.setTextCursor(cursor)
    
    def show_message_box(self, title: str, message: str, msg_type: str = "info"):
        """Show styled message box"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
        
        # Apply styling
        msg_box.setStyleSheet(StyleManager.get_messagebox_stylesheet(msg_type))
        msg_box.exec()
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Let controller handle cleanup
        self.controller.cleanup()
        event.accept()
