#!/bin/bash

sudo apt-get update
sudo apt-get install python3.8
python3 --version

python3 -m pip install --user --upgrade pip
python3 -m pip --version

apt-get install python3-venv

pip install pandas

pip install notebook
jupyter notebook
