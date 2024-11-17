import os
from dotenv import load_dotenv

load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE")
SERVICE_EMAIL = os.getenv("SERVICE_EMAIL")
SERVICE_EMAIL_SECRET = os.getenv("SERVICE_EMAIL_SECRET")
SECRET_AT = os.getenv("SECRET_AT")
SECRET_RT = os.getenv("SECRET_RT")
GOOGLE_ID_CLIENT = os.getenv("GOOGLE_ID_CLIENT")
SECRET_GITHUB = os.getenv("SECRET_GITHUB")
REPO_GITHUB = os.getenv("REPO_GITHUB")
BRANCH_GITHUB = os.getenv("BRANCH_GITHUB")
DIRECTORY_GITHUB = os.getenv("DIRECTORY_GITHUB")
API_URL_GITHUB = os.getenv("API_URL_GITHUB")