import pytest

from pages.product.product_page import ProductPage


@pytest.mark.product
def test_view_products(page):

    product = ProductPage(page)

    product.open()

    assert product.is_products_page_visible()

    product.screenshot("product/01_products_page")

    assert product.is_product_list_visible()

    product.screenshot("product/02_product_list")

    product.view_first_product()

    assert product.is_product_detail_visible()

    product.screenshot("product/03_product_detail")

    assert product.get_product_name() != ""

    assert "Category" in product.get_category()

    assert "Rs." in product.get_price()

    assert "Availability" in product.get_availability()

    assert "Condition" in product.get_condition()

    assert "Brand" in product.get_brand()

    product.screenshot("product/04_product_information")