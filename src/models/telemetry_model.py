"""
Telemetry Model - Handles VS Code telemetry data operations
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any
from pathlib import Path
import json
import uuid
import secrets
import shutil

@dataclass
class TelemetryData:
    """Telemetry data structure"""
    machine_id: str
    device_id: str
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "telemetry.machineId": self.machine_id,
            "telemetry.devDeviceId": self.device_id
        }

@dataclass
class TelemetryOperationResult:
    """Result of a telemetry operation"""
    success: bool
    message: str
    old_data: Optional[TelemetryData] = None
    new_data: Optional[TelemetryData] = None
    backup_path: Optional[Path] = None
    error: Optional[str] = None


class TelemetryModel:
    """Model for managing VS Code telemetry operations"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._current_data: Optional[TelemetryData] = None
        self._backup_path: Optional[Path] = None
    
    @property
    def exists(self) -> bool:
        """Check if storage.json file exists"""
        return self.storage_path.exists()
    
    def load_current_data(self) -> Optional[TelemetryData]:
        """Load current telemetry data from storage.json"""
        if not self.exists:
            return None
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            machine_id = content.get("telemetry.machineId", "")
            device_id = content.get("telemetry.devDeviceId", "")
            
            if machine_id and device_id:
                self._current_data = TelemetryData(
                    machine_id=machine_id,
                    device_id=device_id
                )
                return self._current_data
            
            return None
            
        except Exception:
            return None
    
    def generate_new_telemetry_data(self) -> TelemetryData:
        """Generate new random telemetry data"""
        # Generate 64-character hex string for machine ID
        machine_id = secrets.token_hex(32)  # 32 bytes = 64 hex chars
        
        # Generate UUID4 for device ID
        device_id = str(uuid.uuid4())
        
        return TelemetryData(
            machine_id=machine_id,
            device_id=device_id
        )
    
    def create_backup(self) -> Optional[Path]:
        """Create a backup of storage.json"""
        try:
            if not self.exists:
                return None
            
            backup_path = self.storage_path.with_suffix(f"{self.storage_path.suffix}.backup")
            shutil.copy2(self.storage_path, backup_path)
            self._backup_path = backup_path
            return backup_path
        except Exception:
            return None
    
    def update_telemetry_ids(self, new_data: Optional[TelemetryData] = None) -> TelemetryOperationResult:
        """Update telemetry IDs in storage.json"""
        # Load current data first
        old_data = self.load_current_data()
        
        # Generate new data if not provided
        if new_data is None:
            new_data = self.generate_new_telemetry_data()
        
        # Create backup
        backup_path = self.create_backup()
        if not backup_path:
            return TelemetryOperationResult(
                success=False,
                message="Failed to create backup of storage.json",
                error="Backup creation failed"
            )
        
        # Read current storage.json content
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except Exception as e:
            return TelemetryOperationResult(
                success=False,
                message="Failed to read storage.json",
                error=str(e)
            )
        
        # Update the content
        content.update(new_data.to_dict())
        
        # Write back to file
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return TelemetryOperationResult(
                success=False,
                message="Failed to write updated storage.json",
                error=str(e)
            )
        
        return TelemetryOperationResult(
            success=True,
            message="Successfully updated telemetry IDs",
            old_data=old_data,
            new_data=new_data,
            backup_path=backup_path
        )
    
    def get_telemetry_info(self) -> Dict[str, Any]:
        """Get current telemetry information"""
        if not self.exists:
            return {"exists": False}
        
        current_data = self.load_current_data()
        
        try:
            file_size = self.storage_path.stat().st_size
            
            info = {
                "exists": True,
                "accessible": True,
                "file_size": file_size,
                "path": str(self.storage_path),
                "has_telemetry_data": current_data is not None
            }
            
            if current_data:
                info["current_machine_id"] = current_data.machine_id
                info["current_device_id"] = current_data.device_id
                info["machine_id_length"] = len(current_data.machine_id)
                info["device_id_format"] = "UUID4" if len(current_data.device_id) == 36 else "Unknown"
            
            return info
            
        except Exception as e:
            return {
                "exists": True,
                "accessible": False,
                "error": str(e)
            }
    
    def validate_telemetry_data(self, data: TelemetryData) -> bool:
        """Validate telemetry data format"""
        try:
            # Machine ID should be 64-char hex string
            if len(data.machine_id) != 64:
                return False
            
            # Try to parse as hex
            int(data.machine_id, 16)
            
            # Device ID should be valid UUID4
            uuid.UUID(data.device_id, version=4)
            
            return True
        except (ValueError, TypeError):
            return False
