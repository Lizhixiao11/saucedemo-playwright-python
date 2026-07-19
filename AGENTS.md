# AGENTS.md

## Project Overview

This repository is a personal UI automation testing project for https://www.saucedemo.com/.

The purpose of this project is to demonstrate professional Python UI automation skills using:

- Python
- pytest
- Playwright (synchronous API)
- Page Object Model (POM)
- Excel manual test cases

The goal is to build a clean, maintainable, and production-style automation project.

---

## Project Structure

The project structure must remain consistent.

config/
    config.py

pages/
    login_page.py
    inventory_page.py
    cart_page.py
    checkout_page.py
    checkout_overview_page.py
    checkout_complete_page.py

tests/
    conftest.py
    test_login.py
    test_inventory.py
    test_cart.py
    test_checkout.py
    test_checkout_overview.py
    test_flow.py

test_data/
    Saucedemo Test Case.xlsx

reports/

Do not create duplicate folders or reorganize the project unless explicitly requested.

---

## Framework Rules

Always use:

- Python
- pytest
- Playwright synchronous API

Never introduce:

- Selenium
- unittest
- async Playwright
- Robot Framework
- Behave
- Cypress
- JavaScript
- Java

Use the existing fixtures in tests/conftest.py.

Do not replace the current framework.

---

## Page Object Model Rules

Follow the existing Page Object Model.

Each Page Object should contain:

- Locators
- Reusable page actions
- Reusable page verification methods
- Data retrieval methods

Do not place repeated locators inside test functions.

If a locator already exists inside a Page Object, always reuse it.

Only add new page methods when they will be reused or improve readability.

Do not duplicate existing methods.

---

## Locator Rules

Always prefer stable locators.

Priority:

1. data-test
2. id
3. name
4. stable CSS locator

Avoid XPath unless there is no reasonable alternative.

Avoid text-based locators when a stable data-test locator already exists.

---

## Test Case Source

The Excel file is the source of truth.

Every automated test must correspond to exactly one manual test case.

Do not combine multiple Excel cases into one test.

Before implementing a test:

- Read the corresponding Excel row.
- Understand Preconditions.
- Understand Test Steps.
- Understand Expected Result.

Do not guess missing requirements.

If the Excel case is ambiguous, ask before implementing.

## Framework Verification Tests

Some automated tests exist to verify the automation framework itself rather than business requirements from the Excel test case list.

These tests do not require a corresponding Excel case ID.

Examples:

- successful login verification
- browser/page fixture validation
- basic navigation verification
- environment validation

Framework verification tests should:

- be clearly separated from Excel-based business tests
- not be counted as business test coverage
- follow the same coding style and quality standards
- avoid affecting the traceability of Excel test automation

When modifying these tests, do not create artificial Excel test cases to match them.
---

## Naming Convention

Test file names:

test_login.py
test_inventory.py
test_cart.py
test_checkout.py

Test function names must use the Excel Case ID.

Examples:

test_login_fn_001
test_inv_ui_002
test_cart_ui_004
test_checkout_fn_001

Do not invent different naming styles.

Framework verification tests may use descriptive names instead of Excel Case IDs.

Example:

test_login_success

---

## Test Style

Each test should follow Arrange → Act → Assert.

Tests should be easy to read.

Avoid unnecessary comments.

Keep each test focused on a single business scenario.

Do not place business logic inside Page Objects.

Business assertions should remain inside test functions whenever practical.

---

## Assertions

Prefer Playwright assertions whenever possible.

Examples:

expect(locator).to_be_visible()

expect(locator).to_have_text(...)

expect(locator).to_have_count(...)

For Python assertions, include clear assertion messages when useful.

Avoid weak assertions.

Every assertion should verify business behavior rather than implementation details.

---

## Waiting Strategy

Use Playwright's built-in waiting.

Never use:

time.sleep()

Do not add arbitrary waits.

---

## Code Reuse

Before creating a new method:

1. Check whether a similar method already exists.
2. Reuse existing methods whenever possible.
3. Extend existing methods instead of duplicating code.

Avoid copy-and-paste implementations.

---

## Refactoring Rules

Do not perform large refactors while implementing a test case.

Do not rename files.

Do not change project structure.

Do not modify existing working tests unless necessary.

If a refactor affects multiple files, explain why before making the change.

---

## Running Tests

After implementing a test:

1. Run the new test only.
2. If it passes, run the related test module.
3. Do not automatically run the entire test suite unless requested.

Prefer:

python -m pytest tests/test_cart.py::test_cart_ui_004 -v

instead of immediately running all tests.

---

## Reporting

After completing a task, always provide:

1. Files modified.
2. Methods added or changed.
3. Short implementation summary.
4. Test command executed.
5. Test result.
6. Any assumptions made.

Keep reports concise.

---

## Safety Rules

Do not install new packages unless requested.

Do not modify configuration files unless required.

Do not change fixtures without approval.

Do not delete existing code unless necessary.

Do not change passing tests to satisfy another test.

If uncertain, stop and ask.

---

## Coding Style

Follow the existing coding style in this repository.

Use descriptive method names.

Keep methods short.

Keep responsibilities clear.

Use type hints when appropriate.

Avoid unnecessary abstraction.

Avoid over-engineering.

Write code that is easy for another automation engineer to maintain.

---

## Goal

The priority is correctness, readability, maintainability, and consistency.

Always preserve the existing architecture.

Implement one test case at a time.

Make the smallest reasonable change required to satisfy the current test case.
