"""
Dashboard HTML Generator

Generates an interactive HTML dashboard from execution data.
Reads from history.json, latest_execution.json, and reports.
No modifications to existing files or framework logic.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import quote


class DashboardGenerator:
    """Generates interactive HTML dashboard from execution history."""
    
    def __init__(self, reports_dir: str = "reports"):
        """Initialize dashboard generator.
        
        Args:
            reports_dir: Path to reports directory
        """
        self.reports_dir = Path(reports_dir)
        self.history_file = self.reports_dir / "history" / "history.json"
        self.latest_file = self.reports_dir / "history" / "latest_execution.json"
        self.dashboard_file = self.reports_dir / "dashboard.html"
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load execution history from JSON.
        
        Returns:
            List of execution records or empty list if file not found
        """
        try:
            if self.history_file.exists():
                with open(self.history_file) as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load history: {e}")
        return []
    
    def _load_latest(self) -> Dict[str, Any]:
        """Load latest execution record.
        
        Returns:
            Latest execution record or empty dict if file not found
        """
        try:
            if self.latest_file.exists():
                with open(self.latest_file) as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load latest execution: {e}")
        return {}
    
    def _get_pass_rate_trend(self, history: List[Dict]) -> List[float]:
        """Extract pass rates from history for chart.
        
        Args:
            history: List of execution records
            
        Returns:
            List of pass rates (most recent last)
        """
        rates = []
        for record in history[-10:]:  # Last 10 executions
            if "pass_rate" in record:
                rates.append(record["pass_rate"])
            elif record.get("total", 0) > 0:
                passed = record.get("passed", 0)
                total = record.get("total", 1)
                rates.append((passed / total) * 100)
        return rates
    
    def _get_execution_dates(self, history: List[Dict]) -> List[str]:
        """Extract execution dates from history.
        
        Args:
            history: List of execution records
            
        Returns:
            List of dates (short format)
        """
        dates = []
        for record in history[-10:]:  # Last 10 executions
            if "timestamp" in record:
                try:
                    dt = datetime.fromisoformat(record["timestamp"].replace('Z', '+00:00'))
                    dates.append(dt.strftime("%m-%d %H:%M"))
                except:
                    dates.append("N/A")
        return dates
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def _get_failed_tests(self, latest: Dict) -> List[Dict[str, Optional[str]]]:
        """Extract failed test list from latest execution.
        
        Args:
            latest: Latest execution record
            
        Returns:
            List of failed test info
        """
        failed_tests = []

        source = latest.get("failed_tests", [])
        if not source:
            return failed_tests

        for entry in source:
            if isinstance(entry, str):
                # Backward compatibility with older history format (nodeid only)
                test_name = entry.split("::")[-1] if "::" in entry else entry
                failed_tests.append({
                    "name": test_name,
                    "nodeid": entry,
                    "severity": "Unknown",
                    "screenshot": None,
                    "video": None
                })
                continue

            if isinstance(entry, dict):
                nodeid = entry.get("nodeid") or entry.get("pytest_node_id") or ""
                test_name = entry.get("test_name") or (nodeid.split("::")[-1] if "::" in nodeid else nodeid) or "Unknown"
                failed_tests.append({
                    "name": test_name,
                    "nodeid": nodeid,
                    "severity": entry.get("severity", "Unknown"),
                    "screenshot": entry.get("screenshot"),
                    "video": entry.get("video")
                })

        return failed_tests

    def _artifact_href(self, artifact_path: Optional[str]) -> Optional[str]:
        """Return a URL-safe relative href only when the artifact exists."""
        if artifact_path is None:
            return None

        project_root = self.reports_dir.parent.resolve()
        raw_path = Path(artifact_path)

        candidates = []
        if raw_path.is_absolute():
            candidates.append(raw_path)
        else:
            # Normal relative path from project root (expected): artifacts/...
            candidates.append((project_root / raw_path).resolve())

            # Backward-compatible normalization when path was persisted as reports/artifacts/...
            parts = list(raw_path.parts)
            if "artifacts" in parts:
                artifacts_index = parts.index("artifacts")
                normalized = Path(*parts[artifacts_index:])
                candidates.append((project_root / normalized).resolve())

        artifact = next((candidate for candidate in candidates if candidate.exists()), None)

        if artifact is None:
            return None

        dashboard_base = self.dashboard_file.parent.resolve()
        final_relative = Path(os.path.relpath(str(artifact), start=str(dashboard_base))).as_posix()

        # Encode each path segment to support timestamped or special-char filenames.
        encoded_parts = [quote(part) for part in final_relative.split("/")]
        return "/".join(encoded_parts)
    
    def generate_html(self, output_file: str = None) -> str:
        """Generate HTML dashboard.
        
        Args:
            output_file: Optional output file path. If provided, writes HTML to file.
            
        Returns:
            HTML string
        """
        if output_file is None:
            output_file = str(self.reports_dir / "dashboard.html")
        self.dashboard_file = Path(output_file)
        
        # Load data
        history = self._load_history()
        latest = self._load_latest()
        
        # Extract metrics
        total = latest.get("total", 0)
        passed = latest.get("passed", 0)
        failed = latest.get("failed", 0)
        skipped = latest.get("skipped", 0)
        duration = latest.get("duration", 0)
        pass_rate = latest.get("pass_rate", 0) if total > 0 else 0
        timestamp = latest.get("timestamp", "N/A")
        run_id = latest.get("run_id", "N/A")
        latest_bug_report = latest.get("bug_report")
        
        # Get trend data
        pass_rates = self._get_pass_rate_trend(history)
        dates = self._get_execution_dates(history)
        failed_tests = self._get_failed_tests(latest)
        
        # Generate HTML
        html = self._generate_html_content(
            total, passed, failed, skipped, duration, pass_rate,
            timestamp, run_id, history, pass_rates, dates, failed_tests, latest_bug_report
        )
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html)
        
        return html
    
    def _generate_html_content(self, total: int, passed: int, failed: int, 
                               skipped: int, duration: float, pass_rate: float,
                               timestamp: str, run_id: str, history: List[Dict],
                               pass_rates: List[float], dates: List[str],
                                     failed_tests: List[Dict[str, Optional[str]]],
                                     latest_bug_report: Optional[str]) -> str:
        """Generate complete HTML content.
        
        Returns:
            Complete HTML string
        """
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = timestamp
        
        # Format duration
        duration_str = self._format_duration(duration)
        
        # Build failed tests table
        failed_tests_html = ""
        if failed_tests:
            for test in failed_tests:
                screenshot_href = self._artifact_href(test.get("screenshot"))
                video_href = self._artifact_href(test.get("video"))

                screenshot_button = (
                    f'<a href="{screenshot_href}" class="link-button" target="_blank">Screenshot</a>'
                    if screenshot_href
                    else '<span class="link-button link-button-disabled">Not Available</span>'
                )
                video_button = (
                    f'<a href="{video_href}" class="link-button" target="_blank">Video</a>'
                    if video_href
                    else '<span class="link-button link-button-disabled">Not Available</span>'
                )

                failed_tests_html += f"""
                <tr>
                    <td>{test['name']}</td>
                    <td><span class="severity-{test['severity'].lower() if test['severity'] != 'Unknown' else 'unknown'}">{test['severity']}</span></td>
                    <td>{screenshot_button}</td>
                    <td>{video_button}</td>
                </tr>
                """
        else:
            failed_tests_html = "<tr><td colspan='4' style='text-align: center; color: #666;'>No failed tests</td></tr>"
        
        # Build history table
        history_html = ""
        if history:
            for record in history[-10:][::-1]:  # Last 10, reversed (newest first)
                h_timestamp = record.get("timestamp", "N/A")
                try:
                    dt = datetime.fromisoformat(h_timestamp.replace('Z', '+00:00'))
                    h_time = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    h_time = h_timestamp
                
                h_total = record.get("total", 0)
                h_passed = record.get("passed", 0)
                h_failed = record.get("failed", 0)
                h_pass_rate = record.get("pass_rate", 0)
                h_duration = self._format_duration(record.get("duration", 0))
                
                status_color = "#28a745" if h_failed == 0 else "#dc3545"
                
                history_html += f"""
                <tr>
                    <td>{h_time}</td>
                    <td style="text-align: center;">{h_total}</td>
                    <td style="text-align: center; color: #28a745;">{h_passed}</td>
                    <td style="text-align: center; color: #dc3545;">{h_failed}</td>
                    <td style="text-align: center;">{h_pass_rate:.1f}%</td>
                    <td style="text-align: center;">{h_duration}</td>
                </tr>
                """
        else:
            history_html = "<tr><td colspan='6' style='text-align: center; color: #666;'>No history available</td></tr>"
        
        # Build chart data
        chart_data = "[]"
        chart_labels = "[]"
        if pass_rates:
            chart_data = str(pass_rates).replace("'", "")
            chart_labels = str(dates).replace("'", '"')

        bug_report_href = None
        if latest_bug_report:
            bug_report_file = Path(latest_bug_report)
            if not bug_report_file.is_absolute():
                bug_report_file = (self.reports_dir.parent / bug_report_file).resolve()
            if bug_report_file.exists():
                dashboard_base = self.dashboard_file.parent.resolve()
                bug_report_href = Path(os.path.relpath(str(bug_report_file), start=str(dashboard_base))).as_posix()

        bug_report_link = (
            f'<a href="{bug_report_href}" class="link-button" target="_blank">🐛 Bug Report (Excel)</a>'
            if bug_report_href
            else '<span class="link-button link-button-disabled">🐛 Bug Report Not Available</span>'
        )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .metric-label {{
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-unit {{
            font-size: 14px;
            color: #999;
            margin-top: 5px;
        }}
        
        .pass-rate {{
            position: relative;
            height: 8px;
            background: #eee;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
        }}
        
        .pass-rate-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }}
        
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
            margin-bottom: 20px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            color: #333;
            font-weight: 600;
            border-bottom: 2px solid #eee;
        }}
        
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
            color: #666;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .severity-critical {{
            background: #dc3545;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .severity-high {{
            background: #fd7e14;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .severity-medium {{
            background: #ffc107;
            color: #333;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .severity-unknown {{
            background: #6c757d;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .links-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .link-button {{
            display: block;
            padding: 8px 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            text-align: center;
            font-weight: 500;
            transition: transform 0.2s, box-shadow 0.2s;
            font-size: 12px;
        }}
        
        .link-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        .link-button-disabled {{
            background: #dee2e6;
            color: #6c757d;
            cursor: not-allowed;
        }}

        .link-button-disabled:hover {{
            transform: none;
            box-shadow: none;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        .empty-state-icon {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            .metrics-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            h1 {{
                font-size: 20px;
            }}
            
            .metric-value {{
                font-size: 24px;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            th, td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Test Execution Dashboard</h1>
            <div class="subtitle">Latest execution: {formatted_time} | Run ID: {run_id}</div>
        </header>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Tests</div>
                <div class="metric-value">{total}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Passed</div>
                <div class="metric-value" style="color: #28a745;">{passed}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Failed</div>
                <div class="metric-value" style="color: #dc3545;">{failed}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Skipped</div>
                <div class="metric-value" style="color: #ffc107;">{skipped}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Pass Rate</div>
                <div class="metric-value">{pass_rate:.1f}%</div>
                <div class="pass-rate">
                    <div class="pass-rate-fill" style="width: {pass_rate}%"></div>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Duration</div>
                <div class="metric-value">{duration_str}</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">📈 Pass Rate Trend</div>
            <div class="chart-container">
                <canvas id="trendChart"></canvas>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">❌ Failed Tests</div>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Severity</th>
                        <th>Screenshot</th>
                        <th>Video</th>
                    </tr>
                </thead>
                <tbody>
                    {failed_tests_html}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">📋 Execution History (Last 10)</div>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Pass Rate</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>
                    {history_html}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <div class="section-title">🔗 Quick Links</div>
            <div class="links-grid">
                <a href="report.html" class="link-button">📄 HTML Report</a>
                <a href="TestReport.xlsx" class="link-button" target="_blank">📊 Test Report (Excel)</a>
                <a href="Summary.xlsx" class="link-button" target="_blank">📈 Summary (Excel)</a>
                {bug_report_link}
            </div>
        </div>
    </div>
    
    <script>
        // Pass rate trend chart
        const ctx = document.getElementById('trendChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {chart_labels},
                datasets: [{{
                    label: 'Pass Rate (%)',
                    data: {chart_data},
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: 'white',
                    pointBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        labels: {{
                            font: {{ size: 12 }},
                            color: '#333'
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            color: '#999',
                            callback: function(value) {{
                                return value + '%';
                            }}
                        }},
                        grid: {{
                            color: '#f0f0f0'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#999'
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
