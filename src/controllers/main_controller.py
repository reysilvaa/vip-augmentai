"""
Main Controller - Coordinates application logic following MVC pattern
"""

from typing import TYPE_CHECKING, Optional
from PySide6.QtCore import QObject, QThread, Signal

from ..services.vscode_service import VSCodeService
from ..models.database_model import DatabaseOperationResult
from ..models.telemetry_model import TelemetryOperationResult

if TYPE_CHECKING:
    from ..views.main_window import MainWindow


class OperationWorker(QThread):
    """Worker thread for running operations without blocking UI"""
    
    # Signals
    progress = Signal(str, str)  # message, type
    finished = Signal(object, str)  # result, operation_type
    error = Signal(str, str)  # message, operation_type
    
    def __init__(self, vscode_service: VSCodeService, operation: str):
        super().__init__()
        self.vscode_service = vscode_service
        self.operation = operation
    
    def run(self):
        """Run the operation in background thread"""
        try:
            if self.operation == "clean":
                self.progress.emit("Starting database cleanup process...", "info")
                result = self.vscode_service.clean_database()
                self.finished.emit(result, "clean")
                
            elif self.operation == "modify_ids":
                self.progress.emit("Starting telemetry ID modification...", "info")
                result = self.vscode_service.modify_telemetry_ids()
                self.finished.emit(result, "modify_ids")
                
            elif self.operation == "run_all":
                self.progress.emit("Starting all operations...", "info")
                result = self.vscode_service.run_all_operations()
                self.finished.emit(result, "run_all")
            
            elif self.operation == "restart_vscode":
                self.progress.emit("Restarting VS Code...", "info")
                result = self.vscode_service.restart_vscode()
                self.finished.emit(result, "restart_vscode")
                
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}", self.operation)


