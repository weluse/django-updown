# -*- coding: utf-8 -*-
"""
djang-updown
~~~~~~~~~~~~

A django application which provides simple like and dislike voting

:copyright: 2011, weluse (http://weluse.de)
:author: 2011, Daniel Banck <dbanck@weluse.de>
:license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, find_packages
from updown import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-updown',
    version=".".join(map(str, VERSION)),
    description='django-updown is a reusable Django application for youtube \
    like up and down voting.',
    long_description=readme,
    author='Daniel Banck',
    author_email='dbanck@weluse.de',
    url='http://github.com/weluse/django-updown/tree/master',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests',
    dependency_links=[
        'http://pypi.python.org/pypi/South/',
    ],
    install_requires=[
        'South',
    ],
)
