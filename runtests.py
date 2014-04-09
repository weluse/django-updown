#!/usr/bin/env python
import sys

from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'updown',
        ],
        # Fix for Django versions < 1.5
        AUTH_USER_MODEL='auth.User'
    )

from django.test.simple import DjangoTestSuiteRunner


def runtests(*test_args):
    if not test_args:
        test_args = ['updown']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    test_runner = DjangoTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
