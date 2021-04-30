#!/bin/bash

function result_check {
  if [[ $? -ne 0 ]]
  then
    exit $?
  fi
}

echo $1
if [[ $1 = "build" ]]
then
    python3 -m build
    result_check
fi

if [[ $1 = "push-test" ]]
then
    if [[ -z $PYPITOKENTEST ]]
    then
        echo 'Error: PYPITOKENTEST env var not defined'
        exit 1
    fi
    python3 -m twine upload --repository testpypi dist/* -u __token__ -p "$PYPITOKENTEST"
    result_check
fi

if [[ $1 = "push" ]]
then
    if [[ -z $PYPITOKEN ]]
    then
        echo 'Error: PYPITOKEN env var not defined'
        exit 1
    fi
    python3 -m twine upload dist/* -u __token__ -p "$PYPITOKEN"
    result_check
fi
