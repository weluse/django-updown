# -*- coding: utf-8 -*-
"""
updown.tests
~~~~~~~~~~~~

Tests the models provided by the updown rating app

:copyright: 2011, weluse (http://weluse.de)
:author: 2011, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
import random

from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse

from updown.models import Vote, SCORE_TYPES
from updown.fields import RatingField
from updown.exceptions import CannotChangeVote


class RatingTestModel(models.Model):
    rating = RatingField(can_change_vote=True)
    rating2 = RatingField(can_change_vote=False)

    def __unicode__(self):
        return unicode(self.pk)

class TestRatingModel(TestCase):
    """Test case for the generic rating app"""

    def setUp(self):
        self.instance = RatingTestModel.objects.create()

        self.user = User.objects.create(username=str(random.randint(0, 100000000)))
        self.user2 = User.objects.create(username=str(random.randint(0, 100000000)))


    def test_basic_vote(self):
        """Test a simple vote"""
        self.instance.rating.add(score=SCORE_TYPES['LIKE'], user=self.user)

        self.assertEquals(self.instance.rating_likes, 1)

    def test_change_vote(self):
        self.instance.rating.add(score=SCORE_TYPES['LIKE'], user=self.user)
        self.instance.rating.add(score=SCORE_TYPES['DISLIKE'], user=self.user)

        self.assertEquals(self.instance.rating_likes, 0)
        self.assertEquals(self.instance.rating_dislikes, 1)

    def test_change_vote_disallowed(self):
        self.instance.rating2.add(score=SCORE_TYPES['LIKE'], user=self.user)
        self.assertRaises(CannotChangeVote, self.instance.rating2.add,
                          score=SCORE_TYPES['DISLIKE'], user=self.user)
