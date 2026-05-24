import os
import hashlib
import base64
import hmac


def hash_password(password: str) -> str:
	"""Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
	salt = os.urandom(16)
	dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
	return base64.b64encode(salt + dk).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
	data = base64.b64decode(hashed.encode('utf-8'))
	salt, dk = data[:16], data[16:]
	new_dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
	return hmac.compare_digest(new_dk, dk)
