#!/bin/sh
# Retakes the README screenshots in a clean container (stock Adwaita, fake
# hamachi data) and writes them to screenshots/. Needs podman.
set -eu

here=$(dirname "$(readlink -f "$0")")
root=$(dirname "$(dirname "$here")")
image=hanuchi-screenshots

podman build -t "$image" "$here"
mkdir -p "$root/screenshots"
podman run --rm \
    -v "$root:/src:ro,Z" \
    -v "$root/screenshots:/out:Z" \
    "$image" sh -c '
        mkdir -p "$XDG_RUNTIME_DIR" "$HOME" && chmod 700 "$XDG_RUNTIME_DIR"
        weston --backend=headless --scale=2 --width=2400 --height=1600 \
            --socket=wayland-1 >/tmp/weston.log 2>&1 &
        while [ ! -S "$XDG_RUNTIME_DIR/wayland-1" ]; do sleep 0.2; done
        WAYLAND_DISPLAY=wayland-1 GDK_BACKEND=wayland \
            python3 /src/tools/screenshots/shoot.py /src/src/hanuchi /out
    '
ls -l "$root/screenshots"
