"""
Production settings — PostgreSQL, DEBUG off, strict security.
"""
from .base import *  # noqa: F401, F403
from decouple import config

DEBUG = False

# ─── Database (PostgreSQL) ────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# ─── Security ─────────────────────────────────────────────────────────────────

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# ─── Static files (served by nginx / CDN in prod) ─────────────────────────────

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# ─── CORS ─────────────────────────────────────────────────────────────────────

# model_viewer_plus WebView sends requests from http://localhost:<random-port>.
# We can't predict that origin, so allow all for media/.glb delivery.
CORS_ALLOW_ALL_ORIGINS = True
