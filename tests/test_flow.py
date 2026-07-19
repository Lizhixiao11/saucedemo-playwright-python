import pytest
from playwright.sync_api import expect

from config.config import Config
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_page import CheckoutPage


class TestFlow:
    PRODUCT_NAMES = ("Sauce Labs Bike Light", "Sauce Labs Backpack")
    PRODUCT_PRICES = ("$9.99", "$29.99")

    def test_flow_001(self, inventory_page):
        inventory_page.verify_inventory_page_loaded()
        all_product_names = inventory_page.get_all_product_names()
        assert inventory_page.get_cart_badge_count() == 0

        for product_name in self.PRODUCT_NAMES:
            inventory_page.add_to_cart(product_name)

        assert inventory_page.get_cart_badge_count() == 2
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)
        cart_page.verify_cart_page_loaded()
        expect(cart_page.page).to_have_url(f"{Config.BASE_URL}cart.html")
        assert cart_page.get_cart_item_count() == 2
        assert cart_page.get_all_product_names() == list(self.PRODUCT_NAMES)
        assert cart_page.get_all_prices() == list(self.PRODUCT_PRICES)

        cart_page.click_checkout()

        checkout_page = CheckoutPage(cart_page.page)
        checkout_page.verify_information_page_loaded()
        expect(checkout_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-one.html"
        )
        checkout_page.fill_checkout_information("John", "Doe", "12345")
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(checkout_page.page)
        overview_page.verify_overview_page_loaded()
        expect(overview_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-two.html"
        )
        assert overview_page.get_all_product_names() == list(self.PRODUCT_NAMES)
        assert overview_page.get_all_prices() == list(self.PRODUCT_PRICES)
        assert overview_page.get_item_total() == 39.98
        assert overview_page.get_tax() == 3.20
        assert overview_page.get_total() == 43.18

        overview_page.click_finish()

        complete_page = CheckoutCompletePage(overview_page.page)
        complete_page.verify_complete_page_loaded()
        expect(complete_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-complete.html"
        )
        expect(complete_page.complete_header).to_have_text(
            "Thank you for your order!"
        )
        assert complete_page.get_cart_badge_count() == 0

        complete_page.click_back_home()

        inventory_page.verify_inventory_page_loaded()
        expect(inventory_page.page).to_have_url(
            f"{Config.BASE_URL}inventory.html"
        )
        assert inventory_page.get_cart_badge_count() == 0
        for product_name in all_product_names:
            assert inventory_page.is_add_to_cart_button_visible(product_name)

    def test_flow_002(self, inventory_page):
        badge_counts = [inventory_page.get_cart_badge_count()]

        inventory_page.add_to_cart(self.PRODUCT_NAMES[0])
        badge_counts.append(inventory_page.get_cart_badge_count())

        inventory_page.add_to_cart(self.PRODUCT_NAMES[1])
        badge_counts.append(inventory_page.get_cart_badge_count())
        inventory_page.open_cart()

        cart_page = CartPage(inventory_page.page)
        cart_page.verify_cart_page_loaded()
        assert cart_page.get_cart_item_count() == 2
        badge_counts.append(cart_page.get_cart_badge_count())
        cart_page.click_checkout()

        checkout_page = CheckoutPage(cart_page.page)
        checkout_page.verify_information_page_loaded()
        badge_counts.append(checkout_page.get_cart_badge_count())
        checkout_page.fill_checkout_information("John", "Doe", "12345")
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(checkout_page.page)
        overview_page.verify_overview_page_loaded()
        expect(overview_page.cart_items).to_have_count(2)
        badge_counts.append(overview_page.get_cart_badge_count())
        overview_page.click_finish()

        complete_page = CheckoutCompletePage(overview_page.page)
        complete_page.verify_complete_page_loaded()
        badge_counts.append(complete_page.get_cart_badge_count())

        assert badge_counts == [0, 1, 2, 2, 2, 2, 0]

    def test_flow_008(self, inventory_page):
        inventory_price_map = dict(
            zip(
                inventory_page.get_all_product_names(),
                inventory_page.get_all_prices(),
            )
        )
        expected_prices = {
            product_name: inventory_price_map[product_name]
            for product_name in self.PRODUCT_NAMES
        }

        for product_name in self.PRODUCT_NAMES:
            inventory_page.add_to_cart(product_name)

        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.verify_cart_page_loaded()
        cart_price_map = dict(
            zip(cart_page.get_all_product_names(), cart_page.get_all_prices())
        )
        assert cart_price_map == expected_prices

        cart_page.click_checkout()
        checkout_page = CheckoutPage(cart_page.page)
        checkout_page.verify_information_page_loaded()
        checkout_page.fill_checkout_information("John", "Doe", "12345")
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(checkout_page.page)
        overview_page.verify_overview_page_loaded()
        overview_price_map = dict(
            zip(
                overview_page.get_all_product_names(),
                overview_page.get_all_prices(),
            )
        )
        assert overview_price_map == expected_prices

        expected_item_total = sum(
            float(price.lstrip("$")) for price in expected_prices.values()
        )
        item_total = overview_page.get_item_total()
        tax = overview_page.get_tax()
        total = overview_page.get_total()
        assert item_total == pytest.approx(expected_item_total)
        assert item_total == 39.98
        assert tax == 3.20
        assert total == pytest.approx(item_total + tax)
        assert total == 43.18
