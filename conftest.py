import pytest
from Pages.a_Home_Page import HomePage
from Pages.d_ProductFeed_Page import ProductFeed
from Pages.d2_Product_Page import ProductPage


BASE_URL = "https://www.demoblaze.com/index.html#"
ACC_NAME = "LeonPopy"
ACC_PASS = "Leon12345"
PRODUCT_NAME = "Nexus 6"
CATEGORY_NAME = "Phones"

@pytest.fixture
def StorePage(page):
    page.goto(BASE_URL)
    return page

@pytest.fixture
def cart_with_product(StorePage):
    home_page = HomePage(StorePage)
    feed = ProductFeed(StorePage)
    product_page = ProductPage(StorePage)
    

    feed.product_filter(CATEGORY_NAME)
    feed_price = feed.get_product_price(PRODUCT_NAME)
    feed.open_product(PRODUCT_NAME)

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        product_page.add_to_cart()
    
    alert = dialog_info.value
    assert alert.message == "Product added"

    home_page.open_cart()

    return StorePage, PRODUCT_NAME, feed_price