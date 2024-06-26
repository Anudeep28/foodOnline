"""
Django settings for mainSite project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
# to store env variable
from decouple import config
# Django messages in the template
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')#'django-insecure-3-$@n$rv-%#-w^bkqc=zxr*n@tjzh+(7m!w&rw9tomjon_e5mr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)#True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'accounts',
    'vendor',
    'menu',
    'marketplace',
    'customers',
    'orders',

    # Location field 
    'django.contrib.gis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # To add our own context for all html pages
                'accounts.context_processors.get_restaurant',
                # Customer profile context processor
                'accounts.context_processors.get_customer_profile',
                # this is for Google api key
                'accounts.context_processors.get_google_api_key',
                # this is for Google api key
                'accounts.context_processors.get_paypal_api_key',
                # To add our own context for cart counter
                # This is present in all templates now the value
                'marketplace.context_processors.get_cart_counter',
                # This is to get the cart total vlaue
                'marketplace.context_processors.get_cart_amount',
            ],
        },
    },
]

WSGI_APPLICATION = 'mainSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # commenting out to use postgis
        #'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME'),#'foodonline_db',
        'USER':config('DB_USER'),#'postgres',
        'PASSWORD':config('DB_PASSWORD'),#'Onepiece@28',
        'HOST':config('DB_HOST'),#'localhost',
        'PORT':config('DB_PORT')#5432
    }
}

# Custome USer model 
AUTH_USER_MODEL = 'accounts.User'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [
    'static'
]
# Media URL
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Django Messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


# Logout redirect url for admin page
LOGOUT_REDIRECT_URL = '/accounts/userLogin/'




# Email Configuration in django very important
EMAIL_HOST=config('EMAIL_HOST')#'smtp.outlook.com'
EMAIL_PORT=config('EMAIL_PORT', cast=int)#587
EMAIL_HOST_USER=config('EMAIL_HOST_USER') #'eneru_solutions@outlook.com'
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')  #'tdiwtegtwpvnefqd'
EMAIL_USE_TLS=True
EMAIL_BACKEND=config('EMAIL_BACKEND') #'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')#'Eneru Technologies <eneru_solutions@outlook.com>'


# Adding Google maps api keys
GOOGLE_API_KEY=config('GOOGLE_API_KEY')



# GDAL services
os.environ['PATH'] = os.path.join(BASE_DIR, 'myenv\Lib\site-packages\osgeo') + ';' + os.environ['PATH']
os.environ['PROJ_LIB'] = os.path.join(BASE_DIR, 'myenv\Lib\site-packages\osgeo\data\proj') + ';' + os.environ['PATH']
GDAL_LIBRARY_PATH = os.path.join(BASE_DIR, 'myenv\Lib\site-packages\osgeo\gdal304.dll')


# For paypal gateways
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')

# to securing cross origins
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

# RazorPay key id
RZP_KEY_ID = config('RZP_KEY_ID')
RZP_KEY_SECRET = config('RZP_KEY_SECRET')