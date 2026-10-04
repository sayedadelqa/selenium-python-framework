# Selenium Python Test Automation Framework

![CI](https://github.com/sayedadelqa/selenium-python-framework/actions/workflows/ci.yml/badge.svg)

UI and API test automation framework built with **Selenium 4, Python and Pytest**, using the Page Object Model, explicit waits, **BDD scenarios in Gherkin (pytest-bdd)** and a GitHub Actions CI pipeline.

## What it tests
- **UI** ([saucedemo.com](https://www.saucedemo.com), a public practice site): login (valid and invalid), cart, sorting, checkout.
- **API** ([dummyjson.com](https://dummyjson.com), a public practice API): GET, POST, PUT, DELETE, status codes and response fields.

## Project structure
```
pages/        Page Objects (one class per page, locators + actions, explicit waits in BasePage)
tests/ui/     UI tests
tests/api/    API tests
tests/bdd/    BDD tests: features/ (Gherkin .feature files) and step definitions
api/          API client wrapper around requests
data/         Test data in JSON (no data inside test code)
utils/        Config and helpers
conftest.py   Browser fixture, page fixtures, screenshot-on-failure hook
pytest.ini    Pytest settings and markers
reports/      HTML report (generated)
.github/workflows/ci.yml   CI pipeline
```

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
pytest
```
Selenium 4 downloads the matching browser driver automatically (Selenium Manager). Google Chrome must be installed.

Useful commands:
```bash
pytest -m smoke                 # critical flows only
pytest -m api                   # API tests only
pytest -m bdd                   # BDD scenarios only
pytest --headless               # run without a browser window (used in CI)
pytest --browser-name firefox   # chrome (default), firefox or edge
```

Report: `reports/report.html`. A screenshot is embedded in the report for every failed UI test.

## Design decisions
- **Page Object Model**: locators and page actions live in `pages/`, so UI changes are fixed in one place.
- **Explicit waits only**: `WebDriverWait` with expected conditions in `BasePage`, never `time.sleep()`, to reduce flaky tests.
- **Data-driven**: test data in `data/users.json`, and invalid logins run as parameterized tests.
- **Markers**: `smoke` and `regression` let CI or developers run only what they need.
- **BDD on top of the same layers**: feature files describe behaviour, steps only call Page Objects, and Page Objects own the locators.
- **CI**: every push runs the full suite on GitHub Actions and uploads the report.

See [TEST_STRATEGY.md](TEST_STRATEGY.md) for scope, risks and priorities.
