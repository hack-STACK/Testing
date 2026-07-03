import pytest

from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage


@pytest.mark.cart
def test_remove_product(page):

    product = ProductPage(page)
    cart = CartPage(page)

    # ============================================
    # Open Product Page
    # ============================================

    product.open()

    assert product.is_products_page_visible()

    # ============================================
    # Add Product
    # ============================================

    product.hover_first_product()

    product.add_first_product_to_cart()

    assert product.is_cart_popup_visible()

    # ============================================
    # View Cart
    # ============================================

    product.view_cart()

    assert cart.is_cart_visible()

    cart.screenshot("cart/01_before_delete")

    # ============================================
    # Delete Product
    # ============================================

    cart.delete_first_product()

    # ============================================
    # Verify Empty Cart
    # ============================================

    assert cart.is_cart_empty()

    cart.screenshot("cart/02_after_delete")