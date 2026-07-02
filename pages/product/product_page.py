from config.setting import PRODUCTS_URL, TIMEOUT
from utils.base_page import BasePage


class ProductPage(BasePage):

    URL = PRODUCTS_URL

    # ============================================================
    # Navigation
    # ============================================================

    PRODUCTS_BUTTON = "a[href='/products']"

    # ============================================================
    # Product List
    # ============================================================

    PRODUCT_LIST = ".features_items"

    PRODUCT_CARD = ".product-image-wrapper"

    VIEW_PRODUCT_BUTTON = "a[href*='/product_details/']"

    # ============================================================
    # Search Product
    # ============================================================

    SEARCH_INPUT = "#search_product"

    SEARCH_BUTTON = "#submit_search"

    SEARCHED_PRODUCTS_TITLE = "text=Searched Products"

    # ============================================================
    # Product Detail
    # ============================================================

    PRODUCT_INFORMATION = ".product-information"

    PRODUCT_NAME = ".product-information h2"

    CATEGORY = ".product-information p"

    PRICE = ".product-information span span"

    PRODUCT_INFO = ".product-information p"

    # ============================================================
    # Cart
    # ============================================================

    ADD_TO_CART_BUTTON = ".overlay-content .add-to-cart"

    CART_MODAL = "#cartModal"

    CONTINUE_SHOPPING_BUTTON = ".btn-success"

    VIEW_CART_BUTTON = "#cartModal a[href='/view_cart']"

    # ============================================================
    # Navigation
    # ============================================================

    def open(self):
        self.visit(self.URL)

    def click_products(self):
        self.click(self.PRODUCTS_BUTTON)
        self.page.locator(self.PRODUCT_LIST).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    # ============================================================
    # Product Action
    # ============================================================

    def view_first_product(self):
        self.page.locator(self.VIEW_PRODUCT_BUTTON).first.click()
        self.page.locator(self.PRODUCT_INFORMATION).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    def search_product(self, keyword):
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.page.locator(self.SEARCHED_PRODUCTS_TITLE).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    def hover_first_product(self):
        self.page.locator(self.PRODUCT_CARD).first.wait_for(
            state="visible",
            timeout=TIMEOUT
        )
        self.page.locator(self.PRODUCT_CARD).first.hover()

    def add_first_product_to_cart(self):
        product = self.page.locator(self.PRODUCT_CARD).first
        product.hover()
        product.locator(self.ADD_TO_CART_BUTTON).click()
        self.page.locator(self.CART_MODAL).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    CART_TABLE = "#cart_info_table"

    def view_cart(self):
        self.click(self.VIEW_CART_BUTTON)
        self.page.locator(self.CART_TABLE).wait_for(
            state="visible",
            timeout=TIMEOUT
        )

    # ============================================================
    # Verification
    # ============================================================

    def is_products_page_visible(self):
        return self.page.locator(
            self.PRODUCT_LIST
        ).is_visible()

    def is_product_list_visible(self):
        return self.page.locator(
            self.PRODUCT_LIST
        ).is_visible()

    def is_product_detail_visible(self):
        return self.page.locator(
            self.PRODUCT_INFORMATION
        ).is_visible()

    def is_search_result_visible(self):
        return self.page.locator(
            self.SEARCHED_PRODUCTS_TITLE
        ).is_visible()

    def is_cart_popup_visible(self):
        return self.page.locator(
            self.CART_MODAL
        ).is_visible()

    # ============================================================
    # Product Information
    # ============================================================

    def get_product_name(self):
        return self.text(self.PRODUCT_NAME)

    def get_category(self):
        return self.page.locator(
            self.CATEGORY
        ).first.text_content()

    def get_price(self):
        return self.text(self.PRICE)

    def get_availability(self):
        return self.page.locator(
            self.PRODUCT_INFO
        ).nth(1).text_content()

    def get_condition(self):
        return self.page.locator(
            self.PRODUCT_INFO
        ).nth(2).text_content()

    def get_brand(self):
        return self.page.locator(
            self.PRODUCT_INFO
        ).nth(3).text_content()