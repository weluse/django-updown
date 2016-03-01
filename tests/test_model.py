# -*- coding: utf-8 -*-
"""
tests.test_model
~~~~~~~~~~~~~~~~

Tests the models provided by the updown rating app

:copyright: 2016, weluse (https://weluse.de)
:author: 2016, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import random

from django.test import TestCase
from django.contrib.auth.models import User

from updown.models import SCORE_TYPES
from updown.exceptions import CannotChangeVote

from tests.models import RatingTestModel


class TestRatingModel(TestCase):
    """Test case for the generic rating app"""

    def setUp(self):
        self.instance = RatingTestModel.objects.create()

        self.user = User.objects.create(
            username=str(random.randint(0, 100000000))
        )
        self.user2 = User.objects.create(
            username=str(random.randint(0, 100000000))
        )

    def test_basic_vote(self):
        """Test a simple vote"""
        self.instance.rating.add(SCORE_TYPES['LIKE'], self.user,
                                 '192.168.0.1')

        self.assertEquals(self.instance.rating_likes, 1)

    def test_change_vote(self):
        self.instance.rating.add(SCORE_TYPES['LIKE'], self.user,
                                 '192.168.0.1')
        self.instance.rating.add(SCORE_TYPES['DISLIKE'], self.user,
                                 '192.168.0.1')

        self.assertEquals(self.instance.rating_likes, 0)
        self.assertEquals(self.instance.rating_dislikes, 1)

    def test_change_vote_disallowed(self):
        self.instance.rating2.add(SCORE_TYPES['LIKE'], self.user,
                                  '192.168.0.1')
        self.assertRaises(CannotChangeVote, self.instance.rating2.add,
                          SCORE_TYPES['DISLIKE'], self.user, '192.168.0.1')
