#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Uninstalling Hanuchi..."

rm -f /usr/bin/hanuchi
rm -f /usr/share/applications/hanuchi.desktop
rm -f /usr/share/icons/hicolor/scalable/apps/hanuchi.svg

if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor/
fi

echo "Done."
