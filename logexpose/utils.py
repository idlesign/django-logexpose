from threading import local

try:
    from django.utils.module_loading import import_string as import_func
except ImportError:
    from django.utils.module_loading import import_by_path as import_func

from .settings import DATA_BACKEND, DATA_BACKEND_PARAMS


_THREAD_LOCAL = local()
_THREAD_ATTR_LOGGERS = 'logexpose_loggers'
_THREAD_ATTR_BACKENDS = 'logexpose_backends'


def import_class(cls_path):
    return import_func(cls_path)


def get_backend():
    return import_class(DATA_BACKEND).get_from_thread(DATA_BACKEND_PARAMS)


def thread_get_backend(alias):
    return thread_get_obj(_THREAD_ATTR_BACKENDS, alias)


def thread_get_logger(alias):
    return thread_get_obj(_THREAD_ATTR_LOGGERS, alias)


def thread_init_backend(alias, obj):
    return thread_init_obj(_THREAD_ATTR_BACKENDS, obj, alias)


def thread_init_logger(alias, obj):
    return thread_init_obj(_THREAD_ATTR_LOGGERS, obj, alias)


def thread_get_obj(attr_name, alias):
    return getattr(_THREAD_LOCAL, attr_name, {}).get(alias)


def thread_init_obj(attr_name, obj, alias):
    registry = getattr(_THREAD_LOCAL, attr_name, None)

    if registry is None:
        registry = {}
        setattr(_THREAD_LOCAL, attr_name, registry)

    registry[alias] = obj
    return obj


def get_func_path(func):
    return '%s.%s' % (func.__module__, func.__name__)
