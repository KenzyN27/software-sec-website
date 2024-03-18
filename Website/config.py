from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
WTF_CSRF_ENABLED = True
DEBUG = False
BCRYPT_LOG_ROUNDS = int(environ.get('BCRYPT_LOG_ROUNDS'))