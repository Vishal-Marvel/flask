from datetime import datetime, timedelta
import socket
import smtplib
import random
import math
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app import app, mail

def generate_random():
    n = math.floor(random.random()*1000000)
    return str(n)


def send_mail(to_mail, code):
    subject = f"Verification code:{code}"
    message = "Subject:" + subject + "\n\n" + f'Enter the below code to get verification\n{code}'
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('autostock2021@gmail.com', 'autostock@123')
        server.sendmail('autostock2021@gmail.com', to_mail, message)
        server.quit()
    except socket.gaierror:
        pass

def set_activation_limt():
    now = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    h = timedelta(minutes=60)
    return now + h
        
def send_email(to, template):
    msg = Message(
        subject="Verification",
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


