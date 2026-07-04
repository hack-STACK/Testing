"""
Summary Report Generator - Creates Summary.xlsx with execution metrics.

Generates a comprehensive summary of test execution including environment info,
execution statistics, and performance metrics.
"""

from pathlib import Path
import platform
import sys
from datetime import datetime
from utils.result_collector import ExecutionSession
from utils.excel_writer import ExcelWriter


class SummaryReportGenerator:
    """
    Generates Summary.xlsx with execution statistics and environment info.
    
    Creates a summary sheet with pass/fail counts, rates, execution time,
    and environment information.
    """
    
    def __init__(self, output_dir: Path = Path("reports")):
        """Initialize summary report generator."""
        self.output_dir = Path(output_dir)
    
    def generate(self, session: ExecutionSession) -> Path:
        """
        Generate summary report from execution session.
        
        Args:
            session: ExecutionSession with collected test results
        
        Returns:
            Path to generated Excel file
        """
        writer = ExcelWriter("Summary.xlsx", self.output_dir)
        
        # Execution Summary Sheet
        summary_sheet = writer.add_sheet("Execution Summary")
        self._add_execution_summary(summary_sheet, session)
        
        # Environment Sheet
        env_sheet = writer.add_sheet("Environment")
        self._add_environment_info(env_sheet, session)
        
        # Test Statistics Sheet
        stats_sheet = writer.add_sheet("Statistics")
        self._add_test_statistics(stats_sheet, session)
        
        filepath = writer.save()
        return filepath
    
    def _add_execution_summary(self, sheet, session: ExecutionSession) -> None:
        """Add execution summary section."""
        sheet.add_header_row(["Metric", "Value"], bg_color="1F4E78")
        
        metrics = [
            ("Execution ID", session.execution_id),
            ("Timestamp", session.timestamp),
            ("Total Tests", str(session.total_tests)),
            ("Passed", f"{session.passed_tests} ({session.pass_rate:.1f}%)"),
            ("Failed", f"{session.failed_tests} ({session.fail_rate:.1f}%)"),
            ("Skipped", str(session.skipped_tests)),
            ("Pass Rate", f"{session.pass_rate:.1f}%"),
            ("Fail Rate", f"{session.fail_rate:.1f}%"),
            ("Total Duration", f"{session.duration:.2f}s"),
            ("Average Test Duration", f"{session.duration/max(session.total_tests, 1):.2f}s"),
        ]
        
        for metric, value in metrics:
            sheet.add_row([metric, value], alignment="left")
        
        sheet.set_column_widths({"A": 25, "B": 30})
    
    def _add_environment_info(self, sheet, session: ExecutionSession) -> None:
        """Add environment information section."""
        sheet.add_header_row(["Component", "Version/Info"], bg_color="1F4E78")
        
        environment_info = [
            ("Python Version", sys.version),
            ("Platform", platform.platform()),
            ("Machine Name", platform.node()),
            ("Operating System", f"{platform.system()} {platform.release()}"),
            ("Processor", platform.processor()),
            ("Architecture", platform.machine()),
            ("", ""),
            ("Framework Info", ""),
            ("Playwright Version", session.playwright_version or "Not captured"),
            ("Pytest Version", session.pytest_version or "Not captured"),
            ("Browser", session.browser),
            ("Environment", session.environment),
        ]
        
        for component, info in environment_info:
            sheet.add_row([component, info], alignment="left")
        
        sheet.set_column_widths({"A": 25, "B": 50})
    
    def _add_test_statistics(self, sheet, session: ExecutionSession) -> None:
        """Add test statistics section."""
        sheet.add_header_row(["Test Type", "Count", "Percentage", "Avg Duration"], bg_color="1F4E78")
        
        total = session.total_tests or 1
        
        stats = [
            ("Passed Tests", session.passed_tests, 
             f"{(session.passed_tests/total)*100:.1f}%",
             f"{sum(r.duration for r in session.test_results if r.status == 'PASSED')/max(session.passed_tests, 1):.2f}s"),
            ("Failed Tests", session.failed_tests,
             f"{(session.failed_tests/total)*100:.1f}%",
             f"{sum(r.duration for r in session.test_results if r.status == 'FAILED')/max(session.failed_tests, 1):.2f}s"),
            ("Skipped Tests", session.skipped_tests,
             f"{(session.skipped_tests/total)*100:.1f}%",
             "N/A"),
        ]
        
        for test_type, count, percentage, avg_duration in stats:
            sheet.add_row([test_type, str(count), percentage, avg_duration], alignment="center")
        
        # Add feature breakdown
        sheet.current_row += 1
        sheet.add_header_row(["Feature", "Tests", "Passed", "Failed", "Pass Rate"], bg_color="4472C4")
        
        # Group by feature
        features_dict = {}
        for result in session.test_results:
            if result.feature not in features_dict:
                features_dict[result.feature] = {"total": 0, "passed": 0, "failed": 0}
            
            features_dict[result.feature]["total"] += 1
            if result.status == "PASSED":
                features_dict[result.feature]["passed"] += 1
            elif result.status == "FAILED":
                features_dict[result.feature]["failed"] += 1
        
        for feature, counts in sorted(features_dict.items()):
            pass_rate = (counts["passed"] / counts["total"] * 100) if counts["total"] > 0 else 0
            sheet.add_row([
                feature,
                str(counts["total"]),
                str(counts["passed"]),
                str(counts["failed"]),
                f"{pass_rate:.1f}%"
            ], alignment="center")
        
        sheet.set_column_widths({"A": 20, "B": 15, "C": 15, "D": 15, "E": 15})
