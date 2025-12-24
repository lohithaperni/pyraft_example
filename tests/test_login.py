import pytest

from pages.login_page import LoginPage


def test_valid_login_revalu(driver, base_url, login_users):
    """Test login with valid Revalu platform credentials"""
    valid = login_users["valid_user"]

    page = LoginPage(driver, base_url)
    page.open_login()
    page.login(valid["email"], valid["password"])

    assert page.is_logged_in(), "Login should be successful"

@pytest.mark.smoke
def test_invalid_login_revalu(driver, base_url, login_users):
    """Test login with invalid credentials"""
    invalid = login_users["invalid_user"]

    page = LoginPage(driver, base_url)
    page.open_login()
    page.login(invalid["email"], invalid["password"])

    # Should either stay on login page or show error
    error_text = page.get_error_text()
    # If still on login page, that's also a failure indicator
    assert not page.is_logged_in() or error_text != "", "Login should fail with invalid credentials"

