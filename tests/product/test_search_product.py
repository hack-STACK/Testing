import pytest

from pages.product.product_page import ProductPage
from utils.data_reader import load_json


@pytest.mark.product
def test_search_product(page):

    data = load_json("data/product_data.json")

    keyword = data["search"]["keyword"]

    product = ProductPage(page)

    product.open()

    assert product.is_products_page_visible()

    product.screenshot("product/01_products_page")

    product.search_product(keyword)

    assert product.is_search_result_visible()

    product.screenshot("product/02_search_result")

    assert product.is_product_list_visible()

    product.screenshot("product/03_search_product_list")