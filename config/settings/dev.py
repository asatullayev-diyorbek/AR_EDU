"""
Development settings — SQLite, DEBUG on, relaxed security.
"""
from .base import *  # noqa: F401, F403
from decouple import config

DEBUG = True

# ─── Database ─────────────────────────────────────────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# ─── CORS (dev: allow all) ────────────────────────────────────────────────────

CORS_ALLOW_ALL_ORIGINS = True

# ─── DRF — also expose BrowsableAPI in dev ────────────────────────────────────

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# ─── Dev email backend ────────────────────────────────────────────────────────

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
