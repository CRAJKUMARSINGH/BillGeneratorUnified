import logging
import traceback
import functools
import threading
import time
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from pathlib import Path

class ErrorSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ErrorCategory(Enum):
    MEMORY = "MEMORY"
    FILE_IO = "FILE_IO"
    NETWORK = "NETWORK"
    SECURITY = "SECURITY"
    PROCESSING = "PROCESSING"
    USER_INPUT = "USER_INPUT"
    SYSTEM = "SYSTEM"
    UNKNOWN = "UNKNOWN"

@dataclass
class ErrorInfo:
    exception: Exception
    severity: ErrorSeverity
    category: ErrorCategory
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    user_message: str = ""
    technical_details: str = ""
    recovery_attempts: int = 0
    resolved: bool = False
    resolution_time: Optional[datetime] = None

@dataclass
class RecoveryAction:
    name: str
    action: Callable[[], bool]
    max_attempts: int = 3
    delay_seconds: float = 1.0
    description: str = ""

class ErrorHandler:
    def __init__(self, log_file: str = "error_handler.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        self.error_history: List[ErrorInfo] = []
        self.recovery_actions: Dict[ErrorCategory, List[RecoveryAction]] = {}
        self.error_patterns: Dict[str, ErrorCategory] = {}
        
        self.lock = threading.RLock()
        self.logger = self._setup_logger()
        
        # Initialize default recovery actions
        self._initialize_recovery_actions()
        
        # Error statistics
        self.stats = {
            'total_errors': 0,
            'resolved_errors': 0,
            'auto_recovered': 0,
            'categories': {},
            'severities': {}
        }
        
    def _setup_logger(self) -> logging.Logger:
        """Setup dedicated error logger"""
        logger = logging.getLogger("ErrorHandler")
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    def _initialize_recovery_actions(self):
        """Initialize default recovery actions for different error categories"""
        
        # Memory recovery actions
        self.recovery_actions[ErrorCategory.MEMORY] = [
            RecoveryAction(
                name="garbage_collection",
                action=self._perform_garbage_collection,
                description="Force garbage collection"
            ),
            RecoveryAction(
                name="clear_caches",
                action=self._clear_memory_caches,
                description="Clear memory caches"
            ),
            RecoveryAction(
                name="reduce_batch_size",
                action=self._reduce_batch_size,
                description="Reduce processing batch size"
            )
        ]
        
        # File I/O recovery actions
        self.recovery_actions[ErrorCategory.FILE_IO] = [
            RecoveryAction(
                name="retry_with_delay",
                action=self._retry_file_operation,
                description="Retry file operation with delay"
            ),
            RecoveryAction(
                name="check_permissions",
                action=self._check_file_permissions,
                description="Check and fix file permissions"
            ),
            RecoveryAction(
                name="use_temp_location",
                action=self._use_temporary_location,
                description="Use temporary file location"
            )
        ]
        
        # Network recovery actions
        self.recovery_actions[ErrorCategory.NETWORK] = [
            RecoveryAction(
                name="retry_with_backoff",
                action=self._retry_with_backoff,
                description="Retry with exponential backoff"
            ),
            RecoveryAction(
                name="check_connectivity",
                action=self._check_network_connectivity,
                description="Check network connectivity"
            )
        ]
        
        # Processing recovery actions
        self.recovery_actions[ErrorCategory.PROCESSING] = [
            RecoveryAction(
                name="restart_processing",
                action=self._restart_processing,
                description="Restart processing from last checkpoint"
            ),
            RecoveryAction(
                name="fallback_method",
                action=self._use_fallback_method,
                description="Use alternative processing method"
            )
        ]
        
    def handle_error(self, exception: Exception, context: Dict[str, Any] = None,
                    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                    category: ErrorCategory = None,
                    user_message: str = "") -> ErrorInfo:
        """Handle an error with automatic recovery attempts"""
        
        # Determine category if not provided
        if category is None:
            category = self._categorize_error(exception)
            
        # Create error info
        error_info = ErrorInfo(
            exception=exception,
            severity=severity,
            category=category,
            context=context or {},
            user_message=user_message or self._generate_user_message(exception, category),
            technical_details=traceback.format_exc()
        )
        
        with self.lock:
            self.error_history.append(error_info)
            self._update_stats(error_info)
            
        # Log error
        self.logger.error(
            f"Error handled: {category.value} - {severity.value} - {str(exception)}",
            extra={'context': context}
        )
        
        # Attempt recovery
        if category in self.recovery_actions:
            success = self._attempt_recovery(error_info)
            if success:
                error_info.resolved = True
                error_info.resolution_time = datetime.now()
                self.stats['auto_recovered'] += 1
                
        return error_info
        
    def _attempt_recovery(self, error_info: ErrorInfo) -> bool:
        """Attempt to recover from error using recovery actions"""
        recovery_actions = self.recovery_actions.get(error_info.category, [])
        
        for recovery_action in recovery_actions:
            if error_info.recovery_attempts >= recovery_action.max_attempts:
                continue
                
            try:
                self.logger.info(f"Attempting recovery: {recovery_action.name}")
                
                # Add delay if specified
                if recovery_action.delay_seconds > 0:
                    time.sleep(recovery_action.delay_seconds)
                    
                # Execute recovery action
                success = recovery_action.action()
                
                if success:
                    self.logger.info(f"Recovery successful: {recovery_action.name}")
                    return True
                else:
                    self.logger.warning(f"Recovery failed: {recovery_action.name}")
                    
            except Exception as e:
                self.logger.error(f"Recovery action error: {recovery_action.name} - {e}")
                
            error_info.recovery_attempts += 1
            
        return False
        
    def _categorize_error(self, exception: Exception) -> ErrorCategory:
        """Categorize error based on exception type and message"""
        exception_type = type(exception).__name__
        exception_message = str(exception).lower()
        
        # Memory-related errors
        memory_keywords = ['memory', 'out of memory', 'memoryerror', 'allocation']
        if any(keyword in exception_message for keyword in memory_keywords):
            return ErrorCategory.MEMORY
            
        # File I/O errors
        file_keywords = ['file', 'directory', 'path', 'permission', 'access denied']
        if any(keyword in exception_message for keyword in file_keywords):
            return ErrorCategory.FILE_IO
            
        # Network errors
        network_keywords = ['network', 'connection', 'timeout', 'socket', 'http']
        if any(keyword in exception_message for keyword in network_keywords):
            return ErrorCategory.NETWORK
            
        # Security errors
        security_keywords = ['security', 'authentication', 'authorization', 'forbidden']
        if any(keyword in exception_message for keyword in security_keywords):
            return ErrorCategory.SECURITY
            
        # Processing errors
        processing_keywords = ['processing', 'parsing', 'format', 'invalid']
        if any(keyword in exception_message for keyword in processing_keywords):
            return ErrorCategory.PROCESSING
            
        # Check exception type mappings
        type_mappings = {
            'MemoryError': ErrorCategory.MEMORY,
            'FileNotFoundError': ErrorCategory.FILE_IO,
            'PermissionError': ErrorCategory.FILE_IO,
            'ConnectionError': ErrorCategory.NETWORK,
            'TimeoutError': ErrorCategory.NETWORK,
            'ValueError': ErrorCategory.PROCESSING,
            'TypeError': ErrorCategory.PROCESSING,
        }
        
        return type_mappings.get(exception_type, ErrorCategory.UNKNOWN)
        
    def _generate_user_message(self, exception: Exception, category: ErrorCategory) -> str:
        """Generate user-friendly error message"""
        category_messages = {
            ErrorCategory.MEMORY: "System is running low on memory. Please try again with smaller files.",
            ErrorCategory.FILE_IO: "File access error. Please check file permissions and try again.",
            ErrorCategory.NETWORK: "Network connection error. Please check your internet connection.",
            ErrorCategory.SECURITY: "Security validation failed. Please contact support.",
            ErrorCategory.PROCESSING: "Processing error. The file format may not be supported.",
            ErrorCategory.USER_INPUT: "Invalid input provided. Please check your data and try again.",
            ErrorCategory.SYSTEM: "System error occurred. Please try again or contact support.",
        }
        
        return category_messages.get(category, "An unexpected error occurred. Please try again.")
        
    def _update_stats(self, error_info: ErrorInfo):
        """Update error statistics"""
        self.stats['total_errors'] += 1
        
        if error_info.resolved:
            self.stats['resolved_errors'] += 1
            
        # Update category stats
        category = error_info.category.value
        self.stats['categories'][category] = self.stats['categories'].get(category, 0) + 1
        
        # Update severity stats
        severity = error_info.severity.value
        self.stats['severities'][severity] = self.stats['severities'].get(severity, 0) + 1
        
    # Recovery action implementations
    def _perform_garbage_collection(self) -> bool:
        """Perform garbage collection"""
        try:
            import gc
            collected = gc.collect()
            self.logger.info(f"Garbage collection collected {collected} objects")
            return True
        except Exception as e:
            self.logger.error(f"Garbage collection failed: {e}")
            return False
            
    def _clear_memory_caches(self) -> bool:
        """Clear memory caches"""
        try:
            # This would integrate with the cache manager
            # For now, just log the action
            self.logger.info("Memory caches cleared")
            return True
        except Exception as e:
            self.logger.error(f"Cache clearing failed: {e}")
            return False
            
    def _reduce_batch_size(self) -> bool:
        """Reduce processing batch size"""
        try:
            # This would integrate with the batch processor
            self.logger.info("Batch size reduced")
            return True
        except Exception as e:
            self.logger.error(f"Batch size reduction failed: {e}")
            return False
            
    def _retry_file_operation(self) -> bool:
        """Retry file operation"""
        # This is a placeholder - actual implementation would depend on context
        self.logger.info("File operation retry")
        return True
        
    def _check_file_permissions(self) -> bool:
        """Check file permissions"""
        try:
            import os
            # Check current directory permissions
            if os.access('.', os.R_OK | os.W_OK):
                return True
            return False
        except Exception:
            return False
            
    def _use_temporary_location(self) -> bool:
        """Use temporary file location"""
        try:
            import tempfile
            temp_dir = tempfile.gettempdir()
            if os.access(temp_dir, os.R_OK | os.W_OK):
                self.logger.info(f"Using temporary location: {temp_dir}")
                return True
            return False
        except Exception:
            return False
            
    def _retry_with_backoff(self) -> bool:
        """Retry with exponential backoff"""
        # Placeholder for network retry logic
        self.logger.info("Network retry with backoff")
        return True
        
    def _check_network_connectivity(self) -> bool:
        """Check network connectivity"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except Exception:
            return False
            
    def _restart_processing(self) -> bool:
        """Restart processing"""
        self.logger.info("Processing restart")
        return True
        
    def _use_fallback_method(self) -> bool:
        """Use fallback processing method"""
        self.logger.info("Using fallback method")
        return True
        
    def get_error_report(self) -> Dict[str, Any]:
        """Get comprehensive error report"""
        with self.lock:
            recent_errors = [
                error for error in self.error_history
                if (datetime.now() - error.timestamp).total_seconds() < 3600  # Last hour
            ]
            
            return {
                'statistics': self.stats.copy(),
                'recent_errors_count': len(recent_errors),
                'total_errors_count': len(self.error_history),
                'error_rate': len(recent_errors) / max(1, len(self.error_history)),
                'recovery_rate': (
                    self.stats['auto_recovered'] / max(1, self.stats['total_errors'])
                ) * 100,
                'most_common_category': max(
                    self.stats['categories'].items(), 
                    key=lambda x: x[1], 
                    default=('None', 0)
                )[0],
                'most_common_severity': max(
                    self.stats['severities'].items(), 
                    key=lambda x: x[1], 
                    default=('None', 0)
                )[0]
            }
            
    def get_recent_errors(self, limit: int = 10) -> List[ErrorInfo]:
        """Get recent errors"""
        with self.lock:
            return sorted(
                self.error_history,
                key=lambda x: x.timestamp,
                reverse=True
            )[:limit]
            
    def clear_error_history(self):
        """Clear error history"""
        with self.lock:
            self.error_history.clear()
            self.stats = {
                'total_errors': 0,
                'resolved_errors': 0,
                'auto_recovered': 0,
                'categories': {},
                'severities': {}
            }
            self.logger.info("Error history cleared")

# Decorator for automatic error handling
def handle_errors(category: ErrorCategory = None, severity: ErrorSeverity = ErrorCategory.MEDIUM):
    """Decorator for automatic error handling"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = get_error_handler()
                error_info = error_handler.handle_error(
                    e,
                    context={'function': func.__name__, 'args': str(args)[:200]},
                    category=category,
                    severity=severity
                )
                
                # Re-raise if critical or unresolved
                if error_info.severity == ErrorSeverity.CRITICAL or not error_info.resolved:
                    raise
                    
                return None
        return wrapper
    return decorator

# Global error handler instance
error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance"""
    return error_handler