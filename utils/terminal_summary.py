"""
Terminal Summary - Prints execution summary to console.

Displays test results, artifacts, and report locations in clean format.
"""

from pathlib import Path
from typing import Optional, List


class TerminalSummary:
    """
    Generates and prints clean terminal execution summary.
    """
    
    def __init__(self):
        """Initialize terminal summary printer."""
        self.reports_dir = Path("reports")
        self.artifacts_dir = Path("artifacts")
        self.history_dir = Path("reports/history")
    
    def print_execution_summary(self,
                               run_id: str,
                               duration: float,
                               total_tests: int,
                               passed_tests: int,
                               failed_tests: int,
                               skipped_tests: int,
                               html_report: Optional[Path] = None,
                               excel_report: Optional[Path] = None,
                               summary_report: Optional[Path] = None,
                               bug_report: Optional[Path] = None) -> None:
        """
        Print clean execution summary to console.
        
        Args:
            run_id: Execution ID
            duration: Total execution duration in seconds
            total_tests: Total number of tests
            passed_tests: Number of passed tests
            failed_tests: Number of failed tests
            skipped_tests: Number of skipped tests
            html_report: Path to HTML report (optional)
            excel_report: Path to Excel test report (optional)
            summary_report: Path to Summary Excel report (optional)
            bug_report: Path to Bug Excel report (optional)
        """
        try:
            # Calculate metrics
            pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0.0
            
            # Build summary lines
            lines = []
            lines.append("=" * 60)
            lines.append("TEST EXECUTION SUMMARY")
            lines.append("=" * 60)
            lines.append("")
            
            # Execution info
            lines.append(f"Run ID: {run_id}")
            lines.append(f"Duration: {duration:.2f}s")
            lines.append("")
            
            # Test results
            lines.append("Results:")
            lines.append(f"  Total:  {total_tests}")
            lines.append(f"  Passed: {passed_tests}")
            lines.append(f"  Failed: {failed_tests}")
            lines.append(f"  Skipped: {skipped_tests}")
            lines.append("")
            
            # Pass rate
            lines.append(f"Pass Rate: {pass_rate:.1f}%")
            lines.append("")
            
            # Reports
            lines.append("Reports:")
            if html_report and Path(html_report).exists():
                lines.append(f"  ✓ HTML Report: {html_report}")
            if excel_report and Path(excel_report).exists():
                lines.append(f"  ✓ Test Report: {excel_report}")
            if summary_report and Path(summary_report).exists():
                lines.append(f"  ✓ Summary Report: {summary_report}")
            if bug_report and Path(bug_report).exists():
                lines.append(f"  ✓ Bug Report: {bug_report}")
            lines.append("")
            
            # Artifacts
            lines.append("Artifacts:")
            screenshots_fail = self.artifacts_dir / "screenshots" / "fail"
            screenshots_pass = self.artifacts_dir / "screenshots" / "pass"
            videos = self.artifacts_dir / "videos"
            
            if screenshots_fail.exists():
                count = len(list(screenshots_fail.glob("*.png")))
                if count > 0:
                    lines.append(f"  ✓ Screenshots (failed): {count} files")
            if screenshots_pass.exists():
                count = len(list(screenshots_pass.glob("*.png")))
                if count > 0:
                    lines.append(f"  ✓ Screenshots (passed): {count} files")
            if videos.exists():
                count = len(list(videos.glob("**/*.webm")))
                if count > 0:
                    lines.append(f"  ✓ Videos: {count} files")
            
            if not (screenshots_fail.exists() or screenshots_pass.exists() or videos.exists()):
                lines.append("  (none)")
            lines.append("")
            
            # History
            lines.append("History:")
            latest_file = self.history_dir / "latest_execution.json"
            history_file = self.history_dir / "history.json"
            
            if latest_file.exists():
                lines.append(f"  ✓ Latest: {latest_file}")
            if history_file.exists():
                lines.append(f"  ✓ History: {history_file}")
            
            lines.append("")
            lines.append("=" * 60)
            
            # Print all lines
            for line in lines:
                print(line)
        
        except Exception as e:
            print(f"Error printing execution summary: {e}")
