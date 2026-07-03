import pytest

from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage


@pytest.mark.cart
def test_view_cart(page):

    product = ProductPage(page)
    cart = CartPage(page)

    # ==========================
    # Open Product Page
    # ==========================

    product.open()

    assert product.is_products_page_visible()

    product.screenshot("cart/01_products_page")

    # ==========================
    # Add Product To Cart
    # ==========================

    product.hover_first_product()

    product.add_first_product_to_cart()

    assert product.is_cart_popup_visible()

    product.screenshot("cart/02_cart_popup")

    # ==========================
    # Open Cart
    # ==========================

    product.view_cart()

    assert cart.is_cart_visible()

    cart.screenshot("cart/03_cart_page")

    # ==========================
    # Verify Product
    # ==========================

    assert cart.is_product_in_cart()

    print("Product :", cart.get_product_name())
    print("Price   :", cart.get_product_price())
    print("Qty     :", cart.get_product_quantity())
    print("Total   :", cart.get_product_total())

    cart.screenshot("cart/04_product_in_cart")