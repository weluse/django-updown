"""
Some custom exceptions
"""
from __future__ import unicode_literals


class InvalidRating(ValueError):
    pass


class AuthRequired(TypeError):
    pass


class CannotChangeVote(Exception):
    pass
