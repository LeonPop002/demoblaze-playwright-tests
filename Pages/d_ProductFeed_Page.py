class ProductFeed:
    def __init__(self, page):
        self.page = page

    def open_product(self, product_name):
        self.page.get_by_role("link", name= product_name).click()

    def get_product_price(self, product_name):
        
        return self.page.locator(".card-block").filter(has_text= product_name).locator("h5").inner_text()

    def product_filter(self, category_name):
        self.page.get_by_role("link", name= category_name).click()
