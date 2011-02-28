# -*- coding: utf-8 -*-
"""
updown.exceptions
~~~~~~~~~~~~~~~~~

Some custom exceptions

:copyright: 2011, weluse (http://weluse.de)
:author: 2011, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""

class InvalidRating(ValueError):
    pass

class AuthRequired(TypeError): 
    pass

class CannotChangeVote(Exception): 
    pass
