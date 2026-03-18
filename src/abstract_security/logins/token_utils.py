from .imports import (
    add_delta,
    get_env_value,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_SECONDS
    )

def get_token_exp(seconds=None):
    return add_delta(seconds=seconds or JWT_EXP_DELTA_SECONDS)

def get_app_secret():
    APP_SECRET = get_env_value("JWT_SECRET")
    if not APP_SECRET:
        raise RuntimeError("JWT_SECRET environment variable is required")
    return APP_SECRET

def generate_token(**payload) -> str:
    payload["exp"]= payload.get("exp",get_token_exp())
    return jwt.encode(payload, get_app_secret(), algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    app_secret = get_app_secret()
    return jwt.decode(token, app_secret, algorithms=[JWT_ALGORITHM])

def generate_user_token(username: str=None,
                        is_admin: bool=None,
                        exp:int=None) -> str:
    token_js = {"username": username or 'guest',
                "is_admin": is_admin or False,
                "exp":exp or get_token_exp()}
    return generate_token(**token_js)

def generate_download_token(username: str =None,
                            rel_path: str =None,
                            exp:int=None) -> str:
    token_js = {"sub": username,
                "path": rel_path,
                "exp":exp or get_token_exp()}

    return generate_token(**token_js)

