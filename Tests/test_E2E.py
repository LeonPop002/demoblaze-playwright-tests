import pytest
import time
from playwright.sync_api import expect
from Pages.a_Home_Page import HomePage
from Pages.b_Signup_Page import SignupPage
from Pages.c_Login_Page import SignInPage
from Pages.d_ProductFeed_Page import ProductFeed
from Pages.d2_Product_Page import ProductPage
from Pages.e_CartPage import CartPage
from Pages.f_purchase import PlaceOrder
from conftest import ACC_PASS

product_name = "Apple monitor 24"
category_name = "Monitors"

@pytest.mark.e2e
def test_e2e(StorePage):
    home_page = HomePage(StorePage)
    signup_page = SignupPage(StorePage)
    signin_page = SignInPage(StorePage)
    feed = ProductFeed(StorePage)
    product_page = ProductPage(StorePage)
    cart_page = CartPage(StorePage)
    purchase_page = PlaceOrder(StorePage)

    username = f"leon{int(time.time())}"
#Register process
    home_page.register()
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        signup_page.signup(username, ACC_PASS)
    
    alert = dialog_info.value
    assert alert.message == "Sign up successful."
#LogIn Process
    home_page.open_login()
    signin_page.login(username, ACC_PASS)
    expect(home_page.welcome_home).to_have_text(f"Welcome {username}")
    expect(home_page.logout_home).to_be_visible()

#Check product feed and Add to cart
    feed.product_filter(category_name)
    price = feed.get_product_price(product_name)
    feed.open_product(product_name)
    expect(product_page.product_name).to_have_text(product_name)
    expect(product_page.price).to_contain_text(price)

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        product_page.add_to_cart()
    alert = dialog_info.value
    # Message differs between guest and logged-in user, see BUG-128
    assert alert.message == "Product added."

#Cart feed and Checkout
    home_page.open_cart()
    cart_price = cart_page.get_product_price(product_name)
    expect(cart_page.total_amount).to_have_text(price.replace('$', ''))
    assert price.replace("$", "") == cart_price
    expect(cart_page.order_btn).to_be_visible()

    cart_page.click_order_btn()
    purchase_page.fill_order("Leon popy", "Israel", "Tel aviv", "9999555522221111", "10", "2029")
    expect(purchase_page.amount).to_contain_text(f"Amount: {price.replace('$', '')} USD")
    expect(purchase_page.thanks_purchase).to_have_text("Thank you for your purchase!")
    purchase_page.close_confirmation()
