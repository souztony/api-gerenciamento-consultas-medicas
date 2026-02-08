"""
Django settings for backend project.

This file now acts as the entry point for environment-specific settings.
Set the DJANGO_SETTINGS_MODULE environment variable to:
- backend.core.settings.local (for development)
- backend.core.settings.staging (for staging)
- backend.core.settings.production (for production)

For backward compatibility, this file imports from local settings by default.
"""

import os

# Determine which settings module to use
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'backend.core.settings.local')

# Import the appropriate settings
if 'backend.core.settings.local' in settings_module:
    from backend.core.settings.local import *  # noqa: F403
elif 'backend.core.settings.staging' in settings_module:
    from backend.core.settings.staging import *  # noqa: F403
elif 'backend.core.settings.production' in settings_module:
    from backend.core.settings.production import *  # noqa: F403
else:
    # Default to local if not specified
    from backend.core.settings.local import *  # noqa: F403
    print("Warning: DJANGO_SETTINGS_MODULE not properly set. Using local settings.")
