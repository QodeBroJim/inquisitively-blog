import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com', 'inquisitively.io', 'www.inquisitively.io',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    #whitenoise for static file management during development
    'whitenoise.runserver_nostatic',

    # my created apps
    'marketing',
    'posts',

    #third-party apps
    'allauth', # sign up
    'allauth.account', # login / logout
    'allauth.socialaccount', #authentication through social media
    
    'allauth.socialaccount.providers.discord', # discord authentication
    'allauth.socialaccount.providers.facebook', # fb authentication
    'allauth.socialaccount.providers.github', # github authentication
    'allauth.socialaccount.providers.google', # google authentication
    'allauth.socialaccount.providers.pinterest', # pinterest authentication
    'allauth.socialaccount.providers.reddit', # reddit authentication
    'allauth.socialaccount.providers.tumblr', # stackexchange authentication
    'allauth.socialaccount.providers.twitch', # twitch authentication
    'allauth.socialaccount.providers.twitter', # twitter authentication
    
    'ckeditor', # rich text editor - similar to tinyMCE but was much easier to integrate
    'ckeditor_uploader', #built in media upload tools

    'crispy_forms', # bootstrap 4 form styling

    'django_social_share', # app to implement sharing content via social media sites

    'taggit', #similar to categories; adds more SEO to the site
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#Override SQLite3 with PostgreSQL inside Heroku 
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_in_env'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_in_env', 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static_in_env', 'media-root')

# S3 Storage for Media Uploads
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
AWS_REGION  = 'us-west-1'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = 'inquisitively'
AWS_S3_ADDRESSING_STYLE = 'auto'
AWS_S3_BUCKET_AUTH = False
AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365 # 1 year.
AWS_S3_ENCRYPT_KEY = False
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

# MailChimp
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = "us3"
MAILCHIMP_EMAIL_LIST_ID = os.environ.get('MAILCHIMP_EMAIL_LIST_ID')

# CKeditor
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'width':'auto',
        'height':'500px',
        'toolbar': None,
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': '100%',
        'extraPlugins': ','.join([
            'codesnippet', 'widget', 'lineutils'
        ]),
    }
}

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django-allauth
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_USERNAME_REQUIRED = False
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = 'james@inquisitively.io'
DEFAULT_FROM_EMAIL = 'registration@inquisitively.io'
EMAIL_FROM = 'registration@inquisitively.io'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[Inquisitively] '

ACCOUNT_FORMS = {
    'signup': 'posts.forms.CustomSignupForm',
}

SOCIALACCOUNT_PROVIDERS =  { 'facebook':
                               {'METHOD': 'oauth2',
                                'SCOPE': ['email'],
                                'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
                                'LOCALE_FUNC': lambda request: 'en_US',
                                'VERSION': 'v2.4'
                               },
                            'google': 
                                { 'SCOPE': ['email'],
                                'AUTH_PARAMS': { 'access_type': 'online' }
                                },
                             'pinterest': 
                                {
                                'SCOPE': ['read_public', 'read_relationships',]
                                }
                           }

# Let's Encrypt
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True