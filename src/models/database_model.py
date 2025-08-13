"""
Database Model - Handles database operations and state
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from pathlib import Path
import sqlite3
import tempfile
import shutil

@dataclass
class DatabaseEntry:
    """Represents a database entry"""
    key: str
    value: str
    
@dataclass 
class DatabaseOperationResult:
    """Result of a database operation"""
    success: bool
    message: str
    entries_affected: int = 0
    backup_path: Optional[Path] = None
    error: Optional[str] = None


class DatabaseModel:
    """Model for managing VS Code database operations"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
        self._backup_path: Optional[Path] = None
    
    @property
    def exists(self) -> bool:
        """Check if database file exists"""
        return self.db_path.exists()
    
    @property
    def is_connected(self) -> bool:
        """Check if database connection is active"""
        return self._connection is not None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            if not self.exists:
                return False
            
            self._connection = sqlite3.connect(str(self.db_path))
            return True
        except Exception:
            self._connection = None
            return False
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def create_backup(self) -> Optional[Path]:
        """Create a backup of the database"""
        try:
            if not self.exists:
                return None
            
            backup_path = self.db_path.with_suffix(f"{self.db_path.suffix}.backup")
            shutil.copy2(self.db_path, backup_path)
            self._backup_path = backup_path
            return backup_path
        except Exception:
            return None
    
    def get_augment_entries(self) -> List[DatabaseEntry]:
        """Get all entries containing 'augment'"""
        if not self.connect():
            return []
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT key, value FROM ItemTable WHERE key LIKE '%augment%'")
            rows = cursor.fetchall()
            return [DatabaseEntry(key=row[0], value=row[1]) for row in rows]
        except Exception:
            return []
        finally:
            self.disconnect()
    
    def count_augment_entries(self) -> int:
        """Count entries containing 'augment'"""
        if not self.connect():
            return 0
        
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%augment%'")
            count = cursor.fetchone()[0]
            return count
        except Exception:
            return 0
        finally:
            self.disconnect()
    
    def remove_augment_entries(self) -> DatabaseOperationResult:
        """Remove all entries containing 'augment'"""
        # Create backup first
        backup_path = self.create_backup()
        if not backup_path:
            return DatabaseOperationResult(
                success=False,
                message="Failed to create database backup",
                error="Backup creation failed"
            )
        
        if not self.connect():
            return DatabaseOperationResult(
                success=False,
                message="Failed to connect to database",
                error="Database connection failed"
            )
        
        try:
            cursor = self._connection.cursor()
            
            # Count entries before deletion
            cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%augment%'")
            count_before = cursor.fetchone()[0]
            
            if count_before == 0:
                return DatabaseOperationResult(
                    success=True,
                    message="No Augment-related entries found",
                    entries_affected=0,
                    backup_path=backup_path
                )
            
            # Delete entries
            cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%augment%'")
            entries_affected = cursor.rowcount
            
            # Commit changes
            self._connection.commit()
            
            return DatabaseOperationResult(
                success=True,
                message=f"Successfully removed {entries_affected} Augment-related entries",
                entries_affected=entries_affected,
                backup_path=backup_path
            )
            
        except Exception as e:
            return DatabaseOperationResult(
                success=False,
                message="Failed to remove Augment entries",
                error=str(e)
            )
        finally:
            self.disconnect()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get general database information"""
        if not self.exists:
            return {"exists": False}
        
        if not self.connect():
            return {"exists": True, "accessible": False}
        
        try:
            cursor = self._connection.cursor()
            
            # Get total entries
            cursor.execute("SELECT COUNT(*) FROM ItemTable")
            total_entries = cursor.fetchone()[0]
            
            # Get augment entries
            cursor.execute("SELECT COUNT(*) FROM ItemTable WHERE key LIKE '%augment%'")
            augment_entries = cursor.fetchone()[0]
            
            # Get file size
            file_size = self.db_path.stat().st_size
            
            return {
                "exists": True,
                "accessible": True,
                "file_size": file_size,
                "total_entries": total_entries,
                "augment_entries": augment_entries,
                "path": str(self.db_path)
            }
            
        except Exception as e:
            return {
                "exists": True,
                "accessible": False,
                "error": str(e)
            }
        finally:
            self.disconnect()
