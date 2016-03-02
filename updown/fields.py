"""
Fields needed for the updown ratings
"""
from __future__ import unicode_literals

from django.db.models import IntegerField, PositiveIntegerField
from django.conf import settings

from updown.models import Vote, SCORE_TYPES
from updown.exceptions import InvalidRating, AuthRequired, CannotChangeVote
from updown import forms


if 'django.contrib.contenttypes' not in settings.INSTALLED_APPS:
    raise ImportError("django-updown requires django.contrib.contenttypes "
                      "in your INSTALLED_APPS")

from django.contrib.contenttypes.models import ContentType

__all__ = ('Rating', 'RatingField', 'AnonymousRatingField')

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5


def md5_hexdigest(value):
    return md5(value.encode()).hexdigest()


class Rating(object):
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes


class RatingManager(object):
    def __init__(self, instance, field):
        self.content_type = None
        self.instance = instance
        self.field = field

        self.like_field_name = "{}_likes".format(self.field.name,)
        self.dislike_field_name = "{}_dislikes".format(self.field.name,)

    def get_rating_for_user(self, user, ip_address=None):
        kwargs = {
            'content_type': self.get_content_type(),
            'object_id': self.instance.pk,
            'key': self.field.key
        }

        if not (user and user.is_authenticated()):
            if not ip_address:
                raise ValueError("``user`` or ``ip_address`` must be "
                                 "present.")
            kwargs['user__isnull'] = True
            kwargs['ip_address'] = ip_address
        else:
            kwargs['user'] = user

        try:
            rating = Vote.objects.get(**kwargs)
            return rating.score
        except Vote.DoesNotExist:
            pass
        return

    def get_content_type(self):
        if self.content_type is None:
            self.content_type = ContentType.objects.get_for_model(
                self.instance)
        return self.content_type

    def add(self, score, user, ip_address, commit=True):
        try:
            score = int(score)
        except (ValueError, TypeError):
            raise InvalidRating("{} is not a valid score for {}".format(
                score, self.field.name))

        if score not in SCORE_TYPES.values():
            raise InvalidRating("{} is not a valid score".format(score))

        is_anonymous = (user is None or not user.is_authenticated())
        if is_anonymous and not self.field.allow_anonymous:
            raise AuthRequired("User must be a user, not '{}'".format(user))

        if is_anonymous:
            user = None

        defaults = {
            'score': score,
            'ip_address': ip_address
        }

        kwargs = {
            'content_type': self.get_content_type(),
            'object_id': self.instance.pk,
            'key': self.field.key,
            'user': user
        }
        if not user:
            kwargs['ip_address'] = ip_address

        try:
            rating, created = Vote.objects.get(**kwargs), False
        except Vote.DoesNotExist:
            kwargs.update(defaults)
            rating, created = Vote.objects.create(**kwargs), True

        has_changed = False
        if not created:
            if self.field.can_change_vote:
                has_changed = True
                if (rating.score == SCORE_TYPES['LIKE']):
                    self.likes -= 1
                else:
                    self.dislikes -= 1
                if (score == SCORE_TYPES['LIKE']):
                    self.likes += 1
                else:
                    self.dislikes += 1
                rating.score = score
                rating.save()
            else:
                raise CannotChangeVote()
        else:
            has_changed = True
            if (rating.score == SCORE_TYPES['LIKE']):
                self.likes += 1
            else:
                self.dislikes += 1

        if has_changed:
            if commit:
                self.instance.save()

    def _get_likes(self, default=None):
        return getattr(self.instance, self.like_field_name, default)

    def _set_likes(self, value):
        return setattr(self.instance, self.like_field_name, value)

    likes = property(_get_likes, _set_likes)

    def _get_dislikes(self, default=None):
        return getattr(self.instance, self.dislike_field_name, default)

    def _set_dislikes(self, value):
        return setattr(self.instance, self.dislike_field_name, value)

    dislikes = property(_get_dislikes, _set_dislikes)

    def get_difference(self):
        return self.likes - self.dislikes

    def get_quotient(self):
        return float(self.likes) / max(self.dislikes, 1)


class RatingCreator(object):
    def __init__(self, field):
        self.field = field
        self.like_field_name = "{}_likes".format(self.field.name)
        self.dislike_field_name = "{}_dislikes".format(self.field.name)

    def __get__(self, instance, type=None):
        if instance is None:
            return self.field
        return RatingManager(instance, self.field)

    def __set__(self, instance, value):
        if isinstance(value, Rating):
            setattr(instance, self.like_field_name, value.likes)
            setattr(instance, self.dislike_field_name, value.dislikes)
        else:
            raise TypeError("{} value must be a Rating instance, not '{}'".
                            format(self.field.name, value))


class RatingField(IntegerField):
    def __init__(self, delimiter="|", *args, **kwargs):
        self.can_change_vote = kwargs.pop('can_change_vote', False)
        self.allow_anonymous = kwargs.pop('allow_anonymous', False)
        self.delimiter = delimiter
        kwargs['editable'] = False
        kwargs['default'] = 0
        kwargs['blank'] = True
        super(RatingField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name
        self.like_field = PositiveIntegerField(editable=False, default=0,
                                               blank=True)
        cls.add_to_class("{}_likes".format(self.name), self.like_field)
        self.dislike_field = PositiveIntegerField(editable=False, default=0,
                                                  blank=True)
        cls.add_to_class("{}_dislikes".format(self.name), self.dislike_field)
        self.key = md5_hexdigest(self.name)

        field = RatingCreator(self)
        if not hasattr(cls, '_ratings'):
            cls._ratings = []
        cls._ratings.append(self)

        setattr(cls, name, field)

    def to_python(self, value):
        # If it's already a list, leave it
        if isinstance(value, list):
            return value

        # Otherwise, split by delimiter
        return value.split(self.delimiter)

    def get_prep_value(self, value):
        return self.delimiter.join(value)

    def get_db_prep_save(self, value, connection):
        pass

    def get_db_prep_lookup(self, lookup_type, value, connection,
                           prepared=False):
        raise NotImplementedError(self.get_db_prep_lookup)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RatingField}
        defaults.update(kwargs)
        return super(RatingField, self).formfield(**defaults)


class AnonymousRatingField(RatingField):
    def __init__(self, *args, **kwargs):
        kwargs['allow_anonymous'] = True
        super(AnonymousRatingField, self).__init__(*args, **kwargs)


try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([
        (
            [RatingField],  # Class(es) these apply to
            [],             # Positional arguments (not used)
            {               # Keyword argument
                "delimiter": ["delimiter", {"default": "|"}],
            },
        ),
    ], ["^updown\.fields\.RatingField"])
