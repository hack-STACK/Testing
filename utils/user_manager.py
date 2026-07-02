from pathlib import Path

from config.setting import RUNTIME_DIR, RUNTIME_USER_FILE
from utils.data_reader import load_json, save_json


def _ensure_runtime_dir() -> None:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def save_login_user(email, password):

    _ensure_runtime_dir()

    users = {
        "users": [
            {
                "email": email,
                "password": password,
                "expected": "success"
            },
            {
                "email": email,
                "password": "PasswordSalah",
                "expected": "failed"
            }
        ]
    }

    save_json(RUNTIME_USER_FILE, users)


def load_users():
    _ensure_runtime_dir()

    if not Path(RUNTIME_USER_FILE).exists():
        save_json(RUNTIME_USER_FILE, {"users": []})

    return load_json(RUNTIME_USER_FILE)
