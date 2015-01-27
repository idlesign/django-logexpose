from django.conf import settings

# Data backend class.
DATA_BACKEND = getattr(settings, 'LOGEXPOSE_DATA_BACKEND', 'logexpose.backends.database.DatabaseBackend')

# Data backend initialization parameters.
DATA_BACKEND_PARAMS = getattr(settings, 'LOGEXPOSE_DATA_BACKEND_PARAMS', None)

# Loggers activated by middleware.
MIDDLEWARE_LOGGERS = getattr(settings, 'LOGEXPOSE_MIDDLEWARE_LOGGERS', (
    'logexpose.loggers.request.RequestLogger',
    'logexpose.loggers.process.ProcessLogger',
))
