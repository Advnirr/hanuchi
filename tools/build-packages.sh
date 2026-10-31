#!/bin/sh
# Builds the .deb and the .rpm into dist/: build-packages.sh [deb] [rpm]
# Needs meson, plus dpkg-deb for the .deb and rpmbuild for the .rpm.
# Uses the working tree, not a tag.
set -eu

root=$(dirname "$(dirname "$(readlink -f "$0")")")
version=$(sed -n "s/^ *version: '\(.*\)',/\1/p" "$root/meson.build")
dist="$root/dist"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
mkdir -p "$dist"

build_deb() {
    stage="$work/deb"
    meson setup "$work/build-deb" "$root" --prefix=/usr --buildtype=plain
    meson install -C "$work/build-deb" --destdir "$stage"
    # Debian keeps the license in the copyright file instead.
    rm -rf "$stage/usr/share/licenses"
    install -Dm644 "$root/packaging/deb/copyright" "$stage/usr/share/doc/hanuchi/copyright"
    install -Dm644 "$root/packaging/deb/control" "$stage/DEBIAN/control"
    echo "Installed-Size: $(du -sk --exclude=DEBIAN "$stage" | cut -f1)" >> "$stage/DEBIAN/control"
    dpkg-deb --root-owner-group --build "$stage" "$dist/hanuchi_${version}_all.deb"
}

build_rpm() {
    top="$work/rpm"
    mkdir -p "$top/SOURCES"
    # named like GitHub's tarball of the tag, which Source0 points to
    (cd "$root" && tar -czf "$top/SOURCES/v$version.tar.gz" \
        --transform "s|^|hanuchi-$version/|" \
        meson.build src data LICENSE README.md)
    rpmbuild -bb --define "_topdir $top" "$root/packaging/hanuchi.spec"
    cp "$top"/RPMS/noarch/*.rpm "$dist/"
}

[ $# -gt 0 ] || set -- deb rpm
for kind in "$@"; do
    case $kind in
        deb) build_deb ;;
        rpm) build_rpm ;;
        *) echo "usage: build-packages.sh [deb] [rpm]" >&2; exit 2 ;;
    esac
done
ls -l "$dist"
