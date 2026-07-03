import os
import platform
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# ============================================================================
# CONFIGURATION
# ============================================================================

# Report Directory
REPORT_DIR = "artifacts/reports"

# Test Suite Configuration - Centralized
TEST_SUITES = {
    "Authentication": [
        ("Register", "tests/authentication/test_register.py"),
        ("Login", "tests/authentication/test_login.py"),
        ("Logout", "tests/authentication/test_logout.py"),
        ("Delete Account", "tests/authentication/test_delete_account.py"),
        ("Signup", "tests/authentication/test_signup.py"),
    ],
    "Product": [
        ("View Product", "tests/product/test_view_product.py"),
        ("Add to Cart", "tests/product/test_add_to_cart.py"),
        ("Search Product", "tests/product/test_search_product.py"),
    ],
    "Cart": [
        ("Continue Shopping", "tests/cart/test_continue_shopping.py"),
        ("Multiple Products", "tests/cart/test_multiple_products.py"),
        ("Verify Cart Information", "tests/cart/test_verify_cart_information.py"),
        ("Remove Product", "tests/cart/test_remove_product.py"),
        ("View Cart", "tests/cart/test_view_cart.py"),
        ("Proceed to Checkout", "tests/cart/test_proceed_to_checkout.py"),
    ],
    "Checkout": [],
    "Smoke": [
        ("Home Page", "tests/smoke/test_home.py"),
        ("Open", "tests/test_open.py"),
    ],
    "Regression": [
        ("Register", "tests/authentication/test_register.py"),
        ("Login", "tests/authentication/test_login.py"),
        ("Logout", "tests/authentication/test_logout.py"),
        ("Delete Account", "tests/authentication/test_delete_account.py"),
        ("Signup", "tests/authentication/test_signup.py"),
        ("Continue Shopping", "tests/cart/test_continue_shopping.py"),
        ("Multiple Products", "tests/cart/test_multiple_products.py"),
        ("Verify Cart Information", "tests/cart/test_verify_cart_information.py"),
        ("Remove Product", "tests/cart/test_remove_product.py"),
        ("View Cart", "tests/cart/test_view_cart.py"),
        ("Proceed to Checkout", "tests/cart/test_proceed_to_checkout.py"),
        ("View Product", "tests/product/test_view_product.py"),
        ("Add to Cart", "tests/product/test_add_to_cart.py"),
        ("Search Product", "tests/product/test_search_product.py"),
        ("Home Page", "tests/smoke/test_home.py"),
        ("Open", "tests/test_open.py"),
    ],
}

# Build "All Tests" suite by combining all non-empty test suites
TEST_SUITES["All"] = []
for suite_name, tests in TEST_SUITES.items():
    if suite_name not in ("All", "Regression") and tests:
        TEST_SUITES["All"].extend(tests)

console = Console()


# ============================================================================
# MENU & USER INPUT
# ============================================================================

def display_menu() -> str:
    """
    Display interactive menu and get user selection.
    
    Returns:
        Selected suite name or empty string if user exits
    """
    console.print()
    console.print("[bold cyan]" + "=" * 50 + "[/bold cyan]")
    console.print("[bold cyan] AUTOMATION TESTING FRAMEWORK[/bold cyan]")
    console.print("[bold cyan]" + "=" * 50 + "[/bold cyan]")
    console.print()
    
    menu_items = [
        ("1", "Authentication"),
        ("2", "Product"),
        ("3", "Cart"),
        ("4", "Checkout"),
        ("5", "Smoke"),
        ("6", "Regression"),
        ("7", "All Tests"),
        ("0", "Exit"),
    ]
    
    for key, label in menu_items:
        console.print(f"  {key}. {label}")
    
    console.print()
    choice = console.input("[bold cyan]Choose a suite: [/bold cyan]").strip()
    
    suite_map = {
        "1": "Authentication",
        "2": "Product",
        "3": "Cart",
        "4": "Checkout",
        "5": "Smoke",
        "6": "Regression",
        "7": "All",
    }
    
    if choice == "0":
        console.print("[yellow]Exiting...[/yellow]")
        return ""
    
    return suite_map.get(choice, "")


# ============================================================================
# UI DISPLAY FUNCTIONS
# ============================================================================

