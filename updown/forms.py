"""
updown.forms
~~~~~~~~~~~~

Very basic form fields

:copyright: 2016, weluse (https://weluse.de)
:author: 2016, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
from django import forms


__all__ = ('RatingField',)


class RatingField(forms.ChoiceField):
    pass
