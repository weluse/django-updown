# -*- coding: utf-8 -*-
"""
tests.models
~~~~~~~~~~~~

Defines models required for testing

:copyright: 2016, weluse (https://weluse.de)
:author: 2016, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals

from django.db import models
from updown.fields import RatingField


class RatingTestModel(models.Model):
    rating = RatingField(can_change_vote=True)
    rating2 = RatingField(can_change_vote=False)

    def __unicode__(self):
        return unicode(self.pk)
