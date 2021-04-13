#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='purl',
    version='1.5',
    description=(
        "An immutable URL class for easy URL-building and manipulation"),
    long_description=open('README.rst').read(),
    url='https://github.com/codeinthehole/purl',
    license='MIT',
    author="David Winterbottom",
    author_email="david.winterbottom@gmail.com",
    packages=find_packages(exclude=['tests']),
    install_requires=['six'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
