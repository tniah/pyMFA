# -*- coding: utf-8 -*-

"""
pymfa.tokens.token_class
~~~~~~~~~~~~~~
"""
import secrets

from passlib.totp import generate_secret


class TokenClass(object):

    def __init__(self, db_token, config=None):
        """
        Create a new token object.

        Args:
            db_token: Instance of a ORM database model
        """
        self.token = db_token
        self.type = db_token.type
        self.config = config or {}

    def set_type(self, ttype):
        """
        Set type for the current token object.

        Args:
            ttype: The type of the token like SMS or TOTP
        """
        self.type = ttype
        self.token.type = ttype

    # def check_otp(self, value):
    #     pass

    @property
    def opt_len(self):
        return 6

    @property
    def opt_key(self):
        return ''

    def set_counter(self, opt_counter):
        pass

    def generate_otp_key(self, otp_key_size=None):
        """Generate a new OTP key.

        Args:
            otp_key_size: The size of the key to generate
        Returns:
            The created OTP key as a string.
        """
        if otp_key_size is None:
            if hasattr(self, 'otp_key_size'):
                otp_key_size = getattr(self, 'otp_key_size')
            else:
                otp_key_size = 32
        return generate_secret(otp_key_size * 8)

    def get_opt_key(self):
        pass

    def generate_otp(self, otp_digits=None):
        """Generate a new One-Time Password code.

        Args:
            otp_digits: The number of digits in the generated OTP code
        Returns:
            The created OTP code as a string
        """
        if otp_digits is None:
            if hasattr(self, 'otp_digits'):
                otp_digits = getattr(self, 'otp_digits')
            else:
                otp_digits = 6
        return ''.join(str(secrets.randbelow(10)) for _ in range(otp_digits))

    def get_token_info(self, key=None, default=None):
        """Get the complete token info, or a single key of the token info
        in the database.

        Args:
            key: A key to retrieve
            default: The default value, if it does not exist
                     in the database.
        Returns:
            If key is None, then a dictionary is returned. If a certain key
            is given, a string/boolean is returned.
        """
        token_info = self.token.get_info()
        if key:
            return token_info.get(key, default)
        return token_info

    def get_from_config(self, key=None, default=None):
        """Get the complete token info, or a single key of the token info
        from the configuration.

        Args:
            key: A key to retrieve
            default: The default value, if it does not exist
                     in the configuration.
        Returns:
            If key is None, then a dictionary is returned. If a certain key
            is given, a string/boolean is returned.
        """
        if key:
            return self.config.get(key, default)
        return self.config
