from django.utils.module_loading import import_string

from .settings import MIDDLEWARE_LOGGERS


LOGGERS = []

for middleware_path in MIDDLEWARE_LOGGERS:
    LOGGERS.append(import_string(middleware_path))


class RequestLoggerMiddleware(object):

    def process_request(self, request):

        for logger_cls in LOGGERS:
            logger_cls.process_request(request)

    def process_response(self, request, response):

        for logger_cls in LOGGERS:
            logger_cls.process_response(request, response)

        return response



