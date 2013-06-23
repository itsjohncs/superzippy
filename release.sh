#!/usr/bin/env bash

# This will ensure that the script exits if a failure occurs
set -e

if [[ $# != 1 ]]
then
    echo "Usage: $0 RELEASE_NUMBER"
    echo
    echo "Publishes a release to PyPI and GitHub."
    exit 1
fi

# This will ensure the user is visually prompted upon failure
trap "echo FAILURE: An error has occured! >&2" EXIT

VERSION=$1

echo "Checking for existence of VERSION file."
if [ -f "./VERSION" ]; then
	echo "Found VERSION file."
else
	echo "Could not find VERSION file!"
	exit 2
fi

OLD_VERSION=`cat ./VERSION`
if [[ "$OLD_VERSION" == "$VERSION" ]]; then
	echo "Old version same as new version, skipping commit step."
else
	echo "Changing VERSION file, old version: $OLD_VERSION"
	echo "$VERSION" > ./VERSION

	echo "Creating new commit for version change."
	git add ./VERSION
	git commit -m "Released $VERSION." -e

	echo "Pushing commit."
	git push origin master
fi

echo "Checking for existence of $VERSION tag."
TAGS=`git tag`
if [[ "$TAGS" == *"$VERSION"* ]]; then
	echo "$VERSION tag exists locally."
else
	# This will launch an editor to create the tag message
	echo "$VERSION tag does not exist locally, creating it."
	git tag -a $VERSION

	echo "Pushing tag."
	git push --tags origin
fi

echo "Looking for setup.py in current directory..."
if [ -f "./setup.py" ]; then
	echo "Found setup.py"
else
	echo "Could not find setup.py!"
	exit 2
fi

echo "Updating PyPI..."
./setup.py bdist_egg register upload
./setup.py sdist register upload

echo "Deleting ~/.pypirc that stores your password in plaintext..."
rm -f ~/.pypirc

echo "Finished."
echo "This script cannot detect whether uploads to PyPI were succesful, so "
echo "make sure to check the output of the above commands."

# Unset the trap so we don't freak the user out by telling them an error has
# occured when everything went fine.
trap - EXIT

exit 0
