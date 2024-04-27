#!/bin/bash

set -e

here=$(cd $(dirname $0);pwd)
env_dir=$here/_venv

if [ ! -d "${env_dir}" ]
then
    echo "Creating environment at ${env_dir}"
    conda create -p $env_dir --file $here/requirements.txt -c conda-forge --yes
    conda run -p $env_dir pip install -e $here
else
    echo "environment exists."
fi

