from uuid import uuid4

from django.utils.translation import gettext as _

from .base import BaseLogger


class RequestLogger(BaseLogger):

    alias = 'rlog'
    title = _('Requests')

    def __init__(self, request):
        self.request = request
        self.client_id = 'idle'  # todo
        super(RequestLogger, self).__init__()

    def generate_grp_id(self):
        return '%s/%s' % (self.client_id, uuid4())

    def pick_grp_id(self, grp_id):
        return self.grp_id

    @classmethod
    def process_request(cls, request):
        logger = cls.get_from_thread(request)
        setattr(request, cls.alias, logger)

    @classmethod
    def process_response(cls, request, response):
        logger = getattr(request, cls.alias, None)
        if logger is not None:
            response['Logexpose-Grp-Id'] = logger.grp_id
            response['Logexpose-Client-Id'] = logger.client_id

        return response
