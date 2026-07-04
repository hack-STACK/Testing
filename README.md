# Web Automation Testing Framework

This project was developed as the final project for the **Testing and System Implementation (ISYS6338003)** course at **BINUS University**.

The purpose of this project is to build an automation testing framework that can execute functional web testing using **Python**, **Pytest**, and **Playwright**. The framework follows the **Page Object Model (POM)** design pattern to keep the project organized, reusable, and easier to maintain.

Besides automating browser interactions, the framework also generates detailed reports, stores execution artifacts, maintains execution history, and supports Continuous Integration using GitHub Actions.

---

# Features

The framework automates several user scenarios, including:

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

After every execution, the framework automatically generates reports and stores testing artifacts.

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
├── .github/
│   └── workflows/
│       └── test.yml
│
├── artifacts/
│
├── config/
│
├── data/
│
├── docs/
│
├── logs/
│
├── pages/
│
├── reports/
│
├── tests/
│
├── utils/
│
├── requirements.txt
├── pytest.ini
├── run.py
└── README.md
```

Each folder has its own responsibility, making the project easier to understand and maintain.

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

Install the project dependencies.

```bash
pip install -r requirements.txt
```

Install Playwright browsers.

```bash
playwright install
```

---

# Running the Tests

Run all test cases.

```bash
pytest
```

Run tests inside a specific folder.

```bash
pytest tests/authentication
```

Run a specific test file.

```bash
pytest tests/product/test_add_to_cart.py
```

Or simply execute:

```bash
python run.py
```

---

# Reports

After every execution, the framework automatically generates several reports.

### Reports

```text
reports/
```

Generated reports include:

- report.html
- dashboard.html
- TestReport.xlsx
- Summary.xlsx
- BugReport.xlsx *(generated only when failed test cases exist)*

---

### Artifacts

```text
artifacts/
```

This folder stores:

- Screenshots
- Video recordings
- Other execution artifacts

These files are useful for debugging failed test cases.

---

# Dashboard

The custom dashboard provides a quick overview of the latest test execution.

The dashboard displays:

- Total Tests
- Passed Tests
- Failed Tests
- Skipped Tests
- Pass Rate
- Execution Time
- Execution History
- Report Links

If a test case fails, the dashboard also provides direct access to screenshots and recorded videos.

---

# GitHub Actions

This project supports Continuous Integration using GitHub Actions.

Whenever code is pushed or a Pull Request is created, GitHub Actions can automatically:

- Install project dependencies
- Install Playwright browsers
- Execute automated tests
- Generate reports
- Upload artifacts

Workflow location:

```text
.github/workflows/test.yml
```

---

# Framework Workflow

```text
Start
   │
   ▼
Run Pytest
   │
   ▼
Launch Playwright
   │
   ▼
Execute Test Cases
   │
   ▼
Generate Reports
   │
   ▼
Generate Dashboard
   │
   ▼
Save Artifacts
   │
   ▼
Update History
   │
   ▼
Finish
```

---

# What I Learned

Through this project, I learned how to:

- Build a web automation testing framework from scratch.
- Apply the Page Object Model (POM).
- Organize test cases using Pytest.
- Generate HTML and Excel reports automatically.
- Capture screenshots and videos for debugging.
- Build a simple dashboard to summarize test results.
- Integrate GitHub Actions for Continuous Integration.
- Improve debugging and project maintenance using modular utilities.

---

# Future Improvements

Some features that can still be added include:

- Allure Report integration
- Docker support
- Parallel test execution
- Email notifications
- Cross-browser testing improvements
- API automation testing

---

# AI Assistance

This project was developed under a tight academic deadline. To improve productivity and speed up development, AI tools such as **GitHub Copilot** and **ChatGPT** were used as coding assistants during the development process.

AI was mainly used to:

- Generate initial code suggestions.
- Explain programming concepts.
- Assist with debugging ideas.
- Improve documentation.
- Review code structure and readability.

However, the overall framework architecture, project structure, implementation, debugging, testing, report generation, dashboard development, GitHub Actions integration, and final validation were completed, reviewed, and verified by the project author.

Every AI-generated suggestion was manually evaluated, modified when necessary, and tested before being included in the final project.

---

# Repository

GitHub Repository:

https://github.com/hack-STACK/Testing

---

# Author

**Muhammad Najwan Hibatullah (Juan)**

Student ID: **2902616684**

Bachelor of Information Systems

BINUS University

Course: **Testing and System Implementation (ISYS6338003)**

Semester 2

2025/2026
