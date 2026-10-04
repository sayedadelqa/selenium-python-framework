import pytest
from utils.config import load_json

INVALID = load_json("users.json")["invalid_logins"]


@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login(login_page, inventory_page, users):
    login_page.load()
    login_page.login(**users["valid"])
    assert inventory_page.title_text() == "Products"


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("case", INVALID, ids=["locked-out-user", "wrong-password", "empty-username", "empty-password"])
def test_invalid_login(login_page, case):
    login_page.load()
    login_page.login(case["username"], case["password"])
    assert case["error"] in login_page.error_text()
