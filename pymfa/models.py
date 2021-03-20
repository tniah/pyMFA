# -*- coding: utf-8 -*-
"""
pymfa.models
~~~~~~~~~~~~~~
"""
import json

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint


class MFATokenMixin(object):
    __table_args__ = (UniqueConstraint('user_id', 'type'),)

    user_id = Column('user_id', String(255), nullable=False)
    type = Column('type', String(30), nullable=False, index=True)
    active = Column('active', Boolean, default=True)
    locked = Column('locked', Boolean, default=False)
    _data = Column('data', Text)

    @property
    def data(self):
        if self._data:
            return json.loads(self._data)
        return {}

    @data.setter
    def data(self, value):
        value = value or {}
        self._data = json.dumps(value)

    @property
    def enc_key(self):
        return self.data.get('enc_key')

    @enc_key.setter
    def enc_key(self, value):
        self._set_value('enc_key', value)

    @property
    def hash_algorithm(self):
        return self.data.get('hash_algorithm')

    @hash_algorithm.setter
    def hash_algorithm(self, value):
        self._set_value('hash_algorithm', value)

    @property
    def digits(self):
        return self.data.get('digits')

    @digits.setter
    def digits(self, value):
        self._set_value('digits', value)

    @property
    def counter(self):
        return self.data.get('counter')

    @counter.setter
    def counter(self, value):
        self._set_value('counter', value)

    def _set_value(self, k, v):
        data = self.data
        data[k] = v
        self.data = data
