import pytest

from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage


@pytest.mark.cart
def test_multiple_products(page):
    """Test adding multiple different products to cart."""
    product = ProductPage(page)
    cart = CartPage(page)

    # ============================================
    # Step 1: Open Products page
    # ============================================

    product.open()
    assert product.is_products_page_visible()
    product.screenshot("cart/01_products_page")

    # ============================================
    # Step 2: Add Product #1
    # ============================================

    product.add_product(0)
    assert product.is_cart_popup_visible()
    product.screenshot("cart/02_first_product_added")

    # ============================================
    # Step 3: Continue Shopping
    # ============================================

    product.continue_shopping()
    page.wait_for_load_state("domcontentloaded")
    assert product.is_products_page_visible()
    product.screenshot("cart/03_back_to_products")

    # ============================================
    # Step 4: Add Product #2
    # ============================================

    product.add_product(1)
    assert product.is_cart_popup_visible()
    product.screenshot("cart/04_second_product_added")

    # ============================================
    # Step 5: Continue Shopping
    # ============================================

    product.continue_shopping()
    page.wait_for_load_state("domcontentloaded")
    assert product.is_products_page_visible()
    product.screenshot("cart/05_back_to_products")

    # ============================================
    # Step 6: Add Product #3
    # ============================================

    product.add_product(2)
    assert product.is_cart_popup_visible()
    product.screenshot("cart/06_third_product_added")

    # ============================================
    # Step 7: View Cart
    # ============================================

    product.view_cart()
    assert cart.is_cart_visible()
    cart.screenshot("cart/07_cart_page")

    # ============================================
    # Step 8: Verify exactly three products exist
    # ============================================

    cart.verify_product_count(3)

    # ============================================
    # Step 9: Verify each product name appears
    # ============================================

    product_names = cart.get_all_product_names()
    assert len(product_names) == 3, f"Expected 3 product names, got {len(product_names)}"
    assert all(name.strip() for name in product_names), "Product names should not be empty"
    
    for i, name in enumerate(product_names, 1):
        print(f"Product {i}: {name}")

    cart.screenshot("cart/08_verify_product_names")

    # ============================================
    # Step 10: Verify quantity is 1 for each product
    # ============================================

    for i in range(3):
        row = page.locator(".table tbody tr").nth(i)
        quantity = row.locator(".cart_quantity button").first.text_content()
        assert quantity.strip() == "1", f"Product {i+1} quantity should be 1, but got {quantity}"

    cart.screenshot("cart/09_verify_quantities")
