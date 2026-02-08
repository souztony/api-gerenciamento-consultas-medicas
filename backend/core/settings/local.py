"""
Local development settings
"""

from .base import *  # noqa: F403

# Override settings for local development
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# You can override database settings here if needed
# For example, to use SQLite locally:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# CORS settings for local development (if using CORS)
CORS_ALLOW_ALL_ORIGINS = True

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
