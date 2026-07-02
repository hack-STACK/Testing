import platform
import subprocess
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

TESTS = [
    ("Register", "tests/authentication/test_register.py"),
    ("Login", "tests/authentication/test_login.py"),
    ("Logout", "tests/authentication/test_logout.py"),
    ("Delete Account", "tests/authentication/test_delete_account.py"),
]

passed = 0
failed = 0

results = []

start_time = time.time()

console.print()

console.print(
    Panel.fit(
        "[bold cyan]AUTOMATION TESTING FRAMEWORK[/bold cyan]\n"
        "[white]Playwright + Pytest + Page Object Model[/white]",
        border_style="cyan"
    )
)

env = Table(
    title="Environment",
    border_style="cyan",
    show_header=False
)

env.add_row("Operating System", platform.system())
env.add_row("Python", platform.python_version())
env.add_row("Execution Time", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

console.print(env)

console.print()

for name, path in TESTS:

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        transient=True,
    ) as progress:

        progress.add_task(f"Running {name}...", total=None)

        test_start = time.time()

        result = subprocess.run(
            ["pytest", "-q", path],
            capture_output=True,
            text=True
        )

    duration = time.time() - test_start

    if result.returncode == 0:
        status = "PASS"
        passed += 1
        icon = "✅"
    else:
        status = "FAIL"
        failed += 1
        icon = "❌"

    results.append(
        {
            "name": name,
            "status": status,
            "duration": duration,
            "output": result.stdout + result.stderr
        }
    )

total_duration = time.time() - start_time

table = Table(
    title="Authentication Test Result",
    border_style="green",
    header_style="bold green"
)

table.add_column("No", justify="center")
table.add_column("Test Case")
table.add_column("Status", justify="center")
table.add_column("Duration", justify="right")

for index, result in enumerate(results, start=1):

    color = "green" if result["status"] == "PASS" else "red"

    table.add_row(
        str(index),
        result["name"],
        f"[{color}]{result['status']}[/{color}]",
        f"{result['duration']:.2f}s"
    )

console.print(table)

summary = Table(
    title="Execution Summary",
    border_style="cyan",
    show_header=False
)

summary.add_row("Total Test", str(len(TESTS)))
summary.add_row("Passed", f"[green]{passed}[/green]")
summary.add_row("Failed", f"[red]{failed}[/red]")
summary.add_row(
    "Success Rate",
    f"{(passed/len(TESTS))*100:.0f}%"
)
summary.add_row(
    "Total Duration",
    f"{total_duration:.2f}s"
)

console.print(summary)

console.print()

console.print("[bold cyan]Generating HTML Report...[/bold cyan]")

subprocess.run(
    [
        "pytest",
        "tests/authentication/test_register.py",
        "tests/authentication/test_login.py",
        "tests/authentication/test_logout.py",
        "tests/authentication/test_delete_account.py",
        "--html=reports/authentication_report.html",
        "--self-contained-html",
        "-q"
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

console.print(
    "[bold green]HTML Report Generated[/bold green]"
)

console.print(
    "[cyan]reports/authentication_report.html[/cyan]"
)

if failed == 0:

    console.print()

    console.print(
        Panel.fit(
            "🎉 [bold green]ALL TESTS PASSED[/bold green]",
            border_style="green"
        )
    )

else:

    console.print()

    console.print(
        Panel.fit(
            "❌ [bold red]SOME TESTS FAILED[/bold red]",
            border_style="red"
        )
    )