#!/bin/bash

#
# Test if the current version on PyPi works
# it creates a new virtual environment,
# downloads the package and pytest
# and then runs pytest on the downloaded version
#

if [[ -d tmp_test_pypi ]]
then
    rm -r tmp_test_pypi || exit 1
fi
mkdir tmp_test_pypi || exit 1
cd tmp_test_pypi || exit 1

python3 -m venv init || exit 1
source init/bin/activate || exit 1

if [[ -z $VIRTUAL_ENV ]]
then
    echo "Error: Not in virtual env"
    exit 1
fi

pip install easy-serialize
pip install pytest

python -c "import easy_serialize" | exit 1

cp -r ../tests .

pytest tests

cd ..
rm -r tmp_test_pypi