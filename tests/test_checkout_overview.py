import pytest
from playwright.sync_api import expect

from config.config import Config
from pages.cart_page import CartPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_page import CheckoutPage


pytestmark = pytest.mark.regression


class TestCheckoutOverview:
    PRODUCT_NAMES = ("Sauce Labs Bike Light", "Sauce Labs Backpack")
    PRODUCT_PRICES = ("$9.99", "$29.99")

    def _open_overview(self, inventory_page) -> CheckoutOverviewPage:
        for product_name in self.PRODUCT_NAMES:
            inventory_page.add_to_cart(product_name)

        inventory_page.open_cart()
        cart_page = CartPage(inventory_page.page)
        cart_page.verify_cart_page_loaded()
        cart_page.click_checkout()

        checkout_page = CheckoutPage(inventory_page.page)
        checkout_page.verify_information_page_loaded()
        checkout_page.fill_checkout_information("John", "Doe", "12345")
        checkout_page.click_continue()

        overview_page = CheckoutOverviewPage(inventory_page.page)
        overview_page.verify_overview_page_loaded()
        return overview_page

    def test_ovr_ui_001(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        expect(overview_page.title).to_have_text("Checkout: Overview")
        expect(overview_page.quantity_label).to_have_text("QTY")
        expect(overview_page.description_label).to_have_text("Description")
        expect(overview_page.cart_items).to_have_count(2)
        assert overview_page.get_all_product_names() == list(self.PRODUCT_NAMES)
        assert overview_page.get_all_prices() == list(self.PRODUCT_PRICES)
        expect(overview_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-step-two.html"
        )

    def test_ovr_ui_003(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        expect(overview_page.item_total_label).to_have_text("Item total: $39.98")
        expect(overview_page.tax_label).to_be_visible()
        expect(overview_page.total_label).to_be_visible()
        item_total_box = overview_page.item_total_label.bounding_box()
        tax_box = overview_page.tax_label.bounding_box()
        total_box = overview_page.total_label.bounding_box()
        assert item_total_box and tax_box and total_box
        assert tax_box["x"] == pytest.approx(item_total_box["x"])
        assert total_box["x"] == pytest.approx(item_total_box["x"])

    def test_ovr_fn_001(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        assert overview_page.get_all_product_names() == list(self.PRODUCT_NAMES)
        assert overview_page.get_all_quantities() == ["1", "1"]
        assert overview_page.get_all_prices() == list(self.PRODUCT_PRICES)

    def test_ovr_fn_002(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        item_total = overview_page.get_item_total()
        assert item_total == 39.98
        assert item_total == pytest.approx(9.99 + 29.99)

    def test_ovr_fn_003(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        item_total = overview_page.get_item_total()
        tax = overview_page.get_tax()
        assert tax == 3.20
        assert tax / item_total == pytest.approx(0.08, abs=0.001)

    def test_ovr_fn_004(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        item_total = overview_page.get_item_total()
        tax = overview_page.get_tax()
        total = overview_page.get_total()
        assert total == 43.18
        assert total == pytest.approx(item_total + tax)

    def test_ovr_fn_005(self, inventory_page):
        overview_page = self._open_overview(inventory_page)

        overview_page.click_finish()

        expect(overview_page.page).to_have_url(
            f"{Config.BASE_URL}checkout-complete.html"
        )
        expect(overview_page.complete_header).to_have_text(
            "Thank you for your order!"
        )
        assert overview_page.get_cart_badge_count() == 0

    def test_ovr_fn_006(self, inventory_page):
        """Follow Excel cart.html requirement; the intentional failure documents
        SauceDemo's current inventory.html behavior and must not be fixed by
        changing the expected URL.
        """
        overview_page = self._open_overview(inventory_page)
        overview_product_names = overview_page.get_all_product_names()
        overview_prices = overview_page.get_all_prices()
        overview_item_total = overview_page.get_item_total()

        overview_page.click_cancel()

        expect(overview_page.page).to_have_url(f"{Config.BASE_URL}cart.html")
        cart_page = CartPage(overview_page.page)
        cart_page.verify_cart_page_loaded()
        assert cart_page.get_all_product_names() == overview_product_names
        assert cart_page.get_all_prices() == overview_prices
        assert cart_page.get_cart_item_count() == 2
        cart_total = sum(float(price.lstrip("$")) for price in overview_prices)
        assert cart_total == pytest.approx(overview_item_total)
