from utils.base_page import BasePage


class AccountPage(BasePage):

    # ==========================
    # Account Information
    # ==========================

    TITLE_MR = "#id_gender1"
    TITLE_MRS = "#id_gender2"

    PASSWORD = "#password"

    DAYS = "#days"
    MONTHS = "#months"
    YEARS = "#years"

    NEWSLETTER = "#newsletter"
    SPECIAL_OFFERS = "#optin"

    # ==========================
    # Address Information
    # ==========================

    FIRST_NAME = "#first_name"
    LAST_NAME = "#last_name"
    COMPANY = "#company"

    ADDRESS1 = "#address1"
    ADDRESS2 = "#address2"

    COUNTRY = "#country"

    STATE = "#state"
    CITY = "#city"
    ZIPCODE = "#zipcode"

    MOBILE = "#mobile_number"

    # ==========================
    # Button
    # ==========================

    CREATE_ACCOUNT_BUTTON = "button[data-qa='create-account']"
    CONTINUE_BUTTON = "a[data-qa='continue-button']"
    DELETE_ACCOUNT_BUTTON = "a[href='/delete_account']"

    # ==========================
    # Validation
    # ==========================

    ACCOUNT_INFORMATION = "text=Enter Account Information"
    ACCOUNT_CREATED = "text=Account Created!"
    LOGGED_IN = "text=Logged in as"
    ACCOUNT_DELETED = "text=Account Deleted!"

    # ============================================================
    # Verification
    # ============================================================

    def is_account_information_visible(self):
        return self.page.locator(self.ACCOUNT_INFORMATION).is_visible()

    def is_account_created(self):
        return self.page.locator(self.ACCOUNT_CREATED).is_visible()

    def is_logged_in(self):
        return self.page.locator(self.LOGGED_IN).is_visible()

    def is_account_deleted(self):
        return self.page.locator(self.ACCOUNT_DELETED).is_visible()

    # ============================================================
    # Account Information
    # ============================================================

    def select_title(self, title="Mr"):
        if title.lower() == "mr":
            self.click(self.TITLE_MR)
        else:
            self.click(self.TITLE_MRS)

    def enter_password(self, password):
        self.fill(self.PASSWORD, password)

    def select_date_of_birth(self, day, month, year):
        self.page.select_option(self.DAYS, str(day))
        self.page.select_option(self.MONTHS, str(month))
        self.page.select_option(self.YEARS, str(year))

    def subscribe_newsletter(self):
        self.click(self.NEWSLETTER)

    def subscribe_special_offers(self):
        self.click(self.SPECIAL_OFFERS)

    # ============================================================
    # Address Information
    # ============================================================

    def fill_address(
        self,
        first_name,
        last_name=None,
        company=None,
        address1=None,
        address2=None,
        country=None,
        state=None,
        city=None,
        zipcode=None,
        mobile=None
    ):

        if isinstance(first_name, dict):
            address = first_name

            first_name = address["first_name"]
            last_name = address["last_name"]
            company = address["company"]
            address1 = address["address1"]
            address2 = address["address2"]
            country = address["country"]
            state = address["state"]
            city = address["city"]
            zipcode = address["zipcode"]
            mobile = address["mobile"]

        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.COMPANY, company)

        self.fill(self.ADDRESS1, address1)
        self.fill(self.ADDRESS2, address2)

        self.page.select_option(
            self.COUNTRY,
            label=country
        )

        self.fill(self.STATE, state)
        self.fill(self.CITY, city)
        self.fill(self.ZIPCODE, zipcode)
        self.fill(self.MOBILE, mobile)

    # ============================================================
    # Button
    # ============================================================

    def create_account(self):
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def continue_account(self):
        self.click(self.CONTINUE_BUTTON)

    def delete_account(self):
        self.click(self.DELETE_ACCOUNT_BUTTON)