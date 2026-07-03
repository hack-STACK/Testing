import pytest

from config.setting import REGISTER_DATA_FILE
from pages.authentication.login_page import LoginPage
from pages.authentication.signup_page import SignupPage
from pages.authentication.account_page import AccountPage
from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage
from pages.checkout.checkout_page import CheckoutPage
from utils.data_reader import load_json


@pytest.mark.cart
def test_proceed_to_checkout(page):
    """Test proceeding from Cart to Checkout successfully."""
    
    # ============================================
    # Step 0: Register a new user for checkout
    # ============================================

    user_data = load_json(REGISTER_DATA_FILE)
    account_data = user_data["account"]
    address_data = user_data["address"]

    signup = SignupPage(page)
    account = AccountPage(page)

    signup.open()
    signup.click_signup_login()
    
    assert signup.is_signup_visible()

    registered_user = signup.signup("Juan Testing")
    registered_email = registered_user["email"]

    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_information_visible()

    account.select_title(account_data["title"])
    account.enter_password(account_data["password"])
    account.select_date_of_birth(
        account_data["day"],
        account_data["month"],
        account_data["year"]
    )
    account.subscribe_newsletter()
    account.subscribe_special_offers()
    account.fill_address(address_data)
    account.create_account()

    assert account.is_account_created()
    account.screenshot("cart/00_account_created")

    # ============================================
    # Step 1: Open Products page
    # ============================================

    product = ProductPage(page)
    product.open()
    assert product.is_products_page_visible()
    product.screenshot("cart/01_products_page")

    # ============================================
    # Step 2: Add one product to the cart
    # ============================================

    product.add_first_product_to_cart()
    assert product.is_cart_popup_visible()
    product.screenshot("cart/02_product_added")

    # ============================================
    # Step 3: Open Cart
    # ============================================

    product.view_cart()
    cart = CartPage(page)
    assert cart.is_cart_visible()
    cart.screenshot("cart/03_cart_page")

    # ============================================
    # Step 4: Verify the cart contains the product
    # ============================================

    assert cart.is_product_in_cart()
    product_name = cart.get_product_name()
    assert product_name.strip(), "Product name should not be empty"
    cart.screenshot("cart/04_cart_verified")

    # ============================================
    # Step 5: Click Proceed To Checkout
    # ============================================

    cart.proceed_to_checkout()

    # ============================================
    # Step 6: Verify the Checkout page is displayed
    # ============================================

    checkout = CheckoutPage(page)
    page.wait_for_load_state("domcontentloaded")
    
    assert checkout.is_checkout_page_visible(), (
        "Checkout page should display Address Details, "
        "Review Your Order, or Place Order button"
    )
    
    # Verify at least one expected element is visible
    has_address = checkout.has_address_details()
    has_review = checkout.has_review_order()
    has_place_order = checkout.has_place_order_button()
    
    print(f"\nCheckout Page Elements:")
    print(f"  Address Details: {has_address}")
    print(f"  Review Your Order: {has_review}")
    print(f"  Place Order Button: {has_place_order}")
    
    checkout.screenshot("cart/05_checkout_page")
