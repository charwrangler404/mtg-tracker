#!/usr/bin/env bash

# Install required dependancies
if [ $(which apt) != 'apt not found' ]; then
    sudo apt-get -y install sqlite3 python3-pip
elif [ $(which dnf) != 'dnf not found' ]; then
    sudo dnf install -y sqlite3 python3-pip
else
    echo "Supported package manager not found"
fi

pip3 install --user scrython
