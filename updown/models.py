# -*- coding: utf-8 -*-
"""
updown.models
~~~~~~~~~~~~~

The vote model for storing ratings

:copyright: 2011, weluse (http://weluse.de)
:author: 2011, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

import datetime

_SCORE_TYPE_CHOICES = (
    (-1, 'DISLIKE'),
    (1, 'LIKE'),
)

SCORE_TYPES = dict((value, key) for key, value in _SCORE_TYPE_CHOICES)

class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="updown_votes")
    object_id = models.PositiveIntegerField()
    key = models.CharField(max_length=32)
    score = models.SmallIntegerField(choices=_SCORE_TYPE_CHOICES)
    user = models.ForeignKey(User, blank=True, null=True, related_name="updown_votes")
    ip_address = models.IPAddressField()
    date_added = models.DateTimeField(default=datetime.datetime.now, editable=False)
    date_changed = models.DateTimeField(default=datetime.datetime.now, editable=False)

    content_object = generic.GenericForeignKey()

    class Meta:
        unique_together = (('content_type', 'object_id', 'key', 'user',
                            'ip_address'))

    def __unicode__(self):
        return u"%s voted %s on %s" % (self.user, self.score,
                                       self.content_object)

    def save(self, *args, **kwargs):
        self.date_changed = datetime.datetime.now()
        super(Vote, self).save(*args, **kwargs)

    def partial_ip_address(self):
        ip = self.ip_address.split('.')
        ip[-1] = 'xxx'
        return '.'.join(ip)

    partial_ip_address = property(partial_ip_address)

