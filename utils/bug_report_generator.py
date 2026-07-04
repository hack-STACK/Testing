"""
Bug Report Generator - Creates BugReport.xlsx from failed test results.

Generates a bug report entry for each failed test with severity inference
and suggested root causes based on error analysis.
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
from utils.result_collector import ExecutionSession, TestResult
from utils.excel_writer import ExcelWriter


class BugReportGenerator:
    """
    Generates BugReport.xlsx from failed test results.
    
    Creates one bug entry per failed test with severity levels,
    error types, and suggested root causes.
    """
    
    COLUMNS = [
        "Bug ID",
        "Test Name",
        "Feature",
        "Severity",
        "Priority",
        "Status",
        "Error Type",
        "Exception",
        "Screenshot",
        "Video",
        "Detected Time",
        "Suggested Root Cause",
        "Suggested Resolution"
    ]
    
    # Severity mapping based on error type
    SEVERITY_MAP = {
        "TimeoutError": "High",
        "AssertionError": "High",
        "ElementNotFound": "Critical",
        "NavigationFailed": "Critical",
        "ConnectionError": "High",
        "StaleElementReference": "Medium",
        "AttributeError": "Medium",
        "ValueError": "Low",
        "TypeError": "Low",
        "Exception": "Medium"
    }
    
    def __init__(self, output_dir: Path = Path("reports")):
        """Initialize bug report generator."""
        self.output_dir = Path(output_dir)
        self.bug_counter = 0
    
    def _infer_severity(self, result: TestResult) -> str:
        """Infer severity from error type."""
        if not result.exception_type:
            return "Medium"
        
        # Check for exact matches first
        if result.exception_type in self.SEVERITY_MAP:
            return self.SEVERITY_MAP[result.exception_type]
        
        # Check for substring matches
        for error_type, severity in self.SEVERITY_MAP.items():
            if error_type.lower() in result.exception_type.lower():
                return severity
        
        return "Medium"
    
    def _suggest_root_cause(self, result: TestResult) -> str:
        """Suggest root cause based on error analysis."""
        if not result.error_message:
            return "Unknown - Review error logs"
        
        error_lower = result.error_message.lower()
        
        # Common error patterns and suggestions
        patterns = {
            "timeout": "Element not found or page load delay. Increase wait time or improve element selection.",
            "stale element": "DOM updated after element selection. Create fresh element locators.",
            "connection": "Network connectivity issue or server unavailable. Check network or server status.",
            "assertion": f"Expected condition not met. Verify test data and application state.",
            "element not found": "Element selector invalid or element not rendered. Verify selectors and page state.",
            "navigation": "Page navigation failed. Check URL or server availability.",
            "permission": "Insufficient permissions for action. Verify user role and permissions.",
            "attribute error": "Missing attribute in response. Verify API response structure.",
            "type error": "Type mismatch in operation. Check data types in test data.",
        }
        
        for pattern, suggestion in patterns.items():
            if pattern in error_lower:
                return suggestion
        
        return "Review error message and application logs for more details."
    
    def _suggest_resolution(self, result: TestResult) -> str:
        """Suggest resolution based on error type."""
        if not result.exception_type:
            return "Investigate error in detail"
        
        exception_lower = result.exception_type.lower()
        
        resolutions = {
            "timeouterror": "1. Increase timeout in config.setting.TIMEOUT\n2. Add explicit waits for specific elements\n3. Check page load performance",
            "staleelementreference": "1. Avoid caching locators\n2. Create fresh locators for each operation\n3. Refresh page state between operations",
            "connectionerror": "1. Check network connectivity\n2. Verify target server is running\n3. Check firewall/proxy settings",
            "assertionerror": "1. Verify test preconditions\n2. Check test data validity\n3. Verify expected values match actual state",
            "elementnotfound": "1. Verify element selector in browser DevTools\n2. Check element visibility and DOM state\n3. Add wait_for() before click/fill operations",
        }
        
        for exc_type, resolution in resolutions.items():
            if exc_type in exception_lower:
                return resolution
        
        return "1. Review application logs\n2. Capture screenshots/videos\n3. Verify test environment"
    
    def generate(self, session: ExecutionSession) -> Optional[Path]:
        """
        Generate bug report from failed tests.
        
        Args:
            session: ExecutionSession with collected test results
        
        Returns:
            Path to generated Excel file, or None if no failures
        """
        failed_tests = [r for r in session.test_results if r.status == "FAILED"]
        
        if not failed_tests:
            return None
        
        writer = ExcelWriter("BugReport.xlsx", self.output_dir)
        sheet = writer.add_sheet("Bug Report")
        
        # Add header
        sheet.add_header_row(self.COLUMNS, bg_color="8B0000")  # Dark red
        
        # Add bug entries
        for idx, result in enumerate(failed_tests, start=1):
            severity = self._infer_severity(result)
            priority = "P0" if severity == "Critical" else "P1" if severity == "High" else "P2"
            
            row = [
                f"BUG-{str(idx).zfill(4)}",
                result.test_name,
                result.feature,
                severity,
                priority,
                "New",
                result.exception_type or "Unknown",
                (result.error_message or "")[:100],
                result.screenshot or "",
                result.video or "",
                result.execution_time,
                self._suggest_root_cause(result),
                self._suggest_resolution(result)
            ]
            sheet.add_row(row, alignment="left")
        
        # Add summary
        sheet.current_row += 1
        summary_row = [
            f"Total Failed: {len(failed_tests)}",
            f"Critical: {sum(1 for r in failed_tests if self._infer_severity(r) == 'Critical')}",
            f"High: {sum(1 for r in failed_tests if self._infer_severity(r) == 'High')}",
            f"Medium: {sum(1 for r in failed_tests if self._infer_severity(r) == 'Medium')}",
            f"Low: {sum(1 for r in failed_tests if self._infer_severity(r) == 'Low')}"
        ]
        sheet.add_summary_row("Summary", summary_row)
        
        # Auto-adjust columns
        sheet.auto_adjust_columns(max_width=60)
        sheet.freeze_top_row()
        
        # Save
        filepath = writer.save()
        return filepath
