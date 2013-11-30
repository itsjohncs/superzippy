#!/usr/bin/env bash

# This will ensure that the script exits if a failure occurs
set -e

# This will ensure the user is visually prompted upon failure
trap "echo FAILURE: An error has occured! >&2" EXIT

# Figure out where the clean script is
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Move into the root of the project
cd "$DIR"/..

# All the files that will be deleted without prompting
TO_FORCE_DELETE=$(find . -maxdepth 1 \( -name "*.egg-info" -o -name "build" \
    -o -name "dist" \))

# All the files that will be deleted *with* prompting
TO_DELETE=$(find . -path ./.git -prune -o -name "*~" -print)

if [ -n "${TO_FORCE_DELETE[@]}" ]; then
    echo "Deleting" ${TO_FORCE_DELETE[@]}
    rm -rf ${TO_FORCE_DELETE[@]}
else
    echo "No forced deletions."
fi

if [ -n "${TO_DELETE[@]}" ]; then
    rm -ri ${TO_DELETE[@]}
else
    echo "No interactive deletions."
fi

echo "Finished."

# Unset the trap so we don't freak the user out by telling them an error has
# occured when everything went fine.
trap - EXIT

exit 0
