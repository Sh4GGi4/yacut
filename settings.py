import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///yacut.sqlite3'
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'yacut-default-secret-key')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    DISK_API_URL = 'https://cloud-api.yandex.net/v1/'
