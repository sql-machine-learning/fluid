#!/bin/bash

changed_py_files=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.py$')
echo $changed_py_files
if [[ $changed_py_files == "" ]]; then
    exit 0
fi

pylint $changed_py_files
flake8 $changed_py_files
