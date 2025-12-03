import os


class Config:
    SECRET_KEY = "rahasia_banget"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://webuser:Password123!@localhost/web_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False