from uuid import uuid4
from json import dumps
from collections import deque

from django.utils.translation import gettext as _

from ..utils import thread_get_logger, thread_init_logger, get_func_path


_PARENT_AUTO = object()


class BaseLogger(object):

    alias = 'base'
    title = _('Base Logger')

    def __init__(self, grp_id=None):
        if grp_id is None:
            grp_id = self.generate_grp_id()
        self.grp_id = grp_id
        self.stack = deque()

    def generate_grp_id(self):
        return 'default'

    def generate_msg_id(self):
        return str(uuid4())

    def pick_grp_id(self, grp_id):
        return grp_id or self.grp_id or self.generate_grp_id()

    def _store(self, lvl, msg, grp_id, msg_id, parent_msg_id, props):

        if msg_id is None:
            msg_id = self.generate_msg_id()

        if props is None:
            props = {}

        if parent_msg_id is _PARENT_AUTO:
            parent_msg_id = self.get_parent_msg_id()

        grp_id = self.pick_grp_id(grp_id)

        d = {
            'lvl': lvl,
            'msg': msg,
            'id': msg_id,
            'pid': parent_msg_id,
            'gid': grp_id,
            'logger': self.alias,
            'props': props
        }
        json = dumps(d, default=lambda o: repr(o))
        print(json)

        return grp_id, msg_id, parent_msg_id

    def debug(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._store('debug', msg, grp_id, msg_id, parent_msg_id, props)

    def info(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._store('info', msg, grp_id, msg_id, parent_msg_id, props)

    def warning(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._store('warning', msg, grp_id, msg_id, parent_msg_id, props)

    def error(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._store('error', msg, grp_id, msg_id, parent_msg_id, props)

    def critical(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._store('critical', msg, grp_id, msg_id, parent_msg_id, props)

    def get_parent_msg_id(self):
        try:
            return self.stack[-1]
        except IndexError:
            return None

    def get_level_method(self, level):
        return getattr(self, level)

    def default_func_before(self, func, fargs, fkwargs, level, ids_tuple):
        grp_id, msg_id, parent_msg_id = ids_tuple

        ids_tuple = self.get_level_method(level)(
            'Before `%s`' % get_func_path(func),
            grp_id=grp_id,
            msg_id=msg_id,
            parent_msg_id=parent_msg_id,
            props={'args': fargs, 'kwargs': fkwargs}
        )

        return ids_tuple

    def default_func_after(self, func, fargs, fkwargs, level, ids_tuple):
        grp_id, __, parent_msg_id = ids_tuple

        self.get_level_method(level)(
            'After `%s`' % get_func_path(func),
            grp_id=grp_id,
            parent_msg_id=parent_msg_id
        )

    @classmethod
    def get_from_thread(cls, *args, **kwargs):
        logger = thread_get_logger(cls.alias)
        if logger is None:
            logger = thread_init_logger(cls(*args, **kwargs))
        return logger

    @classmethod
    def process_request(cls, request):
        pass

    @classmethod
    def process_response(cls, request, response):
        pass
