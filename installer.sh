#!/bin/sh

echo "Your Python3 version is:"
pyv="$(python3 --version | cut -d ' ' -f2)"
echo "$pyv"

echo ""
echo "Your pip3 version is:"
pipv="$(pip3 --version | cut -d ' ' -f2)"
echo "$pipv"

echo ""
echo "Installing Virtual Environment..."
pip3 install virtualenv
$(python3 -m venv bm)
$(. bm/bin/activate)

echo ""
echo "Installing Flask, Flask-SQLAlchemy and Pandas..."
pip3 install Flask
pip3 install Flask-SQLAlchemy
pip3 install pandas

echo ""
echo "Application discovery..."
export FLASK_APP=main.py

echo ""
echo "Start Flask server..."
flask run
