from uuid import uuid4
from collections import deque
from threading import current_thread

from django.utils.translation import gettext as _
from django.utils import timezone

from ..utils import thread_get_logger, thread_init_logger, get_func_path, get_backend


_PARENT_AUTO = object()
_BACKEND = get_backend()


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

    def pick_grp_id(self, grp_id=None):
        return grp_id or self.grp_id or self.generate_grp_id()

    def _put(self, lvl, msg, grp_id, msg_id, parent_msg_id, props):

        if msg_id is None:
            msg_id = self.generate_msg_id()

        if props is None:
            props = {}

        if parent_msg_id is _PARENT_AUTO:
            parent_msg_id = self.get_parent_msg_id()

        grp_id = self.pick_grp_id(grp_id)

        _BACKEND.put({
            'time': timezone.now(),
            'logger': self.alias,
            'lvl': lvl,
            'msg': msg,
            'gid': grp_id,
            'mid': msg_id,
            'pid': parent_msg_id,
            'props': props
        })

        return grp_id, msg_id, parent_msg_id

    def debug(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._put('debug', msg, grp_id, msg_id, parent_msg_id, props)

    def info(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._put('info', msg, grp_id, msg_id, parent_msg_id, props)

    def warning(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._put('warning', msg, grp_id, msg_id, parent_msg_id, props)

    def error(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._put('error', msg, grp_id, msg_id, parent_msg_id, props)

    def critical(self, msg, grp_id=None, msg_id=None, props=None, parent_msg_id=_PARENT_AUTO):
        return self._put('critical', msg, grp_id, msg_id, parent_msg_id, props)

    def get_parent_msg_id(self):
        try:
            return self.stack[-1]
        except IndexError:
            return None

    def get_level_method(self, level):
        return getattr(self, level)

    def default_func_before(self, func, fargs, fkwargs, level, ids_tuple):
        grp_id, msg_id, parent_msg_id = ids_tuple

        thread = current_thread()
        ids_tuple = self.get_level_method(level)(
            'Before `%s`' % get_func_path(func),
            grp_id=grp_id,
            msg_id=msg_id,
            parent_msg_id=parent_msg_id,
            props={
                'args': [type(a) for a in fargs],
                'kwargs': {k: type(v) for k, v in fkwargs.items()},
                'thread': '%s (%s)' % (thread.name, thread.ident)
            }
        )

        return ids_tuple

    def default_func_after(self, func, fargs, fkwargs, level, ids_tuple):
        grp_id, __, parent_msg_id = ids_tuple

        ids_tuple = self.get_level_method(level)(
            'After `%s`' % get_func_path(func),
            grp_id=grp_id,
            parent_msg_id=parent_msg_id
        )

        return ids_tuple

    @classmethod
    def get_from_thread(cls, *args, **kwargs):
        alias = cls.alias
        return thread_get_logger(alias) or thread_init_logger(alias, cls(*args, **kwargs))

    @classmethod
    def process_request(cls, request):
        pass

    @classmethod
    def process_response(cls, request, response):
        pass
