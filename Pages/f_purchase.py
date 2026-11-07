class PlaceOrder:
    def __init__(self, page):
        self.page = page
        self.name_field = page.locator("#name")
        self.country_field = page.locator("#country")
        self.city_field = page.locator("#city")
        self.credit_field = page.locator("#card")
        self.month_field = page.locator("#month")
        self.year_field = page.locator("#year")
        self.purchase_btn = page.get_by_role("button", name="Purchase")
        self.thanks_purchase = page.locator(".sweet-alert").locator("h2")
        self.ok_btn = page.get_by_role("button", name="OK")

        self.amount = page.locator(".sweet-alert").locator(".lead")

    def fill_order(self, name, country, city, card, month, year):
        self.name_field.fill(name)
        self.country_field.fill(country)
        self.city_field.fill(city)
        self.credit_field.fill(card)
        self.month_field.fill(month)
        self.year_field.fill(year)
        self.purchase_btn.click()

    def close_confirmation(self):
        self.ok_btn.click()
