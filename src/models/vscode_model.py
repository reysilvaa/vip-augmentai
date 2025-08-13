"""
VS Code Model - Handles VS Code installation and configuration data
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any
from pathlib import Path
import platform
import shutil

@dataclass
class VSCodePaths:
    """Data class for VS Code file paths"""
    state_db: Path
    storage_json: Path
    user_data: Path
    
    @property
    def is_valid(self) -> bool:
        """Check if both required files exist"""
        return self.state_db.exists() and self.storage_json.exists()
    
    @property
    def has_database(self) -> bool:
        """Check if state database exists"""
        return self.state_db.exists()
    
    @property
    def has_storage(self) -> bool:
        """Check if storage.json exists"""
        return self.storage_json.exists()


class VSCodeModel:
    """Model for managing VS Code installation and configuration"""
    
    def __init__(self):
        self._paths: Optional[VSCodePaths] = None
        self._is_installed = False
        self._version_info: Dict[str, Any] = {}
    
    @property
    def paths(self) -> Optional[VSCodePaths]:
        """Get VS Code file paths"""
        if self._paths is None:
            self._paths = self._detect_vscode_paths()
        return self._paths
    
    @property
    def is_installed(self) -> bool:
        """Check if VS Code is properly installed"""
        return self.paths is not None and self.paths.is_valid
    
    @property
    def installation_status(self) -> Dict[str, bool]:
        """Get detailed installation status"""
        if self.paths is None:
            return {"database": False, "storage": False, "complete": False}
        
        return {
            "database": self.paths.has_database,
            "storage": self.paths.has_storage,
            "complete": self.paths.is_valid
        }
    
    def _detect_vscode_paths(self) -> Optional[VSCodePaths]:
        """Detect VS Code installation paths based on OS"""
        system = platform.system().lower()
        
        if system == "windows":
            user_data = Path.home() / "AppData" / "Roaming" / "Code" / "User"
        elif system == "darwin":  # macOS
            user_data = Path.home() / "Library" / "Application Support" / "Code" / "User"
        else:  # Linux
            user_data = Path.home() / ".config" / "Code" / "User"
        
        state_db = user_data / "globalStorage" / "state.vscdb"
        storage_json = user_data / "globalStorage" / "storage.json"
        
        return VSCodePaths(
            state_db=state_db,
            storage_json=storage_json,
            user_data=user_data
        )
    
    def refresh_status(self) -> None:
        """Refresh the VS Code installation status"""
        self._paths = None
        self._is_installed = False
        # This will trigger re-detection on next access
    
    def get_status_message(self) -> str:
        """Get human-readable status message"""
        if not self.paths:
            return "VS Code not detected on this system"
        
        status = self.installation_status
        if status["complete"]:
            return "VS Code installation complete and ready"
        elif status["database"] and not status["storage"]:
            return "VS Code found but storage.json missing"
        elif status["storage"] and not status["database"]:
            return "VS Code found but database missing"
        else:
            return "VS Code installation incomplete"
    
    def get_detailed_info(self) -> Dict[str, Any]:
        """Get detailed VS Code installation information"""
        if not self.paths:
            return {"status": "not_found", "paths": None}
        
        return {
            "status": "found",
            "paths": {
                "state_db": str(self.paths.state_db),
                "storage_json": str(self.paths.storage_json),
                "user_data": str(self.paths.user_data)
            },
            "exists": {
                "state_db": self.paths.state_db.exists(),
                "storage_json": self.paths.storage_json.exists(),
                "user_data": self.paths.user_data.exists()
            },
            "installation_status": self.installation_status
        }
    
    def get_executable_path(self) -> Optional[Path]:
        """Get VS Code executable path based on OS"""
        system = platform.system()
        
        if system == "Windows":
            # Common VS Code installation paths on Windows
            possible_paths = [
                Path.home() / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "Code.exe",
                Path(r"C:\Program Files\Microsoft VS Code\Code.exe"),
                Path(r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"),
            ]
            
            # Check system PATH
            code_exe = shutil.which("code")
            if code_exe:
                possible_paths.insert(0, Path(code_exe))
                
        elif system == "Darwin":  # macOS
            possible_paths = [
                Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"),
                Path("/usr/local/bin/code"),
            ]
        else:  # Linux
            possible_paths = [
                Path("/usr/bin/code"),
                Path("/usr/local/bin/code"),
                Path(f"{Path.home()}/.local/bin/code"),
                Path("/snap/bin/code"),
            ]
        
        # Find first existing executable
        for path in possible_paths:
            if path.exists():
                return path
                
        return None
