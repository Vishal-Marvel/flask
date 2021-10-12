import credentials
from os import path as op
from dotenv import load_dotenv
from flask import url_for, request

dotenv_path = op.join(op.dirname(__file__), '.env')  # Path to .env file
load_dotenv(dotenv_path)

class Config:
    SQLALCHEMY_DATABASE_URI = credentials.sql #To hide password
    #Create the table from terminal (if using gitbash 'winpty python' to start python in git bash terminal)
    SECRET_KEY = credentials.key #To hide password
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECURITY_PASSWORD_SALT = 'aslkj909'
    SECURITY_PASSWORD_HALT = 'sha256_crypt'
    SECURITY_SEND_REGISTER_EMAIL = False
    PYTHONDONTWRITEBYTECODE=1

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'autostock2021@gmail.com'
    MAIL_PASSWORD = 'autostock@123'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'autostock2021@gmail.com'