def print_banner() -> None:
    """Display the application banner."""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]AUTOMATION TESTING FRAMEWORK[/bold cyan]\n"
            "[white]Playwright + Pytest + Page Object Model[/white]",
            border_style="cyan"
        )
    )


def show_environment() -> None:
    """Display environment information."""
    env_table = Table(
        title="Environment",
        border_style="cyan",
        show_header=False
    )
    env_table.add_row("Operating System", platform.system())
    env_table.add_row("Python", platform.python_version())
    env_table.add_row("Execution Time", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    console.print(env_table)
    console.print()


def print_progress(suite_name: str, test_count: int) -> None:
    """Display suite execution header."""
    console.print()
    console.print(f"[bold cyan]Running {suite_name} Suite... ({test_count} tests)[/bold cyan]")
    console.print()


def print_summary(duration: float) -> None:
    """Display execution summary."""
    console.print()
    console.print("[bold cyan]" + "-" * 50 + "[/bold cyan]")
    console.print()
    console.print("[bold]Execution finished[/bold]")
    console.print(f"[bold]Duration[/bold] : {duration:.2f}s")
    console.print()


def show_final_status(success: bool) -> None:
    """Display final status panel."""
    console.print()
    
    if success:
        console.print(
            Panel.fit(
                "🎉 [bold green]ALL TESTS PASSED[/bold green]",
                border_style="green"
            )
        )
    else:
        console.print(
            Panel.fit(
                "❌ [bold red]SOME TESTS FAILED[/bold red]",
                border_style="red"
            )
        )


# ============================================================================
# TEST EXECUTION FUNCTIONS
# ============================================================================

def execute_test_suite(
    tests: List[Tuple[str, str]],
    report_path: str
) -> Tuple[int, float]:
    """
    Execute all tests in a single subprocess call.
    
    pytest handles all output, progress display, and HTML generation.
    run.py only launches and times execution.
    
    Args:
        tests: List of (name, path) tuples
        report_path: Path for HTML report
        
    Returns:
        Tuple of (exit_code, duration)
    """
    # Extract all test paths
    test_paths = [path for _, path in tests]
    
    # Build command with all tests and HTML generation
    command = [
        sys.executable, "-m", "pytest",
        "-v",                              # pytest displays progress
        "--tb=short",
        f"--html={report_path}",
        "--self-contained-html",
        *test_paths
    ]
    
    # Run pytest ONCE (only subprocess call in entire run.py)
    start_time = time.time()
    result = subprocess.run(command, timeout=600)
    duration = time.time() - start_time
    
    # Return exit code and duration
    # pytest's output is already displayed to console
    return result.returncode, duration


# ============================================================================
# REPORT GENERATION
# ============================================================================

def get_report_path(suite_name: str) -> str:
    """
    Generate report path based on suite name.
    
    Args:
        suite_name: Name of the test suite
        
    Returns:
        Full path to the report file
    """
    report_name = f"{suite_name.lower()}_report.html"
    return f"{REPORT_DIR}/{report_name}"


def show_report_location(report_path: str) -> None:
    """
    Display HTML report location.
    
    Args:
        report_path: Path to the HTML report file
    """
    # Ensure report directory exists
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    console.print()
    console.print("[bold cyan]HTML Report:[/bold cyan]")
    console.print(f"[cyan]{report_path}[/cyan]")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> None:
    """Main entry point for the test runner."""
    # Display menu and get user selection
    suite_name = display_menu()
    
    if not suite_name:
        return
    
    # Get the selected test suite
    test_suite = TEST_SUITES.get(suite_name, [])
    
    if not test_suite:
        console.print("[yellow]Selected suite has no tests.[/yellow]")
        return
    
    # Preparation
    print_banner()
    show_environment()
    print_progress(suite_name, len(test_suite))
    
    # Get report path
    report_path = get_report_path(suite_name)
    
    # Execute pytest (single subprocess call)
    print()
    exit_code, duration = execute_test_suite(test_suite, report_path)
    
    # Display results
    print()
    print_summary(duration)
    show_report_location(report_path)
    
    # Final status (convert exit_code to boolean for clarity)
    success = exit_code == 0
    show_final_status(success)


if __name__ == "__main__":
    main()