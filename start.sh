#!/bin/sh

echo "Starting the app..."

python3 -m venv bm
source "./bm/bin/activate"
flask run
