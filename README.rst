django-logexpose
================
https://github.com/idlesign/django-logexpose

.. image:: https://badge.fury.io/py/django-logexpose.png
    :target: http://badge.fury.io/py/django-logexpose

.. image:: https://pypip.in/d/django-logexpose/badge.png
        :target: https://crate.io/packages/django-logexpose


Description
-----------

*Reusable application for Django exposing logs for further analysis.*


Quick start
-----------

1. Add `logexpose.middleware.RequestLoggerMiddleware` to MIDDLEWARE_CLASSES;

2. And you're ready to `logexpose` logging facilities:

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
                'myprop_1': 'some_value'  # Supply some addition properties to a message.
            })

            return 'ping-pong'


Documentation
-------------

http://django-logexpose.readthedocs.org/

