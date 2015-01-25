from django.utils.translation import gettext as _

from .base import BaseLogger


class ProcessLogger(BaseLogger):

    alias = 'plog'
    title = _('Processes')

    @classmethod
    def process_request(cls, request):
        setattr(request, cls.alias, cls.get_from_thread())
