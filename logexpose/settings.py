from django.conf import settings

# Data backend class.
DATA_BACKEND = getattr(settings, 'LOGEXPOSE_DATA_BACKEND', 'logexpose.backends.cache.CacheBackend')

# Data backend name (as in CACHES or DATABASES of settings.py)
DATA_BACKEND_NAME = getattr(settings, 'LOGEXPOSE_DATA_BACKEND_NAME', 'logexpose')

# Loggers activated by middleware.
MIDDLEWARE_LOGGERS = getattr(settings, 'LOGEXPOSE_MIDDLEWARE_LOGGERS', (
    'logexpose.loggers.request.RequestLogger',
    'logexpose.loggers.process.ProcessLogger',
))
