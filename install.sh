#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

echo "Installing Hanuchi..."

cp hanuchi /usr/bin/hanuchi
chmod +x /usr/bin/hanuchi

cp hanuchi.desktop /usr/share/applications/

# ТУТ ИСПРАВИЛ
if [ -f "assets/hanuchi.svg" ]; then
    mkdir -p /usr/share/icons/hicolor/scalable/apps/
    cp assets/hanuchi.svg /usr/share/icons/hicolor/scalable/apps/hanuchi.svg
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor/
    fi
fi

echo "Done."
