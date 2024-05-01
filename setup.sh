#!/bin/bash

set -e

here=$(cd $(dirname $0);pwd)
env_name=not-rocketscience

if [ -z "$(conda info --envs | grep ${env_name})" ]
then
    echo "Creating environment ${env_name}"
    conda create -n $env_name --file $here/requirements.txt -c conda-forge --yes
    conda run -n $env_name pip install -e $here
else
    echo "Environment ${env_name} exists already."
fi
