from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import Config


class TestCart:

    def test_cart_ui_002(self, inventory_page):
        """
        CART-UI-002

        Verify cart item information is displayed correctly.
        """

        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)

        # Verify page
        cart_page.verify_cart_page_loaded()

        # Expected 1
        assert cart_page.get_all_quantities() == ["1", "1"]

        # Expected 2
        assert cart_page.get_all_product_names() == [
            "Sauce Labs Bike Light",
            "Sauce Labs Backpack",
        ]

        expect(cart_page.product_links).to_have_count(2)

        for index in range(2):
            product_link = cart_page.product_links.nth(index)
            expect(product_link).to_be_visible()
            expect(product_link).to_be_enabled()
            expect(product_link).to_have_attribute("href", "#")
            expect(cart_page.product_names.nth(index)).to_have_css(
                "color",
                "rgb(24, 88, 58)",
            )

        # Expected 3
        assert cart_page.get_all_prices() == [
            "$9.99",
            "$29.99",
        ]

        assert cart_page.get_all_descriptions() == [
            "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
            "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
        ]

        # Expected 4
        expect(cart_page.remove_buttons).to_have_count(2)
        expect(cart_page.remove_buttons).to_have_text(["Remove", "Remove"])

        for remove_button in cart_page.remove_buttons.all():
            expect(remove_button).to_have_css(
                "border-color",
                "rgb(226, 35, 26)",
            )
            expect(remove_button).to_have_css("border-style", "solid")

    def test_cart_ui_004(self, page):
        """
        CART-UI-004

        Verify the cart badge count matches the number of items in the cart.
        """
        login = LoginPage(page)
        inventory = InventoryPage(page)
        cart = CartPage(page)

        # Arrange
        login.open(Config.BASE_URL)
        login.login_as_standard_user()

        inventory.add_to_cart("Sauce Labs Bike Light")
        inventory.add_to_cart("Sauce Labs Backpack")

        badge_count = inventory.get_cart_badge_count()

        # Act
        inventory.open_cart()

        cart.verify_cart_page_loaded()

        cart_count = cart.get_cart_item_count()

        # Assert
        assert badge_count == 2
        assert cart_count == 2
        assert badge_count == cart_count

    def test_cart_fn_001(self, inventory_page):
        """
        CART-FN-001

        Verify cart product data matches the inventory page.
        """
        # Arrange
        expected_product_names = [
            "Sauce Labs Bike Light",
            "Sauce Labs Backpack",
        ]

        inventory_product_data = {
            name: (description, price)
            for name, description, price in zip(
                inventory_page.get_all_product_names(),
                inventory_page.get_all_descriptions(),
                inventory_page.get_all_prices(),
            )
        }

        for product_name in expected_product_names:
            inventory_page.add_to_cart(product_name)

        # Act
        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)

        # Assert
        cart_product_names = cart_page.get_all_product_names()
        cart_descriptions = cart_page.get_all_descriptions()
        cart_prices = cart_page.get_all_prices()

        assert cart_product_names == expected_product_names

        for index, product_name in enumerate(cart_product_names):
            expected_description, expected_price = inventory_product_data[
                product_name
            ]
            assert cart_descriptions[index] == expected_description
            assert cart_prices[index] == expected_price

    def test_cart_fn_002(self, inventory_page):
        """
        CART-FN-002

        Verify one product can be removed from the cart.
        """
        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        inventory_page.add_to_cart("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)

        # Act
        cart_page.remove_product("Sauce Labs Bike Light")

        # Assert
        assert not cart_page.is_product_in_cart("Sauce Labs Bike Light")
        assert cart_page.get_all_product_names() == [
            "Sauce Labs Backpack"
        ]
        assert cart_page.get_cart_item_count() == 1
        assert cart_page.get_cart_badge_count() == 1

    def test_cart_fn_005(self, inventory_page):
        """
        CART-FN-005

        Verify Continue Shopping returns to the inventory page without
        changing cart state.
        """
        # Arrange
        product_name = "Sauce Labs Bike Light"
        inventory_page.add_to_cart(product_name)
        expected_badge_count = inventory_page.get_cart_badge_count()
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)

        # Act
        cart_page.click_continue_shopping()

        # Assert
        inventory_page.verify_inventory_page_loaded()
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}inventory.html"
        )
        assert inventory_page.is_remove_button_visible(product_name)
        assert inventory_page.get_cart_badge_count() == expected_badge_count

    def test_cart_fn_006(self, inventory_page):
        """
        CART-FN-006

        Verify Checkout opens the customer information form when the cart
        contains a product.
        """
        # Arrange
        inventory_page.add_to_cart("Sauce Labs Bike Light")
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)

        # Act
        cart_page.click_checkout()

        # Assert
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )
        expect(inventory_page.page.locator(".title")).to_have_text(
            "Checkout: Your Information"
        )
        expect(
            inventory_page.page.locator('[data-test="firstName"]')
        ).to_be_visible()
        expect(
            inventory_page.page.locator('[data-test="lastName"]')
        ).to_be_visible()
        expect(
            inventory_page.page.locator('[data-test="postalCode"]')
        ).to_be_visible()
