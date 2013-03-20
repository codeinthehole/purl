#!/usr/bin/env bash

# The doctests only work in Python2.* due to unicode issues that I
# don't know how to solve.
nosetests --with-doctest --doctest-extension=rst
