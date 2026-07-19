from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        # Page Elements
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.get_by_test_id("error")

    # ---------- Page Actions ----------

    def open(self, url: str):
        self.page.goto(url)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_as_standard_user(self):
        self.login("standard_user", "secret_sauce")

    def login_as_locked_user(self):
        self.login("locked_out_user", "secret_sauce")

    def login_as_problem_user(self):
        self.login("problem_user", "secret_sauce")

    def login_as_performance_user(self):
        self.login("performance_glitch_user", "secret_sauce")

    def get_error_message(self):
        return self.error_message.inner_text()

    def verify_login_page_loaded(self):
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()
