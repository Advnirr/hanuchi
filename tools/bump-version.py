#!/usr/bin/env python3
"""Set the version everywhere it is written: bump-version.py 2.1.0

It lives in meson.build, pkg/PKGBUILD, the RPM spec, the Debian control file,
the README badge and the metainfo <releases> list (a new entry dated today is
added on top). tests/test_version.py fails when they disagree.

The PKGBUILD downloads the tag's tarball, so its sha256 can only be known once
the tag is pushed. After tagging run:

    bump-version.py --pin-sum

which downloads the tarball of the current version and writes its sum.
"""
import datetime
import hashlib
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARBALL = "https://github.com/Advnirr/hanuchi/archive/refs/tags/v{v}.tar.gz"
METAINFO = "data/com.github.hanuchi.metainfo.xml"

# file, pattern with the version as its one group
EDITS = [
    ("meson.build", r"^\s*version: '([\d.]+)',"),
    ("pkg/PKGBUILD", r"^pkgver=([\d.]+)"),
    ("packaging/hanuchi.spec", r"^Version:\s+([\d.]+)"),
    ("packaging/deb/control", r"^Version: ([\d.]+)"),
    ("README.md", r"badge/release-v([\d.]+)-"),
]


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def write(name, text):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(text)


def current_version():
    return re.search(EDITS[0][1], read("meson.build"), re.MULTILINE).group(1)


def bump(version):
    for name, pattern in EDITS:
        text = read(name)
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            raise SystemExit(f"{name}: no version to replace, pattern changed?")
        if match.group(1) == version:
            print(f"{name}: already {version}")
            continue
        text = text[:match.start(1)] + version + text[match.end(1):]
        if name == "pkg/PKGBUILD":
            text = re.sub(r"^pkgrel=\d+", "pkgrel=1", text, flags=re.MULTILINE)
        write(name, text)
        print(f"{name}: {match.group(1)} -> {version}")

    text = read(METAINFO)
    if f'<release version="{version}"' in text:
        print(f"{METAINFO}: already has {version}")
    else:
        today = datetime.date.today().isoformat()
        text, n = re.subn(r"(<releases>\n)(\s*)",
                          rf'\1\2<release version="{version}" date="{today}"/>\n\2', text)
        if not n:
            raise SystemExit(f"{METAINFO}: no <releases> list")
        write(METAINFO, text)
        print(f"{METAINFO}: added release {version} ({today})")

    print(f"\nStill to do by hand: commit, tag v{version}, push, publish the GitHub "
          "release (CI attaches the .deb and .rpm), then bump-version.py --pin-sum "
          "and update the AUR clone.")


def pin_sum():
    version = current_version()
    url = TARBALL.format(v=version)
    print(f"Downloading {url}")  # fixed https URL, not user input
    with urllib.request.urlopen(url, timeout=60) as r:  # nosec B310
        digest = hashlib.sha256(r.read()).hexdigest()
    text = read("pkg/PKGBUILD")
    text, n = re.subn(r"^sha256sums=\('[^']*'\)", f"sha256sums=('{digest}')", text, flags=re.MULTILINE)
    if not n:
        raise SystemExit("pkg/PKGBUILD: no sha256sums=('...') line")
    write("pkg/PKGBUILD", text)
    print(f"pkg/PKGBUILD: sha256 of v{version} is {digest}")


def main(argv):
    if argv[1:] == ["--pin-sum"]:
        pin_sum()
    elif len(argv) == 2 and re.fullmatch(r"\d+\.\d+\.\d+", argv[1]):
        bump(argv[1])
    else:
        raise SystemExit("usage: bump-version.py X.Y.Z | --pin-sum")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
