from threading import local


_THREAD_LOCAL = local()
_THREAD_ATTR = 'logexpose'


def thread_get_logger(logger_alias):
    return getattr(_THREAD_LOCAL, _THREAD_ATTR, {}).get(logger_alias)


def thread_init_logger(logger_obj):
    registry = getattr(_THREAD_LOCAL, _THREAD_ATTR, None)

    if registry is None:
        registry = {}
        setattr(_THREAD_LOCAL, _THREAD_ATTR, registry)

    registry[logger_obj.alias] = logger_obj
    return logger_obj


def get_func_path(func):
    return '%s.%s' % (func.__module__, func.__name__)
