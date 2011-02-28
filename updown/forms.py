"""
updown.forms
~~~~~~~~~~~~~~~~~~~~~~~

Very basic form fields

:copyright: 2011, weluse (http://weluse.de)
:author: 2011, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from django import forms


__all__ = ('RatingField',)

class RatingField(forms.ChoiceField):
    pass
