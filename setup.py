#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = '0.8'

# Python 2/3 compatibility
import sys
if sys.version_info[0] == 3:
    def as_bytes(s):
        return s
else:
    def as_bytes(s):
        return s.encode('utf8')


setup(
    name='purl',
    version=as_bytes(__version__),
    description="An immutable URL class for easy URL-building and manipulation",
    long_description=open('README.rst').read(),
    url='https://github.com/codeinthehole/purl',
    license='MIT',
    author="David Winterbottom",
    author_email="david.winterbottom@gmail.com",
    packages=find_packages(exclude=['tests']),
    install_requires=['six'],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
