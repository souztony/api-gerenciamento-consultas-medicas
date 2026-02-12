"""
Staging environment settings
"""

from .base import *  # noqa: F403

# Security settings for staging
DEBUG = config("DEBUG", default=False, cast=bool)  # noqa: F405

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())  # noqa: F405

# Force HTTPS in staging
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS settings for staging
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="", cast=Csv())  # noqa: F405

# Logging configuration for staging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
