from playwright.sync_api import Page, expect


class CartPage:

    def __init__(self, page: Page):
        self.page = page

        # ---------- Header ----------
        self.title = page.locator(".title")
        self.app_logo = page.locator(".app_logo")

        # ---------- Menu ----------
        self.menu_btn = page.locator('[data-test="open-menu"]')
        self.close_menu_btn = page.locator('[data-test="close-menu"]')
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

        # ---------- Shopping Cart ----------
        self.cart_icon = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')

        # ---------- Cart ----------
        self.cart_container = page.locator('[data-test="cart-contents-container"]')
        self.cart_list = page.locator('[data-test="cart-list"]')
        self.cart_items = page.locator('[data-test="inventory-item"]')

        self.quantity_label = page.locator('[data-test="cart-quantity-label"]')
        self.description_label = page.locator('[data-test="cart-desc-label"]')

        self.item_quantity = page.locator('[data-test="item-quantity"]')
        self.product_names = page.locator('[data-test="inventory-item-name"]')
        self.product_descriptions = page.locator('[data-test="inventory-item-desc"]')
        self.product_prices = page.locator('[data-test="inventory-item-price"]')

        # ---------- Buttons ----------
        self.continue_shopping_btn = page.locator('[data-test="continue-shopping"]')
        self.checkout_btn = page.locator('[data-test="checkout"]')

        # ---------- Footer ----------
        self.footer = page.locator('[data-test="footer"]')

    # ---------- Page Verification ----------

    def verify_cart_page_loaded(self):
        expect(self.title).to_have_text("Your Cart")
        expect(self.cart_list).to_be_visible()

    # ---------- Navigation ----------

    def click_continue_shopping(self):
        self.continue_shopping_btn.click()

    def click_checkout(self):
        self.checkout_btn.click()

    # ---------- Product Actions ----------

    def remove_product(self, product_name: str):
        product = product_name.lower().replace(" ", "-")
        self.page.locator(
            f'[data-test="remove-{product}"]'
        ).click()

    def click_product(self, product_name: str):
        self.page.get_by_text(product_name).click()

    # ---------- Get Information ----------

    def get_product_names(self):
        return self.product_names.all_text_contents()

    def get_product_prices(self):
        return self.product_prices.all_text_contents()

    def get_quantities(self):
        return self.item_quantity.all_text_contents()

    def get_item_count(self):
        return self.cart_items.count()

    def is_product_in_cart(self, product_name: str):
        return product_name in self.get_product_names()