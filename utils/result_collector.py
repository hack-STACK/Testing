"""
Result Collector - Captures test execution data for reporting.

This module collects test execution data during pytest runs without
modifying test files or page objects. Data is collected via pytest hooks
and stored in memory during execution, then exported to various formats.
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class TestResult:
    """Represents a single test execution result."""
    
    test_id: str                              # Unique identifier (e.g., 'AUTH-001')
    test_name: str                            # Function name (e.g., 'test_register')
    feature: str                              # Feature name (e.g., 'Authentication')
    module: str                               # Module path (e.g., 'tests/authentication')
    status: str                               # PASSED, FAILED, SKIPPED
    duration: float                           # Execution time in seconds
    browser: str                              # Browser used (e.g., 'msedge')
    execution_date: str                       # Date of execution (YYYY-MM-DD)
    execution_time: str                       # Time of execution (HH:MM:SS)
    screenshot: Optional[str] = None          # Screenshot file path
    video: Optional[str] = None               # Video file path
    error_message: Optional[str] = None       # Error message if failed
    pytest_node_id: str = ""                  # Pytest node ID
    environment: str = "local"                # Environment (local, ci, etc.)
    exception_type: Optional[str] = None      # Exception type if failed
    stacktrace: Optional[str] = None          # Full stacktrace if failed
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ExecutionSession:
    """Represents a complete test execution session."""
    
    execution_id: str                         # Unique session ID
    timestamp: str                            # Session start timestamp (ISO format)
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    duration: float = 0.0
    browser: str = "msedge"
    environment: str = "local"
    python_version: str = ""
    playwright_version: str = ""
    pytest_version: str = ""
    machine_name: str = ""
    operating_system: str = ""
    test_results: List[TestResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100
    
    @property
    def fail_rate(self) -> float:
        """Calculate fail rate percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.failed_tests / self.total_tests) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert test results to dictionaries
        data['test_results'] = [result.to_dict() for result in self.test_results]
        return data


class ResultCollector:
    """
    Collects test execution results during pytest session.
    
    Thread-safe collection of test data that can be exported in multiple formats.
    Used by pytest hooks to capture execution metrics without modifying tests.
    """
    
    def __init__(self, execution_id: str):
        """Initialize collector with session ID."""
        self.session = ExecutionSession(
            execution_id=execution_id,
            timestamp=datetime.now().isoformat()
        )
        self.results: List[TestResult] = []
        
    def add_result(self, result: TestResult) -> None:
        """Add a test result to the collection."""
        self.results.append(result)
        self.session.test_results.append(result)
        
        # Update summary counts
        self.session.total_tests += 1
        if result.status == "PASSED":
            self.session.passed_tests += 1
        elif result.status == "FAILED":
            self.session.failed_tests += 1
        elif result.status == "SKIPPED":
            self.session.skipped_tests += 1
    
    def set_duration(self, duration: float) -> None:
        """Set total execution duration in seconds."""
        self.session.duration = duration
    
    def set_environment_info(self, 
                            python_version: str,
                            playwright_version: str, 
                            pytest_version: str,
                            machine_name: str,
                            operating_system: str) -> None:
        """Set environment information."""
        self.session.python_version = python_version
        self.session.playwright_version = playwright_version
        self.session.pytest_version = pytest_version
        self.session.machine_name = machine_name
        self.session.operating_system = operating_system
    
    def get_failed_results(self) -> List[TestResult]:
        """Get only failed test results."""
        return [r for r in self.results if r.status == "FAILED"]
    
    def get_passed_results(self) -> List[TestResult]:
        """Get only passed test results."""
        return [r for r in self.results if r.status == "PASSED"]
    
    def get_skipped_results(self) -> List[TestResult]:
        """Get only skipped test results."""
        return [r for r in self.results if r.status == "SKIPPED"]
    
    def to_dict(self) -> Dict:
        """Convert entire session to dictionary."""
        return self.session.to_dict()
