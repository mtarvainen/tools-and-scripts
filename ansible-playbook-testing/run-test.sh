#!/bin/bash
set -e

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

if [ -n "$1" ] ; then
    molecule destroy --scenario-name $1
    molecule converge --scenario-name $1
    exit $?
fi

set +e
for directory in `find molecule/ -maxdepth 1 -mindepth 1 -type d -not -name default -exec ls -ld {} \; | awk '{ gsub("^.*/","",$9); printf $9"\n";}'`
do
    molecule destroy --scenario-name $directory
    molecule converge --scenario-name $directory
done
