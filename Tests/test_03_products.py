import pytest
from playwright.sync_api import expect
from Pages.d_ProductFeed_Page import ProductFeed
from Pages.d2_Product_Page import ProductPage

product_name = "Apple monitor 24"
category_name = "Monitors"

@pytest.mark.positive
def test_product_bio(StorePage):

    feed = ProductFeed(StorePage)
    product_page = ProductPage(StorePage)
    feed.product_filter(category_name)
    
    price = feed.get_product_price(product_name)
    feed.open_product(product_name)
    expect(product_page.product_name).to_have_text(product_name)
    expect(product_page.price).to_contain_text(price)
    expect(product_page.add_product).to_be_visible()

