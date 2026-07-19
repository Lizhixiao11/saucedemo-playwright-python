import pytest
from playwright.sync_api import expect

from config.config import Config
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


pytestmark = pytest.mark.regression


class TestCheckout:

    def _open_checkout(
        self,
        inventory_page,
        product_names=("Sauce Labs Bike Light",),
    ) -> CheckoutPage:
        for product_name in product_names:
            inventory_page.add_to_cart(product_name)

        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(inventory_page.page)
        checkout_page.verify_information_page_loaded()
        return checkout_page

    def test_chk_fn_001(self, inventory_page):
        """
        CHK-FN-001

        Verify submitting an empty checkout form requires First Name.
        """
        # Arrange
        checkout_page = self._open_checkout(inventory_page)

        # Act
        checkout_page.click_continue()

        # Assert
        expect(checkout_page.error_message).to_contain_text(
            "First Name is required"
        )
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )

    def test_chk_fn_002(self, inventory_page):
        """
        CHK-FN-002

        Verify First Name is required when other fields are populated.
        """
        # Arrange
        checkout_page = self._open_checkout(inventory_page)
        checkout_page.fill_checkout_information(
            last_name="Doe",
            postal_code="12345",
        )

        # Act
        checkout_page.click_continue()

        # Assert
        expect(checkout_page.error_message).to_contain_text(
            "First Name is required"
        )
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )

    def test_chk_fn_003(self, inventory_page):
        """
        CHK-FN-003

        Verify Last Name is required when other fields are populated.
        """
        # Arrange
        checkout_page = self._open_checkout(inventory_page)
        checkout_page.fill_checkout_information(
            first_name="John",
            postal_code="12345",
        )

        # Act
        checkout_page.click_continue()

        # Assert
        expect(checkout_page.error_message).to_contain_text(
            "Last Name is required"
        )
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )

    def test_chk_fn_004(self, inventory_page):
        """
        CHK-FN-004

        Verify Postal Code is required when name fields are populated.
        """
        # Arrange
        checkout_page = self._open_checkout(inventory_page)
        checkout_page.fill_checkout_information(
            first_name="John",
            last_name="Doe",
        )

        # Act
        checkout_page.click_continue()

        # Assert
        expect(checkout_page.error_message).to_contain_text(
            "Postal Code is required"
        )
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )

    def test_chk_fn_005(self, inventory_page):
        """
        CHK-FN-005

        Verify valid customer information opens the checkout overview.
        """
        # Arrange
        checkout_page = self._open_checkout(
            inventory_page,
            product_names=(
                "Sauce Labs Bike Light",
                "Sauce Labs Backpack",
            ),
        )
        checkout_page.fill_checkout_information(
            first_name="John",
            last_name="Doe",
            postal_code="12345",
        )

        # Act
        checkout_page.click_continue()

        # Assert
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-two.html"
        )
        expect(checkout_page.title).to_have_text("Checkout: Overview")

    def test_chk_fn_006(self, inventory_page):
        """
        CHK-FN-006

        Verify Cancel returns to the cart without changing cart state.
        """
        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        expected_badge_count = inventory_page.get_cart_badge_count()
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)
        expected_product_names = cart_page.get_all_product_names()
        cart_page.click_checkout()

        checkout_page = CheckoutPage(inventory_page.page)
        checkout_page.verify_information_page_loaded()

        # Act
        checkout_page.click_cancel()

        # Assert
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}cart.html"
        )
        cart_page.verify_cart_page_loaded()
        assert cart_page.get_all_product_names() == expected_product_names
        assert cart_page.get_cart_badge_count() == expected_badge_count
