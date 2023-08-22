#!/bin/bash
set -e

# Workaround for linux/amd64 bug in molecule https://github.com/ansible-community/molecule-docker/issues/114
IMAGE="geerlingguy/docker-rockylinux8-ansible@sha256:fca63eaf52f2b23f4a9c156e53f42bc97bd12058070889b259779d24f0f397a4"
docker pull $IMAGE --quiet
docker tag $IMAGE docker-rockylinux8-ansible:latest
IMAGE="geerlingguy/docker-rockylinux9-ansible@sha256:a1b215066c3723addc94f5cc47d68a4fd23eeed3c0fefad11e2694027dac6e89"
docker pull $IMAGE --quiet
docker tag $IMAGE docker-rockylinux9-ansible:latest

python3 -m venv venv
source venv/bin/activate
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
