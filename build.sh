#!/bin/bash

if [ ! -d ./venv ]; then
	echo "* Virtual Enviroment doesn't exist: creating..."
	python -m venv venv
else
	echo "* Virtual Enviroment already exists: make sure you aren't in it when you run this program"
fi

echo "Ready? (RETURN, )"
read

echo "* Entering venv..."
source venv/bin/activate

echo "* Installing/Updating dependancies..."
pip install -r dep.txt

mkdir bin
echo "* Compiling... 'dist/mpd-vrchat-osc'"
pyinstaller --onefile main.py
mv dist/main dist/mpd-vrchat-osc
