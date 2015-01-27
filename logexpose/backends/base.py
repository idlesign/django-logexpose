from json import dumps

from ..utils import thread_get_backend, thread_init_backend


class BaseDataBackend(object):

    default_params = None

    def __init__(self, params):
        """"""

    @classmethod
    def prepare_props(cls, props):
        return dumps(props, default=lambda o: repr(o))

    @classmethod
    def get_from_thread(cls, params):
        alias = cls.__name__
        return thread_get_backend(alias) or thread_init_backend(alias, cls(params or cls.default_params or {}))
