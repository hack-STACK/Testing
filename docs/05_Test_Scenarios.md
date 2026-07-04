# Test Scenarios

## Professional Test Scenario Management

Test scenarios document the "what" and "why" of test execution. This document provides a comprehensive test scenario matrix for the Automation Exercise Testing Framework, traceable to source test files and organized by feature and priority.

---

## Test Scenario Matrix

### Format

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|

### Legend

**Automation Status:**
- ✓ Fully Automated
- ◐ Partially Automated
- ✗ Manual Only
- ⚠ Pending

**Priority:**
- P0 (Critical): Core functionality, affects users immediately
- P1 (High): Important feature, used regularly
- P2 (Medium): Non-critical, used occasionally
- P3 (Low): Enhancement, rarely used

---

## Authentication Module

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|
| AUTH-001 | User Registration | User registers with valid name and email | Account created successfully, user logged in, confirmation message displayed | ✓ Fully Automated | P0 | tests/authentication/test_register.py |
| AUTH-002 | User Registration | User fills all account information (title, password, DOB, address) | All data saved to account, address displayed in profile | ✓ Fully Automated | P0 | tests/authentication/test_register.py |
| AUTH-003 | User Login | Registered user logs in with correct email and password | User authenticated, dashboard displayed, session established | ✓ Fully Automated | P0 | tests/authentication/test_login.py |
| AUTH-004 | User Login | Multiple login attempts with various credentials | Each valid credential set authenticates correctly | ✓ Fully Automated | P1 | tests/authentication/test_login.py |
| AUTH-005 | User Session | Logged-in user clicks logout | Session terminated, redirected to login page, authentication removed | ✓ Fully Automated | P0 | tests/authentication/test_logout.py |
| AUTH-006 | User Session | User remains logged in after navigation | Session persists across page navigation, user name displayed in header | ✓ Fully Automated | P1 | tests/authentication/test_logout.py |
| AUTH-007 | Account Management | Logged-in user deletes account | Account deleted from system, user logged out, account recovery available | ✓ Fully Automated | P1 | tests/authentication/test_delete_account.py |
| AUTH-008 | Account Management | Deleted user cannot login with deleted credentials | Login fails with appropriate error message | ✗ Not tested | P2 | (Not implemented) |
| AUTH-009 | Signup Process | New user signs up without creating account | Signup form submitted, account information page displayed | ✓ Fully Automated | P1 | tests/authentication/test_signup.py |
| AUTH-010 | Email Validation | Email addresses are unique per user | Registration with duplicate email prevented or handled | ✗ Not tested | P2 | (Not implemented) |

### Authentication Module Analysis

**Coverage:** 8 scenarios fully automated, 2 not tested

**Critical Path Validated:**
- Registration workflow (AUTH-001, AUTH-002)
- Login authentication (AUTH-003, AUTH-004)
- Session management (AUTH-005, AUTH-006)
- Account deletion (AUTH-007)

**Gaps:**
- Invalid input handling (wrong password, invalid email)
- Duplicate account prevention
- Password reset workflow
- Account recovery

---

## Product Module

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|
| PROD-001 | Product Browsing | User views product listings | All products displayed with images, names, prices | ✓ Fully Automated | P0 | tests/product/test_view_product.py |
| PROD-002 | Product Browsing | User clicks on product to view details | Product details page displayed with full information | ✓ Fully Automated | P0 | tests/product/test_view_product.py |
| PROD-003 | Product Browsing | Products displayed with correct information | Product name, description, price, images visible | ✓ Fully Automated | P1 | tests/product/test_view_product.py |
| PROD-004 | Product Search | User searches for product by keyword | Search results display matching products | ✓ Fully Automated | P0 | tests/product/test_search_product.py |
| PROD-005 | Product Search | Search query returns relevant products | Products matching search term displayed | ✓ Fully Automated | P1 | tests/product/test_search_product.py |
| PROD-006 | Product Search | Empty search result | Results page displayed appropriately | ✗ Not tested | P2 | (Not implemented) |
| PROD-007 | Product Filtering | User filters products by category | Category filter applied, only matching products shown | ✗ Not tested | P2 | (Not implemented) |
| PROD-008 | Product Details | Product information is accurate | Price, availability, description match catalog | ✓ Fully Automated | P1 | tests/product/test_view_product.py |

### Product Module Analysis

**Coverage:** 6 scenarios fully automated, 2 not tested

**Critical Path Validated:**
- Product browsing (PROD-001, PROD-002, PROD-003)
- Product search (PROD-004, PROD-005)
- Product information accuracy (PROD-008)

**Gaps:**
- Empty search results handling
- Category filtering
- Product comparison
- Stock availability checking

---

