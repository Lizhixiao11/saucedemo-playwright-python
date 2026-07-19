from playwright.sync_api import Page, expect


class CheckoutOverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.quantity_label = page.locator('[data-test="cart-quantity-label"]')
        self.description_label = page.locator('[data-test="cart-desc-label"]')
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.item_quantities = page.locator('[data-test="item-quantity"]')
        self.product_names = page.locator('[data-test="inventory-item-name"]')
        self.product_prices = page.locator('[data-test="inventory-item-price"]')
        self.item_total_label = page.locator('[data-test="subtotal-label"]')
        self.tax_label = page.locator('[data-test="tax-label"]')
        self.total_label = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def verify_overview_page_loaded(self):
        expect(self.title).to_have_text("Checkout: Overview")
        expect(self.cart_items.first).to_be_visible()

    def get_all_quantities(self) -> list[str]:
        return self.item_quantities.all_text_contents()

    def get_all_product_names(self) -> list[str]:
        return self.product_names.all_text_contents()

    def get_all_prices(self) -> list[str]:
        return self.product_prices.all_text_contents()

    def get_item_total(self) -> float:
        return self._parse_amount(self.item_total_label.text_content())

    def get_tax(self) -> float:
        return self._parse_amount(self.tax_label.text_content())

    def get_total(self) -> float:
        return self._parse_amount(self.total_label.text_content())

    def click_finish(self):
        self.finish_button.click()

    def click_cancel(self):
        self.cancel_button.click()

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())

    @staticmethod
    def _parse_amount(label_text: str) -> float:
        return float(label_text.rsplit("$", 1)[1])
