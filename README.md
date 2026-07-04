# Web Automation Testing Framework

This project was created for the **Automation Testing** course at **BINUS University**.

The goal of this project is to automate web testing using **Python**, **Pytest**, and **Playwright**. The framework uses the **Page Object Model (POM)** to keep the code organized and easier to maintain.

---

# Features

This framework can automate several test scenarios, including:

- User Registration
- User Login
- User Logout
- Delete Account
- View Products
- Search Products
- Add Product to Cart
- Remove Product from Cart
- Continue Shopping
- View Cart
- Verify Cart Information
- Proceed to Checkout

After every test execution, the framework also generates reports automatically.

---

# Technologies Used

- Python
- Pytest
- Playwright
- OpenPyXL
- pytest-html
- GitHub Actions

---

# Project Structure

```text
TestingProject/
│
├── config/
├── data/
├── docs/
├── pages/
├── tests/
├── utils/
├── reports/
├── artifacts/
├── logs/
├── run.py
└── README.md
```

---

# Installation

Clone this repository.

```bash
git clone <repository-url>
```

Go to the project folder.

```bash
cd TestingProject
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install all dependencies.

```bash
pip install -r requirements.txt
```

Install Playwright browsers.

```bash
playwright install
```

---

# Running the Tests

Run all tests.

```bash
pytest
```

Run tests from one folder.

```bash
pytest tests/authentication
```

Run a single test.

```bash
pytest tests/product/test_add_to_cart.py
```

Or run the project using:

```bash
python run.py
```

---

# Reports

After the tests finish, the framework automatically creates several reports.

### Reports Folder

```text
reports/
```

Generated reports:

- report.html
- dashboard.html
- TestReport.xlsx
- Summary.xlsx
- BugReport.xlsx (only if there are failed tests)

### Artifacts Folder

```text
artifacts/
```

This folder stores:

- Screenshots
- Test videos
- Execution artifacts

---

# Dashboard

The dashboard shows a quick summary of the latest test execution.

Information available:

- Total Tests
- Passed Tests
- Failed Tests
- Skipped Tests
- Pass Rate
- Execution Time
- Execution History
- Report Links

If a test fails, the dashboard also provides a screenshot and video for that failed test.

---

# GitHub Actions

This project supports GitHub Actions.

Whenever code is pushed or a pull request is created, the workflow can automatically run the test suite.

Workflow location:

```text
.github/workflows/test.yml
```

---

# Framework Workflow

```text
Run Test
    │
    ▼
Pytest
    │
    ▼
Playwright
    │
    ▼
Page Object Model
    │
    ▼
Execute Test
    │
    ▼
Generate Reports
    │
    ▼
Dashboard & History
    │
    ▼
Artifacts
```

---

# What I Learned

During this project, I learned how to:

- Build a test automation framework
- Apply the Page Object Model (POM)
- Organize automation tests using Pytest
- Generate HTML and Excel reports
- Capture screenshots and videos automatically
- Create a simple dashboard for test results
- Use GitHub Actions for automated testing

---

# Future Improvements

Some features that can still be added are:

- Allure Report
- Docker support
- Parallel test execution
- Email notifications
- More cross-browser testing

---

# Author

**Juan**

BINUS University

Testing and System Implementation

Semester 2
