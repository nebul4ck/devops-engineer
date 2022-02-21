#!/bin/bash

set -x

echo -e "Downloading maldetect current version..." && \
wget -O /usr/src/maldetect-current.tar.gz https://www.rfxn.com/downloads/maldetect-current.tar.gz

echo -e "Untar maldetect-current.tar.gz" && \
tar -xzf /usr/src/maldetect-current.tar.gz --directory /usr/src/

cd $(find /usr/src -name 'maldetect*' -type d)
bash install.sh