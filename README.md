# QA Automation Testing Framework

A modern, scalable test automation framework built with **Playwright**, **Pytest**, and the **Page Object Model** pattern. This project demonstrates best practices in automated testing for e-commerce applications.

## 📋 Project Overview

This is a comprehensive QA automation testing framework designed for the Automation Exercise e-commerce platform. The framework implements industry-standard testing patterns and provides a solid foundation for scaling test automation across multiple modules.

**Framework Highlights:**
- ✅ 16 passing tests covering authentication, product, and cart workflows
- ✅ Page Object Model (POM) architecture for maintainability
- ✅ Atomic test actions with clear separation of concerns
- ✅ Runtime data separation (static vs. dynamic data)
- ✅ Screenshot management with nested directory support
- ✅ HTML reporting with Pytest plugins
- ✅ Video recording for failed test debugging

---

## ✨ Features

### 🔐 Authentication Module
- User registration with account creation
- Email-based login with success/failure verification
- User logout and session management
- Account deletion workflow
- Dynamic email generation for test isolation

### 📦 Product Module
- View product listings and details
- Search products by keyword
- Add products to cart with visual confirmation
- Multi-product browsing and cart workflows

### 🛒 Cart Module
- View and manage shopping cart
- Remove products from cart
- Multi-product cart operations
- Cart data verification (price, quantity, total calculations)
- Proceed to checkout
- Continue shopping between product additions

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Browser Automation** | Playwright (Sync API) | 1.61.0 |
| **Test Framework** | Pytest | 9.1.1 |
| **Language** | Python | 3.14.6 |
| **Test Reporting** | Pytest HTML | 4.2.0 |
| **Reporting Enhancement** | Pytest Sugar | 1.1.1 |
| **Assertion Help** | Pytest Clarity | 1.0.1 |
| **Browser** | Microsoft Edge | Latest |

---

## 📁 Folder Structure

```
TestingProject/
├── pages/                      # Page Object Model implementations
│   ├── authentication/         # Login, signup, account management
│   │   ├── login_page.py
│   │   ├── signup_page.py
│   │   └── account_page.py
│   ├── product/                # Product browsing and search
│   │   └── product_page.py
│   ├── cart/                   # Shopping cart operations
│   │   └── cart_page.py
│   └── checkout/               # Checkout process
│       └── checkout_page.py
│
├── tests/                      # Test suites organized by feature
│   ├── authentication/         # Auth workflow tests (5 tests)
│   │   ├── test_register.py
│   │   ├── test_login.py
│   │   ├── test_logout.py
│   │   ├── test_delete_account.py
│   │   └── test_signup.py
│   ├── product/                # Product feature tests (3 tests)
│   │   ├── test_add_to_cart.py
│   │   ├── test_search_product.py
│   │   └── test_view_product.py
│   ├── cart/                   # Cart feature tests (6 tests)
│   │   ├── test_view_cart.py
│   │   ├── test_remove_product.py
│   │   ├── test_continue_shopping.py
│   │   ├── test_multiple_products.py
│   │   ├── test_verify_cart_information.py
│   │   └── test_proceed_to_checkout.py
│   └── smoke/                  # Smoke test (1 test)
│       └── test_home.py
│
├── utils/                      # Shared utilities
│   ├── base_page.py            # BasePage with common actions
│   ├── user_manager.py         # Test user credential management
│   └── data_reader.py          # JSON data file helpers
│
├── config/                     # Configuration management
│   └── setting.py              # Centralized settings (URLs, timeouts)
│
├── data/                       # Static test data (fixtures)
│   ├── users.json              # Pre-configured user credentials
│   ├── register_data.json      # Account creation test data
│   └── product_data.json       # Product search test data
│
├── runtime/                    # Runtime data (created during test execution)
│   └── latest_user.json        # Dynamically generated user credentials
│
├── screenshots/                # Test screenshots (auto-generated)
│   └── failed/                 # Failed test screenshots
│
├── videos/                     # Test execution videos (Playwright recordings)
│
├── reports/                    # HTML test reports
│   ├── report.html
│   └── authentication_report.html
│
├── conftest.py                 # Pytest configuration and fixtures
├── pytest.ini                  # Pytest settings
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Microsoft Edge browser (or Chromium)
- Git

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd TestingProject
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest -v
```

### Run Tests by Category
```bash
# Authentication tests only
pytest tests/authentication/ -v

# Product tests only
pytest tests/product/ -v

# Cart tests only
pytest tests/cart/ -v

# Smoke tests only
pytest tests/smoke/ -v
```

### Run Specific Test
```bash
pytest tests/authentication/test_login.py -v
```

### Run with Markers
```bash
pytest -m authentication -v
pytest -m cart -v
pytest -m product -v
```

### Run in Headless Mode
```bash
HEADLESS=True pytest -v
```

### Run with Custom Timeout
```bash
# Tests use TIMEOUT=10000ms by default (configured in config/setting.py)
pytest -v
```

