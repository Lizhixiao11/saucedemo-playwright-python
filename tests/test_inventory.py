from pages.inventory_page import InventoryPage


class TestInventory:

    def test_inv_ui_002(self, inventory_page):
        """
        INV-UI-002
        Verify Inventory page is displayed correctly after successful login.
        """

        inventory_page.verify_inventory_page_loaded()

        assert inventory_page.get_item_count() == 6

    def test_inv_fn_001(self, inventory_page):
        """
        INV-FN-001
        Verify user can add a product to the cart.
        """

        # Act
        inventory_page.add_to_cart("Sauce Labs Backpack")

        # Assert
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