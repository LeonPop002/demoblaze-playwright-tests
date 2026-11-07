import pytest
from playwright.sync_api import expect
from Pages.a_Home_Page import HomePage
from Pages.c_Login_Page import SignInPage
from conftest import ACC_NAME, ACC_PASS


@pytest.mark.positive
def test_login_valid(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)
    

    home_page.open_login()
    login_page.login(ACC_NAME, ACC_PASS)
    expect(home_page.welcome_home).to_have_text(f"Welcome {ACC_NAME}")
    expect(home_page.logout_home).to_be_visible()

@pytest.mark.negative
def test_login_with_wrong_username(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)

    home_page.open_login()

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        login_page.login("jjiyr", ACC_PASS)
    
    alert = dialog_info.value
    assert alert.message == "User does not exist."
    
    expect(home_page.logout_home).not_to_be_visible()


@pytest.mark.negative
def test_login_without_name(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)

    home_page.open_login()

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        login_page.login("", ACC_PASS)
    
    alert = dialog_info.value
    assert alert.message == "Please fill out Username and Password."
    
    expect(home_page.logout_home).not_to_be_visible()

@pytest.mark.negative
def test_login_with_wrong_password(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)

    home_page.open_login()
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        login_page.login(ACC_NAME, "aaa123")
        
    alert = dialog_info.value
    assert alert.message == "Wrong password."
    
    expect(home_page.logout_home).not_to_be_visible()


@pytest.mark.negative
def test_login_without_password(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)

    home_page.open_login()
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        login_page.login(ACC_NAME, "")
        
    alert = dialog_info.value
    assert alert.message == "Please fill out Username and Password."
    
    expect(home_page.logout_home).not_to_be_visible()

@pytest.mark.negative
def test_login_without_fields(StorePage):
    home_page = HomePage(StorePage)
    login_page = SignInPage(StorePage)

    home_page.open_login()
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        login_page.login("", "")
        
    alert = dialog_info.value
    assert alert.message == "Please fill out Username and Password."
    
    expect(home_page.logout_home).not_to_be_visible()

