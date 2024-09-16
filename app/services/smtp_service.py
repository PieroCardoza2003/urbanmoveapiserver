import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SERVICE_EMAIL, SERVICE_EMAIL_SECRET

def send_email(subject: str, body: str, to_email: str) -> bool:
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
        return True
    except Exception:
        return False


#send_email("Activacion de su cuenta", "<html><body><p>Introduzaca el codigo 12345 para activar su cuenta.</p></body></html>", "pierocardozazapata@gmail.com")




