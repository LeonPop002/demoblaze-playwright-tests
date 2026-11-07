class ProductPage:
    def __init__(self, page):
        self.page = page
        self.product_name = page.locator(".name")
        self.price = page.locator(".price-container")
        self.add_product = page.get_by_role("link", name="Add to cart")


    def add_to_cart(self):
        self.add_product.click()
        