class MainController(QObject):
    """Main application controller following MVC pattern"""
    
    def __init__(self, view: "MainWindow"):
        super().__init__()
        self.view = view
        self.vscode_service = VSCodeService()
        self.current_worker: Optional[OperationWorker] = None
    
    def initialize(self):
        """Initialize the controller and update view"""
        self.refresh_vscode_status()
    
    def refresh_vscode_status(self):
        """Refresh VS Code installation status and update view"""
        self.vscode_service.refresh_installation_status()
        status_info = self.vscode_service.get_installation_status()
        
        if not status_info["installed"]:
            self.view.update_status("🔴 VS Code Not Found", "error")
            self.view.set_buttons_enabled(False)
            self.view.add_log_message("VS Code installation not detected", "error")
            return
        
        # Update status based on available capabilities
        capabilities = self.vscode_service.get_operation_capabilities()
        
        if capabilities["can_clean_database"] and capabilities["can_modify_telemetry"]:
            self.view.update_status("🟢 VS Code Ready - All features available", "success")
        elif capabilities["can_clean_database"] or capabilities["can_modify_telemetry"]:
            self.view.update_status("🟡 VS Code Partial - Some features available", "warning")
        else:
            self.view.update_status("🔴 VS Code Found - No features available", "error")
        
        # Update button states
        self.view.set_specific_button_enabled("clean", capabilities["can_clean_database"])
        self.view.set_specific_button_enabled("modify", capabilities["can_modify_telemetry"])
        self.view.set_specific_button_enabled("run_all", capabilities["can_run_all"])
        
        # Log detailed status
        self._log_detailed_status(status_info, capabilities)
    
    def _log_detailed_status(self, status_info: dict, capabilities: dict):
        """Log detailed VS Code status information"""
        self.view.add_log_message("VS Code installation detected", "success")
        
        if "services" in status_info["details"]:
            services = status_info["details"]["services"]
            
            # Database status
            if services["database"]["available"]:
                db_info = services["database"]["info"]
                if "augment_entries" in db_info:
                    entry_count = db_info["augment_entries"]
                    if entry_count > 0:
                        self.view.add_log_message(f"Found {entry_count} Augment entries in database", "info")
                    else:
                        self.view.add_log_message("Database clean - no Augment entries found", "info")
            else:
                self.view.add_log_message("Database not accessible", "warning")
            
            # Telemetry status
            if services["telemetry"]["available"]:
                tel_info = services["telemetry"]["info"]
                if tel_info.get("has_telemetry_data"):
                    self.view.add_log_message("Current telemetry IDs detected", "info")
                else:
                    self.view.add_log_message("No telemetry data found", "warning")
            else:
                self.view.add_log_message("Storage.json not accessible", "warning")
    
    def clean_database(self):
        """Clean VS Code database"""
        if self._is_operation_running():
            self.view.show_message_box("⚠️ Operation in Progress", 
                                     "Another operation is currently running. Please wait.", "warning")
            return
        
        capabilities = self.vscode_service.get_operation_capabilities()
        if not capabilities["can_clean_database"]:
            self.view.show_message_box("❌ Operation Not Available", 
                                     "Database cleaning is not available. Please check VS Code installation.", "error")
            return
        
        self._start_operation("clean")
    
    def modify_telemetry_ids(self):
        """Modify VS Code telemetry IDs"""
        if self._is_operation_running():
            self.view.show_message_box("⚠️ Operation in Progress", 
                                     "Another operation is currently running. Please wait.", "warning")
            return
        
        capabilities = self.vscode_service.get_operation_capabilities()
        if not capabilities["can_modify_telemetry"]:
            self.view.show_message_box("❌ Operation Not Available", 
                                     "Telemetry ID modification is not available. Please check VS Code installation.", "error")
            return
        
        self._start_operation("modify_ids")
    
    def run_all_operations(self):
        """Run all available operations"""
        if self._is_operation_running():
            self.view.show_message_box("⚠️ Operation in Progress", 
                                     "Another operation is currently running. Please wait.", "warning")
            return
        
        capabilities = self.vscode_service.get_operation_capabilities()
        if not capabilities["can_run_all"]:
            self.view.show_message_box("❌ No Operations Available", 
                                     "No operations are available. Please check VS Code installation.", "error")
            return
        
        self._start_operation("run_all")
    
    def restart_vscode(self):
        """Restart VS Code"""
        if self._is_operation_running():
            self.view.show_message_box("⚠️ Operation in Progress", 
                                     "Another operation is currently running. Please wait.", "warning")
            return
        
        self._start_operation("restart_vscode")
    
    def _start_operation(self, operation: str):
        """Start an operation in background thread"""
        # Log operation start
        op_names = {
            "clean": "Database Cleaning",
            "modify_ids": "Telemetry ID Modification", 
            "run_all": "All Operations",
            "restart_vscode": "VS Code Restart"
        }
        
        self.view.add_log_message(f"🚀 Starting {op_names.get(operation, operation)}...", "info")
        
        # Disable UI
        self.view.set_buttons_enabled(False)
        self.view.show_progress(True)
        
        # Create and start worker thread
        self.current_worker = OperationWorker(self.vscode_service, operation)
        self.current_worker.progress.connect(self.view.add_log_message)
        self.current_worker.finished.connect(self._on_operation_finished)
        self.current_worker.error.connect(self._on_operation_error)
        self.current_worker.start()
    
    def _on_operation_finished(self, result, operation_type: str):
        """Handle operation completion"""
        self._cleanup_worker()
        self.view.show_progress(False)
        
        if operation_type == "clean":
            self._handle_database_result(result)
        elif operation_type == "modify_ids":
            self._handle_telemetry_result(result)
        elif operation_type == "run_all":
            self._handle_all_operations_result(result)
        elif operation_type == "restart_vscode":
            self._handle_restart_result(result)
        
        # Re-enable UI and refresh status
        self.view.set_buttons_enabled(True)
        self.refresh_vscode_status()
    
    def _on_operation_error(self, error_message: str, operation_type: str):
        """Handle operation error"""
        self._cleanup_worker()
        self.view.show_progress(False)
        self.view.set_buttons_enabled(True)
        
        self.view.add_log_message(f"❌ {operation_type} failed: {error_message}", "error")
        self.view.show_message_box("❌ Operation Failed", error_message, "error")
    
    def _handle_database_result(self, result: DatabaseOperationResult):
        """Handle database operation result"""
        if result.success:
            self.view.add_log_message(result.message, "success")
            if result.entries_affected > 0:
                self.view.add_log_message(f"✨ {result.entries_affected} entries removed", "success")
            if result.backup_path:
                self.view.add_log_message(f"💾 Backup created: {result.backup_path.name}", "info")
            self.view.show_message_box("✅ Database Cleaned", result.message, "success")
        else:
            self.view.add_log_message(f"Database cleaning failed: {result.message}", "error")
            if result.error:
                self.view.add_log_message(f"Error details: {result.error}", "error")
            self.view.show_message_box("❌ Database Cleaning Failed", result.message, "error")
    
    def _handle_telemetry_result(self, result: TelemetryOperationResult):
        """Handle telemetry operation result"""
        if result.success:
            self.view.add_log_message(result.message, "success")
            if result.new_data:
                self.view.add_log_message(f"🆔 New Machine ID: {result.new_data.machine_id[:16]}...", "info")
                self.view.add_log_message(f"📱 New Device ID: {result.new_data.device_id}", "info")
            if result.backup_path:
                self.view.add_log_message(f"💾 Backup created: {result.backup_path.name}", "info")
            
            # Ask if user wants to restart VS Code
            if self._should_restart_vscode():
                self._ask_restart_vscode()
            else:
                self.view.add_log_message("⚠️ Restart VS Code for changes to take effect", "warning")
                self.view.show_message_box("✅ Telemetry IDs Updated", result.message + "\\n\\nRestart VS Code for changes to take effect.", "success")
        else:
            self.view.add_log_message(f"Telemetry ID modification failed: {result.message}", "error")
            if result.error:
                self.view.add_log_message(f"Error details: {result.error}", "error")
            self.view.show_message_box("❌ Telemetry Modification Failed", result.message, "error")
    
    def _handle_all_operations_result(self, result: dict):
        """Handle all operations result"""
        db_result = result.get("database_result")
        tel_result = result.get("telemetry_result")
        overall_success = result.get("overall_success", False)
        
        # Handle individual results
        if db_result:
            self._handle_database_result(db_result)
        
        if tel_result:
            self._handle_telemetry_result(tel_result)
        
        # Overall summary
        if overall_success:
            self.view.add_log_message("🎉 All operations completed successfully!", "success")
            self.view.show_message_box("✅ All Operations Complete", 
                                     "All available operations completed successfully!\\n\\nRestart VS Code for changes to take effect.", 
                                     "success")
        else:
            self.view.add_log_message("⚠️ Some operations failed or were skipped", "warning")
            self.view.show_message_box("⚠️ Operations Completed with Issues", 
                                     "Some operations failed or were not available. Check the log for details.", 
                                     "warning")
    
    def _is_operation_running(self) -> bool:
        """Check if an operation is currently running"""
        return self.current_worker is not None and self.current_worker.isRunning()
    
    def _cleanup_worker(self):
        """Clean up worker thread"""
        if self.current_worker:
            if self.current_worker.isRunning():
                self.current_worker.quit()
                self.current_worker.wait()
            self.current_worker = None
    
    def cleanup(self):
        """Cleanup controller resources"""
        self._cleanup_worker()
        
        # Log cleanup
        backup_count = len(self.vscode_service.get_backup_files())
        if backup_count > 0:
            self.view.add_log_message(f"💾 {backup_count} backup files available", "info")
    
    def _should_restart_vscode(self) -> bool:
        """Check if VS Code should be restarted (if it's currently running)"""
        return self.vscode_service.is_vscode_running()
    
    def _ask_restart_vscode(self):
        """Ask user if they want to restart VS Code"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox()
        msg.setWindowTitle("Restart VS Code")
        msg.setText("VS Code is currently running.\\n\\nRestart VS Code now to apply the changes?")
        msg.setInformativeText("This will close all VS Code windows and reopen VS Code.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setIcon(QMessageBox.Question)
        
        if msg.exec() == QMessageBox.Yes:
            self._start_operation("restart_vscode")
        else:
            self.view.add_log_message("⚠️ Please restart VS Code manually for changes to take effect", "warning")
    
    def _handle_restart_result(self, result: dict):
        """Handle VS Code restart result"""
        if result["success"]:
            self.view.add_log_message("✅ VS Code restarted successfully", "success")
            self.view.show_message_box("✅ VS Code Restarted", "VS Code has been restarted successfully!", "success")
        else:
            self.view.add_log_message(f"❌ Failed to restart VS Code: {result['message']}", "error")
            
            # Provide more detailed feedback
            if result["was_running"] and not result["closed_successfully"]:
                self.view.add_log_message("💡 Try closing VS Code manually and restart it", "info")
            elif not result["started_successfully"]:
                self.view.add_log_message("💡 Try starting VS Code manually", "info")
                
            self.view.show_message_box("❌ Restart Failed", 
                                     f"Could not restart VS Code automatically.\\n\\n{result['message']}\\n\\nPlease restart VS Code manually.", 
                                     "error")
        
        self.view.add_log_message("👋 Application closing...", "info")
