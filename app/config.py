import os
from dotenv import load_dotenv

load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE")
SERVICE_EMAIL = os.getenv("SERVICE_EMAIL")
SERVICE_EMAIL_SECRET = os.getenv("SERVICE_EMAIL_SECRET")
