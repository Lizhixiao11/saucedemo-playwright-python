# SauceDemo UI Automation

## Project overview

This repository is a Python UI automation project for
[SauceDemo](https://www.saucedemo.com/). It demonstrates a maintainable
pytest and Playwright test framework organized with the Page Object Model and
driven by manual business cases maintained in Excel.

## Technology stack

- Python 3.12.10
- pytest 9.1.1
- Playwright for Python 1.61.0 using the synchronous API
- pytest-playwright 0.8.0
- pytest-html 4.2.0
- Page Object Model
- Excel-based manual test cases
- Git

Python 3.12.10 is the currently verified and supported project runtime.

## Project structure

```text
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
    regression_report.html
    screenshots/
```

## P0 coverage

The regression suite automates all 28 P0 Excel business cases:

| Area | P0 cases |
|---|---:|
| Inventory | 5 |
| Cart | 6 |
| Checkout Information | 6 |
| Checkout Overview | 8 |
| End-to-end Flow | 3 |
| Total | 28 |

The framework smoke login test is intentionally separate from the Excel
business-test count.

## Test design

- Each Excel business case maps to one automated test.
- Business test names follow their Excel Case IDs.
- Framework verification tests remain separate from business regression tests.
- Page Objects encapsulate page locators and reusable interactions only.
- Business assertions remain visible in the test cases.

## Installation

Create and activate a Python 3.12.10 virtual environment:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Playwright browser installation

Install the Chromium browser used by the default configuration:

```powershell
python -m playwright install chromium
```

## Configuration

Runtime settings are defined in `config/config.py`:

- `BASE_URL`: SauceDemo URL
- `BROWSER`: Playwright browser engine
- `HEADLESS`: headed or headless execution
- `SLOW_MO`: delay between browser actions in milliseconds
- `TIMEOUT`: default Playwright timeout in milliseconds
- `USERNAME` and `PASSWORD`: SauceDemo standard-user credentials
- `REPORT_DIR` and `SCREENSHOT_DIR`: report output locations

## Execution commands

Run the full suite:

```powershell
python -m pytest
```

Run the framework smoke test:

```powershell
python -m pytest -m smoke
```

Run all Excel P0 business tests:

```powershell
python -m pytest -m regression
```

Run one functional module:

```powershell
python -m pytest tests/test_inventory.py
python -m pytest tests/test_cart.py
python -m pytest tests/test_checkout.py
python -m pytest tests/test_checkout_overview.py
python -m pytest tests/test_flow.py
```

## Marker usage

- `smoke`: framework verification tests required by the business-test setup.
- `regression`: Excel-based P0 business tests.

The marker definitions are maintained in `pytest.ini`.

## Report location

Runtime artifacts belong under `reports/`:

- `reports/screenshots/` for screenshots
- `reports/regression_report.html` for the self-contained regression report

Generate the regression HTML report:

```powershell
pytest -m regression --html=reports/regression_report.html --self-contained-html
```

Generated report content is excluded from Git.

## Known requirement discrepancy

| Case ID | Excel requirement | Actual SauceDemo behavior | Automation result |
|---|---|---|---|
| OVR-FN-006 | Cancel from Checkout Overview navigates to `cart.html` | Cancel navigates to `inventory.html` | Intentional failure |

The `OVR-FN-006` assertion is preserved because the Excel workbook is the
source of truth. This is a known requirement/application discrepancy, not an
unstable automation failure. The regression and full-suite commands currently
return a non-zero result because this test intentionally remains failed.

## Future improvements

- Add GitHub Actions CI for automated test execution.
- Support environment-variable configuration for runtime settings.
- Evaluate parallel execution for faster regression feedback.
- Evaluate Allure reporting for richer result analysis.
