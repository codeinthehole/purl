#!/usr/bin/env python
from setuptools import setup, find_packages
from purl import __version__

setup(name='purl',
      version=__version__.encode('utf8'),
      description="An immutable URL class for easy URL-building and manipulation",
      long_description=open('README.rst').read(),
      license=open('LICENSE').read(),
      url='https://github.com/codeinthehole/purl',
      author="David Winterbottom",
      author_email="david.winterbottom@gmail.com",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      package_data={'': ['LICENSE']},
      )
