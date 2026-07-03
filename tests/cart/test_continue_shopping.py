import pytest

from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage


@pytest.mark.cart
def test_continue_shopping(page):
    """Test continuing shopping after adding a product to cart."""
    product = ProductPage(page)
    cart = CartPage(page)

    # ============================================
    # Step 1: Open Products page
    # ============================================

    product.open()
    assert product.is_products_page_visible()
    product.screenshot("cart/01_products_page")

    # ============================================
    # Step 2: Add the first product
    # ============================================

    product.add_product(0)

    # ============================================
    # Step 3: Verify the Add to Cart modal appears
    # ============================================

    assert product.is_cart_popup_visible()
    product.screenshot("cart/02_modal_appeared")

    # ============================================
    # Step 4: Click Continue Shopping
    # ============================================

    product.continue_shopping()

    # ============================================
    # Step 5: Verify the user remains on the Products page
    # ============================================

    page.wait_for_load_state("domcontentloaded")
    assert product.is_products_page_visible()
    product.screenshot("cart/03_back_on_products_page")

    # ============================================
    # Step 6: Add a second different product
    # ============================================

    product.add_product(1)

    # ============================================
    # Step 7: Open the Cart
    # ============================================

    product.view_cart()
    assert cart.is_cart_visible()
    cart.screenshot("cart/04_cart_page")

    # ============================================
    # Step 8: Verify exactly two products are present
    # ============================================

    cart.verify_product_count(2)
    product.screenshot("cart/05_cart_verified")
