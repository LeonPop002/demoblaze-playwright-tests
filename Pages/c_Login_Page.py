class SignInPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#loginusername")
        self.password = page.locator("#loginpassword")
        self.signin_btn = page.get_by_role("button", name="Log in")
        
    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.signin_btn.click()