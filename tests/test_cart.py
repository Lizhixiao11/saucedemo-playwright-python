from pages.cart_page import CartPage


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
        assert cart_page.get_remove_button_count() == 2