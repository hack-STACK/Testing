import pytest

from pages.product.product_page import ProductPage


@pytest.mark.product
def test_add_to_cart(page):

    product = ProductPage(page)

    product.open()

    assert product.is_products_page_visible()

    product.screenshot("01_products")

    product.hover_first_product()

    product.add_first_product_to_cart()

    assert product.is_cart_popup_visible()

    product.screenshot("02_cart_popup")

    product.continue_shopping()

    product.screenshot("03_continue_shopping")