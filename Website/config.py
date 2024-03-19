from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
WTF_CSRF_ENABLED = True
DEBUG = False
SESSION_PERMANENT = False
BCRYPT_LOG_ROUNDS = int(environ.get('BCRYPT_LOG_ROUNDS'))