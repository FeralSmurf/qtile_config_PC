#!/bin/bash

# Install python-psutil
sudo pacman -S --noconfirm python-psutil

# Install alsa-utils
sudo pacman -S --noconfirm alsa-utils

# Install rofi
sudo pacman -S --noconfirm rofi

# install nitrogen and picom
sudo pacman -S --noconfirm nitrogen picom

echo "All dependencies have been installed."
