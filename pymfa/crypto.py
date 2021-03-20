# -*- coding: utf-8 -*-

"""
pymfa.crypto
~~~~~~~~~~~~~~
"""
import base64
import binascii
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import aead
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from pymfa.errors import InvalidPasswordError
from pymfa.errors import InvalidTokenError
from pymfa.utils import b64encode_and_unicode
from pymfa.utils import to_bytes
from pymfa.utils import to_unicode


class AESGCMCipher(object):
    """A wrapper class for encryption/decryption.

    This class uses AES_GCM cipher to encrypt/decrypt strings.
    """

    class _AESGCM(aead.AESGCM):

        def __init__(self, pwd: str, salt: str = ''):
            salt = salt or 'pyMFA_salt_for_secret'
            key = self.generate_key(pwd, salt)
            super().__init__(key)

        @classmethod
        def generate_key(cls, pwd: str, salt: str) -> bytes:
            if pwd is None or pwd == '':
                raise InvalidPasswordError(
                    'Password should be at least one character long.')

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=to_bytes(salt),
                iterations=150000,
                backend=default_backend())
            return kdf.derive(to_bytes(pwd))

    def __init__(self, pwds: str, salt: str = '', delimiter: str = ','):
        ciphers = []
        for pwd in pwds.split(delimiter):
            ciphers.append(self._AESGCM(pwd, salt))
        self._ciphers = ciphers

    def encrypt(self,
                data: str,
                associated_data: str = '',
                nonce: str = None) -> str:
        iv = to_bytes(nonce) or os.urandom(12)
        v = self._ciphers[0].encrypt(
            nonce=iv,
            data=to_bytes(data),
            associated_data=to_bytes(associated_data))

        ct = binascii.hexlify(iv) + b':' + binascii.hexlify(v)
        return b64encode_and_unicode(ct)

    def decrypt(self, data: str, associated_data: str = '') -> str:
        ct = base64.b64decode(to_bytes(data))
        pos = ct.find(b':')
        iv = binascii.unhexlify(ct[:pos])
        v = binascii.unhexlify(ct[pos + 1:])

        for cipher in self._ciphers:
            try:
                plaintext = cipher.decrypt(
                    nonce=iv,
                    data=v,
                    associated_data=to_bytes(associated_data))
                return to_unicode(plaintext)
            except Exception:
                pass
        raise InvalidTokenError
