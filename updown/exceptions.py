# -*- coding: utf-8 -*-
"""
updown.exceptions
~~~~~~~~~~~~~~~~~

Some custom exceptions

:copyright: 2016, weluse (https://weluse.de)
:author: 2016, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals


class InvalidRating(ValueError):
    pass


class AuthRequired(TypeError):
    pass


class CannotChangeVote(Exception):
    pass
