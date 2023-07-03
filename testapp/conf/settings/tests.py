from .base import *

DEBUG = True
SECRET_KEY = "django-insecure-84yhd3zo%(8r9!+xtqs34$7$)r#-8jd&i43-=lk-q9_nh%6y12"
ALLOWED_HOSTS = ["*"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "tests.sqlite3"),
    }
}

try:
    from .local import *
except ImportError:
    pass
