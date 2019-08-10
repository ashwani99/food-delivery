import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True # for debugging only

    JWT_SECRET_KEY = os.environ.get('FOOD_DELIVERY_SECRET') or 'a2425227c10583d2e55dc009bab731851ebeeba02b836eef'
    JWT_ACCESS_TOKEN_EXPIRES = False # for debugging only