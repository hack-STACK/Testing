import os
from pathlib import Path

BASE_URL = "https://automationexercise.com"
LOGIN_URL = f"{BASE_URL}/login"
PRODUCTS_URL = f"{BASE_URL}/products"
CART_URL = f"{BASE_URL}/view_cart"

TIMEOUT = 10000

BROWSER = "msedge"
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

USERS_FILE = DATA_DIR / "users.json"
REGISTER_DATA_FILE = DATA_DIR / "register_data.json"