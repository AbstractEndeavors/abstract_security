from .imports import getpass,bcrypt,secrets,string as _string

def generate_salt(rounds=None):
    rounds = rounds or 10
    salt = bcrypt.gensalt(rounds=rounds)
    return salt


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.
    """
    if not password or not hashed:
        return False

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except ValueError:
        # invalid hash format
        return False
    
def bcrypt_plain_text(plaintext_pwd,rounds=None):
    salt = generate_salt(rounds=rounds)
    plaintext_pwd = plaintext_pwd.encode("utf-8")
    encrypted_bcrypt_hash = bcrypt.hashpw(plaintext_pwd,salt)
    bcrypt_hash = encrypted_bcrypt_hash.decode("utf-8")
    return bcrypt_hash


def hash_password(password: str, rounds: int = 12) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    salt = bcrypt.gensalt(rounds=rounds)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def generate_password(length=16) -> str:
    alphabet = _string.ascii_letters + _string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
