=============
django-updown
=============

``django-updown`` is a simple Django application for adding youtube like up and down voting.

---------
Changelog
---------

**0.2**:

- Updated related_name to avoid namespace clashes.
- Added south as dependency

-----
Usage
-----
Add ``"updown"`` to your ``INSTALLED_APPS`` then just add a ``RatingField`` to your model and go::

   from django.db import models
   from updown.fields import RatingField


   class Video(models.Model):
      rating = RatingField()

You can also allow the user to change his vote::

   class Video(models.Model):
      rating = RatingField(can_change_vote=True)

Now you can write your own view to submit ratings or use the predefinded::

   from updown.views import AddRatingFromModel


   urlpatterns = patterns("",
         url(r"^(?P<object_id>\d+)/rate/(?P<score>[\d\-]+)$", AddRatingFromModel(), {
               'app_label': 'video',
               'model': 'Video',
               'field_name': 'rating',
         }, name="video_rating"),
   )

To submit a vote just go to ``video/<id>/rate/(1|-1)``. If you allowed users to
change they're vote, they can do it with the same url.

----------------
Troubleshooting
----------------
If you previously used this app you may get to a point where migrations are
failing.
Try::

    ./manage.py migrate updown --fake 0001

to skip the initial migration. After this apply the migrations again::

    ./manage.py migrate updown

------
Thanks
------
Thanks a lot to ``django-ratings`` for the inspiring code
