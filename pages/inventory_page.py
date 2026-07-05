from playwright.sync_api import Page, expect


class InventoryPage:

    def __init__(self, page: Page):
        self.page = page

        # Header
        self.title = page.locator(".title")

        # Menu
        self.menu_btn = page.locator('[data-test="open-menu"]')
        self.close_menu_btn = page.locator('[data-test="close-menu"]')
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

        # Cart
        self.cart_icon = page.locator('[data-test="shopping-cart-link"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]') 

        # Inventory
        self.inventory_list = page.locator('[data-test="inventory-list"]')
        self.inventory_items = page.locator('[data-test="inventory-item"]')
        self.product_names = page.locator('[data-test="inventory-item-name"]')
        self.product_prices = page.locator('[data-test="inventory-item-price"]')

        # Sort
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')

        # Footer
        self.footer = page.locator('[data-test="footer"]')

    # ---------- Page Verification ----------

    def verify_inventory_page_loaded(self):
        expect(self.title).to_have_text("Products")
        expect(self.inventory_list).to_be_visible()

    # ---------- Menu ----------

    def open_menu(self):
        self.menu_btn.click()

    def close_menu(self):
        self.close_menu_btn.click()

    def logout(self):
        self.open_menu()
        self.logout_link.click()

    # ---------- Shopping Cart ----------

    def open_cart(self):
        self.cart_icon.click()

    def get_cart_badge_count(self):
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    # ---------- Product ----------

    def add_to_cart(self, product_name: str):
        product = product_name.lower().replace(" ", "-")
        self.page.locator(
            f'[data-test="add-to-cart-{product}"]'
        ).click()

    def remove_from_cart(self, product_name: str):
        product = product_name.lower().replace(" ", "-")
        self.page.locator(
            f'[data-test="remove-{product}"]'
        ).click()

    def click_product(self, product_name: str):
        self.page.get_by_text(product_name).click()

    def get_all_product_names(self):
        return self.product_names.all_text_contents()

    def get_all_prices(self):
        return self.product_prices.all_text_contents()

    # ---------- Sort ----------

    def sort_by(self, value: str):
        """
        az
        za
        lohi
        hilo
        """
        self.sort_dropdown.select_option(value)

    def get_item_count(self):
        return self.inventory_items.count()