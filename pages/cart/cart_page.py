from config.setting import CART_URL, TIMEOUT
from utils.base_page import BasePage


class CartPage(BasePage):

    URL = CART_URL

    # ============================================================
    # Cart
    # ============================================================

    CART_TABLE = "#cart_info_table"

    CART_ROWS = "#cart_info_table tbody tr"

    PRODUCT_NAME = ".cart_description h4 a"

    PRODUCT_PRICE = ".cart_price p"

    PRODUCT_QUANTITY = ".cart_quantity button"

    PRODUCT_TOTAL = ".cart_total p"

    DELETE_BUTTON = "a.cart_quantity_delete"

    EMPTY_CART_TEXT = "text=Cart is empty"

    CHECKOUT_BUTTON = ".check_out"

    # ============================================================
    # Navigation
    # ============================================================

    def open(self):
        self.visit(self.URL)

    # ============================================================
    # Cart Action
    # ============================================================

    def delete_first_product(self):
        self.page.locator(self.DELETE_BUTTON).first.click()
        self.page.locator(self.EMPTY_CART_TEXT).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

    # ============================================================
    # Verification
    # ============================================================

    def is_cart_visible(self):
        return self.page.locator(
            self.CART_TABLE
        ).is_visible()

    def is_product_in_cart(self):
        return self.page.locator(
            self.CART_ROWS
        ).count() > 0

    def is_cart_empty(self):
        return self.page.locator(
            self.EMPTY_CART_TEXT
        ).is_visible()

    def is_checkout_button_visible(self):
        return self.page.locator(
            self.CHECKOUT_BUTTON
        ).is_visible()

    # ============================================================
    # Product Information
    # ============================================================

    def get_product_name(self):
        return self.page.locator(
            self.PRODUCT_NAME
        ).first.text_content()

    def get_product_price(self):
        return self.page.locator(
            self.PRODUCT_PRICE
        ).first.text_content()

    def get_product_quantity(self):
        return self.page.locator(
            self.PRODUCT_QUANTITY
        ).first.text_content()

    def get_total_products(self):
        return self.page.locator(self.CART_ROWS).count()
    
    def get_product_total(self):
        return self.page.locator(
        self.PRODUCT_TOTAL
    ).first.text_content()