import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


# --- Sécurité -----------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me-in-production")
DEBUG = env_bool("DEBUG", False)

# '.wasmer.app' = tous les sous-domaines *.wasmer.app
ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".wasmer.app"]
extra_hosts = os.environ.get("EXTRA_ALLOWED_HOSTS", "")
ALLOWED_HOSTS += [h.strip() for h in extra_hosts.split(",") if h.strip()]

# Indispensable derrière le proxy HTTPS de Wasmer, sinon les POST (formulaires)
# renvoient "403 CSRF verification failed".
CSRF_TRUSTED_ORIGINS = ["https://*.wasmer.app"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- Applications -------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Wasmer attend une variable publique nommée `app` dans config/wsgi.py
WSGI_APPLICATION = "config.wsgi.app"

# --- Base de données ----------------------------------------------------
# Sur Wasmer Edge, la base MySQL est injectée via DB_HOST / DB_PORT / DB_NAME /
# DB_USERNAME / DB_PASSWORD. Le port n'est PAS 3306 : toujours lire DB_PORT.
# En local, sans DB_HOST, on retombe sur SQLite pour pouvoir lancer le projet
# sans installer MySQL (mettre USE_SQLITE=0 + DB_* pour tester avec MySQL).
if os.environ.get("DB_HOST") and not env_bool("USE_SQLITE", False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ.get("DB_USERNAME") or os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- i18n ---------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques (WhiteNoise) ------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Sert les statiques (dont ceux de l'admin) même si collectstatic n'a pas été lancé.
WHITENOISE_USE_FINDERS = True

# --- Logs vers la console (visibles dans les logs Wasmer) ----------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
