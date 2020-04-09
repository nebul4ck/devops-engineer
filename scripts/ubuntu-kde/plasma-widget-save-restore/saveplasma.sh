#!/bin/sh

# Save plasma Widgets

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

echo "Creating plasma copy..."
cp -f "$dir_conf/$plasma" "$dir_conf/$plasma"-"$resolution" \
&& echo " ...OK"
