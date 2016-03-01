# -*- coding: utf-8 -*-
"""
djang-updown
~~~~~~~~~~~~

A django application which provides simple like and dislike voting

:copyright: 2016, weluse (https://weluse.de)
:author: 2016, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
import os
import re
from setuptools import setup, find_packages


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('updown')


setup(
    name='django-updown',
    version=version,
    description='django-updown is a reusable Django application for youtube \
    like up and down voting.',
    long_description=readme,
    author='Daniel Banck',
    author_email='dbanck@weluse.de',
    url='http://github.com/weluse/django-updown/tree/master',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
