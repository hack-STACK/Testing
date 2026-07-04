"""
Test Report Generator - Creates TestReport.xlsx from collected test results.

Generates a comprehensive test execution report with detailed metrics for each test.
"""

from pathlib import Path
from typing import Optional
from utils.result_collector import ResultCollector, ExecutionSession
from utils.excel_writer import ExcelWriter


class TestReportGenerator:
    """
    Generates TestReport.xlsx from test execution results.
    
    Creates a detailed report with one row per test execution including
    status, duration, environment, screenshots, and videos.
    """
    
    COLUMNS = [
        "Test ID",
        "Test Name",
        "Feature",
        "Module",
        "Status",
        "Duration (s)",
        "Browser",
        "Execution Date",
        "Execution Time",
        "Screenshot",
        "Video",
        "Error Message",
        "Pytest Node ID",
        "Environment"
    ]
    
    def __init__(self, output_dir: Path = Path("reports")):
        """Initialize report generator."""
        self.output_dir = Path(output_dir)
    
    def generate(self, session: ExecutionSession) -> Path:
        """
        Generate test report from execution session.
        
        Args:
            session: ExecutionSession with collected test results
        
        Returns:
            Path to generated Excel file
        """
        writer = ExcelWriter("TestReport.xlsx", self.output_dir)
        sheet = writer.add_sheet("Test Results")
        
        # Add header
        sheet.add_header_row(self.COLUMNS)
        
        # Add test results
        for result in session.test_results:
            row = [
                result.test_id,
                result.test_name,
                result.feature,
                result.module,
                result.status,
                f"{result.duration:.2f}",
                result.browser,
                result.execution_date,
                result.execution_time,
                result.screenshot or "",
                result.video or "",
                result.error_message or "",
                result.pytest_node_id,
                result.environment
            ]
            sheet.add_row(row, alignment="left")
        
        # Add summary at bottom
        sheet.current_row += 1
        summary_row = [
            "",
            f"TOTAL: {session.total_tests}",
            f"PASSED: {session.passed_tests}",
            f"FAILED: {session.failed_tests}",
            f"SKIPPED: {session.skipped_tests}",
            f"{session.pass_rate:.1f}%",
            f"{session.duration:.2f}s"
        ]
        sheet.add_summary_row("Summary", summary_row[:6])
        
        # Auto-adjust columns
        sheet.auto_adjust_columns()
        sheet.freeze_top_row()
        
        # Save
        filepath = writer.save()
        return filepath
