import random
from utils.datetime_utils import datetime_limit, datetime_unix, datetime_now

activate_users = {}

def prints_users():
    print(activate_users)

def set_activate_user(email: str, code: str):
    activate_users[email] = {
        'code': code,
        'exp': datetime_unix(datetime_limit(5)) # el codigo expira en 5 minutos
    }


def validate_code(email: str, code: str) -> bool:
    now = datetime_unix(datetime_now())
    try:
        user = activate_users[email]
        if user['code'] == code and now <= user['exp']:
            del activate_users[email]
            return True
        return False
    except:
        return False


def clearDataStore():
    now = datetime_unix(datetime_now())
    for email, data in activate_users.items():
        if now > data['exp']:
            del activate_users[email]


def generate_random_code() -> str:
    number = random.randint(0, 99999)
    return f"{number:05d}"