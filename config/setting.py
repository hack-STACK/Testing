from pathlib import Path

BASE_URL = "https://automationexercise.com"
LOGIN_URL = f"{BASE_URL}/login"
PRODUCTS_URL = f"{BASE_URL}/products"
CART_URL = f"{BASE_URL}/view_cart"

TIMEOUT = 10000

BROWSER = "msedge"
HEADLESS = False

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RUNTIME_DIR = BASE_DIR / "runtime"

USERS_FILE = DATA_DIR / "users.json"
REGISTER_DATA_FILE = DATA_DIR / "register_data.json"
RUNTIME_USER_FILE = RUNTIME_DIR / "latest_user.json"