## Shopping Cart Module

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|
| CART-001 | Add to Cart | User adds single product to empty cart | Product added, cart count = 1, product visible in cart | ✓ Fully Automated | P0 | tests/product/test_add_to_cart.py |
| CART-002 | Add to Cart | User adds multiple different products | All products added, cart count = 3, quantities correct | ✓ Fully Automated | P0 | tests/cart/test_multiple_products.py |
| CART-003 | Add to Cart | Adding duplicate product increases quantity | Item quantity incremented, total updated | ✗ Not tested | P1 | (Not implemented) |
| CART-004 | View Cart | User views cart contents | All added products displayed with quantities and prices | ✓ Fully Automated | P0 | tests/cart/test_view_cart.py |
| CART-005 | View Cart | Cart displays accurate totals | Subtotal, tax (if applicable), total calculated correctly | ✓ Fully Automated | P1 | tests/cart/test_verify_cart_information.py |
| CART-006 | Remove from Cart | User removes product from cart | Product removed, cart updated, count decremented | ✓ Fully Automated | P0 | tests/cart/test_remove_product.py |
| CART-007 | Remove from Cart | Removing last product empties cart | Cart becomes empty, empty state message displayed | ✗ Not tested | P2 | (Not implemented) |
| CART-008 | Continue Shopping | User continues shopping from cart | Navigation to products maintained, new items can be added | ✓ Fully Automated | P1 | tests/cart/test_continue_shopping.py |
| CART-009 | Cart Verification | Cart information is accurate | Quantities, prices, subtotals match product information | ✓ Fully Automated | P0 | tests/cart/test_verify_cart_information.py |
| CART-010 | Cart Persistence | Cart persists after logout and re-login | Cart contents preserved after session ends and new session begins | ✗ Not tested | P2 | (Not implemented) |
| CART-011 | Quantity Management | User adjusts product quantity | Quantity changes, totals update accordingly | ✗ Not tested | P1 | (Not implemented) |

### Shopping Cart Module Analysis

**Coverage:** 6 scenarios fully automated, 5 not tested

**Critical Path Validated:**
- Add to cart single/multiple (CART-001, CART-002)
- View cart (CART-004, CART-005)
- Remove from cart (CART-006)
- Continue shopping (CART-008)
- Cart verification (CART-009)

**Gaps:**
- Duplicate product handling (quantity increment)
- Empty cart state
- Cart persistence across sessions
- Quantity adjustment
- Stock depletion scenarios

---

## Checkout Module

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|
| CHKOUT-001 | Checkout Process | User proceeds to checkout from cart | Checkout page displayed, items summary shown, payment form accessible | ✓ Fully Automated | P0 | tests/cart/test_proceed_to_checkout.py |
| CHKOUT-002 | Address Information | Checkout displays user's saved address | Address from registration shown as default | ✗ Not tested | P1 | (Not implemented) |
| CHKOUT-003 | Shipping Options | User selects shipping method | Shipping option selected, delivery date estimated | ✗ Not tested | P1 | (Not implemented) |
| CHKOUT-004 | Payment Information | User enters payment details | Payment information validated, card accepted | ✗ Not tested | P0 | (Not implemented) |
| CHKOUT-005 | Order Confirmation | Order confirmed and placed | Order number generated, confirmation email sent, order visible in history | ✗ Not tested | P0 | (Not implemented) |
| CHKOUT-006 | Order Summary | Final order summary before payment | Items, quantities, shipping, total all correct | ✗ Not tested | P1 | (Not implemented) |

### Checkout Module Analysis

**Coverage:** 1 scenario fully automated, 5 not tested

**Critical Path Validated:**
- Proceed to checkout (CHKOUT-001)

**Major Gaps:**
- Full checkout workflow not implemented
- Payment processing
- Order confirmation
- Address validation
- Shipping selection

**Note:** Checkout module partially implemented; full workflow testing pending

---

## Smoke and Sanity Tests

| Test ID | Feature | Scenario | Expected Result | Automation Status | Priority | Source Test File |
|---------|---------|----------|-----------------|------------------|----------|------------------|
| SMOKE-001 | Site Accessibility | Application home page loads | Home page displays without errors, navigation visible | ✓ Fully Automated | P0 | tests/smoke/test_home.py |
| SMOKE-002 | Site Navigation | Basic site navigation functions | Navigation menu accessible, links functional | ✓ Fully Automated | P0 | tests/test_open.py |
| SMOKE-003 | Application Health | Application responds to requests | No 500 errors, page load times acceptable | ✓ Fully Automated | P0 | tests/test_open.py |
| SMOKE-004 | Browser Compatibility | Application functions in Edge browser | All features work in Chromium-based Edge | ✓ Fully Automated | P1 | All tests |

### Smoke Test Analysis

**Coverage:** 4 scenarios fully automated

