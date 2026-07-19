import re

import pytest
from playwright.sync_api import expect

from config.config import Config
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = pytest.mark.regression

class TestInventory:

    def test_inv_ui_002(self, inventory_page):
        """
        INV-UI-002
        Verify Inventory page is displayed correctly after successful login.
        """

        inventory_page.verify_inventory_page_loaded()

        assert inventory_page.get_item_count() == 6
        expect(inventory_page.product_images).to_have_count(6)
        expect(inventory_page.product_links).to_have_count(6)
        expect(inventory_page.product_names).to_have_count(6)
        expect(inventory_page.product_descriptions).to_have_count(6)
        expect(inventory_page.product_prices).to_have_count(6)
        expect(inventory_page.add_to_cart_buttons).to_have_count(6)

        for index in range(6):
            product_image = inventory_page.product_images.nth(index)
            product_link = inventory_page.product_links.nth(index)
            product_name = inventory_page.product_names.nth(index)
            product_description = inventory_page.product_descriptions.nth(index)
            product_price = inventory_page.product_prices.nth(index)
            add_to_cart_button = inventory_page.add_to_cart_buttons.nth(index)

            expect(product_image).to_be_visible()
            expect(product_image).to_have_attribute("src", re.compile(r".+"))
            expect(product_link).to_be_visible()
            expect(product_link).to_be_enabled()
            expect(product_link).to_have_attribute("href", "#")
            expect(product_name).to_be_visible()
            assert product_name.inner_text().strip()
            expect(product_description).to_be_visible()
            assert product_description.inner_text().strip()
            expect(product_price).to_be_visible()
            assert re.fullmatch(r"\$\d+\.\d{2}", product_price.inner_text())
            expect(add_to_cart_button).to_be_visible()
            expect(add_to_cart_button).to_be_enabled()
            expect(add_to_cart_button).to_have_text("Add to cart")

    def test_inv_fn_001(self, inventory_page):
        """
        INV-FN-001
        Verify user can add a product to the cart.
        """

        # Act
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        # Assert
        assert inventory_page.is_remove_button_visible(
            "Sauce Labs Bike Light"
        )
        assert inventory_page.get_cart_badge_count() == 1

    def test_inv_fn_002(self, inventory_page):
        """
        INV-FN-002

        Verify multiple products can be added into cart.
        """

        # Step 1
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        # Step 2
        inventory_page.add_to_cart("Sauce Labs Backpack")

        # Expected 1
        assert inventory_page.is_remove_button_visible(
            "Sauce Labs Bike Light"
        )

        assert inventory_page.is_remove_button_visible(
            "Sauce Labs Backpack"
        )

        # Expected 2
        assert inventory_page.get_cart_badge_count() == 2

    def test_inv_fn_003(self, inventory_page):
        """
        INV-FN-003

        Verify product can be removed from inventory page.
        """

        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")

        assert inventory_page.get_cart_badge_count() == 1

        # Act
        inventory_page.remove_from_cart("Sauce Labs Bike Light")

        # Expected 1
        assert inventory_page.is_add_to_cart_button_visible(
            "Sauce Labs Bike Light"
        )

        # Expected 2
        assert inventory_page.get_cart_badge_count() == 0


    def test_inv_fn_010(self, inventory_page):
        """
        INV-FN-010

        Verify user can navigate to Cart page by clicking cart icon.
        """

        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        badge_count = inventory_page.get_cart_badge_count()
        assert badge_count == 1

        # Act
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)

        # Assert
        cart_page.verify_cart_page_loaded()
        expect(inventory_page.page).to_have_url(f"{Config.BASE_URL}cart.html")
        assert cart_page.get_all_product_names() == [
            "Sauce Labs Bike Light"
        ]
        assert cart_page.get_cart_item_count() == badge_count
