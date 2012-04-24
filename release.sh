#!/bin/bash
# Cut a release to PyPi and update Github with tag.

# Ensure there are no uncomitted changes
git diff --quiet HEAD
[ $? -ne 0 ] && echo "Uncommitted changes!" && exit 1

# Pluck release number out of setup.py
RELEASE_NUM=`grep version setup.py | cut -d\' -f2`
git tag | grep $RELEASE_NUM > /dev/null && \
	echo "New version number required ($RELEASE_NUM already used)" && exit 1

# Push to PyPi
./setup.py sdist upload

# Tag in Git
git tag $RELEASE_NUM -m "Tagging release $RELEASE_NUM"
git push origin master
git push --tags