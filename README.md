# django-updown

> Simple Django application for adding Youtube like up and down voting.

[![Build Status](https://secure.travis-ci.org/weluse/django-updown.png?branch=master)](http://travis-ci.org/weluse/django-updown)

## Install

```
pip install django-updown
```

## Usage

Add `"updown"` to your `INSTALLED_APPS`. Then just add a `RatingField` to
your existing model:

    from django.db import models
    from updown.fields import RatingField

    class Video(models.Model):
        # ...other fields...
        rating = RatingField()

You can also allow the user to change his vote:

    class Video(models.Model):
        # ...other fields...
        rating = RatingField(can_change_vote=True)

Now you can write your own view to submit ratings or use the predefined:

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
