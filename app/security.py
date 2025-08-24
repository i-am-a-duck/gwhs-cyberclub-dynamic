import pyotp
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(pwhash: str, password: str) -> bool:
    return check_password_hash(pwhash, password)

def new_totp_secret() -> str:
    return pyotp.random_base32()

def verify_totp(secret: str, token: str) -> bool:
    try:
        return pyotp.TOTP(secret).verify(token, valid_window=1)
    except Exception:
        return False
