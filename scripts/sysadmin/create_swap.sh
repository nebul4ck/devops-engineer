#!/bin/bash

# Create a 1GB swap file
dd if=/dev/zero of=/swap_file bs=1024 count=1048576
chmod 600 /swap_file
mkswap /swap_file
swapon /swap_file

# fstab for automount
# /swap_file swap swap defaults 0 0
