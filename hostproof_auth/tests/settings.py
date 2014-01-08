DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                      # Or path to database file if using sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^n4-$%m-w((n4=7g4j!(x3%=l68t=__j!24-3)0%bjd8i2e5th'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'hostproof_auth.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'hostproof_auth',
)

AUTH_USER_MODEL = 'hostproof_auth.User'

AUTHENTICATION_BACKENDS = (
    'hostproof_auth.auth.ModelBackend',
)
