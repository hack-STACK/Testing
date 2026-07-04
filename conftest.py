import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from time import time

import pytest

from config.setting import BROWSER, HEADLESS
from playwright.sync_api import sync_playwright
from utils.result_collector import ResultCollector, TestResult
from utils.logger import get_logger
from utils.report_generator import TestReportGenerator
from utils.bug_report_generator import BugReportGenerator
from utils.summary_generator import SummaryReportGenerator
from utils.artifact_manager import ArtifactManager
from utils.history_manager import HistoryManager
from utils.terminal_summary import TerminalSummary
from utils.dashboard_generator import DashboardGenerator


def get_module_from_test_path(test_path):
    """Extract module name from test path.
    
    Examples:
        'tests/authentication/test_login.py' -> 'authentication'
        'tests/product/test_search.py' -> 'product'
        'tests/cart/test_checkout.py' -> 'cart'
        'tests/smoke/test_home.py' -> 'smoke'
    """
    parts = test_path.split("/")
    if len(parts) >= 2 and parts[0] == "tests":
        return parts[1]
    return "other"


def organize_video(test_path, test_name):
    """Move and rename video file to organized folder structure.
    
    Videos are recorded with random GUIDs by Playwright.
    This function moves them to: videos/{module}/{test_name}.webm
    """
    module = get_module_from_test_path(test_path)
    videos_dir = Path("videos")
    module_dir = videos_dir / module
    
    # Create module directory
    module_dir.mkdir(parents=True, exist_ok=True)
    
    # Find the most recent video file (latest by modification time)
    video_files = sorted(
        videos_dir.glob("page@*.webm"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    
    if video_files:
        latest_video = video_files[0]
        new_path = module_dir / f"{test_name}.webm"
        
        try:
            shutil.move(str(latest_video), str(new_path))
        except Exception:
            # If move fails, just leave the original file
            pass


def skip_if_cloudflare_challenge(page, is_github_actions):
    if is_github_actions and "One moment" in page.title():
        pytest.skip("Cloudflare challenge on GitHub Actions")


@pytest.fixture
def page(request):

    with sync_playwright() as p:

        is_github_actions = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
        launch_kwargs = {
            "headless": HEADLESS,
            "args": ["--start-maximized"]
        }
        if not is_github_actions:
            launch_kwargs["channel"] = BROWSER

        browser = p.chromium.launch(**launch_kwargs)

        context = browser.new_context(
            viewport=None,
            record_video_dir="videos/"
        )

        page = context.new_page()
        original_goto = page.goto

        def goto_with_cloudflare_check(*args, **kwargs):
            response = original_goto(*args, **kwargs)
            skip_if_cloudflare_challenge(page, is_github_actions)
            return response

        page.goto = goto_with_cloudflare_check

        yield page

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:

            os.makedirs("screenshots/failed", exist_ok=True)

            page.screenshot(
                path=f"screenshots/failed/{request.node.name}.png",
                full_page=True
            )

        context.close()
        browser.close()
        
        # Organize video after test completes
        test_path = request.node.nodeid.split("::")[0]
        test_name = request.node.name
        organize_video(test_path, test_name)


# ============================================================
# PHASE 1: RESULT COLLECTION - Module Level Storage
# ============================================================

# Module-level storage for collector (shared across hooks)
_execution_collector = None
_execution_logger = None


def pytest_configure(config):
    """Initialize result collector at pytest configuration."""
    global _execution_collector, _execution_logger
    
    execution_id = f"EXE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    _execution_collector = ResultCollector(execution_id)
    _execution_logger = get_logger()
    
    # Store in config for access
    config.qafw_collector = _execution_collector
    config.qafw_logger = _execution_logger
    
    # Configure pytest-html if available
    try:
        config.option.htmlpath = "reports/report.html"
        # Ensure reports directory exists
        Path("reports").mkdir(parents=True, exist_ok=True)
    except AttributeError:
        # pytest-html plugin not available
        pass
    except Exception as e:
        _execution_logger.error(f"Failed to configure pytest-html: {e}")
    
    _execution_logger.framework_info(f"Framework initialized - Execution ID: {execution_id}")


def pytest_sessionstart(session):
    """Store start time for duration calculation."""
    session.qafw_start_time = time()


def pytest_runtest_logreport(report):
    """Capture test results for reporting."""
    global _execution_collector, _execution_logger
    
    if report.when != "call" or _execution_collector is None:
        return
    
    # Parse test information
    test_name = report.nodeid.split("::")[-1]
    test_path = report.nodeid.split("::")[0]
    module = get_module_from_test_path(test_path)
    
    # Determine feature from test path
    path_parts = test_path.split("/")
    feature = path_parts[1] if len(path_parts) > 1 else "General"
    feature = feature.capitalize()
    
    # Determine status
    status = "PASSED" if report.passed else "FAILED" if report.failed else "SKIPPED"
    
    # Get duration
    duration = report.duration if hasattr(report, 'duration') else 0.0
    
    # Create result
    result = TestResult(
        test_id=f"{feature[:3].upper()}-{test_name}",
        test_name=test_name,
        feature=feature,
        module=module,
        status=status,
        duration=duration,
        browser=BROWSER,
        execution_date=datetime.now().strftime("%Y-%m-%d"),
        execution_time=datetime.now().strftime("%H:%M:%S"),
        pytest_node_id=report.nodeid,
        environment="local"
    )
    
    # Capture error information if failed
    if report.failed:
        if report.longrepr:
            result.error_message = str(report.longrepr)
        if hasattr(report, 'exc_type') and report.exc_type:
            result.exception_type = report.exc_type.__name__
    
    # Add to collector
    _execution_collector.add_result(result)
    _execution_logger.test_end(test_name, status, duration)


def pytest_sessionfinish(session, exitstatus):
    """Finalize session and log summary."""
    global _execution_collector, _execution_logger
    
    if _execution_collector is None or _execution_logger is None:
        return
    
    # Calculate total duration
    if hasattr(session, 'qafw_start_time'):
        total_duration = time() - session.qafw_start_time
        _execution_collector.set_duration(total_duration)
    
    # Log summary
    _execution_logger.execution_summary(
        _execution_collector.session.total_tests,
        _execution_collector.session.passed_tests,
        _execution_collector.session.failed_tests,
        _execution_collector.session.skipped_tests,
        _execution_collector.session.duration
    )
    
    # Generate Excel reports
    test_report_path = None
    summary_path = None
    bug_path = None
    
    try:
        _execution_logger.framework_info("Generating Excel reports...")
        
        # Test Report
        test_report_gen = TestReportGenerator()
        test_report_path = test_report_gen.generate(_execution_collector.session)
        _execution_logger.framework_info(f"Test Report generated: {test_report_path}")
        
        # Summary Report
        summary_gen = SummaryReportGenerator()
        summary_path = summary_gen.generate(_execution_collector.session)
        _execution_logger.framework_info(f"Summary Report generated: {summary_path}")
        
        # Bug Report (if there are failures)
        if _execution_collector.session.failed_tests > 0:
            bug_gen = BugReportGenerator()
            bug_path = bug_gen.generate(_execution_collector.session)
            if bug_path:
                _execution_logger.framework_info(f"Bug Report generated: {bug_path}")
    
    except Exception as e:
        _execution_logger.error(f"Failed to generate Excel reports: {e}")
    
    # Organize screenshots and videos
    artifact_metadata = {"screenshots": [], "videos": []}
    try:
        _execution_logger.framework_info("Organizing artifacts...")
        artifact_mgr = ArtifactManager()
        
        # Organize screenshots
        ss_moved, ss_errors = artifact_mgr.organize_all_screenshots()
        if ss_moved > 0:
            _execution_logger.framework_info(f"Organized {ss_moved} screenshot(s)")
        
        # Organize videos
        vid_moved, vid_errors = artifact_mgr.organize_all_videos()
        if vid_moved > 0:
            _execution_logger.framework_info(f"Organized {vid_moved} video(s)")

        artifact_metadata = artifact_mgr.get_execution_artifacts()
    
    except Exception as e:
        _execution_logger.error(f"Failed to organize artifacts: {e}")
    
    # Record execution in history
    try:
        _execution_logger.framework_info("Recording execution history...")
        history_mgr = HistoryManager()

        screenshot_by_test = {
            item.get("test_name"): item.get("path")
            for item in artifact_metadata.get("screenshots", [])
            if item.get("test_name") and not item.get("passed", False)
        }
        video_by_test = {
            item.get("test_name"): item.get("path")
            for item in artifact_metadata.get("videos", [])
            if item.get("test_name")
        }

        failed_tests_data = []
        for result in _execution_collector.session.test_results:
            if result.status != "FAILED":
                continue

            failed_tests_data.append({
                "nodeid": result.pytest_node_id,
                "test_name": result.test_name,
                "screenshot": screenshot_by_test.get(result.test_name),
                "video": video_by_test.get(result.test_name)
            })
        
        success = history_mgr.record_execution(
            run_id=_execution_collector.session.execution_id,
            total_tests=_execution_collector.session.total_tests,
            passed_tests=_execution_collector.session.passed_tests,
            failed_tests_count=_execution_collector.session.failed_tests,
            skipped_tests=_execution_collector.session.skipped_tests,
            duration=_execution_collector.session.duration,
            test_report_path=test_report_path,
            summary_report_path=summary_path,
            bug_report_path=bug_path,
            browser=BROWSER,
            headless=HEADLESS,
            failed_tests_data=failed_tests_data
        )
        
        if success:
            _execution_logger.framework_info("Execution history recorded")
    
    except Exception as e:
        _execution_logger.error(f"Failed to record execution history: {e}")
    
    # Print terminal summary
    try:
        summary_printer = TerminalSummary()
        html_report_path = Path("reports/report.html") if Path("reports/report.html").exists() else None
        
        summary_printer.print_execution_summary(
            run_id=_execution_collector.session.execution_id,
            duration=_execution_collector.session.duration,
            total_tests=_execution_collector.session.total_tests,
            passed_tests=_execution_collector.session.passed_tests,
            failed_tests=_execution_collector.session.failed_tests,
            skipped_tests=_execution_collector.session.skipped_tests,
            html_report=html_report_path,
            excel_report=test_report_path,
            summary_report=summary_path,
            bug_report=bug_path
        )
    except Exception as e:
        _execution_logger.error(f"Failed to print terminal summary: {e}")
    
    # Generate dashboard
    try:
        dashboard_gen = DashboardGenerator()
        dashboard_gen.generate_html("reports/dashboard.html")
        _execution_logger.framework_info("Dashboard generated: reports/dashboard.html")
    except Exception as e:
        _execution_logger.error(f"Failed to generate dashboard: {e}")
    
    # Store in session config for later retrieval
    session.config.qafw_collector = _execution_collector


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Original hook - kept for backward compatibility with pytest-html plugin."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)