**Purpose:** Rapid validation that application is functional for further testing

**Scope:** Basic sanity checks only; detailed testing in feature modules

---

## Test Scenario Summary

### Total Test Coverage

| Module | Total Scenarios | Automated | Not Tested | Coverage % |
|--------|-----------------|-----------|---------|-----------|
| Authentication | 10 | 8 | 2 | 80% |
| Product | 8 | 6 | 2 | 75% |
| Shopping Cart | 11 | 6 | 5 | 55% |
| Checkout | 6 | 1 | 5 | 17% |
| Smoke Tests | 4 | 4 | 0 | 100% |
| **Total** | **39** | **25** | **14** | **64%** |

### Test Distribution by Priority

| Priority | Count | Percentage | Status |
|----------|-------|-----------|--------|
| P0 (Critical) | 15 | 38% | Mostly automated (12/15) |
| P1 (High) | 16 | 41% | Partially automated (11/16) |
| P2 (Medium) | 8 | 21% | Mostly not tested (2/8) |
| **Total** | **39** | **100%** | **64% automated** |

### Test Distribution by Type

| Type | Count | Percentage |
|------|-------|-----------|
| Happy Path (Success) | 22 | 56% |
| Alternative Path | 9 | 23% |
| Error/Edge Case | 8 | 21% |

---

## Automation Recommendations

### Immediate (High Priority)

**Complete P0 Scenarios:**
1. AUTH-008: Failed login handling
2. CART-003: Duplicate product handling
3. CHKOUT-002: Address display in checkout
4. CHKOUT-004: Payment processing

**Complete High-Impact P1 Scenarios:**
1. PROD-007: Category filtering
2. CART-011: Quantity adjustment
3. CHKOUT-002: Shipping options

### Medium-term

**Expand Alternative Paths:**
1. Empty search results (PROD-006)
2. Empty cart state (CART-007)
3. Order confirmation (CHKOUT-005)

**Add Error Scenarios:**
1. Invalid payment (Payment decline)
2. Out of stock (Product unavailable)
3. Checkout failure recovery

### Long-term

**Advanced Scenarios:**
1. Multi-user concurrent shopping
2. Cart persistence across devices
3. Wishlist and save-for-later features
4. Promotional code application

---

## Test Scenario Traceability

### Source Test File Mapping

```
tests/authentication/
    test_register.py       → AUTH-001, AUTH-002, AUTH-010
    test_login.py          → AUTH-003, AUTH-004
    test_logout.py         → AUTH-005, AUTH-006
    test_delete_account.py → AUTH-007, AUTH-008
    test_signup.py         → AUTH-009

tests/product/
    test_view_product.py   → PROD-001, PROD-002, PROD-003, PROD-008
    test_search_product.py → PROD-004, PROD-005, PROD-006, PROD-007

tests/cart/
    test_add_to_cart.py           → CART-001
    test_multiple_products.py     → CART-002, CART-003, CART-011
    test_view_cart.py             → CART-004
    test_verify_cart_information.py → CART-005, CART-009
    test_remove_product.py        → CART-006, CART-007
    test_continue_shopping.py     → CART-008
    test_proceed_to_checkout.py   → CHKOUT-001, CHKOUT-006

tests/smoke/
    test_home.py → SMOKE-001
    test_open.py → SMOKE-002, SMOKE-003
```

---

## Test Execution Guidelines

### Sequential Execution (Current Implementation)

```bash
# Run all tests
pytest tests/ -v

# Run by module
pytest tests/authentication/ -v      # Authentication module
pytest tests/product/ -v             # Product module
pytest tests/cart/ -v                # Cart module
pytest tests/smoke/ -v               # Smoke tests

# Run by marker
pytest -m authentication -v
pytest -m product -v
pytest -m smoke -v
```

### Parallel Execution (Future Implementation)

```bash
# Run 4 tests in parallel
pytest tests/ -n 4

# Run with better failure output
pytest tests/ -n 4 --dist=loadscope
```

### Continuous Integration

```bash
# Full regression suite
pytest tests/ -v --tb=short

# With HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html

# With video recording
# Videos automatically recorded in videos/ directory
```

---

## Conclusion

This test scenario matrix provides comprehensive coverage of the Automation Exercise Testing Framework's test cases. It documents:

- **25 automated scenarios** covering critical functionality
- **14 pending scenarios** representing gaps and future work
- **64% coverage** of defined test scenarios
- **P0 and P1 priorities** mostly covered, P2 expansion pending

The framework successfully validates core e-commerce workflows (authentication, product browsing, shopping cart) with room for expansion into advanced features (checkout, payments, edge cases).

Continuous maintenance and expansion of this test scenario matrix ensures ongoing alignment between business requirements, test implementation, and automation coverage.
