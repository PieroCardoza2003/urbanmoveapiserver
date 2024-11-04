import jwt
from config import SECRET_AT, SECRET_RT
from utils.datetime_utils import datetime_now, datetime_limit


def create_jwt(payload, secret):
    return jwt.encode(payload, secret, algorithm="HS256")


def get_access_token(id: str):
    payload = {
        "sub": str(id),
        "exp": datetime_limit(15), # 15m
        "iat": datetime_now()
    }
    token = create_jwt(payload=payload, secret=SECRET_AT)
    return (payload, token)


def get_refresh_token(id: str):
    payload = {
        "sub": str(id),
        "exp": datetime_limit(30 * 24 * 60), # 30d
        "iat": datetime_now()
    }
    token = create_jwt(payload=payload, secret=SECRET_RT)
    return (payload, token)


def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_RT, algorithms=["HS256"])
        return payload
    except:
        return None
