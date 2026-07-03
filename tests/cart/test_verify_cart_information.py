import pytest

from pages.product.product_page import ProductPage
from pages.cart.cart_page import CartPage


@pytest.mark.cart
def test_verify_cart_information(page):
    """Test verifying cart product information and calculations."""
    product = ProductPage(page)
    cart = CartPage(page)

    # ============================================
    # Step 1: Open Products page
    # ============================================

    product.open()
    assert product.is_products_page_visible()
    product.screenshot("cart/01_products_page")

    # ============================================
    # Step 2: Add one product
    # ============================================

    product.add_first_product_to_cart()
    assert product.is_cart_popup_visible()
    product.screenshot("cart/02_product_added")

    # ============================================
    # Step 3: Open Cart
    # ============================================

    product.view_cart()
    assert cart.is_cart_visible()
    cart.screenshot("cart/03_cart_page")

    # ============================================
    # Step 4: Verify product information
    # ============================================

    # Get product information from cart
    product_name = cart.get_product_name(0)
    product_price_text = cart.get_product_price(0)
    product_quantity_text = cart.get_product_quantity(0)
    product_total_text = cart.get_product_total(0)

    # Verify product name is not empty
    assert product_name.strip(), "Product name should not be empty"
    print(f"Product Name: {product_name}")

    # Verify product price is not empty
    assert product_price_text.strip(), "Product price should not be empty"
    print(f"Product Price: {product_price_text}")

    # Verify product quantity is not empty
    assert product_quantity_text.strip(), "Product quantity should not be empty"
    print(f"Product Quantity: {product_quantity_text}")

    # Verify product total is not empty
    assert product_total_text.strip(), "Product total should not be empty"
    print(f"Product Total: {product_total_text}")

    cart.screenshot("cart/04_verify_information")

    # ============================================
    # Step 5: Verify Total = Price × Quantity
    # ============================================

    # Extract numeric values from text
    price = float(product_price_text.replace("Rs.", "").strip())
    quantity = int(product_quantity_text.strip())
    total = float(product_total_text.replace("Rs.", "").strip())

    # Verify calculation
    expected_total = price * quantity
    assert total == expected_total, (
        f"Product total mismatch: Expected {expected_total} "
        f"(Price {price} × Quantity {quantity}), "
        f"but got {total}"
    )

    print(f"\nVerification Passed:")
    print(f"  Price: {price}")
    print(f"  Quantity: {quantity}")
    print(f"  Total: {total}")
    print(f"  Calculation: {price} × {quantity} = {expected_total} ✓")

    cart.screenshot("cart/05_calculation_verified")
