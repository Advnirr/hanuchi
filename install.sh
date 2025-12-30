#!/bin/bash

# Hanuchi Installer
# Simple, agnostic installer for non-Arch systems.

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

echo "Installing Hanuchi..."

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 could not be found."
    exit 1
fi

# 2. Check for Hamachi
if ! command -v hamachi &> /dev/null; then
    echo "WARNING: 'hamachi' command not found. Please install LogMeIn Hamachi first."
    # We proceed anyway, maybe it's in a weird path not in sudo's PATH
fi

# 3. Install Files
echo "Copying binary..."
cp hanuchi /usr/bin/hanuchi
chmod +x /usr/bin/hanuchi

echo "Copying desktop entry..."
cp hanuchi.desktop /usr/share/applications/

# Icon (assuming you have assets/icon.svg)
if [ -f "assets/icon.svg" ]; then
    echo "Copying icon..."
    mkdir -p /usr/share/icons/hicolor/scalable/apps/
    cp assets/icon.svg /usr/share/icons/hicolor/scalable/apps/hanuchi.svg
    # Update icon cache if possible
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor/
    fi
else
    echo "Note: assets/icon.svg not found, skipping icon installation."
fi

echo "-----------------------------------"
echo "Hanuchi installed successfully!"
echo "Run it via application menu or type 'hanuchi' in terminal."
echo "Dependencies note: Ensure you have GTK4, Libadwaita and Python GObject installed via your package manager."
