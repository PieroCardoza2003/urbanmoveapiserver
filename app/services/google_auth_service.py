from google.oauth2 import id_token
from google.auth.transport import requests
from config import GOOGLE_ID_CLIENT

def verify_token(token):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_ID_CLIENT)

        name_user = id_info['given_name']
        email_user = id_info['email']

        if not name_user or not email_user:
            return None
        return (name_user, email_user)
    
    except Exception:
        return None

