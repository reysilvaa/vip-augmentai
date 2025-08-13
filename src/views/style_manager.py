"""
Style Manager - Centralized styling for the application
"""

from typing import Dict, Any

class StyleManager:
    """Manages application styling and themes"""
    
    # Color palette
    COLORS = {
        "primary": "#4a9eff",
        "primary_dark": "#357abd",
        "primary_light": "#5ba8ff",
        "secondary": "#2b2b2b",
        "background": "#1e1e1e",
        "surface": "#2a2a2a",
        "surface_light": "#3a3a3a",
        "text_primary": "#ffffff",
        "text_secondary": "#cccccc",
        "text_muted": "#aaaaaa",
        "success": "#28a745",
        "success_light": "#34ce57",
        "warning": "#ffc107",
        "warning_dark": "#e0a800",
        "error": "#dc3545",
        "error_light": "#e45565",
        "info": "#17a2b8",
        "clean": "#ff6b35",
        "clean_hover": "#ff7b45",
        "modify": "#28a745",
        "modify_hover": "#34ce57",
        "run_all": "#6f42c1",
        "run_all_hover": "#7952cc"
    }
    
    @classmethod
    def get_main_stylesheet(cls) -> str:
        """Get the main application stylesheet"""
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['secondary']}, stop:1 {cls.COLORS['background']});
                color: {cls.COLORS['text_primary']};
            }}
            QWidget {{
                background-color: transparent;
                color: {cls.COLORS['text_primary']};
            }}
            QSplitter {{
                background: {cls.COLORS['secondary']};
            }}
            QSplitter::handle {{
                background: {cls.COLORS['primary']};
                width: 3px;
                border-radius: 1px;
            }}
            QSplitter::handle:hover {{
                background: {cls.COLORS['primary_light']};
            }}
            QWidget#sidebar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['surface']}, stop:1 {cls.COLORS['surface_light']});
                border-right: 2px solid {cls.COLORS['primary']};
            }}
            QWidget#mainContent {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['secondary']}, stop:1 {cls.COLORS['background']});
            }}
        """
    
    @classmethod
    def get_groupbox_stylesheet(cls) -> str:
        """Get GroupBox styling"""
        return f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {cls.COLORS['primary']};
                border-radius: 12px;
                margin: 15px 5px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(74, 158, 255, 0.1), stop:1 rgba(74, 158, 255, 0.05));
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 15px 0 15px;
                color: {cls.COLORS['primary']};
                font-weight: bold;
            }}
        """
    
    @classmethod
    def get_button_stylesheet(cls) -> str:
        """Get Button styling"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['primary_dark']});
                color: {cls.COLORS['text_primary']};
                border: none;
                border-radius: 10px;
                padding: 15px 25px;
                font-size: 13px;
                font-weight: bold;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['primary_light']}, stop:1 {cls.COLORS['primary']});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['primary_dark']}, stop:1 #2a5f8f);
            }}
            QPushButton:disabled {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #666666, stop:1 #444444);
                color: #999999;
            }}
            QPushButton#cleanBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['clean']}, stop:1 #e55a2b);
            }}
            QPushButton#cleanBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['clean_hover']}, stop:1 #f56a3b);
            }}
            QPushButton#modifyBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['modify']}, stop:1 #218838);
            }}
            QPushButton#modifyBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['modify_hover']}, stop:1 {cls.COLORS['modify']});
            }}
            QPushButton#runAllBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['run_all']}, stop:1 #5a2d91);
            }}
            QPushButton#runAllBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['run_all_hover']}, stop:1 #6339a2);
            }}
            QPushButton#restartBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fd7e14, stop:1 #e8680e);
                color: #000000;
                font-weight: bold;
            }}
            QPushButton#restartBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff8c26, stop:1 #fd7e14);
            }}
            QPushButton#clearBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {cls.COLORS['warning']}, stop:1 {cls.COLORS['warning_dark']});
                color: #000000;
                font-weight: bold;
            }}
            QPushButton#clearBtn:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffcd3c, stop:1 #ffb700);
            }}
        """
    
    @classmethod
    def get_text_stylesheet(cls) -> str:
        """Get text widget styling"""
        return f"""
            QTextEdit {{
                border: 2px solid #444444;
                border-radius: 8px;
                background-color: #1a1a1a;
                color: {cls.COLORS['text_primary']};
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                padding: 10px;
            }}
            QLabel {{
                color: {cls.COLORS['text_primary']};
                font-size: 12px;
            }}
            QLabel#titleLabel {{
                color: {cls.COLORS['primary']};
                font-size: 20px;
                font-weight: bold;
                padding: 10px 0;
            }}
            QLabel#statusLabel {{
                font-size: 11px;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
                background-color: rgba(74, 158, 255, 0.1);
            }}
            QLabel#descLabel {{
                color: {cls.COLORS['text_secondary']};
                font-size: 10px;
                padding: 5px;
            }}
        """
    
    @classmethod
    def get_progressbar_stylesheet(cls) -> str:
        """Get progress bar styling"""
        return f"""
            QProgressBar {{
                border: 2px solid #444444;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                color: {cls.COLORS['text_primary']};
                background-color: {cls.COLORS['surface']};
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {cls.COLORS['primary']}, stop:1 {cls.COLORS['primary_dark']});
                border-radius: 6px;
            }}
        """
    
    @classmethod
    def get_separator_stylesheet(cls) -> str:
        """Get separator styling"""
        return f"""
            QFrame#separator {{
                background-color: #444444;
                max-height: 2px;
            }}
        """
    
    @classmethod
    def get_complete_stylesheet(cls) -> str:
        """Get complete application stylesheet"""
        return (
            cls.get_main_stylesheet() +
            cls.get_groupbox_stylesheet() +
            cls.get_button_stylesheet() +
            cls.get_text_stylesheet() +
            cls.get_progressbar_stylesheet() +
            cls.get_separator_stylesheet()
        )
    
    @classmethod
    def get_status_style(cls, status_type: str) -> str:
        """Get status-specific styling"""
        styles = {
            "success": f"""
                QLabel#statusLabel {{
                    background-color: rgba(40, 167, 69, 0.2);
                    color: {cls.COLORS['success']};
                    border: 2px solid {cls.COLORS['success']};
                }}
            """,
            "warning": f"""
                QLabel#statusLabel {{
                    background-color: rgba(255, 193, 7, 0.2);
                    color: {cls.COLORS['warning']};
                    border: 2px solid {cls.COLORS['warning']};
                }}
            """,
            "error": f"""
                QLabel#statusLabel {{
                    background-color: rgba(220, 53, 69, 0.2);
                    color: {cls.COLORS['error']};
                    border: 2px solid {cls.COLORS['error']};
                }}
            """
        }
        return styles.get(status_type, "")
    
    @classmethod
    def get_messagebox_stylesheet(cls, msg_type: str) -> str:
        """Get message box styling"""
        if msg_type == "success":
            bg_color = cls.COLORS['success']
            hover_color = cls.COLORS['success_light']
        elif msg_type == "error":
            bg_color = cls.COLORS['error']
            hover_color = cls.COLORS['error_light']
        else:
            bg_color = cls.COLORS['warning']
            hover_color = "#ffcd3c"
        
        return f"""
            QMessageBox {{
                background-color: {cls.COLORS['secondary']};
                color: {cls.COLORS['text_primary']};
            }}
            QMessageBox QPushButton {{
                background-color: {bg_color};
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {hover_color};
            }}
        """
