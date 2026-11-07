class SignupPage:
    def __init__(self, page):
        self.page = page
        self.username = page.locator("#sign-username")
        self.password = page.locator("#sign-password")
        self.signup_btn = page.get_by_role("button", name="Sign up")
        
    def signup(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.signup_btn.click()
