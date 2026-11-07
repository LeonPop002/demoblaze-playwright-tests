import pytest
import time
from playwright.sync_api import expect
from Pages.a_Home_Page import HomePage
from Pages.b_Signup_Page import SignupPage
from Pages.c_Login_Page import SignInPage
from conftest import ACC_NAME, ACC_PASS

@pytest.mark.positive
def test_signup_valid(StorePage):
    home_page = HomePage(StorePage)
    signup_page = SignupPage(StorePage)
    username = f"leon{int(time.time())}"

    home_page.register()

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        signup_page.signup(username, ACC_PASS)

    alert = dialog_info.value
    assert alert.message == "Sign up successful."
    
@pytest.mark.negative
def test_signup_with_already_name(StorePage):
    home_page = HomePage(StorePage)
    signup_page = SignupPage(StorePage)
    
    home_page.register()

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        signup_page.signup(ACC_NAME, ACC_PASS)

    alert = dialog_info.value
    assert alert.message == "This user already exist."

@pytest.mark.negative
@pytest.mark.xfail(raises=AssertionError, reason="BUG-123: Create account with password shorter than 6 symbols")
def test_signup_with_short_password(StorePage):
    home_page = HomePage(StorePage)
    signup_page = SignupPage(StorePage)
    username = f"leon{int(time.time())}"

    home_page.register()

    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        signup_page.signup(username, "A")

    alert = dialog_info.value
    assert alert.message == "The password is too short."

@pytest.mark.negative
@pytest.mark.xfail(reason="Like BUG-123: Account created with short password")
def test_short_password_account_is_not_created(StorePage):
    home_page = HomePage(StorePage)
    signup_page = SignupPage(StorePage)
    username = f"leon{int(time.time())}"

    home_page.register()
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog") as dialog_info:
        signup_page.signup(username, "A")

    #Check if a WEB create a user name after error

    login_page = SignInPage(StorePage)
    
    home_page.open_login()
    
    StorePage.once("dialog", lambda dialog: dialog.accept())
    with StorePage.expect_event("dialog", timeout=5000) as dialog_info:
        login_page.login(username, "A")
        
    alert = dialog_info.value
    assert alert.message == "User does not exist."
        
    expect(home_page.logout_home).not_to_be_visible()
    


