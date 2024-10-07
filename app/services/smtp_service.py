import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SERVICE_EMAIL, SERVICE_EMAIL_SECRET
from utils.templete_utils import templeate_email
from services.activate_user_service import set_activate_user


def send_email(subject: str, body: str, to_email: str):
    smtp_email = SERVICE_EMAIL
    smtp_secret = SERVICE_EMAIL_SECRET
    
    message = MIMEMultipart()
    message['From'] = smtp_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_secret)
            server.sendmail(smtp_email, to_email, message.as_string())
        return
    except Exception:
        return


def send_verifycode(asunto: str, email: str, code: str):
    # se envia un email con el codigo de verificacion
    send_email(subject=asunto, body=templeate_email(code), to_email=email)
    # se añade a la lista en espera de verificacion
    set_activate_user(email=email, code=code)
