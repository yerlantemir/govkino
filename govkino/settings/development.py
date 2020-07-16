from .base import *     # noqa: F403


SECRET_KEY = os.environ.get('SECRET_KEY', 'development')    # noqa: F405

DEBUG = True

INSTALLED_APPS += [     # noqa: F405
    'django_extensions',
]
