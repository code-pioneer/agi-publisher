import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
#environ.Env.read_env(env_file=f'{BASE_DIR}/.env')
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'),overwrite=True)

SECRET_KEY = 'django-insecure-9n-#a+j7w6fc9li$q%x%s4+cz&z3q=%8k_6rye%*vlm58!6wzf'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'home',
    'blog',
    'videos'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mainapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),'/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainapp.wsgi.application'
ASGI_APPLICATION = 'mainapp.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


TIME_ZONE = 'America/New_York'

STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'none'

LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = False
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ], 
        'AUTH_PARAMS': {
            'access_type':'offline',
        }
    }
}

DEBUG = env("DEBUG", default=False)

LLM_MODEL = env("LLM_MODEL", default=None)
OPENAI_API_KEY  = env("OPENAI_API_KEY",default=None)
STREAMING = True

IMAGE_GEN_MODEL = env("IMAGE_GEN_MODEL", default=None)
SIZE = env("IMAGE_SIZE", default="1024x1024")

SERPER_API_KEY = env("SERPER_API_KEY",default=None)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

NUM_OF_SEARCHES= env("NUM_OF_SEARCHES",default="3")
SHORT_VIDEO_SIZE= int(env("SHORT_VIDEO_SIZE",default="60"))
LONG_VIDEO_SIZE= int(env("LONG_VIDEO_SIZE",default="300"))