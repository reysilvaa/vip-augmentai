"""
VS Code Service - High-level VS Code operations
"""

import subprocess
import platform
import time
import psutil
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..models.vscode_model import VSCodeModel
from ..models.database_model import DatabaseModel, DatabaseOperationResult
from ..models.telemetry_model import TelemetryModel, TelemetryOperationResult
from .file_service import FileService


class VSCodeService:
    """Service for high-level VS Code operations"""
    
    def __init__(self):
        self.vscode_model = VSCodeModel()
        self._database_model: Optional[DatabaseModel] = None
        self._telemetry_model: Optional[TelemetryModel] = None
    
    @property
    def database_model(self) -> Optional[DatabaseModel]:
        """Get database model instance"""
        if self._database_model is None and self.vscode_model.paths:
            self._database_model = DatabaseModel(self.vscode_model.paths.state_db)
        return self._database_model
    
    @property
    def telemetry_model(self) -> Optional[TelemetryModel]:
        """Get telemetry model instance"""
        if self._telemetry_model is None and self.vscode_model.paths:
            self._telemetry_model = TelemetryModel(self.vscode_model.paths.storage_json)
        return self._telemetry_model
    
    def get_installation_status(self) -> Dict[str, Any]:
        """Get comprehensive VS Code installation status"""
        base_status = self.vscode_model.get_detailed_info()
        
        if base_status["status"] == "not_found":
            return {
                "installed": False,
                "message": "VS Code not detected",
                "details": base_status
            }
        
        # Add service-specific information
        status = {
            "installed": True,
            "message": self.vscode_model.get_status_message(),
            "details": base_status,
            "services": {
                "database": self._get_database_status(),
                "telemetry": self._get_telemetry_status()
            }
        }
        
        return status
    
    def _get_database_status(self) -> Dict[str, Any]:
        """Get database service status"""
        if not self.database_model:
            return {"available": False, "reason": "No database model"}
        
        if not self.database_model.exists:
            return {"available": False, "reason": "Database file not found"}
        
        db_info = self.database_model.get_database_info()
        return {
            "available": True,
            "info": db_info
        }
    
    def _get_telemetry_status(self) -> Dict[str, Any]:
        """Get telemetry service status"""
        if not self.telemetry_model:
            return {"available": False, "reason": "No telemetry model"}
        
        if not self.telemetry_model.exists:
            return {"available": False, "reason": "Storage.json file not found"}
        
        tel_info = self.telemetry_model.get_telemetry_info()
        return {
            "available": True,
            "info": tel_info
        }
    
    def clean_database(self) -> DatabaseOperationResult:
        """Clean Augment entries from VS Code database"""
        if not self.database_model:
            return DatabaseOperationResult(
                success=False,
                message="Database not available",
                error="Database model not initialized"
            )
        
        if not self.database_model.exists:
            return DatabaseOperationResult(
                success=False,
                message="Database file not found",
                error="VS Code database file does not exist"
            )
        
        return self.database_model.remove_augment_entries()
    
    def modify_telemetry_ids(self) -> TelemetryOperationResult:
        """Modify VS Code telemetry IDs"""
        if not self.telemetry_model:
            return TelemetryOperationResult(
                success=False,
                message="Telemetry service not available",
                error="Telemetry model not initialized"
            )
        
        if not self.telemetry_model.exists:
            return TelemetryOperationResult(
                success=False,
                message="Storage.json file not found",
                error="VS Code storage.json file does not exist"
            )
        
        return self.telemetry_model.update_telemetry_ids()
    
    def run_all_operations(self) -> Dict[str, Any]:
        """Run both database cleaning and telemetry ID modification"""
        results = {
            "database_result": None,
            "telemetry_result": None,
            "overall_success": False
        }
        
        # Run database cleaning
        if self.database_model and self.database_model.exists:
            results["database_result"] = self.clean_database()
        
        # Run telemetry modification
        if self.telemetry_model and self.telemetry_model.exists:
            results["telemetry_result"] = self.modify_telemetry_ids()
        
        # Determine overall success
        db_success = results["database_result"] is None or results["database_result"].success
        tel_success = results["telemetry_result"] is None or results["telemetry_result"].success
        results["overall_success"] = db_success and tel_success
        
        return results
    
    def get_operation_capabilities(self) -> Dict[str, bool]:
        """Get available operations based on current VS Code installation"""
        return {
            "can_clean_database": self.database_model is not None and self.database_model.exists,
            "can_modify_telemetry": self.telemetry_model is not None and self.telemetry_model.exists,
            "can_run_all": (
                (self.database_model is not None and self.database_model.exists) or
                (self.telemetry_model is not None and self.telemetry_model.exists)
            )
        }
    
    def refresh_installation_status(self) -> None:
        """Refresh VS Code installation detection"""
        self.vscode_model.refresh_status()
        self._database_model = None
        self._telemetry_model = None
    
    def get_backup_files(self) -> List[Dict[str, Any]]:
        """Get list of backup files created"""
        backup_files = []
        
        if self.vscode_model.paths:
            base_dir = self.vscode_model.paths.user_data / "globalStorage"
            
            # Look for backup files
            for backup_file in base_dir.glob("*.backup*"):
                file_info = FileService.get_file_info(backup_file)
                if file_info["exists"]:
                    backup_files.append(file_info)
        
        return backup_files
    
    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """Clean up old backup files, keeping the most recent ones"""
        if not self.vscode_model.paths:
            return 0
        
        backup_files = self.get_backup_files()
        if len(backup_files) <= keep_count:
            return 0
        
        # Sort by modification time, newest first
        backup_files.sort(key=lambda x: x["modified"], reverse=True)
        
        # Remove old backups
        removed_count = 0
        for backup_info in backup_files[keep_count:]:
            if FileService.safe_delete(Path(backup_info["path"])):
                removed_count += 1
        
        return removed_count

    def is_vscode_running(self) -> bool:
        """Check if VS Code is currently running"""
        try:
            system = platform.system().lower()
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                proc_name = proc.info['name']
                if not proc_name:
                    continue
                
                proc_name_lower = proc_name.lower()
                
                # Cross-platform VS Code process detection
                if system == "windows":
                    # Windows: Code.exe, code.exe
                    vscode_names = ['code.exe', 'code-tunnel.exe', 'code-insiders.exe']
                elif system == "darwin":
                    # macOS: Electron, Code, Visual Studio Code
                    vscode_names = ['code', 'visual studio code', 'electron']
                    # Check executable path for VS Code app bundle
                    try:
                        exe_path = proc.info.get('exe', '')
                        if exe_path and 'visual studio code' in exe_path.lower():
                            return True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                else:
                    # Linux: code, code-insiders, code-oss
                    vscode_names = ['code', 'code-insiders', 'code-oss', 'codium', 'vscodium']
                
                # Check if process name matches any VS Code variant
                if any(name in proc_name_lower for name in vscode_names):
                    return True
                    
            return False
        except Exception:
            return False
    
    def close_vscode(self) -> bool:
        """Close all VS Code processes"""
        try:
            system = platform.system().lower()
            closed_processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                proc_name = proc.info['name']
                if not proc_name:
                    continue
                    
                proc_name_lower = proc_name.lower()
                is_vscode_process = False
                
                # Cross-platform VS Code process detection
                if system == "windows":
                    vscode_names = ['code.exe', 'code-tunnel.exe', 'code-insiders.exe']
                    is_vscode_process = any(name in proc_name_lower for name in vscode_names)
                elif system == "darwin":
                    vscode_names = ['code', 'visual studio code', 'electron']
                    is_vscode_process = any(name in proc_name_lower for name in vscode_names)
                    # Check executable path for VS Code app bundle
                    if not is_vscode_process:
                        try:
                            exe_path = proc.info.get('exe', '')
                            if exe_path and 'visual studio code' in exe_path.lower():
                                is_vscode_process = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                else:
                    vscode_names = ['code', 'code-insiders', 'code-oss', 'codium', 'vscodium']
                    is_vscode_process = any(name in proc_name_lower for name in vscode_names)
                
                if is_vscode_process:
                    try:
                        proc.terminate()
                        closed_processes.append(proc.info['pid'])
                    except psutil.NoSuchProcess:
                        pass
                    except psutil.AccessDenied:
                        try:
                            proc.kill()
                            closed_processes.append(proc.info['pid'])
                        except:
                            pass
            
            # Wait for processes to close
            if closed_processes:
                time.sleep(3 if system == "darwin" else 2)
                
            return len(closed_processes) > 0
        except Exception:
            return False
    
    def start_vscode(self, workspace_path: Optional[str] = None) -> bool:
        """Start VS Code with optional workspace"""
        try:
            system = platform.system().lower()
            
            # Get VS Code executable path
            exe_path = self.vscode_model.get_executable_path()
            if not exe_path or not exe_path.exists():
                return False
            
            # Build command
            cmd = [str(exe_path)]
            if workspace_path:
                cmd.append(workspace_path)
            
            # Start VS Code with platform-specific settings
            if system == "windows":
                subprocess.Popen(cmd, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
            elif system == "darwin":
                # macOS: Use 'open' command for .app bundles, or direct execution
                if str(exe_path).endswith('.app'):
                    cmd = ['open', str(exe_path)]
                    if workspace_path:
                        cmd.extend(['--args', workspace_path])
                subprocess.Popen(cmd, shell=False)
            else:
                # Linux: Direct execution with environment
                env = None
                # Set DISPLAY if not set (for GUI apps)
                import os
                if 'DISPLAY' not in os.environ and 'WAYLAND_DISPLAY' not in os.environ:
                    env = os.environ.copy()
                    env['DISPLAY'] = ':0'
                subprocess.Popen(cmd, shell=False, env=env)
            
            return True
        except Exception:
            return False
    
    def restart_vscode(self, workspace_path: Optional[str] = None) -> Dict[str, Any]:
        """Restart VS Code (close and reopen)"""
        result = {
            "success": False,
            "message": "",
            "was_running": False,
            "closed_successfully": False,
            "started_successfully": False
        }
        
        try:
            # Check if VS Code was running
            result["was_running"] = self.is_vscode_running()
            
            if result["was_running"]:
                # Close VS Code
                result["closed_successfully"] = self.close_vscode()
                
                if result["closed_successfully"]:
                    # Wait a bit for cleanup
                    time.sleep(3)
                    
                    # Start VS Code again
                    result["started_successfully"] = self.start_vscode(workspace_path)
                    
                    if result["started_successfully"]:
                        result["success"] = True
                        result["message"] = "VS Code restarted successfully"
                    else:
                        result["message"] = "VS Code closed but failed to restart"
                else:
                    result["message"] = "Failed to close VS Code processes"
            else:
                # VS Code wasn't running, just try to start it
                result["started_successfully"] = self.start_vscode(workspace_path)
                if result["started_successfully"]:
                    result["success"] = True
                    result["message"] = "VS Code started successfully"
                else:
                    result["message"] = "Failed to start VS Code"
            
            return result
            
        except Exception as e:
            result["message"] = f"Error during VS Code restart: {str(e)}"
            return result
