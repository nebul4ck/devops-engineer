#!/bin/sh

if [ $# -ne 1 ]; then
	echo "Usage: ./make_package.sh python_version"
	echo "python_version: [2.7|3.5]"
	exit 1
fi

PYTHON_VERSION=$1

rsync -av --delete -r --exclude '*pyc' ./src/pydeb/* ./pydeb/usr/lib/python${PYTHON_VERSION}/dist-packages/pydeb/
cp ./src/pydeb.conf-prod ./pydeb/etc/pydeb/pydeb.conf
cp ./src/logging.conf-prod ./pydeb/etc/pydeb/logging.conf
cp ./src/pydeb_main.py ./pydeb/usr/bin/pydeb
chmod +x ./pydeb/usr/bin/pydeb

exit 0
