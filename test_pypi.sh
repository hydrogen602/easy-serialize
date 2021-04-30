#!/bin/bash

rm -r tmp_test_pypi || exit 1
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

python3 