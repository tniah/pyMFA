# -*- coding: utf-8 -*-

"""
pymfa.tokens.totp
~~~~~~~~~~~~~~
"""
from pymfa.tokens.token_class import TokenClass
from passlib import totp


class TOTPToken(TokenClass):
    """The Time-based One-Time Password (TOTP) class."""
    _hash_algorithm = 'sha1'
    _digits = 6
    _time_period = 30
    _time_window = 30

    def __init__(self, db_token, config=None):
        """
        Create a new TOTP token object.

        Args:
            db_token: Instance of a ORM database model.
        """
        super().__init__(db_token, config)
        self.set_type(ttype='totp')

    @property
    def hash_algorithm(self):
        return self.get_token_info('hash_algorithm') \
               or self.get_from_config('hash_algorithm') \
               or self._hash_algorithm

    @property
    def digits(self):
        return int(self.get_token_info('digits')
                   or self.get_from_config('digits')
                   or self._digits)

    @property
    def time_period(self):
        return int(self.get_token_info('time_period')
                   or self.get_from_config('time_period')
                   or self._time_period)

    @property
    def time_window(self):
        return int(self.get_token_info('time_window')
                   or self.get_from_config('time_window')
                   or self._time_window)

    @property
    def last_counter(self):
        return self.get_token_info('last_counter')

    def generate_otp(self, otp_digits=None):
        pass

    def check_otp(self, opt_code, counter=None):
        pass
