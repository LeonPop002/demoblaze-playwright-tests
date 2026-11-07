class CartPage:
    def __init__(self, page):
        self.page = page
        self.order_btn = page.get_by_role("button", name="Place Order")
        self.total_amount = page.locator("#totalp")




    def get_product_price(self, product_name):
        return self.page.locator(".success").filter(has_text= product_name).locator("td").nth(2).inner_text()

    def get_product_row(self, product_name):
        return self.page.locator(".success").filter(has_text=product_name)
    
    def click_order_btn(self):
        self.order_btn.click()