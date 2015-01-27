from django.db import DEFAULT_DB_ALIAS

from .base import BaseDataBackend
from ..models import Record


class DatabaseBackend(BaseDataBackend):

    default_params = {
        'db_alias': DEFAULT_DB_ALIAS
    }

    def __init__(self, params):
        super(DatabaseBackend, self).__init__(params)
        self.db_alias = params.get('db_alias')

    def put(self, data):
        record = Record(**data)
        record.props = self.prepare_props(record.props)
        record.save(using=self.db_alias)
