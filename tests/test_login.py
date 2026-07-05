import pytest

from pages.login_page import LoginPage
from config.config import Config


class TestLogin:

    @pytest.mark.smoke
    def test_login_success(self, page):
        """
        Verify user can login successfully with valid credentials.
        """

        # Arrange
        login_page = LoginPage(page)
        login_page.open(Config.BASE_URL)

        # Act
        login_page.login(
            Config.USERNAME,
            Config.PASSWORD
        )

        # Assert
        login_page.should_have_url(
            "https://www.saucedemo.com/inventory.html"
        )