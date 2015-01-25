from functools import wraps

from .utils import thread_get_logger, get_func_path
from .exceptions import LoggerNotRegistered


def logexpose(logger_alias, func_before=None, func_after=None, level='debug'):
    def wrapper(func):
        @wraps(func)
        def faked(*args, **kwargs):

            logger = thread_get_logger(logger_alias)
            if logger is None:
                raise LoggerNotRegistered(
                    'Function `%s` tried to use an unregistered `%s` logger.' % (get_func_path(func), logger_alias)
                )

            func_before_real = func_before or getattr(logger, 'default_func_before', None)
            func_after_real = func_after or getattr(logger, 'default_func_after', None)

            grp_id = None
            msg_id = logger.generate_msg_id()
            parent_msg_id = logger.get_parent_msg_id()

            logger.stack.append(msg_id)

            try:
                if func_before_real:
                    grp_id = func_before_real(
                        func=func, fargs=args, fkwargs=kwargs, level=level,
                        ids_tuple=(None, msg_id, parent_msg_id)
                    )[0]

                result = func(*args, **kwargs)

                if func_after_real:
                    func_after_real(
                        func=func, fargs=args, fkwargs=kwargs, level=level,
                        ids_tuple=(grp_id, None, parent_msg_id)
                    )

            finally:
                logger.stack.pop()

            return result
        return faked

    return wrapper
