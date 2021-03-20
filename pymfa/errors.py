# -*- coding: utf-8 -*-

"""
pymfa.errors
~~~~~~~~~~~~~~
"""


class PyMFAError(Exception):
    pass


class InvalidPasswordError(PyMFAError):
    pass


class InvalidTokenError(PyMFAError):
    pass
