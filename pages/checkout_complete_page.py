from playwright.sync_api import Page, expect


class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

    def verify_complete_page_loaded(self):
        expect(self.title).to_have_text("Checkout: Complete!")
        expect(self.complete_header).to_be_visible()

    def click_back_home(self):
        self.back_home_button.click()

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())