---

## 📊 Generating HTML Reports

### Full Test Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Authentication-only Report
```bash
pytest tests/authentication/ --html=reports/authentication_report.html --self-contained-html
```

### View Reports
Open the generated HTML file in a browser:
```bash
open reports/report.html  # macOS
start reports/report.html # Windows
```

**Report Features:**
- Test execution summary
- Pass/fail breakdown
- Test duration tracking
- Screenshots for failed tests
- Video recordings embedded

---

## 🏗️ Project Architecture

### Page Object Model (POM)
The framework uses the Page Object Model pattern for maintainability and reusability:

```
BasePage (utils/base_page.py)
  ├── LoginPage
  ├── SignupPage
  ├── AccountPage
  ├── ProductPage
  ├── CartPage
  └── CheckoutPage
```

**BasePage provides atomic actions:**
- `is_visible(selector)` - Check element visibility with timeout
- `visit(url)` - Navigate to URL with DOM content load wait
- `click(selector)` - Click element after visibility check
- `fill(selector, text)` - Fill input field with text
- `text(selector)` - Get element text content
- `screenshot(name)` - Capture screenshot with nested directory support

### Data Management
- **Static Data:** `data/` folder contains JSON fixtures (users, products, account info)
- **Runtime Data:** `runtime/` folder stores dynamically created user credentials
- **Test Isolation:** Each test run creates fresh credentials in `runtime/latest_user.json`

### Test Execution Order
Authentication tests run in enforced sequential order to simulate real user workflows:
1. `test_register.py` - Create account
2. `test_login.py` - Login with account
3. `test_logout.py` - Logout
4. `test_delete_account.py` - Delete account
5. `test_signup.py` - Alternative signup flow

---

## 📸 Screenshot Examples

Screenshots are automatically captured during test execution:

```
screenshots/
├── authentication/
│   ├── 01_account_information.png
│   ├── 02_filled_form.png
│   ├── 03_account_created.png
│   └── login_success.png
├── cart/
│   ├── 01_products_page.png
│   ├── 02_cart_popup.png
│   ├── 03_cart_page.png
│   └── 07_checkout_page.png
├── product/
│   ├── 01_products_page.png
│   ├── 02_search_result.png
│   └── 03_product_detail.png
└── failed/
    └── [screenshots of failed tests]
```

**Automatic nested directories:** Test code can use `screenshot("authentication/login_success")` and directories are created automatically.

---

## 🔮 Future Improvements

### Testing Enhancements
- [ ] Add API testing layer for backend validation
- [ ] Implement visual regression testing
- [ ] Add performance testing and metrics
- [ ] Create cross-browser test matrix (Chrome, Firefox, Safari)

### Framework Enhancements
- [ ] Add test data builders for complex scenarios
- [ ] Implement custom logging and test diagnostics
- [ ] Add failure analysis and reporting dashboard
- [ ] Create test execution history tracking

### CI/CD Integration
- [ ] GitHub Actions workflow for automated test runs
- [ ] Parallel test execution configuration
- [ ] Slack notifications for test results
- [ ] Test result trending and analytics

---

## 📝 Test Statistics

| Category | Count | Status |
|----------|-------|--------|
| Authentication Tests | 5 | ✅ Passing |
| Product Tests | 3 | ✅ Passing |
| Cart Tests | 6 | ✅ Passing |
| Smoke Tests | 1 | ✅ Passing |
| **Total Tests** | **16** | **✅ All Passing** |

**Average Execution Time:** ~2.5 minutes for full suite

---

## 🤝 Contributing

When adding new tests:

1. Create test file in appropriate `tests/` subdirectory
2. Use existing page objects from `pages/`
3. Create new page objects if needed (inherit from BasePage)
4. Follow atomic action pattern (one action per method)
5. Use pytest markers (@pytest.mark.authentication, etc.)
6. Add descriptive assertions with meaningful messages
7. Run `pytest -v` to verify no regressions

---

## 📚 Key Concepts

### Atomic Actions
Each page object method performs a single, well-defined action:
- ❌ Bad: `def complete_registration()` (multiple actions)
- ✅ Good: `def enter_password()`, `def select_title()`, `def create_account()`

### Test Independence
- Tests use dynamically generated credentials (UUID-based emails)
- Runtime data stored in `runtime/` folder
- No test data pollution between runs

### Wait Strategy
- All interactions include explicit waits (timeout=10000ms)
- Uses Playwright's built-in timeout handling
- Avoids race conditions and flaky tests

---

## 👨‍💻 Author

Created as a university QA Automation project demonstrating modern testing best practices.

---

## 📄 License

This project is provided for educational purposes.

---

## 📞 Support

For questions or issues:
1. Check existing test examples in `tests/` folder
2. Review page object implementations in `pages/`
3. Consult `config/setting.py` for configuration options

---

**Last Updated:** 2026-07-03  
**Framework Version:** 1.0  
**Test Status:** ✅ All 16 tests passing
