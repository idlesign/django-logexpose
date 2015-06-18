django-logexpose
================
https://github.com/idlesign/django-logexpose

.. image:: https://img.shields.io/pypi/v/django-logexpose.svg
    :target: https://pypi.python.org/pypi/django-logexpose

.. image:: https://img.shields.io/pypi/dm/django-logexpose.svg
    :target: https://pypi.python.org/pypi/django-logexpose

.. image:: https://img.shields.io/pypi/l/django-logexpose.svg
    :target: https://pypi.python.org/pypi/django-logexpose

.. image:: https://img.shields.io/coveralls/idlesign/django-logexpose/master.svg
    :target: https://coveralls.io/r/idlesign/django-logexpose

.. image:: https://img.shields.io/travis/idlesign/django-logexpose/master.svg
    :target: https://travis-ci.org/idlesign/django-logexpose

.. image:: https://img.shields.io/codeclimate/github/idlesign/django-logexpose.svg
   :target: https://codeclimate.com/github/idlesign/django-logexpose


Description
-----------

*Reusable application for Django exposing logs for further analysis.*


Quick start
-----------

1. Add `logexpose.middleware.RequestLoggerMiddleware` to MIDDLEWARE_CLASSES;

2. And you're ready to use `logexpose` logging facilities:

    .. code-block:: python

        from django.shortcuts import render

        from logexpose.decorators import logexpose
        from logexpose.toolbox import get_logger


        @logexpose('rlog')  # This enables automatic trace logging using RequestLogger (`rlog`)
        def index(request):

            # This nested function call will also be automatically traced
            # if the function is decorated with @logexpose (see below).
            inner_function()

            # Loggers are also available by their aliases as `request` attributes.
            request.rlog.debug('Some debugging info')

            return render(request, 'some.html', {})

        @logexpose('rlog', level='error')  # Trace this one too but issue `error` level messages.
        def inner_function():

            # Functions with no access to `request` also can get loggers by their aliases.
            get_logger('rlog').warning('A warning!', props={
                'myprop_1': 'some_value'  # Supply some additional properties to a message.
            })

            return 'ping-pong'


Documentation
-------------

http://django-logexpose.readthedocs.org/
