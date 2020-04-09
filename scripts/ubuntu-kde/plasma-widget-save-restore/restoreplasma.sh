#!/bin/sh

# Restore plasma widgets

prg=$(basename $0)
resolution="$1"
dir_conf="/home/$USER/.config"
plasma="plasma-org.kde.plasma.desktop-appletsrc"


help() {
	echo "usage: $prg <resolution>"
	echo "\t$prg 1920x975"
	exit 1
}

if  [ "$#" -lt 1 ] || [ "$#" -gt 1 ];
then
	help
fi

plasma_copy="$plasma-$resolution"

echo "Restoring plasma desktop..."
if [ ! -f "$dir_conf/$plasma_copy" ];
then
	echo "$dir_conf/$plasma_copy not exists!"
	echo "Exit..."
	exit 1
else
	kbuildsycoca5 && kquitapp5 plasmashell && \
	cp -f "$dir_conf/$plasma_copy" "$dir_conf/$plasma"  && \
	kstart5 plasmashell > /dev/null 2>&1 & disown
fi
