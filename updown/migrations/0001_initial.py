# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('key', models.CharField(max_length=32)),
                ('score', models.SmallIntegerField(choices=[(-1, 'DISLIKE'), (1, 'LIKE')])),
                ('ip_address', models.GenericIPAddressField()),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_changed', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('content_type', models.ForeignKey(related_name='updown_votes', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='updown_votes', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('content_type', 'object_id', 'key', 'user', 'ip_address')]),
        ),
    ]
