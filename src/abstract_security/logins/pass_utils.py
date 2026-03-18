from .imports import getpass,bcrypt

def generate_salt(rounds=None):
    rounds = rounds or 10
    salt = bcrypt.gensalt(rounds=rounds)
    return salt

def verify_password(raw_pwd: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(raw_pwd.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False
    
def verify_stored_password(plaintext_pwd: str, stored_hash: str) -> bool:
    """
    Returns True if plaintext matches the bcrypt stored_hash, else False.
    If the stored_hash isn’t a valid bcrypt hash, logs and returns False.
    """
    if not plaintext_pwd or not stored_hash:
        return False
    try:
        return bcrypt.checkpw(
            plaintext_pwd.encode("utf8"),
            stored_hash.encode("utf8")
        )
    except ValueError as e:
        # invalid salt or hash format
        logging.error("Invalid bcrypt hash in DB: %s", e)
        return False
    
def bcrypt_plain_text(plaintext_pwd,rounds=None):
    salt = generate_salt(rounds=rounds)
    plaintext_pwd = plaintext_pwd.encode("utf-8")
    encrypted_bcrypt_hash = bcrypt.hashpw(plaintext_pwd,salt)
    bcrypt_hash = encrypted_bcrypt_hash.decode("utf-8")
    return bcrypt_hash





