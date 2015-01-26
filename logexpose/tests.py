from django.test import TestCase, RequestFactory
from django.http.response import HttpResponse

from .loggers.base import BaseLogger
from .loggers.request import RequestLogger
from .loggers.process import ProcessLogger
from .utils import thread_get_logger, thread_init_logger, get_func_path, _THREAD_LOCAL
from .toolbox import get_logger
from .decorators import logexpose as logexpose_decor
from .middleware import RequestLoggerMiddleware
from .exceptions import LoggerNotRegistered


LEVELS = ('debug', 'info', 'warning', 'error', 'critical')


def test_func(a, b=10, d=66):
    return a


class LogexposeTestCase(TestCase):

    def tearDown(self):
        # Cleaning.
        try:
            delattr(_THREAD_LOCAL, 'logexpose')
        except AttributeError:
            pass


class BaseLoggerTest(LogexposeTestCase):

    def test_grp_id(self):
        logger_1 = BaseLogger()
        self.assertEqual(logger_1.grp_id, 'default')

        logger_2 = BaseLogger(grp_id=33)
        self.assertEqual(logger_2.grp_id, 33)

        grp_id = logger_1.pick_grp_id()
        self.assertEqual(grp_id, 'default')

        grp_id = logger_2.pick_grp_id()
        self.assertEqual(grp_id, 33)

    def test_msg_id(self):
        logger_1 = BaseLogger()
        self.assertIsNotNone(logger_1.generate_msg_id())

    def test_level_method(self):
        logger_1 = BaseLogger()
        self.assertEqual(logger_1.get_level_method('debug'), logger_1.debug)
        self.assertEqual(logger_1.get_level_method('info'), logger_1.info)
        self.assertEqual(logger_1.get_level_method('warning'), logger_1.warning)
        self.assertEqual(logger_1.get_level_method('error'), logger_1.error)
        self.assertEqual(logger_1.get_level_method('critical'), logger_1.critical)

    def test_levels(self):
        logger_1 = BaseLogger()

        for level in LEVELS:
            msg = 'simple'
            grp_id = 12
            msg_id = 21
            parent_msg_id = 10
            props = {'a': 'b'}

            gid, mid, pid = getattr(logger_1, level)(msg, grp_id, msg_id, props, parent_msg_id)

            self.assertEqual(gid, grp_id)
            self.assertEqual(mid, msg_id)
            self.assertEqual(pid, parent_msg_id)

            msg = 'simple2'
            grp_id = None
            msg_id = None
            props = None

            gid, mid, pid = getattr(logger_1, level)(msg, grp_id, msg_id, props)

            self.assertEqual(gid, 'default')
            self.assertIsInstance(mid, str)
            self.assertEqual(pid, None)

    def test_process_request(self):
        self.assertIsNone(BaseLogger.process_request(22))

    def test_process_response(self):
        self.assertIsNone(BaseLogger.process_response(24, 42))

    def test_default_func_before(self):
        logger_1 = BaseLogger()
        ids_tuple = (1, 2, 3)
        new_ids_tuple = logger_1.default_func_before(test_func, [1, 23], {'another': 'yes'}, 'info', ids_tuple)

        self.assertEqual(ids_tuple, new_ids_tuple)

    def test_default_func_after(self):
        logger_1 = BaseLogger()
        ids_tuple = (1, 2, 3)
        gid, mid, pid = logger_1.default_func_after(test_func, [11, 2], {'another': 'no'}, 'warning', ids_tuple)

        self.assertEqual(gid, ids_tuple[0])
        self.assertIsInstance(mid, str)
        self.assertNotEqual(mid, ids_tuple[1])
        self.assertEqual(pid, ids_tuple[2])

    def test_get_from_thread(self):
        logger = thread_get_logger('base')
        self.assertIsNone(logger)

        logger = BaseLogger.get_from_thread()
        self.assertIsInstance(logger, BaseLogger)


class RequestLoggerTest(LogexposeTestCase):

    def test_pick_grp_id(self):
        req = RequestFactory().get('/')

        logger_1 = RequestLogger(req)
        logger_1.grp_id = 44
        self.assertEqual(logger_1.pick_grp_id(99), 44)


class UtilsTest(LogexposeTestCase):

    def test_get_from_thread(self):
        logger = thread_get_logger('base')
        self.assertIsNone(logger)

        logger = thread_init_logger(BaseLogger)
        self.assertIs(logger, BaseLogger)

        logger = thread_get_logger('base')
        self.assertIs(logger, BaseLogger)

    def test_get_func_path(self):
        path = get_func_path(test_func)
        self.assertIn('tests.test_func', path)


class ToolboxTest(LogexposeTestCase):

    def test_get_logger(self):
        logger = get_logger('base')
        self.assertIsNone(logger)

        thread_init_logger(BaseLogger)

        logger = get_logger('base')
        self.assertIs(logger, BaseLogger)


class MiddlewareTest(LogexposeTestCase):

    def test_middleware(self):
        mware = RequestLoggerMiddleware()

        logger = get_logger('rlog')
        self.assertIsNone(logger)

        logger = get_logger('plog')
        self.assertIsNone(logger)


        req = RequestFactory().get('/')
        mware.process_request(req)

        logger = get_logger('rlog')
        self.assertIsInstance(logger, RequestLogger)

        logger = get_logger('plog')
        self.assertIsInstance(logger, ProcessLogger)

        resp = mware.process_response(req, HttpResponse())
        self.assertIn('logexpose-client-id', resp._headers)


class DecoratorsTest(LogexposeTestCase):

    def test_logexpose_dec(self):
        func = logexpose_decor('base')(test_func)

        self.assertRaises(LoggerNotRegistered, func, 'func_result', 2)

        BaseLogger.get_from_thread()  # Initialize logger.
        result = func('func_result', 2)

        self.assertEqual(result, 'func_result')
