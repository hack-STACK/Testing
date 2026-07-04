"""
Logger - Centralized logging for test execution framework.

Provides structured logging for test execution, framework events, and errors.
Logs are written to both file and console with appropriate formatting.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ExecutionLogger:
    """
    Centralized logger for test execution framework.
    
    Provides structured logging to both file and console, with different
    levels for different output streams.
    """
    
    def __init__(self, log_dir: Path = Path("logs")):
        """Initialize logger."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("QA_Automation")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # File handler (all levels)
        log_file = self.log_dir / f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler (info and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        self.log_file = log_file
    
    def info(self, message: str) -> None:
        """Log info level message."""
        self.logger.info(message)
    
    def debug(self, message: str) -> None:
        """Log debug level message."""
        self.logger.debug(message)
    
    def warning(self, message: str) -> None:
        """Log warning level message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error level message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical level message."""
        self.logger.critical(message)
    
    def test_start(self, test_name: str) -> None:
        """Log test start."""
        self.info(f"[TEST START] {test_name}")
    
    def test_end(self, test_name: str, status: str, duration: float) -> None:
        """Log test completion."""
        self.info(f"[TEST END] {test_name} - Status: {status} - Duration: {duration:.2f}s")
    
    def test_error(self, test_name: str, error: str) -> None:
        """Log test error."""
        self.error(f"[TEST ERROR] {test_name} - {error}")
    
    def framework_info(self, message: str) -> None:
        """Log framework-level information."""
        self.info(f"[FRAMEWORK] {message}")
    
    def execution_summary(self, total: int, passed: int, failed: int, skipped: int, duration: float) -> None:
        """Log execution summary."""
        self.info(f"[SUMMARY] Total: {total}, Passed: {passed}, Failed: {failed}, Skipped: {skipped}, Duration: {duration:.2f}s")


# Global logger instance
_logger_instance: Optional[ExecutionLogger] = None


def get_logger(log_dir: Path = Path("logs")) -> ExecutionLogger:
    """Get or create global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = ExecutionLogger(log_dir)
    return _logger_instance
