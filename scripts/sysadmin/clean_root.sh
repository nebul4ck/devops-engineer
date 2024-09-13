#!/bin/bash

# Get the current (in use) kernel version
echo -n "############################################"
echo -n "Exporting current (in-use) kernel version..."
echo -n "############################################"
export kernel_package_version=$(uname -r)
echo -n "########################################################"
echo -n "The kernel version in used is: ${kernel_package_version}"
echo -n "########################################################"

# Set all installed kernel versions. Candidates to be purged from OS.
echo -n "###########################################################"
echo -n "Select kernel versions which are candidates to be purged..."
echo -n "###########################################################"
export kernel_tobe_deleted=$(dpkg --get-selections | grep linux-image | grep -v $(echo $kernel_package_version) | awk '{print $1}')
echo -n "######################################################################"
echo -n "The candidates kernel version to be purged are: ${kernel_tobe_deleted}"
echo -n "######################################################################"

echo -n "#################################"
echo -n "Deleting older kernel versions..."
echo -n "#################################"

# Purge old Kernel version
for kernel in ${kernel_tobe_deleted[@]}; do 
	echo "Kernet to be deleted is: ${kernel}";
	apt-get purge ${kernel}
done
echo -n "############################################"
echo -n "The older kernel versions have been purged!."
echo -n "############################################"

echo -n "##################"
echo -n "Updating APT CACHE"
echo -n "##################"
apt update -y

echo -n "#####################"
echo -n "Upgrading Packages..."
echo -n "#####################"
apt dist-upgrade -y

echo -n "#####################################"
echo -n "Auto-removing old package versions..."
echo -n "#####################################"
apt auto-remove -y

echo -n "##################"
echo -n "Cleaning APT CACHE"
echo -n "##################"
apt-get clean
apt-get autoclean

echo -n "###################################"
echo -n "Deleting tmp and older log files..."
echo -n "###################################"
rm -rf /tmp/*
find /var/log/journal/** -type f -ctime +3 -exec rm -rf {} \;

echo -n "########################"
echo -n "DONE!, The / is cleaned!"
echo -n "########################"