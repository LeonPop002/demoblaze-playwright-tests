class HomePage:

    def __init__(self, page):
        self.page = page
        self.signup_home = page.locator("#signin2")
        self.login_home = page.locator("#login2")
        self.logout_home = page.locator("#logout2")
        self.welcome_home = page.locator("#nameofuser")
        self.cart_btn = page.get_by_role("link", name="Cart", exact=True)

    def register(self):
        self.signup_home.click()

    def open_login(self):
        self.login_home.click()

    def open_cart(self):
        self.cart_btn.click()
