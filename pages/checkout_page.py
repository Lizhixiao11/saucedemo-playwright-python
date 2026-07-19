from playwright.sync_api import Page, expect


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------- Header ----------
        self.title = page.locator('[data-test="title"]')

        # ---------- Information Form ----------
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')

        # ---------- Validation ----------
        self.error_message = page.locator('[data-test="error"]')

        # ---------- Shopping Cart ----------
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

        # ---------- Buttons ----------
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.continue_button = page.locator('[data-test="continue"]')

    # ---------- Page Verification ----------

    def verify_information_page_loaded(self):
        expect(self.title).to_have_text("Checkout: Your Information")
        expect(self.first_name_input).to_be_visible()
        expect(self.last_name_input).to_be_visible()
        expect(self.postal_code_input).to_be_visible()

    # ---------- Form Actions ----------

    def fill_checkout_information(
        self,
        first_name: str = "",
        last_name: str = "",
        postal_code: str = "",
    ):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def click_continue(self):
        self.continue_button.click()

    def click_cancel(self):
        self.cancel_button.click()

    def get_cart_badge_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.text_content())
