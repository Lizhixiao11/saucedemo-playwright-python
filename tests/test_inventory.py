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