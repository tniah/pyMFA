# -*- coding: utf-8 -*-

"""
pymfa.tokens.hotp
~~~~~~~~~~~~~~
"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor import hotp as _hotp

from pymfa.tokens.token_class import TokenClass
from pymfa.utils import to_bytes
from pymfa.utils import to_unicode


class HOTPToken(TokenClass):
    """The HMAC-based One-Time Password (HOTP) class."""

    def __init__(self, db_token):
        super().__init__(db_token)
        self.set_type(ttype='hotp')

    @property
    def hashlib(self):
        return hashes.SHA1()

    def get_otp(self):
        """Return the next HOTP value."""
        otp_length = int(self.token.otp_length)
        otp_key = self.token.get_otp_key()

        hotp = _hotp.HOTP(
            key=to_bytes(otp_key),
            length=otp_length,
            algorithm=self.hashlib,
            enforce_key_length=True)
        counter = int(self.token.counter)
        return to_unicode(hotp.generate(counter))

    def check_otp(self, otp_value):
        otp_length = int(self.token.otp_length)
        otp_key = self.token.get_otp_key()

        hotp = _hotp.HOTP(
            key=to_bytes(otp_key),
            length=otp_length,
            algorithm=self.hashlib)
        counter = int(self.token.counter)
        try:
            hotp.verify(to_bytes(otp_value), counter)
        except _hotp.InvalidToken:
            return False

        # on success, increase opt counter by 1
        self.set_counter(counter + 1)
        return True
