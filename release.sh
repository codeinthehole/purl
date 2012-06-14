#!/bin/bash
# Cut a release to PyPi and update Github with tag.

# Ensure there are no uncomitted changes
git diff --quiet HEAD
[ $? -ne 0 ] && echo "Uncommitted changes!" && exit 1

# Push to PyPi
./setup.py sdist upload

# Tag in Git
git push origin master
git push --tags