from pytest_bdd import scenarios, when, then, parsers

scenarios("features/login.feature")


@when("the user logs in with valid credentials")
def login_valid(login_page, users):
    login_page.login(**users["valid"])


@when(parsers.re(r'the user logs in with username "(?P<username>.*)" and password "(?P<password>.*)"'))
def login_with(login_page, username, password):
    login_page.login(username, password)


@then("the products page is displayed")
def products_displayed(inventory_page):
    assert inventory_page.title_text() == "Products"


@then(parsers.parse('the error message contains "{message}"'))
def error_contains(login_page, message):
    assert message in login_page.error_text()
