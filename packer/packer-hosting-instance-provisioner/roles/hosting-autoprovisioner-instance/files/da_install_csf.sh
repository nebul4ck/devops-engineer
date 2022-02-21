#!/bin/bash

set -x

if [ -f /usr/src/csf.tgz ];
then
    echo -e "Removing csf.tgz file..." && \
    rm /usr/src/csf.tgz && \
    echo -e "The file csf.tgz was deleted."
fi

echo "Downloading the new version of csf..."
wget -O /usr/src/csf.tgz https://download.configserver.com/csf.tgz

echo "Untar csf.tgz file..."
tar -xzf /usr/src/csf.tgz --directory /usr/src/

echo "Install csf: run install.sh..."
cd /usr/src/csf/; bash /usr/src/csf/install.sh

echo "Downloading csf configuration files..."
wget -O /etc/csf/csf.conf http://almacenator.net/files/csf.conf
wget -O /etc/csf/csf.ignore http://almacenator.net/files/csf.ignore
wget -O /etc/csf/csf.allow http://almacenator.net/files/csf.allow

echo "Restarting csf..."
csf -r
service lfd restart

echo "The csf installation has been done sucessfully."
exit 0