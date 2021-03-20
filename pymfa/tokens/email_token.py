# -*- coding: utf-8 -*-

"""
pymfa.tokens.email
~~~~~~~~~~~~~~
"""
from pymfa.tokens.token_class import TokenClass


class EmailToken(TokenClass):

    def __init__(self, token_model):
        super().__init__(token_model)
