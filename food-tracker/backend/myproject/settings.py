from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', os.getenv('FOOD_SECRET_KEY', 'django-insecure--CHANGE-ME-IN-PRODUCTION--replace-with-secure-key!!'))
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_framework',
    'corsheaders',
    'food_tracker',
]
SITE_ID = 1
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
ROOT_URLCONF = 'myproject.urls'
TEMPLATES = [{ 'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': { 'context_processors': ['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'myproject.wsgi.application'
# Shared DB with HT3 (habits-app) for unified auth: uses same postgres as HT3 when FOOD vars point to db
if os.getenv('FOOD_DB_HOST'):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('FOOD_DB_NAME', os.getenv('DB_NAME', 'habittracker')), 'USER': os.getenv('FOOD_DB_USER', os.getenv('DB_USER', 'ht_user')), 'PASSWORD': os.getenv('FOOD_DB_PASSWORD', os.getenv('DB_PASSWORD', 'ht_password')), 'HOST': os.getenv('FOOD_DB_HOST', 'db'), 'PORT': os.getenv('FOOD_DB_PORT', '5432')}}
elif os.getenv('DB_HOST'):
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('DB_NAME', 'habittracker'), 'USER': os.getenv('DB_USER', 'ht_user'), 'PASSWORD': os.getenv('DB_PASSWORD', 'ht_password'), 'HOST': os.getenv('DB_HOST', 'db'), 'PORT': os.getenv('DB_PORT', '5432')}}
else:
    # Fallback for local dev without docker (keeps sqlite)
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'}]
LANGUAGE_CODE='ru-ru'
TIME_ZONE='Europe/Moscow'
USE_I18N=True
USE_TZ=True
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.SessionAuthentication'],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated']}
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS','http://localhost:5173,http://localhost:3000,http://habits-app.ru.local,https://habits-app.ru').split(',')
CORS_ALLOW_CREDENTIALS = True
# Proxy / CSRF for nginx
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://habits-app.ru,https://www.habits-app.ru,http://habits-app.ru.local,http://localhost:8002,http://localhost:5173').split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = False
# Shared session with HT3
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_AGE = 1209600
CSRF_COOKIE_NAME = "csrftoken"
ACCOUNT_EMAIL_VERIFICATION='none'
ACCOUNT_AUTHENTICATION_METHOD='username_email'
ACCOUNT_EMAIL_REQUIRED=False
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL='/food-tracker/'
