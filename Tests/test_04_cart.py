import pytest
from playwright.sync_api import expect
from Pages.e_CartPage import CartPage
from Pages.f_purchase import PlaceOrder

@pytest.mark.positive
def test_product_cart_item(cart_with_product):
    page, product_name, feed_price = cart_with_product
    cart_page = CartPage(page)
    
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    cart_price = cart_page.get_product_price(product_name)
    assert feed_price.replace("$", "") == cart_price
    expect(cart_page.order_btn).to_be_visible()

@pytest.mark.positive
def test_purchase(cart_with_product):
    page, _, feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)

    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))
    
    cart_page.click_order_btn()
    purchase_page.fill_order("Leon popy", "Israel", "Tel aviv", "9999555522221111", "10", "2029")
    expect(purchase_page.thanks_purchase).to_have_text("Thank you for your purchase!")
    expect(purchase_page.amount).to_contain_text(f"Amount: {feed_price.replace('$', '')} USD")
    purchase_page.close_confirmation()

@pytest.mark.negative
@pytest.mark.xfail(raises=AssertionError, reason="BUG-124: the order amount is calculated in the browser, so clicking Purchase before the cart total loads sends 0")
def test_purchase_with_no_expect_amount(cart_with_product):
    page, _, feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
    
    # No wait for the cart total here on purpose, this is what triggers BUG-124

    cart_page.click_order_btn()
    purchase_page.fill_order("Leon popy", "Israel", "Tel aviv", "9999555522221111", "10", "2029")
    expect(purchase_page.thanks_purchase).to_have_text("Thank you for your purchase!")
    expect(purchase_page.amount).to_contain_text(f"Amount: {feed_price.replace('$', '')} USD")
    purchase_page.close_confirmation()

@pytest.mark.negative
def test_purchase_without_fields(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
    
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))
    cart_page.click_order_btn()

    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("", "", "", "", "", "")
            
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()

@pytest.mark.negative
def test_purchase_without_name(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
        
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    
    cart_page.click_order_btn()
    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("", "Israel", "Tel aviv", "9999555522221111", "10", "2029")
            
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()

@pytest.mark.negative
@pytest.mark.xfail(reason="BUG-125: Complete purchase without country or city")
def test_purchase_without_country_city(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
        
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    cart_page.click_order_btn()
    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("Leon Popy", "", "", "9999555522221111", "10", "2029")
                
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()

@pytest.mark.negative
def test_purchase_without_card(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
        
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    cart_page.click_order_btn()
    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("Leon Popy", "Israel", "Tel aviv", "", "10", "2029")
            
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()

@pytest.mark.negative
@pytest.mark.xfail(reason="BUG-126: Complete purchase with old year")
def test_purchase_with_old_year(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
        
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    cart_page.click_order_btn()
    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("Leon Popy", "Israel", "Tel aviv", "9999555522221111", "10", "1990")
            
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()

@pytest.mark.negative
@pytest.mark.xfail(reason="BUG-127: Complete purchase with wrong card number")
def test_purchase_with_wrong_card_num(cart_with_product):
    page, _ , feed_price = cart_with_product
    cart_page = CartPage(page)
    purchase_page = PlaceOrder(page)
        
    expect(cart_page.total_amount).to_have_text(feed_price.replace('$', ''))

    cart_page.click_order_btn()
    page.once("dialog", lambda dialog: dialog.accept())
    with page.expect_event("dialog", timeout=5000) as dialog_info:
        purchase_page.fill_order("Leon Popy", "Israel", "Tel aviv", "ABC456", "10", "2029")
            
    alert = dialog_info.value
    assert alert.message == "Please fill out Name and Creditcard."
    expect(purchase_page.thanks_purchase).not_to_be_visible()
