"""
History Manager - Tracks test execution history.

Maintains two JSON files:
- reports/history/latest_execution.json: Most recent execution
- reports/history/history.json: Array of all executions (keeps last 100)
"""

import json
import sys
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


class HistoryManager:
    """
    Manages execution history tracking.
    
    Creates and maintains JSON files with execution metadata.
    """
    
    def __init__(self, history_dir: Path = Path("reports/history")):
        """Initialize history manager."""
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        self.latest_file = self.history_dir / "latest_execution.json"
        self.history_file = self.history_dir / "history.json"
    
    def record_execution(self,
                        run_id: str,
                        total_tests: int,
                        passed_tests: int,
                        failed_tests_count: int,
                        skipped_tests: int,
                        duration: float,
                        test_report_path: Optional[Path] = None,
                        summary_report_path: Optional[Path] = None,
                        bug_report_path: Optional[Path] = None,
                        browser: str = "msedge",
                        headless: bool = False,
                        failed_tests_data: Optional[List[Dict[str, Any]]] = None,
                        failed_test_nodeids: Optional[List[str]] = None) -> bool:
        """
        Record a test execution in history.
        
        Args:
            run_id: Unique execution ID (e.g., EXE_20260704_130107_59ade5f)
            total_tests: Total number of tests executed
            passed_tests: Number of passed tests
            failed_tests_count: Number of failed tests
            skipped_tests: Number of skipped tests
            duration: Execution duration in seconds
            test_report_path: Path to TestReport.xlsx (optional)
            summary_report_path: Path to Summary.xlsx (optional)
            bug_report_path: Path to BugReport.xlsx (optional)
            browser: Browser name (e.g., 'msedge')
            headless: Whether browser runs in headless mode
            failed_test_nodeids: List of failed test nodeids
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Calculate pass rate
            pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0.0
            
            # Get html report path if exists
            html_report = self._get_html_report()
            
            # Capture environment info
            environment = self._capture_environment(browser, headless)
            
            # Capture git info
            git_info = self._capture_git_info()
            
            # Persist caller-provided failed tests data as source of truth.
            # Backward compatibility: support legacy nodeid-only input.
            if failed_tests_data is not None:
                failed_tests_list = failed_tests_data
            else:
                failed_tests_list = [
                    {
                        "nodeid": nodeid,
                        "test_name": nodeid.split("::")[-1] if "::" in nodeid else nodeid,
                        "screenshot": None,
                        "video": None
                    }
                    for nodeid in (failed_test_nodeids or [])
                ]
            
            # Create execution record
            execution_record = {
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "duration": round(duration, 2),
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests_count,
                "skipped": skipped_tests,
                "pass_rate": round(pass_rate, 2),
                "html_report": html_report,
                "excel_report": str(test_report_path) if test_report_path else None,
                "summary_report": str(summary_report_path) if summary_report_path else None,
                "bug_report": str(bug_report_path) if bug_report_path else None,
                "environment": environment,
                "git": git_info,
                "failed_tests": failed_tests_list
            }
            
            # Save as latest execution
            self._save_latest(execution_record)
            
            # Append to history
            self._append_to_history(execution_record)
            
            return True
        
        except Exception as e:
            print(f"Error recording execution in history: {e}")
            return False
    
    def _get_html_report(self) -> Optional[str]:
        """Check if html_report exists and return path."""
        try:
            report_path = Path("reports/report.html")
            if report_path.exists():
                return str(report_path)
        except Exception:
            pass
        return None
    
    def _capture_environment(self, browser: str, headless: bool) -> Dict[str, Any]:
        """Capture environment information."""
        try:
            from importlib.metadata import version
            
            playwright_version = None
            pytest_version = None
            
            try:
                playwright_version = version('playwright')
            except Exception:
                pass
            
            try:
                pytest_version = version('pytest')
            except Exception:
                pass
            
            return {
                "python_version": platform.python_version(),
                "pytest_version": pytest_version,
                "playwright_version": playwright_version,
                "browser": browser,
                "headless": headless,
                "operating_system": sys.platform,
                "platform": platform.platform(),
                "architecture": platform.machine()
            }
        except Exception as e:
            print(f"Error capturing environment: {e}")
            return {
                "python_version": platform.python_version(),
                "pytest_version": None,
                "playwright_version": None,
                "browser": browser,
                "headless": headless,
                "operating_system": sys.platform,
                "platform": platform.platform(),
                "architecture": platform.machine()
            }
    
    def _capture_git_info(self) -> Optional[Dict[str, str]]:
        """Capture git branch and commit hash if in git repository."""
        try:
            # Check if we're in a git repo by trying to run git commands
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd="."
            )
            
            if result.returncode != 0:
                return None
            
            branch = result.stdout.strip()
            
            # Get short commit hash
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd="."
            )
            
            if result.returncode != 0:
                return None
            
            commit = result.stdout.strip()
            
            return {
                "branch": branch,
                "commit": commit
            }
        
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # Git not available or not a git repo
            return None
    
    def _save_latest(self, execution_record: Dict[str, Any]) -> None:
        """Save execution as latest_execution.json."""
        try:
            with open(self.latest_file, 'w', encoding='utf-8') as f:
                json.dump(execution_record, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving latest execution: {e}")
    
    def _append_to_history(self, execution_record: Dict[str, Any]) -> None:
        """Append execution to history.json, keeping last 100 records."""
        try:
            # Load existing history
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            # Ensure it's a list
            if not isinstance(history, list):
                history = []
            
            # Append new record
            history.append(execution_record)
            
            # Keep only last 100 records
            if len(history) > 100:
                history = history[-100:]
            
            # Save updated history
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"Error appending to history: {e}")
    
    def get_latest_execution(self) -> Optional[Dict[str, Any]]:
        """Load and return latest execution record."""
        try:
            if self.latest_file.exists():
                with open(self.latest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading latest execution: {e}")
        
        return None
    
    def get_history(self, limit: int = 10) -> list:
        """
        Load and return execution history.
        
        Args:
            limit: Maximum number of recent records to return (0 for all)
        
        Returns:
            List of execution records
        """
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                if isinstance(history, list):
                    if limit > 0:
                        return history[-limit:]
                    return history
        except Exception as e:
            print(f"Error loading history: {e}")
        
        return []
