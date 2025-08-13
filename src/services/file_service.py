"""
File Service - Handles file operations and utilities
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import tempfile
from datetime import datetime

class FileService:
    """Service for file operations"""
    
    @staticmethod
    def create_backup(file_path: Path, backup_suffix: str = "backup") -> Optional[Path]:
        """Create a backup of the specified file"""
        try:
            if not file_path.exists():
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = file_path.with_suffix(f"{file_path.suffix}.{backup_suffix}_{timestamp}")
            
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None
    
    @staticmethod
    def ensure_directory(directory_path: Path) -> bool:
        """Ensure directory exists, create if not"""
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_copy(source: Path, destination: Path) -> bool:
        """Safely copy file with error handling"""
        try:
            if not source.exists():
                return False
            
            # Ensure destination directory exists
            FileService.ensure_directory(destination.parent)
            
            shutil.copy2(source, destination)
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_move(source: Path, destination: Path) -> bool:
        """Safely move file with error handling"""
        try:
            if not source.exists():
                return False
            
            # Ensure destination directory exists
            FileService.ensure_directory(destination.parent)
            
            shutil.move(str(source), str(destination))
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_delete(file_path: Path) -> bool:
        """Safely delete file"""
        try:
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_info(file_path: Path) -> Dict[str, Any]:
        """Get detailed file information"""
        try:
            if not file_path.exists():
                return {"exists": False}
            
            stat = file_path.stat()
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "created": datetime.fromtimestamp(stat.st_ctime),
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "permissions": oct(stat.st_mode)[-3:],
                "path": str(file_path),
                "name": file_path.name,
                "suffix": file_path.suffix
            }
        except Exception:
            return {"exists": False, "error": "Access denied or file error"}
    
    @staticmethod
    def list_directory(directory_path: Path, pattern: str = "*") -> List[Path]:
        """List files in directory matching pattern"""
        try:
            if not directory_path.exists() or not directory_path.is_dir():
                return []
            
            return list(directory_path.glob(pattern))
        except Exception:
            return []
    
    @staticmethod
    def create_temp_directory() -> Optional[Path]:
        """Create a temporary directory"""
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix="augment_vip_"))
            return temp_dir
        except Exception:
            return None
    
    @staticmethod
    def cleanup_temp_directory(temp_dir: Path) -> bool:
        """Clean up temporary directory"""
        try:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return True
        except Exception:
            return False
    
    @staticmethod
    def calculate_directory_size(directory_path: Path) -> int:
        """Calculate total size of directory"""
        try:
            total_size = 0
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            return total_size
        except Exception:
            return 0
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
