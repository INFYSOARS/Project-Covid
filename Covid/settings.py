"""
Django settings for Covid project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from logging import exception
from pathlib import Path
import os

try:
    import environ
    env = environ.Env()
    environ.Env.read_env()
    EMAIL_USER = env('email_user')
    EMAIL_PASS = env('email_pass')
    HEROKU_SECRET = env('heroku_secret')
    DB_USER = env('db_user')
    DB_PASS = env('db_pass')
    CELERY_URL = env('celery_url')
    print("LOCALHOST Is Setting Up The Environment Variables...!!!")
except:
    EMAIL_USER = os.environ.get("email_user")
    EMAIL_PASS = os.environ.get("email_pass")
    HEROKU_SECRET = os.environ.get("heroku_secret")
    DB_USER = os.environ.get("db_user")
    DB_PASS = os.environ.get("db_pass")
    CELERY_URL = os.environ.get("celery_url")
    print("WEBSERVER Is Setting Up The Environment Variables...!!!")

print("=========================== Welcome!, Team InfySoars Presents 'Project Covid' ==============================")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'staticfiles'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = HEROKU_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost','127.0.0.1','infysoars-project-covid.onrender.com']

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


ROOT_URLCONF = 'Covid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'Covid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#---------------------------------------------------------------------------------------------------------------------------------------------
# Added Manually

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Redis

# CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'


# RabbitMQ

# BROKER_URL = 'amqps://xwwclfrs:n8Dz-5ooraTsgcmm_Vsu8WzDPYNPHRsx@jackal.rmq.cloudamqp.com/xwwclfrs'
# RESULT_BACKEND = 'amqps://xwwclfrs:n8Dz-5ooraTsgcmm_Vsu8WzDPYNPHRsx@jackal.rmq.cloudamqp.com/xwwclfrs'
# BROKER_POOL_LIMIT = 1 # Will decrease connection usage
# BROKER_HEARTBEAT = None # We're using TCP keep-alive instead
# BROKER_CONNECTION_TIMEOUT = 30 # May require a long timeout due to Linux DNS timeouts etc
# RESULT_BACKEND = None # AMQP is not recommended as result backend as it creates thousands of queues
# EVENT_QUEUE_EXPIERS = 60 # Will delete all celeryev. queues without consumers after 1 minute.
# WORKER_PREFETCH_MULTIPLIER = 1 # Disable prefetching, it's causes problems and doesn't help performance
# WORKER_CONCURRENCY = 50 # If you tasks are CPU bound, then limit to the number of cores, otherwise increase substainally


CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("email_user")
EMAIL_HOST_PASSWORD = os.environ.get("email_pass")
EMAIL_PORT = 587
EMAIL_USER_SSL = False



# WKHTMLTOPDF_CMD = '/usr/local/bin/wkhtmltopdf'
