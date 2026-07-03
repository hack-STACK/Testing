from config.setting import TIMEOUT
from utils.base_page import BasePage


class CheckoutPage(BasePage):

    # ============================================================
    # Checkout Page Elements
    # ============================================================

    ADDRESS_DETAILS = "text=Address Details"
    REVIEW_ORDER = "text=Review Your Order"
    PLACE_ORDER = "button:has-text('Place Order')"

    # ============================================================
    # Verification
    # ============================================================

    def is_checkout_page_visible(self):
        """Verify the checkout page is displayed with key elements."""
        return (
            self.has_address_details() or
            self.has_review_order() or
            self.has_place_order_button()
        )

    def has_address_details(self):
        """Check if Address Details section is visible."""
        return self.page.locator(self.ADDRESS_DETAILS).is_visible()

    def has_review_order(self):
        """Check if Review Your Order section is visible."""
        return self.page.locator(self.REVIEW_ORDER).is_visible()

    def has_place_order_button(self):
        """Check if Place Order button is visible."""
        return self.page.locator(self.PLACE_ORDER).is_visible()
