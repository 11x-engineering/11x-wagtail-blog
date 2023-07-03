from .base import *

LOCAL_DIR = os.path.join(
    os.path.dirname(BASE_DIR),
    ".local"
)
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR, exist_ok=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-84yhd3zo%(8r9!+xtqs34$7$)r#-8jd&i43-=lk-q9_nh%6y12"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(LOCAL_DIR, "dev.sqlite3"),
    }
}


try:
    from .local import *
except ImportError:
    pass
